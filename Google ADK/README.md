# Google ADK

Hands-on notebooks and a small sample project for learning the
[Google Agent Development Kit (ADK)](https://google.github.io/adk-docs/) — building,
running, and debugging LLM agents backed by Gemini models.

These are sample/learning files, not production code — each notebook is a
small, focused example meant to build up basic, practical knowledge of
Agentic AI and GenAI development (agent structure, tool use, multi-agent
orchestration, memory) rather than a polished application.

## Contents

| File | Topic |
|---|---|
| [prepration.ipynb](prepration.ipynb) | Getting started: installing `google-adk`, loading API keys from `.env`, configuring retry options, building a first `Agent` with `google_search`, running it with `InMemoryRunner`, and scaffolding a project with `adk create` / `adk web`. |
| [multi_agent.ipynb](multi_agent.ipynb) | Multi-agent patterns: agents as tools (`AgentTool`), `SequentialAgent`, `ParallelAgent`, and `LoopAgent` — e.g. a research coordinator, a parallel research team with an aggregator, and a draft/critique/refine writing loop. |
| [MCP.ipynb](MCP.ipynb) | Custom function tools (with docstrings/type hints as the tool contract), an agentic currency-conversion assistant, using a dedicated agent for math instead of trusting the LLM, connecting to MCP servers via `McpToolset` (image generation, Kaggle datasets), and long-running/human-in-the-loop tool calls that pause for approval. |
| [short_memory_management.ipynb](short_memory_management.ipynb) | Session-based (short-term) memory: `SessionService` implementations (`InMemory` vs. persistent), session state/events, session isolation, and adding conversation compaction for efficiency. |
| [long_memory_management.ipynb](long_memory_management.ipynb) | Long-term memory across sessions: saving and retrieving memories with `load_memory`/`preload_memory`, searching memory, and autosaving. |
| [debugging.ipynb](debugging.ipynb) | Debugging an ADK agent: enabling `DEBUG` logging to a file, scaffolding an agent with `adk create`, writing `research_agent/agent.py`, and serving it locally with `adk web --log_level DEBUG`. |
| [research_agent/](research_agent/) | Sample agent package generated via `adk create` (imported in `debugging.ipynb`), runnable with `adk web .`. |

## Setup

```bash
pip install google-adk python-dotenv
```

Each runnable project directory (this folder and `research_agent/`) needs its own
`.env` file with a Gemini API key:

```bash
echo 'GOOGLE_API_KEY="<your-key>"' > .env
```

Some notebooks (`MCP.ipynb`) also spawn MCP servers over `npx`, so Node.js must be
installed on your system.

## Running

- Open any notebook and run cells top to bottom (`load_dotenv()` picks up the local `.env`).
- To launch the ADK web UI for `research_agent/`:
  ```bash
  cd research_agent
  adk web .
  ```

## Notes

- The `.adk/` directories (session/artifact storage created when running agents)
  hold local conversation state, not source.
