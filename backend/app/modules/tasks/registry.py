from pathlib import Path
import json

from fastapi import HTTPException


TASK_REGISTRY_PATH = (
    Path(__file__).resolve().parents[2]
    / "datasets"
    / "seed"
    / "task_registry.json"
)


def load_tasks() -> list[dict]:
    try:
        with open(TASK_REGISTRY_PATH, "r", encoding="utf-8") as file:
            return json.load(file)

    except FileNotFoundError:
        raise HTTPException(
            status_code=500,
            detail="task_registry.json not found",
        )

    except json.JSONDecodeError:
        raise HTTPException(
            status_code=500,
            detail="Invalid task_registry.json format",
        )


def get_task_by_id(task_id: str) -> dict:
    tasks = load_tasks()

    task = next(
        (task for task in tasks if task.get("id") == task_id),
        None,
    )

    if not task:
        raise ValueError(f"Task '{task_id}' not found")

    return task