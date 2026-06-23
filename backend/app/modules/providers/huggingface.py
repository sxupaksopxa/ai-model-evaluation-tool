from app.modules.providers.base import BaseProvider


class HuggingFaceProvider(BaseProvider):
    async def run(self, model_ref: str, prompt: str) -> dict:
        return {
            "output": "Hugging Face provider is not implemented yet.",
            "estimated_cost": None,
            "raw_response": None,
        }