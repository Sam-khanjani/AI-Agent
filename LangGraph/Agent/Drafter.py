"""Interactive document-drafting LangGraph agent ("Drafter").

A ReAct-style agent for iterative document editing: `agent` prompts the
user for input each turn (via `input()`) and hands it to the model, which
can call the `update` tool (rewrites the module-level `document_content`
string) or the `save` tool (writes it to a `.txt` file). Unlike
`ReAct_base.py`/`ReAct_multi_tools.py`, the loop always visits `tools`
after `agent` and `should_continue` decides whether to keep going by
inspecting the *last tool result* — it only routes to `END` once it sees a
`ToolMessage` confirming the document was saved, not just whenever the
model stops requesting tool calls.
"""

from typing import Annotated, Sequence, TypedDict
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, AIMessage, BaseMessage ,ToolMessage, SystemMessage
from langchain_groq import ChatGroq
from langchain_core.tools import tool
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode

load_dotenv()

document_content = ""

class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]
    user_happy: bool


@tool
def update(content: str) -> str:
    """Updates the document wth the provided content."""
    global document_content
    document_content = content
    return f"Document has been updated successfully! The current content is: \n{document_content}"


@tool
def save(filename: str) -> str:
    """Save the current document to a text file. Does not end the session.
    Args:
        filename: Name for the text file.
        """
    if not filename.endswith('.txt'):
        filename = f"{filename}.txt"

    try:
        with open(filename, 'w') as file:
            file.write(document_content)
        print(f"\n Document has been saved to: {filename}")
        return f"Document has been saved successfully to {filename}"
    except Exception as e:
        return f"Error saving document: {str(e)}"


tools= [update,save]

model=ChatGroq(model="openai/gpt-oss-20b", max_tokens=512, temperature=0).bind_tools(tools)

def our_agent(state: AgentState) -> AgentState:
    system_prompt = SystemMessage(content=
                                  f"""You are Drafter, a helpful writing assistant. You are going to help the user update and modify documents.
    - If the user wants to update or modify content, use the 'update' tool with the complete updated content.
    - If the user wants to save a copy to disk, use the 'save' tool. Saving does not end the session.
    - Make sure to always show the current document state after modifications.
    The current document content is: {document_content}""")

    if not state["messages"]:
        user_input = "I'm ready to help you update a document,  what would you like to create?"
        user_message = HumanMessage(content=user_input)
    else:
        user_input = input("\nWhat would you lke to do with the document? (type 'exit' once you're happy with it)")
        print(f"\n USER: {user_input}")
        user_message = HumanMessage(content=user_input)

    # "Happy" is a deterministic signal from the human, decided here in code —
    # it is deliberately kept independent of whether a 'save' tool call ever happened.
    if user_input.strip().lower() == "exit":
        return {
            "messages": list(state["messages"]) + [user_message],
            "user_happy": True,
        }

    all_messages = [system_prompt] + list(state["messages"]) + [user_message]
    response = model.invoke(all_messages)


    print(f"\n AI:{response.content}")
    if hasattr(response, "tool_calls") and response.tool_calls:
        print(f" USING TOOLS: {[tc['name'] for tc in response.tool_calls]}")

    return {
        "messages": list(state["messages"]) + [user_message, response],
        "user_happy": False,
    }




def should_continue(state: AgentState) -> str:
    """Determine if we should continue or end the conversation.

    "Happy" (the human is done giving feedback) and "saved" (the document was
    written to disk) are two independent reasons to stop — either one alone
    is enough to end the session.
    """

    if state.get("user_happy"):
        print("\n✅ Ending: you said you're happy with the draft.")
        return "end"

    messages = state["messages"]

    if not messages:
        return "continue"

    # Look for the most recent successful result specifically from the
    # 'save' tool (matched by tool name, not by guessing at its wording).
    for message in reversed(messages):
        if (isinstance(message, ToolMessage) and
            message.name == "save" and
            "successfully" in message.content.lower()):
            print("\n💾 Ending: document was saved to disk.")
            return "end"

    return "continue"




def print_messages(messages):
    """Function I made to print the messages in a more readable format"""
    if not messages:
        return
    
    for message in messages[-3:]:
        if isinstance(message, ToolMessage):
            print(f"\n🛠️ TOOL RESULT: {message.content}")




graph = StateGraph(AgentState)

graph.add_node("agent", our_agent)
graph.add_node("tools", ToolNode(tools))

graph.set_entry_point("agent")

graph.add_edge("agent", "tools")


graph.add_conditional_edges(
    "tools",
    should_continue,
    {
        "continue": "agent",
        "end": END,
    },
)

app = graph.compile()

def run_document_agent():
    print("\n ===== DRAFTER =====")
    
    state = {"messages": []}
    
    for step in app.stream(state, stream_mode="values"):
        if "messages" in step:
            print_messages(step["messages"])
    
    print("\n ===== DRAFTER FINISHED =====")

if __name__ == "__main__":
    run_document_agent()
    