from pathlib import Path
import json

from fastapi import HTTPException


MODEL_REGISTRY_PATH = (
    Path(__file__).resolve().parents[2]
    / "datasets"
    / "seed"
    / "model_registry.json"
)


def load_models() -> list[dict]:
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


def get_model_by_id(model_id: str) -> dict:
    models = load_models()

    model = next(
        (model for model in models if model.get("id") == model_id),
        None,
    )

    if not model:
        raise ValueError(f"Model '{model_id}' not found")

    return model


def get_models_by_task(task_id: str) -> list[dict]:
    models = load_models()

    return [
        model for model in models
        if task_id in model.get("supported_tasks", [])
    ]