import json
import os
import sys
from datetime import datetime

JSON_FILE = "tasks.json"
CONFIRM_DELETE = (
    "Are you sure you want to delete all tasks? Type 'yes' to confirm: "
)


def print_help():
    help_text = """
    Usage: task-cli [command] [options]

    Commands:
      add <description>         Add a new task with the given description
      update <id> <description> Update the description of a task by its ID
      delete <id>               Delete a task by its ID
      mark-in-progress <id>     Mark a task as in-progress by its ID
      mark-done <id>            Mark a task as done by its ID
      list                      List all tasks
      list done                 List all tasks that are done
      list todo                 List all tasks that are todo
      list in-progress          List all tasks that are in-progress

    Options:
      -h, --help                Show this help message and exit
    """
    print(help_text)


def create_json_file():
    if not os.path.exists("tasks.json"):
        with open("tasks.json", "w") as f:
            data = []
            json.dump(data, f)


def load_tasks():
    try:
        with open(JSON_FILE, "r") as f:
            tasks = json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        tasks = []
    return tasks


def save_tasks(tasks):
    with open(JSON_FILE, "w") as f:
        json.dump(tasks, f, indent=4)


def add_task(description):
    tasks = load_tasks()
    task_id = len(tasks) + 1
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    new_task = {
        "id": task_id,
        "description": description,
        "status": "todo",
        "createdAt": now,
        "updatedAt": now,
    }
    tasks.append(new_task)
    save_tasks(tasks)
    print(f"Added task {task_id}: {description}")


def update_task(task_id, description):
    tasks = load_tasks()

    for task in tasks:
        if task.get("id") == int(task_id):
            task["description"] = description
            task["updatedAt"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            break
    else:
        print(f"Task with ID {task_id} not found.")
        return

    save_tasks(tasks)
    print(f"Updated task {task_id}: {description}")


def delete_task(task_id, delete_all=False):
    tasks = load_tasks()

    if delete_all:
        tasks = []
        with open(JSON_FILE, "w") as f:
            json.dump(tasks, f, indent=4)
        print("All tasks deleted.")
        return

    tasks = [task for task in tasks if task.get("id") != int(task_id)]
    for idx, task in enumerate(tasks, start=1):
        task["id"] = idx
    save_tasks(tasks)
    print(f"Deleted task {task_id}")


def mark_task(task_id, status):
    tasks = load_tasks()

    for task in tasks:
        if task.get("id") == int(task_id):
            task["status"] = status
            task["updatedAt"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            break
    else:
        print(f"Task with ID {task_id} not found.")
        return
    save_tasks(tasks)
    print(f"Marked task {task_id} as {status}.")


def list_tasks(status=None):
    tasks = load_tasks()
    if not tasks:
        print("No tasks found.")
        return

    print(
        f"{'ID':<5} {'Description':<30} "
        f"{'Status':<12} "
        f"{'Created At':<24} "
        f"{'Updated At':<24}"
    )
    print("-" * 100)
    for task in tasks:
        if status is None or task.get("status") == status:
            print(
                f"{str(task.get('id', '')):<5} "
                f"{str(task.get('description', '')):<30} "
                f"{str(task.get('status', '')):<12} "
                f"{str(task.get('createdAt', '')):<24} "
                f"{str(task.get('updatedAt', '')):<24}"
            )


def main():

    if len(sys.argv) < 2 or sys.argv[1] in ("-h", "--help"):
        print_help()
        return

    create_json_file()
    args = sys.argv[1:]
    if not args:
        print_help()
        return

    command = args[0]
    if command == "add" and len(args) > 1:
        description = " ".join(args[1:])
        add_task(description)
    elif command == "update" and len(args) > 2:
        task_id = args[1]
        description = " ".join(args[2:])
        update_task(task_id, description)
    elif command == "delete" and len(args) > 1:
        if args[1] == "all":
            confirm = input(CONFIRM_DELETE)
            if confirm.lower() == "yes":
                delete_task(None, delete_all=True)
            else:
                print("Delete all cancelled.")
        else:
            task_id = args[1]
            delete_task(task_id)
    elif command == "mark-in-progress" and len(args) > 1:
        task_id = args[1]
        mark_task(task_id, "in-progress")
    elif command == "mark-done" and len(args) > 1:
        task_id = args[1]
        mark_task(task_id, "done")
    elif command == "list":
        if len(args) == 1:
            list_tasks()
        elif args[1] == "done":
            list_tasks("done")
        elif args[1] == "todo":
            list_tasks("todo")
        elif args[1] == "in-progress":
            list_tasks("in-progress")
        else:
            print_help()
    else:
        print_help()


if __name__ == "__main__":
    main()
