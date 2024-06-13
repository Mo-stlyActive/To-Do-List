# todo_list.py

def add_task(tasks, task):
    tasks.append({"task": task, "completed":False})


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
    for i, tasks in enumerate(tasks):
        status = "Completed" if tasks["completed"] else "Pending"
        print(f"{i+1}. {task['task']} - {status}")





def main():
    tasks = []

    while True:
        print("\n===== TO-DO List Menu ======")
        print("1. Add Task")
        print("2. Mark Task Complete")
        print("3. Delete Task")
        print("4. List Tasks")
        print("5. Exit")

        choice = input("Enter your choice (1-5): ")

        if choice == '1':
            task = input("Enter task: ")
            add_task(tasks, task)
        elif choice == '2':
            index = int(input("Enter index of task to mark complete: ")) - 1
            mark_task_complete(tasks, index)
        elif choice == '3':
            index = int(input("Enter index of task to delete: ")) - 1
            delete_task(tasks, index)
        elif choice == '4':
            list_tasks(tasks)
        elif choice == '5':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please enter a number from 1 to 5.")


if __name__ == "__main__":
    main()