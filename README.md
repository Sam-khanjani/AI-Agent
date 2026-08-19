# AI-Agent

A personal, hands-on repo for learning agentic AI and RAG patterns across two
frameworks: Google's [Agent Development Kit (ADK)](https://google.github.io/adk-docs/)
and [LangGraph](https://langchain-ai.github.io/langgraph/), plus a small
Retrieval-Augmented Generation (RAG) project built on top of LangGraph.

Everything here is a **sample/learning file**, not production code — each
notebook or script is a small, self-contained example meant to build up basic,
practical knowledge of Agentic AI, LLMs, RAG, and GenAI development in
general: how agents are structured, how state and memory work, how tool use
and multi-agent orchestration fit together, and how retrieval augments an
LLM. Good starting point if you're new to any of these topics, agnostic of
which specific framework you end up using long-term.

## Structure

| Folder | What's in it |
|---|---|
| [Google ADK/](<Google ADK>) | Notebooks + a sample agent package for Google's ADK — building, running, and debugging Gemini-backed agents. Full breakdown in its own [README](<Google ADK/README.md>). |
| [LangGraph/](LangGraph/) | Notebooks progressing from a single-node graph up to branching and cycles, plus a folder of standalone `.py` agent scripts (conversation memory, ReAct tool-calling, an interactive document drafter, and a RAG agent). |

## Setup

Requires Python 3.12+. All folders share one virtual environment at the repo root:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

There's no single `requirements.txt` yet — dependencies were installed ad hoc as
each notebook/script was built. See the `pip install` line under each section
below for what that part of the repo needs.

### API keys

Nothing is hardcoded — every runnable folder reads its own local `.env` file:

| `.env` location | Variables needed |
|---|---|
| `Google ADK/.env`, `Google ADK/research_agent/.env` | `GOOGLE_API_KEY` |
| `LangGraph/Agent/.env` | `GROQ_API_KEY` (all agents), plus `GOOGLE_API_KEY` (only needed for `RAG/` — see below) |

## Google ADK

Learning notebooks for Google's Agent Development Kit: installing/configuring
agents, custom function tools & MCP tool servers, multi-agent orchestration
(sequential / parallel / loop), short-term session memory vs. long-term
cross-session memory, and debugging an ADK agent. Also includes
`research_agent/`, a small agent package scaffolded via `adk create`.

Full per-notebook breakdown: [Google ADK/README.md](<Google ADK/README.md>).

```bash
pip install google-adk python-dotenv
```

## LangGraph

### Notebooks — read in this order

Each one builds directly on the concepts from the last:

| Notebook | Introduces |
|---|---|
| [First_agent.ipynb](LangGraph/First_agent.ipynb) | The core model: a state schema (`TypedDict`), a node function, `StateGraph`, `compile()`, `invoke()`. |
| [Multiple_inputs.ipynb](LangGraph/Multiple_inputs.ipynb) | Several input fields on one state schema, and branching logic *inside* a node. |
| [Sequential_Agent.ipynb](LangGraph/Sequential_Agent.ipynb) | Chaining two nodes with `add_edge`; state accumulating as it passes through them. |
| [Conditional_Agent.ipynb](LangGraph/Conditional_Agent.ipynb) | Real graph branching via `add_conditional_edges` and a dedicated router node/function. |
| [Loop.ipynb](LangGraph/Loop.ipynb) | A genuine cycle — a node routing back to itself until a stop condition is met — plus LangGraph's default recursion-limit safety net. |

```bash
pip install langgraph
```

### Agent/ — standalone agent scripts

Each file is runnable on its own (`python <file>.py`) and carries a module
docstring explaining exactly what it does; short version:

| Script | Purpose |
|---|---|
| [Agent_one_message.py](LangGraph/Agent/Agent_one_message.py) | Minimal single-turn agent: one prompt, one reply, done. |
| [Agent_simple_conversation.py](LangGraph/Agent/Agent_simple_conversation.py) | Loops the above — but each turn is still memoryless, since history isn't threaded between calls. |
| [Agent_temp_memory.py](LangGraph/Agent/Agent_temp_memory.py) | Threads the full conversation history into every turn, so the model has real memory — but only for the life of the running process. |
| [Agent_txt_memory.py](LangGraph/Agent/Agent_txt_memory.py) | Same as above, plus saves the full transcript to `logging.txt` when you type `exit`. |
| [ReAct_base.py](LangGraph/Agent/ReAct_base.py) | Classic ReAct tool-calling loop (`agent` ↔ `tools`) with a single arithmetic tool. |
| [ReAct_multi_tools.py](LangGraph/Agent/ReAct_multi_tools.py) | Same loop with three tools, so the model can chain multiple tool calls to answer one query. |
| [Drafter.py](LangGraph/Agent/Drafter.py) | Interactive document-drafting agent built for a "speed up drafting documents" brief: the human gives continuous feedback while the agent calls `update`/`save` tools. Ending the session ("I'm happy, type `exit`") and persisting to disk ("`save`") are tracked as two independent signals, not one. |

```bash
pip install langchain-groq langchain-core python-dotenv
```
Needs `GROQ_API_KEY` in `LangGraph/Agent/.env` — get one at [console.groq.com](https://console.groq.com/keys).

### Agent/RAG/ — retrieval-augmented generation

A two-step RAG pipeline over `iso27001.pdf`, deliberately split so the slow
part (embedding) only ever has to run once:

| Script | Purpose |
|---|---|
| [embed_documents.py](LangGraph/Agent/RAG/embed_documents.py) | Run **once** (or whenever the source PDF changes): loads the PDF, chunks it, embeds it, and persists the vectors to a local `chroma_db/` folder. |
| [RAG_Agent.py](LangGraph/Agent/RAG/RAG_Agent.py) | Run **every time you want to chat**: connects to the existing `chroma_db/` and answers questions through a retriever tool in a ReAct loop. Fails fast with a clear message if `chroma_db/` doesn't exist yet, instead of a confusing crash. |

```bash
pip install langchain-community langchain-chroma langchain-text-splitters langchain-google-genai pypdf
```
Also needs `GOOGLE_API_KEY` in `LangGraph/Agent/.env` — Groq (used for the chat
model everywhere else in this repo) has no embeddings API, so embeddings here
run on Gemini instead while chat still runs on Groq.

## Notes
- License: [LICENSE](LICENSE).
