# todo_list.py
import tkinter as tk
from tkinter import messagebox
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

# Function to handle button click events

def add_task_click():
    task = entry_task.get()
    deadline = entry_deadline.get()
    add_task(tasks, task, deadline)
    save_tasks(tasks)
    list_tasks_in_gui()

def mark_complete_click():
    index = int(entry_index.get()) - 1
    mark_task_complete(tasks, index)
    save_tasks(tasks)
    list_tasks_in_gui()

def delete_task_click():
    index = int(entry_index.get()) - 1
    delete_task(tasks, index)
    save_tasks(tasks)
    list_tasks_in_gui()

def check_approaching_deadlines_click():
    check_approaching_deadlines(tasks)

def list_tasks_in_gui():
    list_tasks(tasks)
    # Update GUI list view here

# Initialize tkinter GUI

root = tk.Tk()
root.title("To-Do List App")

# Create GUI components

label_task = tk.Label(root, text="Task:")
label_task.grid(row=0, column=0, padx=10, pady=10)

entry_task = tk.Entry(root, width=50)
entry_task.grid(row=0, column=1, padx=10, pady=10)

label_deadline = tk.Label(root, text="Deadline (YYYY-MM-DD):")
label_deadline.grid(row=1, column=0, padx=10, pady=10)

entry_deadline = tk.Entry(root, width=50)
entry_deadline.grid(row=1, column=1, padx=10, pady=10)

button_add_task = tk.Button(root, text="Add Task", command=add_task_click)
button_add_task.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky="WE")

label_index = tk.Label(root, text="Task Index:")
label_index.grid(row=3, column=0, padx=10, pady=10)

entry_index = tk.Entry(root, width=50)
entry_index.grid(row=3, column=1, padx=10, pady=10)

button_mark_complete = tk.Button(root, text="Mark Complete", command=mark_complete_click)
button_mark_complete.grid(row=4, column=0, columnspan=2, padx=10, pady=10, sticky="WE")

button_delete_task = tk.Button(root, text="Delete Task", command=delete_task_click)
button_delete_task.grid(row=5, column=0, columnspan=2, padx=10, pady=10, sticky="WE")

button_check_deadlines = tk.Button(root, text="Check Approaching Deadlines", command=check_approaching_deadlines_click)
button_check_deadlines.grid(row=6, column=0, columnspan=2, padx=10, pady=10, sticky="WE")

# Load tasks initially
tasks = load_tasks()
list_tasks_in_gui()

# Start the GUI event loop
root.mainloop()