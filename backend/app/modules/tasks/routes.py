from pathlib import Path
import json

from fastapi import APIRouter, HTTPException

router = APIRouter()

TASK_REGISTRY_PATH = (
    Path(__file__).resolve().parents[2]
    / "datasets"
    / "seed"
    / "task_registry.json"
)


def load_tasks():
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


@router.get("/")
def get_tasks():
    """
    Returns all supported task types.
    """
    return load_tasks()


@router.get("/{task_id}")
def get_task(task_id: str):
    """
    Returns a specific task definition.
    """
    tasks = load_tasks()

    task = next(
        (task for task in tasks if task["id"] == task_id),
        None,
    )

    if not task:
        raise HTTPException(
            status_code=404,
            detail=f"Task '{task_id}' not found",
        )

    return task