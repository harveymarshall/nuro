# nuro

CLI Productivity Tool for task and habit management.

Currently **nuro** has the ability to create and manage tasks using lists to group them.

## Tasks

Tasks can have the follwing attributes.

| Attribute  | Type               | Default           | Description          |
| ---------- | ------------------ | ----------------- | -------------------- |
| title      | str                | (required)        | Title of the task    |
| created_at | datetime           | current_timestamp | Creation timestamp   |
| due        | Optional[datetime] | None              | Due date/time        |
| tags       | List[str]          | []                | List of tags         |
| list       | Optional[str]      | None              | Associated list name |
| done       | bool               | False             | Completion status    |

These current commands are available for Tasks: 1. add (Adds a new Task) 2. show (Lists tags with optional filters)

## Lists
