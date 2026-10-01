# LangGraph Tool Agent

A simple LangGraph agent that uses Claude or Gemini as its LLM and has three tools.

## Flow

```
START ──▶ agent (LLM) ─────has tool calls?──▶ tools ──┐
              ▲               │ no                    │
              │               ▼                       │
              │              END                      │
              └───────────────────────────────────────┘
```

## Structure

```
app/
  config.py   # provider (anthropic/google), model names, system prompt
  tools.py    # calculator, get_current_datetime, convert_units
  graph.py    # StateGraph: agent node + ToolNode + conditional edge
  main.py     # CLI chat application
tests/
  test_agent.py  # offline tests (no API key needed)
```

## Setup

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # then set LLM_PROVIDER and its API key in .env
```

## Run

```bash
python -m app.main
```

Example prompts:
- `What is (1250 * 0.18) + 42?`
- `What time is it in Asia/Kolkata?`
- `Convert 72 F to C and 10 miles to km`

## Test

```bash
pytest -q
```
