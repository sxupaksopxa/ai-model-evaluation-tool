from abc import ABC, abstractmethod


class BaseProvider(ABC):
    @abstractmethod
    async def run(
        self,
        model: dict,
        task_id: str,
        prompt: str,
        api_keys: dict[str, str] | None = None,
    ) -> dict:
        pass