# LangGraph

Hands-on notebooks and standalone agent scripts for learning
[LangGraph](https://langchain-ai.github.io/langgraph/) — building agents as
graphs of nodes and edges over a shared state, from a single node up through
branching, cycles, tool-calling, and a small RAG project.

These are sample/learning files, not production code — each notebook or
script is a small, focused example meant to build up basic, practical
knowledge of Agentic AI, LLMs, and RAG (state/memory, branching and cycles,
ReAct-style tool-calling, retrieval) rather than a polished application.

## Contents

| Notebook | Topic |
|---|---|
| [First_agent.ipynb](First_agent.ipynb) | The core model: a state schema (`TypedDict`), a node function `(state) -> partial_state`, `StateGraph`, `add_node`/`set_entry_point`/`set_finish_point`, `compile()`, `invoke()`. |
| [Multiple_inputs.ipynb](Multiple_inputs.ipynb) | A state schema with several input fields at once, one node reading them all, and branching logic *inside* a node (`if`/`elif`/`else` on an `operation` field) before conditional edges are introduced. |
| [Sequential_Agent.ipynb](Sequential_Agent.ipynb) | Chaining two nodes with `add_edge`; state accumulating as it's threaded from one node into the next. |
| [Conditional_Agent.ipynb](Conditional_Agent.ipynb) | Real graph branching via `add_conditional_edges` and a dedicated router node/function; `START`/`END` sentinels; two chained decision points. |
| [Loop.ipynb](Loop.ipynb) | A genuine cycle — a node whose conditional edge routes back to itself until a stop condition is met — plus LangGraph's default 25-step recursion-limit safety net for when a stop condition is wrong. |

Each notebook builds directly on ideas from the last, so read them in the order above.

```bash
pip install langgraph
```

## Agent/ — standalone agent scripts

Runnable `.py` scripts (not notebooks), each with its own module docstring
explaining exactly what it does. They share one `.env` in this folder.

| Script | Purpose |
|---|---|
| [Agent_one_message.py](Agent/Agent_one_message.py) | Minimal single-turn agent: one prompt via `input()`, one reply, done. |
| [Agent_simple_conversation.py](Agent/Agent_simple_conversation.py) | Loops the above until you type `exit` — but each turn is still memoryless, since only the current message is sent, not any history. |
| [Agent_temp_memory.py](Agent/Agent_temp_memory.py) | Threads the full running conversation into every turn, so the model has real memory of earlier turns — but only for the life of the process; nothing is persisted. |
| [Agent_txt_memory.py](Agent/Agent_txt_memory.py) | Same threading as above, plus writes the full transcript to `logging.txt` once you type `exit`. |
| [ReAct_base.py](Agent/ReAct_base.py) | Classic ReAct tool-calling loop (`our_agent` ↔ `tools`, via `ToolNode` and a conditional edge) with one arithmetic tool. |
| [ReAct_multi_tools.py](Agent/ReAct_multi_tools.py) | Same loop with three tools (`add`, `subtract`, `multiply`), so the model can chain several tool calls to answer one multi-step query. |
| [Drafter.py](Agent/Drafter.py) | Interactive document-drafting agent: the human gives continuous feedback each turn while the model calls `update`/`save` tools on a draft. Ending the session (human types `exit` — "I'm happy") and persisting to disk (`save` tool) are tracked as two independent, separately-logged signals rather than one standing in for the other. |

```bash
pip install langchain-groq langchain-core python-dotenv
```

Needs a `.env` in `Agent/` with a Groq API key:

```bash
echo 'GROQ_API_KEY="<your-key>"' > Agent/.env
```
Get one at [console.groq.com/keys](https://console.groq.com/keys).

## Agent/RAG/ — retrieval-augmented generation

A small RAG pipeline answering questions over `iso27001.pdf`, split into two
scripts on purpose: embedding is slow and only needs to happen once, while
chatting happens repeatedly.

| Script | Purpose |
|---|---|
| [embed_documents.py](Agent/RAG/embed_documents.py) | Run **once** (or again whenever the source PDF changes): loads `iso27001.pdf`, splits it with `RecursiveCharacterTextSplitter`, embeds the chunks, and persists them to a local `chroma_db/` folder next to it. |
| [RAG_Agent.py](Agent/RAG/RAG_Agent.py) | Run **every time you want to chat**: connects to the existing `chroma_db/` (read-only — never re-embeds) and answers questions through a `retriever_tool` in the same ReAct-style loop as `ReAct_base.py`. Fails fast with a clear message if `chroma_db/` doesn't exist yet, instead of a confusing crash. |

```bash
pip install langchain-community langchain-chroma langchain-text-splitters langchain-google-genai pypdf
```

Also needs `GOOGLE_API_KEY` in `Agent/.env` — Groq (used for chat everywhere
else in this folder) has no embeddings API, so embedding specifically runs on
Gemini while chat still runs on Groq:

```bash
echo 'GOOGLE_API_KEY="<your-key>"' >> Agent/.env
```

## Running

- Notebooks: open and run cells top to bottom.
- Scripts: `python <file>.py` from within `Agent/` (or `Agent/RAG/` for the RAG pair) so the local `.env` and any relative paths resolve correctly.

## Notes

- `chroma_db/` is locally rebuildable state, not source — regenerate it with
  `embed_documents.py` rather than expecting it to already exist.
- `Agent_txt_memory.py`'s `logging.txt` is a per-run transcript, not a source file.
