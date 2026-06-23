import json
import logging

from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field

from app.limiter import limiter
from app.modules.evaluations.service import (
    evaluate_models,
    evaluate_models_streaming,
)

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
    Returns the complete result after all models finish.
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


@router.post("/stream")
@limiter.limit("10/minute")
async def evaluate_stream(request: Request, payload: EvaluationRequest):
    """
    Evaluate models with Server-Sent Events (SSE) streaming.
    Yields per-model progress updates as each model completes.
    """

    async def event_generator():
        try:
            async for update in evaluate_models_streaming(
                task_id=payload.task_id,
                model_ids=payload.model_ids,
                input_text=payload.input_text,
                api_keys=payload.api_keys,
            ):
                yield f"data: {json.dumps(update)}\n\n"
            yield "data: [DONE]\n\n"
        except ValueError as exc:
            yield f"data: {json.dumps({'error': str(exc)})}\n\n"
        except Exception as exc:
            logger.error(f"Streaming evaluation failed: {exc}")
            yield f"data: {json.dumps({'error': 'Evaluation failed due to an internal error.'})}\n\n"

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
        },
    )
