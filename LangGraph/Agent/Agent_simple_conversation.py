"""Looping single-turn LangGraph agent.

Same one-node graph as `Agent_one_message.py` (`process` sends a message to
`ChatGroq` and prints the reply), wrapped in an input loop that keeps
prompting until the user types "exit". Note: each `agent.invoke()` call only
carries the current message — there's no shared history threaded across
turns, so despite the loop the model has no memory of earlier turns.
"""

from typing import TypedDict, List
from langchain_core.messages import HumanMessage
from langchain_groq import ChatGroq
from langgraph.graph import StateGraph, START, END
from dotenv import load_dotenv

load_dotenv()


class AgentState(TypedDict):
    messages: List[HumanMessage]


llm = ChatGroq(model="openai/gpt-oss-20b", max_tokens=512, temperature=0)


def process(state: AgentState) -> AgentState:
    response = llm.invoke(state["messages"])
    print(f"\nAI: {response.content}")
    return state


graph = StateGraph(AgentState)
graph.add_node("process", process)
graph.add_edge(START, "process")
graph.add_edge("process", END)
agent = graph.compile()

user_input = input("1. Enter: ")
counter=1
while user_input != "exit":    
    agent.invoke({"messages": [HumanMessage(content=user_input)]})
    counter+=1
    user_input = input(f" {counter}. Enter: ")