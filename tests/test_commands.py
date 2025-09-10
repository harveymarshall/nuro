import pytest
from typer.testing import CliRunner

from nuro.main import app

runner = CliRunner()


def test_tasks_add_dry_run(monkeypatch):
    # Patch TinyDB to avoid writing to disk
    class DummyTable:
        def insert(self, *args, **kwargs):
            return 1

        def get(self, *args, **kwargs):
            return None

        def update(self, *args, **kwargs):
            return None

    monkeypatch.setattr("nuro.commands.task.tasks_table", DummyTable())
    monkeypatch.setattr("nuro.commands.task.lists_table", DummyTable())
    result = runner.invoke(
        app, ["tasks", "add", "Test Task", "--tags", "test", "--list", "TestList"]
    )
    assert result.exit_code == 0
    assert "Task added" in result.output


def test_tasks_show_empty(monkeypatch):
    class DummyTable:
        def all(self):
            return []

        def search(self, *args, **kwargs):
            return []

    monkeypatch.setattr("nuro.commands.task.tasks_table", DummyTable())
    result = runner.invoke(app, ["tasks", "show"])
    assert result.exit_code == 0
    assert "No tasks found" in result.output
