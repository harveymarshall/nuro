
import typer
from commands.task import task_app as add_task_app

app = typer.Typer()

app.add_typer(add_task_app, name="task")

if __name__ == "__main__":
    app()
