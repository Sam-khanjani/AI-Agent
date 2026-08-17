"""Minimal single-turn LangGraph agent.

Builds a one-node graph (`process`) that sends one user message to a
Groq-hosted chat model (`openai/gpt-oss-20b` via `ChatGroq`) and prints the
reply. Prompts once via `input()`, invokes the graph once, then exits.
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

user_input = input("Enter: ")
agent.invoke({"messages": [HumanMessage(content=user_input)]})