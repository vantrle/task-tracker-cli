import json
import os
import pytest
import shutil

from task_tracker.cli import (
    add_task,
    create_json_file,
    delete_task,
    list_tasks,
    load_tasks,
    mark_task,
    update_task,
    JSON_FILE,
)


def setup_module(module):
    # Backup the original tasks.json if exists
    if os.path.exists(JSON_FILE):
        shutil.copy(JSON_FILE, JSON_FILE + ".bak")
        create_json_file()


def teardown_module(module):
    # Restore the original tasks.json
    if os.path.exists(JSON_FILE + ".bak"):
        shutil.move(JSON_FILE + ".bak", JSON_FILE)
    else:
        if os.path.exists(JSON_FILE):
            os.remove(JSON_FILE)


def test_add_task():
    add_task("Test task")
    tasks = load_tasks()
    assert len(tasks) == 1
    assert tasks[0]["description"] == "Test task"
    assert tasks[0]["status"] == "todo"


def test_update_task():
    add_task("Task to update")
    update_task(1, "Updated task")
    tasks = load_tasks()
    assert tasks[0]["description"] == "Updated task"


def test_delete_task():
    tasks = load_tasks()
    len_tasks = len(tasks)
    add_task("Task to delete")
    delete_task(len_tasks + 1)
    tasks = load_tasks()
    assert len(tasks) == len_tasks


def test_delete_all():
    add_task("Task 1")
    add_task("Task 2")
    tasks = load_tasks()
    len_tasks = len(tasks)
    add_task("Task to delete")
    delete_task(1)
    with open(JSON_FILE, "r") as f:
        tasks = json.load(f)
    assert len(tasks) == len_tasks


@pytest.mark.parametrize("status", ["done", "in-progress"])
def test_mark_task(status):
    add_task("Task to mark")
    mark_task(1, status)
    tasks = load_tasks()
    assert tasks[0]["status"] == status


def test_list_tasks(capsys):
    add_task("Task 1")
    add_task("Task 2")
    list_tasks()
    captured = capsys.readouterr()
    assert "Task 1" in captured.out
    assert "Task 2" in captured.out
