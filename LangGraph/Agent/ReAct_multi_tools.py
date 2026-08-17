"""ReAct-style tool-calling LangGraph agent with multiple tools.

Same `our_agent` <-> `tools` ReAct loop as `ReAct_base.py`, but bound to
three arithmetic tools (`add`, `subtract`, `multiply`) instead of one, so
the model can chain several tool calls across loop iterations to answer a
multi-step query in a single run.
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
    return a + b

@tool
def subtract(a: int, b:int):
    """subtraction function"""
    return a - b

@tool
def multiply(a: int, b:int):
    """Multiplication fuction"""
    return a * b

tools=[add, subtract, multiply]

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

inputs={"messages":[("user", "Add 40 + 12 then subtract result from 100 then multiply result by 2 ")]}
print_stream(app.stream(inputs, stream_mode="values"))
