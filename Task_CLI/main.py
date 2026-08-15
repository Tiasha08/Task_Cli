#built a Task CLI that can be used to manage tasks in a simple way. The CLI allows users to add, view, and delete tasks from a task list. The tasks are stored in a JSON file for persistence.
import json
import os
from datetime import datetime
import argparse
from pdb import main
file_name = "tasks.json"

def load_tasks():
    if os.path.exists(file_name):
        with open(file_name, "r", encoding="utf-8") as file:
            return json.load(file)
    else:
        return []

def save_tasks(tasks):
   
    try:
        with open(file_name, "w", encoding="utf-8") as file:
            json.dump(tasks, file, indent=2)
    except OSError as e:
        print(f"Error saving to file: {e}")



def get_next_id(tasks):

    if not tasks:
        return 1
    else:
        return max(task["id"] for task in tasks) + 1
def main():
    parser = argparse.ArgumentParser(description="Task Tracker CLI")
    subparsers = parser.add_subparsers(dest="command")

    add_parser = subparsers.add_parser("add")
    add_parser.add_argument("description")

    list_parser = subparsers.add_parser("list")
    delete_parser = subparsers.add_parser("delete")
    delete_parser.add_argument("id", type=int)
    update_parser = subparsers.add_parser("update")
    update_parser.add_argument("id", type=int)
    update_parser.add_argument("description")
    markdone_parser = subparsers.add_parser("markdone")
    markdone_parser.add_argument("id", type=int)
    inprogress_parser = subparsers.add_parser("inprogress")
    inprogress_parser.add_argument("id", type=int)

    args = parser.parse_args()

    if args.command == "add":
        tasks = load_tasks()
        new_id = get_next_id(tasks)
        now = str(datetime.now())
        new_task = {
            "id": new_id,
            "description": args.description,
            "status": "todo",
            "createdAt": now,
            "updatedAt": now
        }
        tasks.append(new_task)
        save_tasks(tasks)
        print(f"Task added successfully (ID: {new_id})")
    elif args.command == "list":
        tasks = load_tasks()
        if not tasks:
            print("No tasks found.")
        else:
            for task in tasks:
                print(f"ID: {task['id']}, Description: {task['description']}, Status: {task['status']}, Created At: {task['createdAt']}, Updated At: {task['updatedAt']}")     
    elif args.command == "delete":
        tasks = load_tasks()
        tasks = [task for task in tasks if task["id"] != args.id]
        save_tasks(tasks)
        print(f"Task deleted successfully (ID: {args.id})")

    elif args.command == "update":
        tasks = load_tasks()
        for task in tasks:
            if task["id"] == args.id:
                task["description"] = args.description
                task["updatedAt"] = str(datetime.now())
                save_tasks(tasks)
                print(f"Task updated successfully (ID: {args.id})")
                break
            else:
                print(f"No task found with ID: {args.id}")
    elif args.command == "markdone":
        tasks = load_tasks()
        for task in tasks:
            if task["id"] == args.id:
                task["status"] = "done"
                task["updatedAt"] = str(datetime.now())
                save_tasks(tasks)
                print(f"Task marked as done (ID: {args.id})")
                break
        else:
            print(f"No task found with ID: {args.id}")
    elif args.command == "inprogress":
        tasks = load_tasks()
        for task in tasks:
            if task["id"] == args.id:
                task["status"] = "in progress"
                task["updatedAt"] = str(datetime.now())
                save_tasks(tasks)
                print(f"Task marked as in progress (ID: {args.id})")
                break
        else:
            print(f"No task found with ID: {args.id}")
if __name__ == "__main__":
    main()