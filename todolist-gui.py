# KidsCode-Lab 
# L2 - Lesson 02

# CustomTkiner To-Do List API Client - Full Functional Answer
#   This module provides a thin client for interacting with a Flask-based To-Do API.
#   It allows listing, adding, deleting, and marking tasks as done.

# Update API URL, Class Code, and Student ID .env file:
#       TODO_API_BASE  = "https://kidscode-lab-todo.azurewebsites.net"
#       CLASS_CODE     = "LEVEL_2"
#       STUDENT_ID   = "STUDENT01"

import os, sys
import tkinter as tk
from tkinter import messagebox
from datetime import datetime, date
import customtkinter as ctk

# API client for your Flask To-Do API
from todolist_api import TodoAPI

# ---------- Theme ----------
# "Dark" | "Light" | "System"
ctk.set_appearance_mode("Dark")
# "blue" | "green" | "dark-blue" | "dark-green"        
ctk.set_default_color_theme("blue")

# ---------- Layout helpers ----------
DEFAULT_PADX = 5
DEFAULT_PADY = 5
DEFAULT_STICKY = "ew"

def place(widget, row, col, *, padx=DEFAULT_PADX, pady=DEFAULT_PADY, sticky=DEFAULT_STICKY, **kw):
    """
    Grid a widget with sane defaults and return it
    Example: title = place(ctk.CTkLabel(frame, text="Title"), 0, 0)
    """
    widget.grid(row=row, column=col, padx=padx, pady=pady, sticky=sticky, **kw)
    return widget

def configure_grid(frame, *, col_weights=None, row_weights=None):
    """Apply weights in one call. Example: configure_grid(f, col_weights=[0,1,0])."""
    if col_weights:
        for i, w in enumerate(col_weights):
            frame.grid_columnconfigure(i, weight=w)
    if row_weights:
        for i, w in enumerate(row_weights):
            frame.grid_rowconfigure(i, weight=w)

# ---------- Helper: Command factory ----------
def make_on_add_command(state):
    """Return a function the 'Add' button can call (no parameters)."""
    def cmd():
        on_add(state)
    return cmd

def make_mark_done_command(state, task_id):
    """Return a function the '✓' button can call for this task."""
    def cmd():
        mark_done_id(state, task_id)
    return cmd

def make_delete_command(state, task_id):
    """Return a function the '🗑' button can call for this task."""
    def cmd():
        delete_id(state, task_id)
    return cmd

# ---------- Windows Icon ----------
def resource_path(rel_path: str) -> str:
    """Get absolute path to resource, works for dev and for PyInstaller --onefile."""
    if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, rel_path)  # temp folder created by PyInstaller
    return os.path.join(os.path.dirname(__file__), rel_path)

def apply_window_icon(root: tk.Tk):
    # Prefer .ico on Windows
    ico = resource_path("favicon.ico")
    if os.path.exists(ico):
        try:
            root.iconbitmap(ico)  # Windows
            return
        except Exception:
            pass
    # Fallback for non-Windows (if you later add PNG)
    png = resource_path("favicon.png")
    if os.path.exists(png):
        try:
            img = tk.PhotoImage(file=png)
            root.iconphoto(True, img)  # sets default for all toplevels
        except Exception:
            pass

# ---------- App entry ----------
def main():
    # Dictionary to hold app state

    # set your class code and student ID
    class_code = "LEVEL_2"  
    student_id = "STUDENT01"

    state = { 
        "root": ctk.CTk(),  # main window
        "api": TodoAPI(class_code, student_id),     # your API client instance
        "task_title_var": ctk.StringVar(),          # task title input
        "due_date_var": ctk.StringVar(),            # due date input
        "scroll": None,                             # scrollable frame for tasks
    }

    # Setup main window
    root = state["root"]
    root.title("To-Do List")
    root.geometry("800x560")
    root.minsize(760, 520)

    # Set icon (Windows .ico)
    apply_window_icon(root)

    # Create a 2-row layout: add form (row 0), list (row 1)
    configure_grid(root, col_weights=[1], row_weights=[0, 1])

    build_add_form(root, state)
    build_task_list(root, state)
    refresh_tasks(state, first_run=True)

    root.mainloop()

# ---------- UI builders ----------

# Build the "Add Task" form at the top of the window
# This contains input fields for task title and due date, and an "Add" button.
def build_add_form(root, state):

    # Create a frame for the form
    form = ctk.CTkFrame(root, corner_radius=12)

    # Place it in the first row of the main window
    place(form, 0, 0, padx=10, pady=10)

    # Create a 6 columns grid: [Task label][Task entry][Due label][Due entry][spacer][Add]
    configure_grid(form, col_weights=[0, 1, 0, 1, 1, 0])

    # Add widgets to the grid in the form
    place(ctk.CTkLabel(form, text="Task"), 0, 0, sticky="e")
    place(ctk.CTkEntry(form, textvariable=state["task_title_var"],
                       placeholder_text="e.g., Finish worksheet"), 0, 1)

    place(ctk.CTkLabel(form, text="Due (YYYY-MM-DD)"), 0, 2, sticky="e")
    place(ctk.CTkEntry(form, textvariable=state["due_date_var"],
                       placeholder_text="YYYY-MM-DD", width=140), 0, 3)

    place(ctk.CTkLabel(form, text=""), 0, 4)  # spacer grows (col weight=1)
    place(ctk.CTkButton(form, text="Add", width=100,
                        command=make_on_add_command(state)), 0, 5, sticky="e")

# Build the task list area below the form
# This is a scrollable frame that will contain task "cards".
def build_task_list(root, state):
    # Create a frame to hold the scrollable area
    # This frame will have rounded corners and will be placed in the second row
    # of the main window (row 1).
    ctk.set_widget_scaling(1.0)
    outer = ctk.CTkFrame(root, corner_radius=12)
    place(outer, 1, 0, padx=10, pady=(0, 10), sticky="nsew")
    configure_grid(outer, col_weights=[1], row_weights=[1])

    # Scrollable area of task "cards"
    scroll = ctk.CTkScrollableFrame(outer, corner_radius=12)
    place(scroll, 0, 0, padx=8, pady=8, sticky="nsew")
    configure_grid(scroll, col_weights=[1])
    state["scroll"] = scroll

    # Content inside the scrollable frame will be dynamically populated
    # with task cards when tasks are fetched from the API.

# ---------- Actions ----------

# Action to add a new task
# This reads the title and due date from the input fields,
# validates them, and calls the API to add the task.
def on_add(state):
    title = (state["task_title_var"].get() or "").strip()
    due   = (state["due_date_var"].get() or "").strip()

    if not title:
        messagebox.showwarning("Missing", "Please enter a task title.")
        return

    if due:
        try:
            datetime.strptime(due, "%Y-%m-%d")
        except ValueError:
            messagebox.showwarning("Invalid date", "Please use YYYY-MM-DD.")
            return

    try:
        state["api"].add_task(title, due)
        state["task_title_var"].set("")
        state["due_date_var"].set("")
        refresh_tasks(state)
    except Exception as e:
        messagebox.showerror("Add Task", f"Failed to add task:\n{e}")

# Refresh the task list by fetching tasks from the API
# If it's the first run, show an info message if it fails.
# Otherwise, show an error message.
def refresh_tasks(state, first_run=False):
    try:
        tasks = state["api"].list_tasks()
    except Exception as e:
        msg = (
            "Could not reach the API.\n\n"
            "Ensure server is running and\n"
            "TODO_API_BASE / CLASS_CODE / STUDENT_ID are set.\n\n"
            f"Error: {e}"
        )
        (messagebox.showinfo if first_run else messagebox.showerror)("Refresh", msg)
        return
    render_tasks(state, tasks)

# Mark a task as done by its ID
# This updates the task status in the API and refreshes the task list.
def mark_done_id(state, task_id):
    try:
        state["api"].mark_done(task_id)
        refresh_tasks(state)
    except Exception as e:
        messagebox.showerror("Mark Done", f"Failed: {e}")

# Delete a task by its ID
# This removes the task from the API and refreshes the task list.
def delete_id(state, task_id):
    try:
        state["api"].delete_task(task_id)
        refresh_tasks(state)
    except Exception as e:
        messagebox.showerror("Delete", f"Failed: {e}")

# ---------- Task (Card) Rendering ----------

# Render the list of tasks in the scrollable frame
# This creates a card for each task with title, due date, status badge,
# and action buttons (mark done, delete).
def render_tasks(state, tasks):
    scroll = state["scroll"]

    # clear previous
    for w in scroll.winfo_children():
        w.destroy()

    if not tasks:
        place(ctk.CTkLabel(scroll, text="No tasks yet.", font=("Segoe UI", 12)), 0, 0, sticky="w")
        return

    today = date.today()

    # Sort tasks by due date (if available) and title
    for i, t in enumerate(tasks):
        tid   = t.get("id")
        title = t.get("title") or t.get("task") or "(untitled)"
        due   = t.get("due_date") or t.get("expiration_date") or ""
        done  = bool(t.get("done"))

        # Create a row frame for each task
        # This will contain the title, status badge, meta info, and buttons.
        row = ctk.CTkFrame(scroll, corner_radius=10)
        place(row, i, 0, padx=8, pady=6, sticky="ew")
        # columns: text (expands), badge/buttons (fixed)
        configure_grid(row, col_weights=[1, 0])

        # Top-left: task title
        place(ctk.CTkLabel(row, text=title, font=("Segoe UI", 14), anchor="w", justify="left"),
              0, 0, padx=10, pady=(10, 0), sticky="w")

        # Top-right: status badge (same column as done and delete buttons to align)
        badge_text  = "Done" if done else "Pending"
        badge_color = "#16a34a" if done else "#64748b"
        place(ctk.CTkLabel(row, text=badge_text, font=("Segoe UI", 11, "bold"),
                           fg_color=badge_color, text_color="white",
                           corner_radius=999, padx=12, pady=6),
              0, 1, padx=10, pady=(10, 0), sticky="e")

        # Bottom-left: meta (due date; amber if overdue and not done)
        meta_text  = f"Due: {due}" if due else " "
        meta_color = ("#6b7280", "#9ca3af")
        try:
            if due and (not done) and datetime.strptime(due, "%Y-%m-%d").date() < today:
                meta_color = ("#a16207", "#f59e0b")
        except Exception:
            pass
        place(ctk.CTkLabel(row, text=meta_text, font=("Segoe UI", 12), text_color=meta_color),
              1, 0, padx=10, pady=(2, 10), sticky="w")

        # Bottom-right: row-only action buttons (under badge)
        btns = ctk.CTkFrame(row, fg_color="transparent")
        place(btns, 1, 1, padx=10, pady=(0, 8), sticky="e")

        place(ctk.CTkButton(btns, text="✓", width=36, height=28,
                            state="disabled" if done else "normal",
                            command=make_mark_done_command(state, tid)),
                            0, 0)
        place(ctk.CTkButton(btns, text="🗑", width=36, height=28,
                            fg_color="#ef4444", hover_color="#dc2626",
                            command=make_delete_command(state, tid)),
                            0, 1)

# ---------- Run ----------
if __name__ == "__main__":
    main()
