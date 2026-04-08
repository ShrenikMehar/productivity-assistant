
# Productivity Assistant

A multi-agent AI system built with Google ADK that helps users manage tasks and retrieve information through natural conversation.

## Live Demo

- **Cloud Run**: https://productivity-assistant-78379404779.europe-west1.run.app

- **Demo Video**: https://drive.google.com/file/d/1L-64Zq1xDK8OtJZy-XNzUzvgiPIUBHqK/view?usp=sharing

## Architecture

```

User

 └── Coordinator Agent (root)

       ├── Task Manager Agent → SQLite DB

       │     tools: add_task, list_tasks, complete_task, delete_task

       └── Research Agent → Wikipedia API

             tools: wikipedia_search

```

## Agents

- **Coordinator** — root agent, understands intent and routes to the right specialist

- **Task Manager** — add, list, complete, and delete tasks persisted in SQLite

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

## Deploy

```bash

uvx --from google-adk==1.14.0 adk deploy cloud_run \

  --project=$PROJECT_ID \

  --region=europe-west1 \

  --service_name=productivity-assistant \

  --with_ui .

```

