# KidsCode-Lab 
# L2 - Lesson 02

# CustomTkiner To-Do List API Client - Student Template
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
# Assumed to be provided and working.
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
    """Grid a widget with sane defaults and return it."""
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

# ---------- Command factory helpers (given) ----------
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

# ---------- App entry ----------
def main():
    # set your class code and student ID (or read from .env in your API class)
    class_code = "LEVEL_2"
    student_id = "STUDENT01"

    state = {
        "root": ctk.CTk(),                 # main window
        "api": TodoAPI(class_code, student_id),  # API client instance
        "task_title_var": ctk.StringVar(), # task title input
        "due_date_var": ctk.StringVar(),   # due date input
        "scroll": None,                    # scrollable frame for tasks
    }

    root = state["root"]
    root.title("To-Do List")
    root.geometry("800x560")
    root.minsize(760, 520)

    apply_window_icon(root)

    # Layout: add form (row 0), list (row 1)
    configure_grid(root, col_weights=[1], row_weights=[0, 1])

    build_add_form(root, state)
    build_task_list(root, state)
    refresh_tasks(state, first_run=True)

    root.mainloop()

# ---------- UI builders ----------
def build_add_form(root, state):
    """Top form for entering a task title and due date."""
    form = ctk.CTkFrame(root, corner_radius=12)
    place(form, 0, 0, padx=10, pady=10)
    configure_grid(form, col_weights=[0, 1, 0, 1, 1, 0])

    # Labels + Entries
    place(ctk.CTkLabel(form, text="Task"), 0, 0, sticky="e")
    place(ctk.CTkEntry(form, textvariable=state["task_title_var"],
                       placeholder_text="e.g., Finish worksheet"), 0, 1)

    place(ctk.CTkLabel(form, text="Due (YYYY-MM-DD)"), 0, 2, sticky="e")
    place(ctk.CTkEntry(form, textvariable=state["due_date_var"],
                       placeholder_text="YYYY-MM-DD", width=140), 0, 3)

    place(ctk.CTkLabel(form, text=""), 0, 4)  # spacer grows

    # ---------- TODO 1 ----------
    # Create the "Add" button and place it at (row=0, col=5).
    # Requirements:
    #   - text="Add"
    #   - width=100
    #   - command should be the function returned by make_on_add_command(state)
    #
    # Example call shape (fill in the args yourself):
    # add_btn = ctk.CTkButton(form, text=..., width=..., command=...)
    # place(add_btn, 0, 5, sticky="e")
    # --------------------------------
    # YOUR CODE HERE


def build_task_list(root, state):
    """Scrollable area to display task cards."""
    ctk.set_widget_scaling(1.0)
    outer = ctk.CTkFrame(root, corner_radius=12)
    place(outer, 1, 0, padx=10, pady=(0, 10), sticky="nsew")
    configure_grid(outer, col_weights=[1], row_weights=[1])

    scroll = ctk.CTkScrollableFrame(outer, corner_radius=12)
    place(scroll, 0, 0, padx=8, pady=8, sticky="nsew")
    configure_grid(scroll, col_weights=[1])
    state["scroll"] = scroll

# ---------- Actions ----------
def on_add(state):
    """Add a new task: read inputs, validate, call API, refresh."""
    # ---------- TODO 2 ----------
    # Steps to implement:
    # 1) Read text from state["task_title_var"] and state["due_date_var"]
    #    (trim with .strip())
    # 2) If title is empty -> show messagebox.showwarning and return.
    # 3) If due date is provided, validate with datetime.strptime(due, "%Y-%m-%d").
    #    If invalid, show messagebox.showwarning and return.
    # 4) Call state["api"].add_task(title, due)
    # 5) Clear the two StringVars (set them to "")
    # 6) Call refresh_tasks(state)
    #
    # Use try/except around the API call and show messagebox.showerror on failure.
    # --------------------------------
    # YOUR CODE HERE
    messagebox.showinfo("TODO", "on_add() is not implemented yet. Complete TODO 2.")


def refresh_tasks(state, first_run=False):
    """Fetch tasks from the API and render them."""
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


def mark_done_id(state, task_id):
    """Mark a task as done by its ID."""
    try:
        state["api"].mark_done(task_id)
        refresh_tasks(state)
    except Exception as e:
        messagebox.showerror("Mark Done", f"Failed: {e}")


def delete_id(state, task_id):
    """Delete a task by its ID."""
    try:
        state["api"].delete_task(task_id)
        refresh_tasks(state)
    except Exception as e:
        messagebox.showerror("Delete", f"Failed: {e}")

# ---------- Rendering ----------
def render_tasks(state, tasks):
    """Render tasks inside the scrollable frame as simple 'cards'."""
    scroll = state["scroll"]

    # Clear previous
    for w in scroll.winfo_children():
        w.destroy()

    if not tasks:
        place(ctk.CTkLabel(scroll, text="No tasks yet.", font=("Segoe UI", 12)), 0, 0, sticky="w")
        return

    today = date.today()

    for i, t in enumerate(tasks):
        tid   = t.get("id")
        title = t.get("title") or t.get("task") or "(untitled)"
        due   = t.get("due_date") or t.get("expiration_date") or ""
        done  = bool(t.get("done"))

        row = ctk.CTkFrame(scroll, corner_radius=10)
        place(row, i, 0, padx=8, pady=6, sticky="ew")
        configure_grid(row, col_weights=[1, 0])

        # ---------- TODO 3 ----------
        # HINTS:
        # - Use datetime.strptime(due, "%Y-%m-%d").date() and compare with 'today'.
        # - Use the provided 'place' helper to grid each widget.
        # - Create the buttons inside a small CTkFrame with fg_color="transparent".
        # --------------------------------

        # A) Add a CTkLabel to show the task title at (row=0, col=0),
        #    font=("Segoe UI", 14), left aligned.
        # YOUR CODE HERE


        # B) Add a status badge (Done/Pending) at (row=0, col=1).
        #    - text: "Done" if done else "Pending"
        #    - colors: done -> "#16a34a", pending -> "#64748b"
        #    - font=("Segoe UI", 11, "bold"), text_color="white",
        #      corner_radius=999, some padding (padx=12, pady=6)
        # YOUR CODE HERE


        # C) Add a "Due:" label at (row=1, col=0), font=("Segoe UI", 12).
        #    If overdue and not done, show amber-ish color:
        #    meta_color = ("#a16207", "#f59e0b"); otherwise grey:
        #    meta_color = ("#6b7280", "#9ca3af")
        # YOUR CODE HERE
        
        
        # D) Create a small button frame at (row=1, col=1),
        #    and add two buttons:
        #       - "✓" (width=36, height=28), disabled if done,
        #         command = make_mark_done_command(state, tid)
        #       - "🗑" (width=36, height=28), red colors, command = make_delete_command(state, tid)
        #
        # YOUR CODE HERE


# ---------- Run ----------
if __name__ == "__main__":
    main()
