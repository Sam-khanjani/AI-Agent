"""In-process conversational LangGraph agent (short-lived, "temp" memory).

Same one-node graph as `Agent_one_message.py`, but accumulates a running
`conversation_hisory` list and threads the full history into `agent.invoke`
on every turn, so the model can see earlier turns for the rest of this run.
Also prints the full running message state after each response. Memory
lives only in this Python list — nothing is written to disk, so it's gone
the moment the process exits; see `Agent_txt_memory.py` for a version that
persists the conversation to a file.
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


conversation_hisory = []

user_input = input("1. Enter: ")
counter=1
while user_input != "exit":    
    conversation_hisory.append(HumanMessage(content=user_input))
    result = agent.invoke({"messages": conversation_hisory})
    #print(result["messages"])
    conversation_hisory = result["messages"]
    counter+=1
    user_input = input(f"\n {counter}. Enter: ")

