from __future__ import annotations

from dataclasses import dataclass
from typing import Dict

from aios.providers.base import BaseModelProvider


class ProviderNotFoundError(KeyError):
    """Raised when a provider name is not registered in the registry."""


@dataclass
class ProviderRegistry:
    """
    Maps provider names -> provider instances.

    The Router returns a provider name (string).
    The Executor resolves that name into a concrete BaseModelProvider here.
    """

    _providers: Dict[str, BaseModelProvider]

    def __init__(self) -> None:
        self._providers = {}

    def register(self, name: str, provider: BaseModelProvider) -> None:
        if not name or not isinstance(name, str):
            raise ValueError("Provider name must be a non-empty string.")
        self._providers[name] = provider

    def get(self, name: str) -> BaseModelProvider:
        try:
            return self._providers[name]
        except KeyError as e:
            available = ", ".join(sorted(self._providers.keys())) or "(none)"
            raise ProviderNotFoundError(
                f"Provider '{name}' not found. Available providers: {available}"
            ) from e

    def has(self, name: str) -> bool:
        return name in self._providers

    def list(self) -> Dict[str, BaseModelProvider]:
        # Return a shallow copy to prevent accidental mutation.
        return dict(self._providers)
