from pathlib import Path
import json

from fastapi import APIRouter, HTTPException, Query

router = APIRouter()

MODEL_REGISTRY_PATH = (
    Path(__file__).resolve().parents[2]
    / "datasets"
    / "seed"
    / "model_registry.json"
)


def load_models():
    try:
        with open(MODEL_REGISTRY_PATH, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        raise HTTPException(
            status_code=500,
            detail="model_registry.json not found",
        )
    except json.JSONDecodeError:
        raise HTTPException(
            status_code=500,
            detail="Invalid model_registry.json format",
        )


@router.get("/")
def get_models(task_id: str | None = Query(default=None)):
    """
    Returns all models.

    Optional:
    - filter by task_id
    Example:
    /api/models?task_id=summarization
    """
    models = load_models()

    if task_id:
        models = [
            model for model in models
            if task_id in model.get("supported_tasks", [])
        ]

    return models


@router.get("/{model_id}")
def get_model(model_id: str):
    """
    Returns a specific model definition.
    """
    models = load_models()

    model = next(
        (model for model in models if model["id"] == model_id),
        None,
    )

    if not model:
        raise HTTPException(
            status_code=404,
            detail=f"Model '{model_id}' not found",
        )

    return model