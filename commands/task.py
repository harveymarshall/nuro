import typer
from datetime import datetime, timedelta
from typing import List, Optional

from rich.table import Table
from rich.console import Console

from db.db import tasks_table
from models.task import Task
from utils.datetime_util import parse_date
from db.db import tasks_table

task_app = typer.Typer()

@task_app.command("list")
def list_tasks(
    list_name: Optional[str] = typer.Option(None, "--list", "-l", help="Filter by list name"),
    tag: Optional[str] = typer.Option(None, "--tag", "-t", help="Filter by tag"),
    done: Optional[bool] = typer.Option(None, "--done", help="Filter by completion (true/false)")
):
    """List your tasks with optional filters."""
    from tinydb import Query
    TaskQuery = Query()

    query = None

    if list_name:
        query = TaskQuery.list == list_name
    if tag:
        tag_query = TaskQuery.tags.any([tag])
        query = tag_query if query is None else query & tag_query
    if done is not None:
        done_query = TaskQuery.done == done
        query = done_query if query is None else query & done_query

    if query:
        results = tasks_table.search(query)
    else:
        results = tasks_table.all()

    if not results:
        typer.echo("📭 No tasks found.")
        return

    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Status", style="bold")
    table.add_column("Title")
    table.add_column("Due")
    table.add_column("Tags")
    table.add_column("List")

    for task in results:
        status = "✅" if task.get("done") else "🔲"
        due = task.get("due", "")
        tags = ", ".join(task.get("tags", []))
        list_name = task.get("list", "")
        table.add_row(
            status,
            task.get("title", ""),
            due[:10] if due else "",
            tags,
            list_name
        )

    console = Console()
    console.print(table)


@task_app.command("add")
def add_task(
    title: str = typer.Argument(..., help="The task description"),
    tags: List[str] = typer.Option([], "--tags", "-t", help="Tags like @work"),
    list_name: Optional[str] = typer.Option(None, "--list", "-l", help="List name"),
    due: Optional[str] = typer.Option(None, "--due", "-d", help="Due date (YYYY-MM-DD)")
):
    """Add a new task to your list."""
    due_date = parse_date(due) if due else None
    task = Task(
        title=title,
        tags=tags,
        list=list_name,
        due=due_date,
        created_at=datetime.now(),
    )
    task_dict = task.model_dump(mode='json', exclude_none=True)
    task_id = tasks_table.insert(task_dict)
    typer.echo(f"✅ Task added with ID {task_id}")

@task_app.command("update")
def update_task(
    title: str = typer.Argument(..., help="The task description")
):
    """Update a task in list"""
    from tinydb import Query
    TaskQuery = Query()
    existing_task = tasks_table.get(TaskQuery.title == title)
    if not existing_task:
        typer.echo(f"❌ Task with title '{title}' not found.")
        return

    new_title = typer.prompt("New title", default=existing_task.get("title"))
    new_tags = typer.prompt("New tags (comma separated)", default=",".join(existing_task.get("tags", [])))
    new_list = typer.prompt("New list", default=existing_task.get("list", ""))
    new_due = typer.prompt("New due date (YYYY-MM-DD)", default=existing_task.get("due", ""))

    updated_task = {
        "title": new_title,
        "tags": [tag.strip() for tag in new_tags.split(",")] if new_tags else [],
        "list": new_list if new_list else None,
        "due": new_due if new_due else None,
        "updated_at": datetime.now().isoformat()
    }

    tasks_table.update(updated_task, TaskQuery.title == title)
    typer.echo(f"✅ Task '{title}' updated.")

@task_app.command("upcoming")
def upcoming_tasks():
    """Show tasks due in the next 5 days."""

    now = datetime.now()
    five_days_later = now + timedelta(days=5)

    upcoming = []

    table = Table(show_header=True, header_style="bold magenta", title="📅 Upcoming Tasks (Due in next 5 days):\n")
    table.add_column("Status", style="bold")
    table.add_column("Title")
    table.add_column("Due")

    for task in tasks_table.all():
        due_str = task.get("due")
        if due_str:
            try:
                due_date = datetime.fromisoformat(due_str)
                if now <= due_date <= five_days_later and not task.get("done", False):
                    upcoming.append((task["title"], due_date.strftime("%Y-%m-%d")))
            except ValueError:
                continue

    if not upcoming:
        typer.echo("📭 No upcoming tasks due in the next 5 days.")
        return

    for task in upcoming:
        status = "🔜"
        title = task[0]
        due = task[1]
        table.add_row(
            status,
            title,
            due[:10] if due else "",
        )

    console = Console()
    console.print(table)
