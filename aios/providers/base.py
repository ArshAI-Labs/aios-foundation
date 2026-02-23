from abc import ABC, abstractmethod
from typing import Dict, Any


class BaseModelProvider(ABC):
    """
    Abstract base class for all model providers.

    AIOS interacts only with this interface.
    Concrete providers (OpenAI, Claude, Gemini, etc.)
    must implement this contract.
    """

    @abstractmethod
    def generate(self, prompt: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute model inference.

        :param prompt: Final constructed prompt string
        :param context: Structured execution context
        :return: Structured response dictionary
        """
        pass
