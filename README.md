# Task Tracker CLI

A simple command-line tool to manage your tasks, written in Python.

## Features
- Add, update, delete tasks
- Mark tasks as in-progress or done
- List tasks by status
- Stores tasks in a local JSON file

## Installation

Clone the repository and install dependencies:

```
pip install -r requirements.txt
pip install .
```

Or use the provided Makefile:

```
make install
```

## Usage

Run the CLI tool:

```
task-cli [command] [options]
```

### Commands

- `add <description>`: Add a new task
- `update <id> <description>`: Update a task's description
- `delete <id>`: Delete a task
- `mark-in-progress <id>`: Mark a task as in-progress
- `mark-done <id>`: Mark a task as done
- `list`: List all tasks
- `list done|todo|in-progress`: List tasks by status

## Development

Run tests:

```
make test
```

Lint code:

```
make lint
```

Build source distribution:

```
make build
```

## License

This project is licensed under the MIT License.
