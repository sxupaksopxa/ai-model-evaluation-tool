from app.modules.providers.local import LocalProvider
from app.modules.providers.openrouter import OpenRouterProvider
from app.modules.providers.gemini import GeminiProvider
from app.modules.providers.huggingface import HuggingFaceProvider


_PROVIDERS = {
    "Local": LocalProvider(),
    "OpenRouter": OpenRouterProvider(),
    "Google": GeminiProvider(),
    "Hugging Face": HuggingFaceProvider(),
}


def get_provider(provider_name: str):
    provider = _PROVIDERS.get(provider_name)

    if provider is None:
        raise ValueError(
            f"Unsupported provider: {provider_name}"
        )

    return provider