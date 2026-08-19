# Contributing

Thanks for your interest in this repo! It's a personal, hands-on collection
of **sample/learning files** for Agentic AI, LLMs, RAG, and GenAI development
using Google's [Agent Development Kit (ADK)](https://google.github.io/adk-docs/)
and [LangGraph](https://langchain-ai.github.io/langgraph/) — see the
[root README](README.md) for the full layout.

Contributions are welcome, especially if you're also learning these
frameworks: new minimal examples, clearer explanations, bug fixes in the
sample code, or corrections to the docs all help.

By participating, you're expected to follow the
[Code of Conduct](CODE_OF_CONDUCT.md).

## Why this repo exists (a note from the maintainer)

I built this as a teaching source — a place where someone (including future
me) can come back, remember how a concept works, and have a small working
example to build their own code from. That's the lens I'd like contributions
viewed through: the goal isn't to grow this into a framework or a product,
it's to stay a clear, memorable reference that's easy to learn from and easy
to extend. When in doubt, prioritize clarity over completeness.

## Ways to contribute

- **Report a bug** — open an issue describing what you ran, what you
  expected, and what actually happened (include the traceback if there is
  one).
- **Fix a bug** — open a PR. Small, focused fixes are easiest to review.
- **Add a new example** — a new notebook or standalone script that teaches
  one clear concept (mirroring the existing progression, e.g.
  `LangGraph/First_agent.ipynb` → `Conditional_Agent.ipynb` → `Loop.ipynb`).
  This includes new AI Agent and RAG examples beyond what's here already —
  a different agent pattern, a different retrieval setup, a different kind
  of tool use.
- **Add other tools/frameworks relevant to AI agents** — this repo currently
  covers Google ADK and LangGraph, but examples using other agent
  frameworks, tool integrations, vector stores, or GenAI-adjacent tooling
  are welcome too, as long as they're introduced the same way everything
  else here is: a small, focused, well-explained example, not a dependency
  dump.
- **Extend existing code with more features** — e.g. adding a capability to
  one of the sample agents. Please keep the *teaching* value front and
  center when doing this: add a docstring/markdown note explaining the new
  concept, don't just bolt on complexity. If a feature would make an
  existing example harder to follow, consider adding it as a new example
  instead of expanding the original.
- **Improve the docs** — clarify a README, fix a broken link, add a missing
  teaching note to a notebook.

## Development setup

Requires Python 3.12+. All folders share one virtual environment at the repo
root:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install whatever a given folder needs — see the `pip install` line in that
folder's README (root, `Google ADK/README.md`, `LangGraph/README.md`).

### API keys

Runnable scripts/notebooks read credentials from a local `.env` file next to
them (e.g. `GOOGLE_API_KEY`, `GROQ_API_KEY` — see the relevant README for
which one). **Never commit a `.env` file or paste a real key into a
notebook, script, issue, or PR.** If you accidentally commit one, rotate the
key immediately, don't just delete the commit.

## Making a change

1. Fork the repo and create a branch off `main`.
2. Make your change. For Python scripts, keep the existing style: a short
   module docstring at the top explaining what the file does and how it
   differs from similar files nearby (see any file in `LangGraph/Agent/` for
   the pattern). For notebooks, prefer short markdown cells near the code
   they explain over long blocks of prose.
3. Sanity-check your change actually runs:
   ```bash
   python -m py_compile path/to/your_file.py
   python path/to/your_file.py
   ```
   For notebooks, run all cells top to bottom in a fresh kernel.
4. Update the relevant README's contents table if you added or renamed a
   file.
5. Open a pull request with a short description of what changed and why.

## Style notes

- Prefer small, self-contained examples over large ones — the point of this
  repo is to be a clear starting reference, not a production system.
- Don't add dependencies unless the example genuinely needs them, and note
  the install command in the relevant README.
- Avoid hardcoding machine-specific paths (e.g. Windows drive paths); resolve
  paths relative to the script/notebook itself when a file needs one.

## Questions

Open an issue, or reach out at samkhanjani1997@gmail.com.
