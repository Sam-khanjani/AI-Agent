"""Conversational LangGraph agent that saves its transcript to a text file.

Builds on `Agent_temp_memory.py`: keeps the same in-process
`conversation_history` list threaded through `agent.invoke` each turn, but
once you type "exit" it writes the full Human/AI exchange out to
`logging.txt` in the current directory. That gives you a persisted
transcript across runs, even though the agent itself still has no memory
once the process restarts (it's just reading an old log, not reloading it
as context).
"""

from typing import TypedDict, List, Union
from langchain_core.messages import HumanMessage, AIMessage
from langchain_groq import ChatGroq
from langgraph.graph import StateGraph, START, END
from dotenv import load_dotenv

load_dotenv()

class AgentState(TypedDict):
    messages: List[Union[HumanMessage,AIMessage]]


llm = ChatGroq(model="openai/gpt-oss-20b", max_tokens=1024, temperature=0)


def process(state: AgentState) -> AgentState:
    """This node will solve the request you input"""
    response = llm.invoke(state["messages"])
    state["messages"].append(AIMessage(content=response.content))
    print(f"\n.AI: {response.content}")
    print("CURRENT STATE: ", state["messages"])
    return state

graph = StateGraph(AgentState)
graph.add_node("process", process)
graph.add_edge(START, "process")
graph.add_edge("process", END)
agent = graph.compile()


conversation_history = []

user_input = input("1. Enter: ")
counter=1
while user_input != "exit":    
    conversation_history.append(HumanMessage(content=user_input))
    result = agent.invoke({"messages": conversation_history})
    #print(result["messages"])
    conversation_history = result["messages"]
    counter+=1
    user_input = input(f"\n {counter}. Enter: ")


with open("logging.txt","w") as file:
    file.write("Your Conversation Log: \n")
    
    for message in conversation_history:
        if isinstance(message, HumanMessage):
            file.write(f"You: {message.content}\n")
        elif isinstance(message, AIMessage):
            file.write(f"Ai: {message.content}\n\n")
    file.write("End of Conversation")

print("Conversation saved to logging.txt")