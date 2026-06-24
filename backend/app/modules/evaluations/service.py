import asyncio
import time

from app.modules.models.registry import get_model_by_id
from app.modules.tasks.registry import get_task_by_id
from app.modules.providers.provider_factory import get_provider
from app.modules.analysis.service import generate_basic_analysis

from app.modules.analysis.templates import build_prompt
from app.modules.analysis.template_or import build_openrouter_prompt


async def _evaluate_single_model(
    model_id: str,
    task_id: str,
    input_text: str,
    api_keys: dict[str, str] | None = None,
) -> dict:
    model = get_model_by_id(model_id)

    if task_id not in model.get("supported_tasks", []):
        return {
            "model_id": model_id,
            "status": "unsupported_task",
            "output": None,
            "analysis": None,
            "estimated_cost": None,
            "latency_ms": None,
        }

    provider = get_provider(model["provider"])

    if model["type"] in [
        "classification",
        "embedding",
        "question_answering",
    ]:
        prompt = input_text

    elif model["provider"] == "OpenRouter":
        prompt = build_openrouter_prompt(
            task_id,
            input_text,
        )

    else:
        prompt = build_prompt(
            task_id,
            input_text,
        )

    start_time = time.time()

    try:
        provider_result = await provider.run(
            model=model,
            task_id=task_id,
            prompt=prompt,
            api_keys=api_keys,
        )

        latency_ms = round((time.time() - start_time) * 1000)

        output = provider_result.get("output", "")

        return {
            "model_id": model_id,
            "model_name": model["name"],
            "provider": model["provider"],
            "status": "success",
            "output": output,
            "score": provider_result.get("score"),
            "analysis": generate_basic_analysis(output),
            "estimated_cost": provider_result.get("estimated_cost"),
            "latency_ms": latency_ms,
        }

    except Exception as exc:
        return {
            "model_id": model_id,
            "model_name": model.get("name"),
            "provider": model.get("provider"),
            "status": "failed",
            "error": str(exc),
            "output": None,
            "analysis": None,
            "estimated_cost": None,
            "latency_ms": None,
        }


async def evaluate_models(
    task_id: str,
    model_ids: list[str],
    input_text: str,
    api_keys: dict[str, str] | None = None,
) -> dict:
    task = get_task_by_id(task_id)

    results = []

    for model_id in model_ids:
        try:
            result = await asyncio.wait_for(
                _evaluate_single_model(
                    model_id,
                    task_id,
                    input_text,
                    api_keys,
                ),
                timeout=120,
            )
        except asyncio.TimeoutError:
            model = get_model_by_id(model_id)
            result = {
                "model_id": model_id,
                "model_name": model.get("name"),
                "provider": model.get("provider"),
                "status": "failed",
                "error": "Model evaluation timed out after 120 seconds.",
                "output": None,
                "analysis": None,
                "estimated_cost": None,
                "latency_ms": None,
            }
        results.append(result)

    return {
        "task_id": task_id,
        "task_name": task["name"],
        "input_text": input_text,
        "results": results,
    }


async def evaluate_models_streaming(
    task_id: str,
    model_ids: list[str],
    input_text: str,
    api_keys: dict[str, str] | None = None,
):
    task = get_task_by_id(task_id)
    total = len(model_ids)

    for i, model_id in enumerate(model_ids):
        try:
            result = await asyncio.wait_for(
                _evaluate_single_model(
                    model_id,
                    task_id,
                    input_text,
                    api_keys,
                ),
                timeout=120,
            )
        except asyncio.TimeoutError:
            model = get_model_by_id(model_id)
            result = {
                "model_id": model_id,
                "model_name": model.get("name"),
                "provider": model.get("provider"),
                "status": "failed",
                "error": "Model evaluation timed out after 120 seconds.",
                "output": None,
                "analysis": None,
                "estimated_cost": None,
                "latency_ms": None,
            }

        yield {
            "progress": i + 1,
            "total": total,
            "model_id": model_id,
            "model_name": result.get("model_name"),
            "result": result,
            "task_name": task["name"],
        }
