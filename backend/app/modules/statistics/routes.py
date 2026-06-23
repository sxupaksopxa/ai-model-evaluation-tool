from fastapi import APIRouter

router = APIRouter()


@router.get("/")
def get_statistics():
    return {
        "total_evaluations": 0,
        "total_ratings": 0,
        "models": [],
        "tasks": [],
        "message": "Statistics will be calculated after evaluations and ratings are stored.",
    }


@router.get("/models")
def get_model_statistics():
    return {
        "models": [],
        "message": "Model-level statistics are not available yet.",
    }


@router.get("/tasks")
def get_task_statistics():
    return {
        "tasks": [],
        "message": "Task-level statistics are not available yet.",
    }