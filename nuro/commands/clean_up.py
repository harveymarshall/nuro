import typer
from datetime import datetime, timedelta
from typing import List, Optional

from rich.table import Table
from rich.console import Console

from ..models.list import List as MyListModel
from ..utils.datetime_util import parse_date
from ..db.db import tasks_table
from ..db.db import lists_table

clean_up_app = typer.Typer()

@clean_up_app.command("lists")
def clean_up_lists():
    lists = lists_table.all()
    for lst in lists:
        tasks = tasks_table.search(lambda t: t.get("list_id") == lst["id"])
        if not tasks:
            lists_table.remove(doc_ids=[lst.doc_id])
            typer.echo("✅ Removed all lists with no tasks assigned.")

@clean_up_app.command("tasks")
def clean_up_tasks(
    time: Optional[int] = typer.Option(None, "--time", "-t", help="Remove tasks where due date is passed by 7 days or the value given for time")
):
    if time:
        threshold_date = datetime.now() - timedelta(days=time)
        tasks = tasks_table.all()
        for task in tasks:
            due_date_str = task.get("due_date")
            if due_date_str:
                due_date = parse_date(due_date_str)
                if due_date and due_date < threshold_date:
                    tasks_table.remove(doc_ids=[task.doc_id])
        typer.echo(f"✅ Removed all tasks with due dates older than {time} days.")
    else:
        threshold_date = datetime.now() - timedelta(days=7)
        tasks = tasks_table.all()
        for task in tasks:
            due_date_str = task.get("due_date")
            if due_date_str:
                due_date = parse_date(due_date_str)
                if due_date and due_date < threshold_date:
                    tasks_table.remove(doc_ids=[task.doc_id])
        typer.echo(f"✅ Removed all tasks with due dates older than 7 days.")

