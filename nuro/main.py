
import typer
from .commands.task import task_app as add_task_app
from .commands.list import list_app as add_list_app
from .commands.clean_up import clean_up_app as add_cleanup_app

app = typer.Typer()

app.add_typer(add_task_app, name="tasks")
app.add_typer(add_list_app, name="lists")
app.add_typer(add_cleanup_app, name="cleanup")

if __name__ == "__main__":
    app()
