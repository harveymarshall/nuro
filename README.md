# nuro

CLI Productivity Tool for task and habit management.

Currently **nuro** has the ability to create and manage tasks using lists to group them.

## Installation

### From GitHub

```sh
pip install git+https://github.com/harveymarshall/nuro.git@main
```

### From Local Clone

Clone the repository, then run:

```sh
pip install -e .
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
nuro tasks delete list
```

This will delete the list with that name.
