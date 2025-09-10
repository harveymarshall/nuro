from datetime import datetime, timedelta
from typing import List, Optional

import typer
from rich.console import Console
from rich.table import Table
from tinydb import Query

from ..db.db import lists_table, tasks_table
from ..utils.datetime_util import parse_date

clean_up_app = typer.Typer()


@clean_up_app.command("lists")
def clean_up_lists():
    lists = lists_table.all()
    removed_lists = []
    for lst in lists:
        if not lst.get("tasks", []):
            lists_table.remove(Query().name == lst["name"])
            removed_lists.append(lst["name"])
    if len(removed_lists) > 0:
        typer.echo(f"✅ Removed all lists with no tasks assigned. {removed_lists}")
    else:
        typer.echo("No Lists to remove; all have tasks assigned.")


@clean_up_app.command("tasks")
def clean_up_tasks(
    time: Optional[int] = typer.Option(
        None,
        "--time",
        "-t",
        help="Remove tasks where due date is passed by 7 days or the value given for time",
    ),
    done: Optional[bool] = typer.Option(
        None, "--done", "-d", help="flag to delete all tasks where done is true"
    ),
):
    if time:
        threshold_date = datetime.now() - timedelta(days=time)
        tasks = tasks_table.all()
        for task in tasks:
            due_date_str = task.get("due_date")
            if due_date_str:
                due_date = parse_date(due_date_str)
                if due_date and due_date < threshold_date:
                    tasks_table.remove(Query().title == task["title"])
        typer.echo(f"✅ Removed all tasks with due dates older than {time} days.")
    elif done:
        tasks = tasks_table.all()
        removed_tasks = []
        for task in tasks:
            if task.get("done") in [True, "true", "True", 1]:
                tasks_table.remove(Query().title == task["title"])
                removed_tasks.append(task["title"])
        if removed_tasks:
            typer.echo(
                f"✅ Removed all tasks that were set to done status: {removed_tasks}"
            )
        else:
            typer.echo("No tasks with done status found to remove.")
    else:
        threshold_date = datetime.now() - timedelta(days=7)
        tasks = tasks_table.all()
        for task in tasks:
            due_date_str = task.get("due_date")
            if due_date_str:
                due_date = parse_date(due_date_str)
                if due_date and due_date < threshold_date:
                    tasks_table.remove(Query().title == task["title"])
        typer.echo(f"✅ Removed all tasks with due dates older than 7 days.")
