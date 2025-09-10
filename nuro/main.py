
import typer
from .commands.task import task_app as add_task_app
from .commands.list import list_app as add_list_app

app = typer.Typer()

app.add_typer(add_task_app, name="tasks")
app.add_typer(add_list_app, name="lists")

if __name__ == "__main__":
    app()
