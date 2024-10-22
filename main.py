import json

def load_tasks():
    try:
        with open("data.json", "r") as f:
            tasks = json.load(f)
        return tasks
    except:
        return []
def save_tasks(tasks):
    try:
        with open("data.json", "w") as f:
            json.dump(tasks, f)
        return f"Tasks saved successfully"
    except Exception as e:
        return f"Error saving tasks: {str(e)}" 

def add_tasks(tasks, description):
    new_id = len(tasks) + 1
    default_status = "incomplete"
    new_task = {
        "id": new_id, "description": description, "status": "incomplete"
    } 
    tasks.append(new_task)
    save_tasks(tasks)
    return f"task was added successfully"

def list_tasks(tasks):
    if len(tasks) == 0:
        return f"tasks list is empty"

    for task in tasks:
        print( f"Task ID: {task['id']} \n, Description: {task['description']} \n, Status: {task['status']}\n")


def complete_tasks(tasks, task_id):
    for task in tasks:
        if task["id"] == task_id:
            print("task founded")
            task["status"] = "complete"
            save_tasks(tasks)
            return f"task completed"
    
    return f"task not found"
        
def delete_tasks(tasks, task_id):
    for task in tasks:
        if task["id"] == task_id:
            tasks.remove(task)
            save_tasks(tasks)
            return f"task was removed successfully"
    return f"task not found"

def main():
    tasks = load_tasks()
    
    while True:
        command = input("Enter a command (add/list/complete/delete/quit): ").strip().lower()
        
        if command == "quit":
            save_tasks(tasks)
            break
        
        
        elif command == "add":
            description = input("Enter task description: ")
            result = add_tasks(tasks, description)
            print(result)
            
            
        elif command == "list":
            if len(tasks) == 0:
                print ("tasks list is empty")
            list_tasks(tasks)
            pass
            #or
            #result=list_tasks(tasks)
            #if result:
            # print(result)
            
        elif command == "complete":
            task_id = int(input("Enter task ID to mark as complete: "))
            result = complete_tasks(tasks, task_id)
            print (result)
            
            
        elif command == "delete":
            message = input("are you sure you want to delete this task?(True/False): ").lower()
            try:
                if message == "true":
                    task_id = int(input("Enter task ID for deletion: "))
                    result = delete_tasks(tasks, task_id)
                    print(result)
        
            except ValueError:
                print("please enter a valid numnber")
                continue
        
        
        else:
            print("Invalid comamnd. Please try again.")
    
    
if __name__ == "__main__":
    main()
