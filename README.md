# LangGraph Tool Agent

A simple LangGraph agent that uses Claude as its LLM and has three tools.

## Flow

```
START ──▶ agent (Claude) ──has tool calls?──▶ tools ──┐
              ▲               │ no                    │
              │               ▼                       │
              │              END                      │
              └───────────────────────────────────────┘
```

## Structure

```
app/
  config.py   # model name, max tokens, system prompt (from env)
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
cp .env.example .env   # then put your ANTHROPIC_API_KEY in .env
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
