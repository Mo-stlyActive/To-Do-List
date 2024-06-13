# todo_list.py

import json
import os
from datetime import datetime, timedelta

def add_task(tasks, task, deadline=None):
    try:
        if deadline:
            deadline = datetime.strptime(deadline, "%Y-%m-%d")
            if deadline.date() < datetime.now().date():
                print("Deadline cannot be set for the past. Task added without deadline.")
                deadline = None
    except ValueError:
        print("Invalid date format. Task added without deadline.")
        deadline = None
    
    tasks.append({"task": task, "completed": False, "deadline": deadline})


def delete_task(tasks, index):
    if index < len (tasks):
        del tasks[index]
    else:
        print("invalid index!")


def mark_task_complete(tasks,index):
    if index < len(tasks):
        tasks[index]["completed"] = True
    else:
        print("invalid index!")

def list_tasks(tasks):
    for i, task in enumerate(tasks):
        status = "Completed" if task["completed"] else "Pending"
        deadline = task["deadline"] if task["deadline"] else "No deadline"
        print(f"{i + 1}. {task['task']} - Deadline: {deadline} - Status: {status}")



def save_tasks(tasks):
    serialized_tasks = []
    for task in tasks:
        serialized_task = task.copy()
        if serialized_task["deadline"]:
            serialized_task["deadline"] = serialized_task["deadline"].strftime("%Y-%m-%d")
        serialized_tasks.append(serialized_task)
    
    with open("tasks.json", "w") as f:
        json.dump(serialized_tasks, f)

def load_tasks():
    tasks = []
    try:
        if os.path.exists("tasks.json"):
            with open("tasks.json", "r") as f:
                serialized_tasks = json.load(f)
                for serialized_task in serialized_tasks:
                    task = serialized_task.copy()
                    if task["deadline"]:
                        task["deadline"] = datetime.strptime(task["deadline"], "%Y-%m-%d")
                    tasks.append(task)
    except json.decoder.JSONDecodeError:
        print("Error loading tasks. File may be empty or corrupted.")
    
    return tasks


def check_approaching_deadlines(tasks):
    today = datetime.now().date()
    approaching_tasks = [task for task in tasks if task["deadline"] and not task["completed"] and task["deadline"].date() <= today + timedelta(days=2)]
    
    if approaching_tasks:
        print("\n===== Approaching Deadlines =====")
        for task in approaching_tasks:
            print(f"{task['task']} - Deadline: {task['deadline'].strftime('%Y-%m-%d')}")
            # Optionally, trigger a reminder notification here
            # Example: send_notification(task, "Approaching deadline")
    else:
        print("No approaching deadlines.")

def send_notification(task, message):
    # Placeholder for actual notification sending mechanism
    print(f"Reminder: {message} for task '{task['task']}'")

def main():
    tasks = load_tasks()
    
    while True:
        print("\n===== To-Do List Menu =====")
        print("1. Add Task")
        print("2. Mark Task Complete")
        print("3. Delete Task")
        print("4. List Tasks")
        print("5. Check Approaching Deadlines")
        print("6. Exit")
        
        choice = input("Enter your choice (1-5): ")
        
        if choice == '1':
            task = input("Enter task: ")
            deadline = input("Enter deadline (optional, format YYYY-MM-DD): ")
            add_task(tasks, task, deadline)
            save_tasks(tasks)
        elif choice == '2':
            index = int(input("Enter index of task to mark complete: ")) - 1
            mark_task_complete(tasks, index)
            save_tasks(tasks)
        elif choice == '3':
            index = int(input("Enter index of task to delete: ")) - 1
            delete_task(tasks, index)
            save_tasks(tasks)
        elif choice == '4':
            list_tasks(tasks)
        elif choice == '5':
            check_approaching_deadlines(tasks)
        elif choice == '6':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please enter a number from 1 to 5.")

    save_tasks(tasks)

if __name__ == "__main__":
    main()