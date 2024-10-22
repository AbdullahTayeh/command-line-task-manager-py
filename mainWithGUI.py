import json
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import ttkthemes

class ModernTaskManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Modern Task Manager")
        self.root.geometry("900x600")
        
        self.style = ttkthemes.ThemedStyle(self.root)
        self.style.set_theme("arc")
        
        self.tasks = self.load_tasks()
        self.setup_gui()
        
    def setup_gui(self):
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(1, weight=1)
        
        header_frame = ttk.Frame(self.root)
        header_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=5)
        
        ttk.Label(header_frame, text="New Task:", font=('Helvetica', 10)).pack(side="left", padx=5)
        self.task_entry = ttk.Entry(header_frame, width=40, font=('Helvetica', 10))
        self.task_entry.pack(side="left", padx=5)
        
        ttk.Label(header_frame, text="Priority:").pack(side="left", padx=5)
        self.priority_var = tk.StringVar(value="Medium")
        priority_combo = ttk.Combobox(header_frame, textvariable=self.priority_var, 
                                    values=["High", "Medium", "Low"], width=10)
        priority_combo.pack(side="left", padx=5)
        
        add_button = ttk.Button(header_frame, text="Add Task", command=self.add_task,
                              style="Accent.TButton")
        add_button.pack(side="left", padx=5)
        
        content_frame = ttk.Frame(self.root)
        content_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=5)
        content_frame.grid_columnconfigure(0, weight=1)
        content_frame.grid_rowconfigure(0, weight=1)
        
        self.tree = ttk.Treeview(content_frame, columns=("ID", "Description", "Status", "Priority", "Date"),
                                show="headings", selectmode="browse")
        
        self.tree.heading("ID", text="ID", command=lambda: self.sort_column("ID", False))
        self.tree.heading("Description", text="Description", command=lambda: self.sort_column("Description", False))
        self.tree.heading("Status", text="Status", command=lambda: self.sort_column("Status", False))
        self.tree.heading("Priority", text="Priority", command=lambda: self.sort_column("Priority", False))
        self.tree.heading("Date", text="Date Added", command=lambda: self.sort_column("Date", False))
        
        self.tree.column("ID", width=50, anchor="center")
        self.tree.column("Description", width=400)
        self.tree.column("Status", width=100, anchor="center")
        self.tree.column("Priority", width=100, anchor="center")
        self.tree.column("Date", width=150, anchor="center")
        
        scrollbar = ttk.Scrollbar(content_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")
        
        button_frame = ttk.Frame(content_frame)
        button_frame.grid(row=1, column=0, columnspan=2, pady=10)
        
        ttk.Button(button_frame, text="Complete Task", 
                  command=self.complete_task).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Delete Task", 
                  command=self.delete_task).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Clear Completed", 
                  command=self.clear_completed).pack(side="left", padx=5)
        
        self.status_var = tk.StringVar()
        status_bar = ttk.Label(self.root, textvariable=self.status_var, anchor="w")
        status_bar.grid(row=2, column=0, sticky="ew", padx=10, pady=5)
        
        self.task_entry.bind('<Return>', lambda e: self.add_task())
        self.tree.bind('<Double-1>', lambda e: self.toggle_status())
        
        self.refresh_tasks_display()
        
    def add_task(self):
        description = self.task_entry.get().strip()
        if description:
            new_id = len(self.tasks) + 1
            new_task = {
                "id": new_id,
                "description": description,
                "status": "Pending",
                "priority": self.priority_var.get(),
                "date": datetime.now().strftime("%Y-%m-%d %H:%M")
            }
            self.tasks.append(new_task)
            self.save_tasks()
            self.task_entry.delete(0, tk.END)
            self.refresh_tasks_display()
            self.status_var.set(f"Task added: {description}")
        else:
            messagebox.showwarning("Warning", "Please enter a task description")
            
    def toggle_status(self):
        selected_item = self.tree.selection()
        if selected_item:
            item = self.tree.item(selected_item[0])
            task_id = int(item['values'][0])
            for task in self.tasks:
                if task["id"] == task_id:
                    task["status"] = "Completed" if task["status"] == "Pending" else "Pending"
                    self.save_tasks()
                    self.refresh_tasks_display()
                    break

    def complete_task(self):
        selected_item = self.tree.selection()
        if selected_item:
            item = self.tree.item(selected_item[0])
            task_id = int(item['values'][0])
            for task in self.tasks:
                if task["id"] == task_id:
                    task["status"] = "Completed"
                    self.save_tasks()
                    self.refresh_tasks_display()
                    self.status_var.set("Task marked as completed")
                    break
        else:
            messagebox.showwarning("Warning", "Please select a task")

    def delete_task(self):
        selected_item = self.tree.selection()
        if selected_item:
            if messagebox.askyesno("Confirm", "Are you sure you want to delete this task?"):
                item = self.tree.item(selected_item[0])
                task_id = int(item['values'][0])
                self.tasks = [task for task in self.tasks if task["id"] != task_id]
                self.save_tasks()
                self.refresh_tasks_display()
                self.status_var.set("Task deleted")
        else:
            messagebox.showwarning("Warning", "Please select a task")

    def clear_completed(self):
        if messagebox.askyesno("Confirm", "Remove all completed tasks?"):
            self.tasks = [task for task in self.tasks if task["status"] != "Completed"]
            self.save_tasks()
            self.refresh_tasks_display()
            self.status_var.set("Completed tasks cleared")

    def sort_column(self, col, reverse):
        l = [(self.tree.set(k, col), k) for k in self.tree.get_children('')]
        l.sort(reverse=reverse)
        for index, (val, k) in enumerate(l):
            self.tree.move(k, '', index)
        self.tree.heading(col, command=lambda: self.sort_column(col, not reverse))

    def refresh_tasks_display(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        for task in self.tasks:
            values = (task["id"], task["description"], task["status"],
                     task.get("priority", "Medium"), task.get("date", ""))
            tag = "completed" if task["status"] == "Completed" else ""
            self.tree.insert("", "end", values=values, tags=(tag,))
        
        self.update_status_count()

    def update_status_count(self):
        total = len(self.tasks)
        completed = len([t for t in self.tasks if t["status"] == "Completed"])
        self.status_var.set(f"Total tasks: {total} | Completed: {completed} | Pending: {total-completed}")

    def load_tasks(self):
        try:
            with open("data.json", "r") as f:
                return json.load(f)
        except:
            return []

    def save_tasks(self):
        try:
            with open("data.json", "w") as f:
                json.dump(self.tasks, f, indent=2)
        except Exception as e:
            messagebox.showerror("Error", f"Error saving tasks: {str(e)}")

def main():
    root = tk.Tk()
    app = ModernTaskManager(root)
    root.mainloop()

if __name__ == "__main__":
    main()