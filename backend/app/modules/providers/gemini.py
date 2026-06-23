from app.modules.providers.base import BaseProvider


class GeminiProvider(BaseProvider):
    async def run(self, model_ref: str, prompt: str) -> dict:
        return {
            "output": "Gemini provider is not implemented yet.",
            "estimated_cost": None,
            "raw_response": None,
        }