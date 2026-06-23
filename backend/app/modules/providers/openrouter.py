import httpx

from app.modules.providers.base import BaseProvider
from app.modules.analysis.template_or import build_openrouter_prompt


class OpenRouterProvider(BaseProvider):

    async def run(
        self,
        model: dict,
        task_id: str,
        prompt: str,
        api_keys: dict[str, str] | None = None,
    ):
        if model["type"] != "llm":
            raise ValueError(
                f"OpenRouter only supports llm models. Got: {model['type']}"
            )

        openrouter_key = (
            api_keys.get("openrouter")
            if api_keys
            else None
        )

        if not openrouter_key:
            raise ValueError(
                "OpenRouter API key is required for OpenRouter models."
            )

        openrouter_prompt = build_openrouter_prompt(
            task_id,
            prompt,
        )

        return await self._run_llm(
            model,
            task_id,
            openrouter_prompt,
            openrouter_key,
        )

    async def _run_llm(
        self,
        model: dict,
        task_id: str,
        prompt: str,
        openrouter_key: str,
    ):
        url = "https://openrouter.ai/api/v1/chat/completions"

        headers = {
            "Authorization": f"Bearer {openrouter_key}",
            "Content-Type": "application/json",
        }

        payload = {
            "model": model["model_ref"],
            "messages": [
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            "temperature": 0.2,
            "max_tokens": 512,
        }

        async with httpx.AsyncClient(timeout=60) as client:
            response = await client.post(
                url,
                headers=headers,
                json=payload,
            )

        response.raise_for_status()
        data = response.json()

        output = data["choices"][0]["message"]["content"]

        return {
            "output": output,
            "score": None,
            "estimated_cost": "OpenRouter",
            "raw_response": data,
        }