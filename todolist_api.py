# KidsCode-Lab 
# L2 - Lesson 02

# CustomTkiner To-Do List API Server
#   This Flask-based module provides a APIs for interacting with To-Do thin client
#   It allows listing, adding, deleting, and marking tasks as done

# This moduel has deployed to Azure App Service
#   https://kidscode-lab-todo.azurewebsites.net

# Use below URL to check health of the API:
#   https://kidscode-lab-todo.azurewebsites.net/api/health
#
# On GUI .env file, update API URL, Class Code, and Student ID:#       TODO_API_BASE  = "https://kidscode-lab-todo.azurewebsites.net"
#       CLASS_CODE     = "LEVEL_2"
#       STUDENT_ID   = "STUDENT01"

import os
import json
import requests
from dataclasses import dataclass

try:
    # Optional: load settings from .env if python-dotenv is installed
    # (pip install python-dotenv) — safe to ignore if not present
    from dotenv import load_dotenv  # type: ignore
    load_dotenv()
except Exception:
    pass

# ---- Defaults / settings ----
DEFAULT_BASE_URL  = "http://127.0.0.1:5000"
DEFAULT_CLASS     = "LEVEL_2"
DEFAULT_STUDENT   = "STUDENT01"
DEFAULT_API_KEY   = ""  # optional

def _getenv(name: str, default: str) -> str:
    return os.environ.get(name, default).strip() or default

@dataclass
class Settings:
    base_url: str
    class_code: str
    student_id: str
    api_key: str

    @classmethod
    def from_env(cls) -> "Settings":
        return cls(
            base_url=_getenv("TODO_API_BASE", DEFAULT_BASE_URL).rstrip("/"),
            class_code=_getenv("CLASS_CODE", DEFAULT_CLASS),
            student_id=_getenv("STUDENT_ID", DEFAULT_STUDENT),
            api_key=_getenv("API_KEY", DEFAULT_API_KEY),
        )

class TodoAPI:
    """Thin client for your Flask To-Do API."""

    def __init__(self, 
                 class_code: str | None = None,
                 student_id: str | None = None,
                 base_url: str | None = None,
                 api_key: str | None = None):
        s = Settings.from_env()
        self.base_url  = (base_url or s.base_url).rstrip("/")
        self.class_code = class_code or s.class_code
        self.student_id = student_id or s.student_id
        self.api_key    = api_key or s.api_key

    # ---- internal helpers ----
    def _q(self) -> dict:
        return {"class_code": self.class_code, "student_id": self.student_id}

    def _headers(self) -> dict:
        h = {
            "X-Class-Code": self.class_code,
            "X-Student-Id": self.student_id,
        }
        if self.api_key:
            h["X-API-Key"] = self.api_key
        return h

    # ---- public methods ----
    def health(self) -> dict:
        r = requests.get(f"{self.base_url}/api/health", timeout=10)
        r.raise_for_status()
        return r.json()

    def list_tasks(self) -> list[dict]:
        r = requests.get(f"{self.base_url}/api/tasks",
                         params=self._q(), headers=self._headers(), timeout=15)
        r.raise_for_status()
        return r.json()

    def add_task(self, title: str, due_date_str: str | None):
        data = {
            "task": title,
            "expiration_date": due_date_str or ""
        }
        r = requests.post(f"{self.base_url}/add",
                          params=self._q(), headers=self._headers(), data=data, timeout=15)
        if r.status_code not in (200, 201, 204, 302, 303):
            r.raise_for_status()
        return True

    def delete_task(self, task_id: int):
        r = requests.get(f"{self.base_url}/delete/{task_id}",
                         params=self._q(), headers=self._headers(), timeout=15)
        if r.status_code not in (200, 204, 302, 303):
            r.raise_for_status()
        return True

    def mark_done(self, task_id: int):
        r = requests.get(f"{self.base_url}/done/{task_id}",
                         params=self._q(), headers=self._headers(), timeout=15)
        if r.status_code not in (200, 204, 302, 303):
            r.raise_for_status()
        return True
