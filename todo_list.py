import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import json
import os
from datetime import datetime, timedelta
import threading
import time
from plyer import notification

DATE_FORMAT = "%d/%m/%y"

def add_task(tasks, task, deadline=None):
    try:
        if deadline:
            deadline = datetime.strptime(deadline, DATE_FORMAT)
            if deadline < datetime.now():
                print("Deadline cannot be set for the past. Task added without deadline.")
                deadline = None
    except ValueError:
        print("Invalid date format. Task added without deadline.")
        deadline = None
    
    tasks.append({"task": task, "completed": False, "deadline": deadline})

def delete_task(tasks, index):
    if index < len(tasks):
        del tasks[index]
    else:
        print("Invalid index!")

def mark_task_complete(tasks, index):
    if index < len(tasks):
        tasks[index]["completed"] = True
    else:
        print("Invalid index!")

def list_tasks(tasks):
    for i, task in enumerate(tasks):
        status = "Completed" if task["completed"] else "Pending"
        deadline = task["deadline"].strftime(DATE_FORMAT) if task["deadline"] else "No deadline"
        print(f"{i + 1}. {task['task']} - Deadline: {deadline} - Status: {status}")

def save_tasks(tasks):
    serialized_tasks = []
    for task in tasks:
        serialized_task = task.copy()
        if serialized_task["deadline"]:
            serialized_task["deadline"] = serialized_task["deadline"].strftime(DATE_FORMAT)
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
                    if "deadline" not in task:
                        task["deadline"] = None
                    elif task["deadline"]:
                        task["deadline"] = datetime.strptime(task["deadline"], DATE_FORMAT)
                    tasks.append(task)
    except json.decoder.JSONDecodeError:
        print("Error loading tasks. File may be empty or corrupted.")
    
    return tasks

def check_approaching_deadlines(tasks):
    today = datetime.now()
    approaching_tasks = [task for task in tasks if task["deadline"] and not task["completed"] and task["deadline"] <= today + timedelta(days=2)]
    
    if approaching_tasks:
        for task in approaching_tasks:
            print(f"{task['task']} - Deadline: {task['deadline'].strftime(DATE_FORMAT)}")
            send_notification(task, "Approaching deadline")

def send_notification(task, message):
    notification.notify(
        title='Task Reminder',
        message=f"{message}: {task['task']} - Due: {task['deadline'].strftime(DATE_FORMAT)}",
        timeout=10
    )

def background_deadline_check():
    while True:
        check_approaching_deadlines(tasks)
        time.sleep(60)  # Check every 60 seconds

def add_task_click():
    task = entry_task.get()
    deadline = entry_deadline.get()
    add_task(tasks, task, deadline)
    save_tasks(tasks)
    list_tasks_in_gui()

def mark_complete_click():
    try:
        index = task_listbox.curselection()[0]
        mark_task_complete(tasks, index)
        save_tasks(tasks)
        list_tasks_in_gui()
    except IndexError:
        messagebox.showwarning("Warning", "Please select a task to mark as complete")

def delete_task_click():
    try:
        index = task_listbox.curselection()[0]
        delete_task(tasks, index)
        save_tasks(tasks)
        list_tasks_in_gui()
    except IndexError:
        messagebox.showwarning("Warning", "Please select a task to delete")

def check_approaching_deadlines_click():
    check_approaching_deadlines(tasks)

def list_tasks_in_gui():
    task_listbox.delete(0, tk.END)
    for task in tasks:
        status = "Completed" if task["completed"] else "Pending"
        deadline = task["deadline"].strftime(DATE_FORMAT) if task["deadline"] else "No deadline"
        task_listbox.insert(tk.END, f"{task['task']} - Deadline: {deadline} - Status: {status}")

# Initialize tkinter GUI
root = tk.Tk()
root.title("To-Do List App")

# Create GUI components
frame = tk.Frame(root)
frame.pack(padx=10, pady=10)

label_task = tk.Label(frame, text="Task:")
label_task.grid(row=0, column=0, padx=5, pady=5)

entry_task = tk.Entry(frame, width=50)
entry_task.grid(row=0, column=1, padx=5, pady=5)

label_deadline = tk.Label(frame, text="Deadline (DD/MM/YY hh:mma):")
label_deadline.grid(row=1, column=0, padx=5, pady=5)

entry_deadline = tk.Entry(frame, width=50)
entry_deadline.grid(row=1, column=1, padx=5, pady=5)

button_add_task = tk.Button(frame, text="Add Task", command=add_task_click)
button_add_task.grid(row=2, column=0, columnspan=2, padx=5, pady=5, sticky="WE")

task_listbox = tk.Listbox(root, width=100, height=15)
task_listbox.pack(padx=10, pady=10)

button_mark_complete = tk.Button(root, text="Mark Complete", command=mark_complete_click)
button_mark_complete.pack(padx=10, pady=5, fill="x")

button_delete_task = tk.Button(root, text="Delete Task", command=delete_task_click)
button_delete_task.pack(padx=10, pady=5, fill="x")

button_check_deadlines = tk.Button(root, text="Check Approaching Deadlines", command=check_approaching_deadlines_click)
button_check_deadlines.pack(padx=10, pady=5, fill="x")

# Load tasks initially
tasks = load_tasks()
list_tasks_in_gui()

# Start the deadline check in a background thread
thread = threading.Thread(target=background_deadline_check, daemon=True)
thread.start()

# Start the GUI event loop
root.mainloop()
