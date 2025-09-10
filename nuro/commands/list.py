from datetime import datetime, timedelta
from typing import List, Optional

import typer
from rich.console import Console
from rich.table import Table

from ..db.db import lists_table, tasks_table
from ..models.list import List as MyListModel
from ..utils.datetime_util import parse_date

list_app = typer.Typer()


@list_app.command("show")
def list_tasks(
    name: Optional[str] = typer.Option(
        None, "--name", "-l", help="Filter by list name"
    ),
    tag: Optional[str] = typer.Option(None, "--tag", "-t", help="Filter by tag"),
):
    from tinydb import Query

    ListQuery = Query()

    query = None

    if name:
        query = ListQuery.list == name
    if tag:
        tag_query = ListQuery.tags.any([tag])
        query = tag_query if query is None else query & tag_query

    if query:
        results = lists_table.search(query)
    else:
        results = lists_table.all()

    if not results:
        typer.echo("📭 No lists found.")
        return

    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Name")
    table.add_column("Tags")
    table.add_column("Tasks")
    table.add_column("Completed Tasks")

    for lists in results:
        tags = ", ".join(lists.get("tags", []))
        name = lists.get("name", "")
        task_ids = lists.get("tasks", [])
        tasks_count = str(len(task_ids))
        completed_tasks = 0
        for task_id in task_ids:
            # TinyDB uses doc_id for primary key
            task_obj = tasks_table.get(doc_id=task_id)
            if task_obj and task_obj.get("done") in [True, "true", "True", 1]:
                completed_tasks += 1

        table.add_row(name, tags, tasks_count, f"{completed_tasks} / {tasks_count}")

    console = Console()
    console.print(table)


@list_app.command("add")
def add_list(
    name: str = typer.Argument(..., help="The list name"),
    tags: List[str] = typer.Option([], "--tags", "-t", help="Tags like @work"),
):
    from tinydb import Query

    if name:
        list_query = Query()
        existing_list = lists_table.get(list_query.name == name)
        if existing_list:
            typer.echo(f"❌ List with name: {name} already exists.")
        else:
            # List doesn't exist, create it
            new_list = MyListModel(
                name=name, tags=tags, created_at=datetime.now(), tasks=[]
            )
            lists_table.insert(new_list.model_dump(mode="json", exclude_none=True))
            typer.echo(f"✅ New List Added with name: {name}")


@list_app.command("delete")
def delete_list(name: str = typer.Argument(..., help="The list name")):
    from tinydb import Query

    if name:
        list_query = Query()
        if lists_table.get(list_query.name == name):
            list_obj = lists_table.get(list_query.name == name)
            if list_obj and "tasks" in list_obj:
                attached_tasks = list_obj["tasks"]
                for task in attached_tasks:
                    task_query = Query()
                    task_obj = tasks_table.get(task_query.id == task)
                    if task_obj:
                        tasks_table.update({"list": None}, task_query.id == task)
                # You can process attached_tasks here if needed
            lists_table.remove(list_query.name == name)
            typer.echo(f"🗑️  List {name} deleted.")
        else:
            typer.echo(f"❌ No Lists with Name: {name}")
