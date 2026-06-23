from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel, Field
import logging

from app.limiter import limiter
from app.modules.evaluations.service import evaluate_models

router = APIRouter()

logger = logging.getLogger(__name__)


class EvaluationRequest(BaseModel):
    task_id: str = Field(..., min_length=1)
    model_ids: list[str] = Field(..., min_length=1)
    input_text: str = Field(..., min_length=1, max_length=1000,)
    api_keys: dict[str, str] | None = None


@router.post("/")
@limiter.limit("10/minute")
async def evaluate(request: Request, payload: EvaluationRequest):
    """
    Evaluate the same input against one or many selected models.
    """

    try:
        result = await evaluate_models(
            task_id=payload.task_id,
            model_ids=payload.model_ids,
            input_text=payload.input_text,
            api_keys=payload.api_keys,
        )

        return result

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        )

    except Exception as exc:
        logger.error(f"Evaluation failed: {exc}")
        raise HTTPException(
            status_code=500,
            detail="Evaluation failed due to an internal error.",
        )