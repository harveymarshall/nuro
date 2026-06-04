

# nuro

CLI Productivity Tool for task and habit management.

Currently **nuro** has the ability to create and manage tasks using lists to group them.

## Requirements

- **Python 3.13+** (check with `python3 --version`)
- On Linux/macOS, install [uv](https://docs.astral.sh/uv/getting-started/installation/) for the simplest setup (uv can also install Python 3.13 for you)

## Installation

### Install from GitHub (recommended)

Install **nuro** as a global CLI with [uv](https://docs.astral.sh/uv/) (isolated from your system Python):

```sh
uv tool install "nuro @ git+https://github.com/harveymarshall/nuro.git@main"
```

Ensure `~/.local/bin` is on your `PATH`, then verify:

```sh
nuro --help
```

If you do not have Python 3.13 yet:

```sh
uv python install 3.13
```

### Install with pip

Use a **Python 3.13+** virtual environment (required on most Linux distros that ship Python 3.12 by default):

```sh
python3.13 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install "nuro @ git+https://github.com/harveymarshall/nuro.git@main"
nuro --help
```

### Install from a local clone (development)

```sh
git clone https://github.com/harveymarshall/nuro.git
cd nuro
uv sync
nuro --help
```

Run tests (optional):

```sh
uv run pytest
```

## Usage Examples

### Tasks

Tasks can have the follwing attributes.

| Attribute  | Type               | Default           | Description          |
| ---------- | ------------------ | ----------------- | -------------------- |
| title      | str                | (required)        | Title of the task    |
| created_at | datetime           | current_timestamp | Creation timestamp   |
| due        | Optional[datetime] | None              | Due date/time        |
| tags       | List[str]          | []                | List of tags         |
| list       | Optional[str]      | None              | Associated list name |
| done       | bool               | False             | Completion status    |

- **Add a new task:**

```sh
nuro tasks add "Buy groceries" --tags shopping,errands --list Personal --due 2025-09-15
```

- **Update a task:**

```sh
nuro tasks update "Buy groceries"
```

This will prompt you to update the title, tags, list, and due date for the specified task.

- **Show all tasks:**

```sh
nuro tasks show
```

- **Show tasks in a specific list:**

```sh
nuro tasks show --list Personal
```

- **Show only completed tasks:**

```sh
nuro tasks show --done true
```

- **Delete a task:**

```sh
nuro tasks delete "Title"
```

This will delete the task with that title.

### Lists

- **Add a new list:**

```sh
nuro lists add "Personal"
```

- **Show all lists:**

```sh
nuro lists show
```

- **Delete a list:**

```sh
nuro lists delete "Personal"
```

This will delete the list with that name.
