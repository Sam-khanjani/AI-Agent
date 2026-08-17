"""Minimal ReAct-style tool-calling LangGraph agent.

Demonstrates the classic ReAct loop: `our_agent` (an LLM bound to one tool,
`add`) routes to a `tools` node and back via a conditional edge
(`should_continue`) for as long as the model keeps requesting tool calls,
ending once its last response has none. Uses `app.stream(...,
stream_mode="values")` to print each step as it happens instead of a single
`invoke()` call.
"""

from typing import Annotated, Sequence, TypedDict
from dotenv import load_dotenv
from langchain_core.messages import BaseMessage ,ToolMessage, SystemMessage
from langchain_groq import ChatGroq
from langchain_core.tools import tool
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode

load_dotenv()

class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]


@tool
def add(a:int, b:int):
    """This is an addition function that add 2 numbers together"""

    return a+b

tools=[add]

model=ChatGroq(model="openai/gpt-oss-20b", max_tokens=512, temperature=0).bind_tools(tools)

def model_call(state:AgentState) -> AgentState:
    system_prompt= SystemMessage(content= 
                                 "You are my AI assistant, please answer my query to the best of your ability.")
    response= model.invoke([system_prompt] + state["messages"])

    return {"messages":  [response]}

#conditional edge
def should_continue(state: AgentState):
    messages = state["messages"]
    last_message = messages[-1]
    if not last_message.tool_calls:
        return "end"

    else: 
        return"continue"


graph = StateGraph(AgentState)
graph.add_node("our_agent",model_call)

tool_node = ToolNode(tools=tools)
graph.add_node("tools",tool_node)

graph.set_entry_point("our_agent")

graph.add_conditional_edges(
    "our_agent",
    should_continue,
    {
        "continue": "tools",
        "end": END
    }
)

graph.add_edge("tools", "our_agent")
app=graph.compile()

def print_stream(stream):
    for s in stream:
        message = s["messages"][-1]
        if isinstance(message,tuple):
            print(message)

        else:
            message.pretty_print()

inputs={"messages":[("user", "Add 40 + 12. add 100 + 1")]}
print_stream(app.stream(inputs, stream_mode="values"))
