import os
import sqlite3
import logging
from dotenv import load_dotenv

from google.adk import Agent
from google.adk.agents import SequentialAgent
from google.adk.tools.tool_context import ToolContext
from google.adk.tools.langchain_tool import LangchainTool
from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper

load_dotenv()
model_name = os.getenv("MODEL")

DB_PATH = "/tmp/tasks.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            status TEXT DEFAULT 'pending',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

init_db()

def add_task(title: str) -> dict:
    """Add a new task to the database."""
    conn = sqlite3.connect(DB_PATH)
    conn.execute("INSERT INTO tasks (title) VALUES (?)", (title,))
    conn.commit()
    conn.close()
    return {"status": "success", "message": f"Task '{title}' added."}

def list_tasks() -> dict:
    """List all tasks from the database."""
    conn = sqlite3.connect(DB_PATH)
    rows = conn.execute("SELECT id, title, status FROM tasks").fetchall()
    conn.close()
    tasks = [{"id": r[0], "title": r[1], "status": r[2]} for r in rows]
    return {"tasks": tasks}

def complete_task(task_id: int) -> dict:
    """Mark a task as completed."""
    conn = sqlite3.connect(DB_PATH)
    conn.execute("UPDATE tasks SET status='completed' WHERE id=?", (task_id,))
    conn.commit()
    conn.close()
    return {"status": "success", "message": f"Task {task_id} marked as completed."}

def delete_task(task_id: int) -> dict:
    """Delete a task by ID."""
    conn = sqlite3.connect(DB_PATH)
    conn.execute("DELETE FROM tasks WHERE id=?", (task_id,))
    conn.commit()
    conn.close()
    return {"status": "success", "message": f"Task {task_id} deleted."}

wikipedia_tool = LangchainTool(
    tool=WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper())
)

task_manager_agent = Agent(
    name="task_manager",
    model=model_name,
    description="Manages user tasks — add, list, complete, and delete tasks.",
    instruction="""
    You are a task manager. Help users manage their to-do list.
    Use the available tools to add, list, complete, or delete tasks.
    Always confirm what action you took.
    """,
    tools=[add_task, list_tasks, complete_task, delete_task],
)

research_agent = Agent(
    name="research_agent",
    model=model_name,
    description="Answers general knowledge and research questions using Wikipedia.",
    instruction="""
    You are a research assistant. Answer the user's question using Wikipedia.
    Be concise and helpful.
    """,
    tools=[wikipedia_tool],
)

root_agent = Agent(
    name="coordinator",
    model=model_name,
    description="Personal productivity assistant that coordinates task management and research.",
    instruction="""
    You are a personal productivity assistant. You help users manage tasks and answer questions.
    
    - If the user wants to add, list, complete, or delete tasks → transfer to 'task_manager'
    - If the user asks a general knowledge or research question → transfer to 'research_agent'
    - For greetings or unclear requests → respond directly and ask what they need help with
    
    Always be helpful and concise.
    """,
    sub_agents=[task_manager_agent, research_agent],
)
