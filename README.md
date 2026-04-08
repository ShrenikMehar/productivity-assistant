# Productivity Assistant

A multi-agent AI system built with Google ADK that helps users manage tasks and retrieve information through natural conversation.

## Agents

- **Coordinator** — root agent, routes requests to the right specialist
- **Task Manager** — add, list, complete, and delete tasks (stored in SQLite)
- **Research Agent** — answers general knowledge questions using Wikipedia

## Tech Stack

- Google ADK 1.14.0
- Gemini 2.5 Flash via Vertex AI
- Google Cloud Run
- SQLite
- LangChain + Wikipedia

## Run locally

```bash
uv venv && source .venv/bin/activate
uv pip install -r requirements.txt
adk web --allow_origins="*"
```
