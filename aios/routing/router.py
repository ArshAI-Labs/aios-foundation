from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass(frozen=True)
class RouteDecision:
    """
    Immutable, explainable routing decision.
    """
    provider: str
    reason: str
    strategy: str
    metadata: Dict[str, Any]


class Router:
    """
    v0.1 Router

    Responsibilities:
      - Choose a provider based on context (intent, sensitivity, cost/latency hints)
      - Return an explainable RouteDecision
      - Stay model-agnostic (returns provider name only)

    Note:
      In v0.2+, routing will be strategy-driven and pluggable.
    """

    def __init__(
        self,
        default_provider: str = "mock",
        sensitivity_map: Optional[Dict[str, str]] = None,
    ) -> None:
        self.default_provider = default_provider

        # Simple sensitivity-to-provider mapping (can be overridden by caller).
        # Example:
        #   {"high": "claude", "regulated": "claude", "low": "openai"}
        self.sensitivity_map = sensitivity_map or {
            "high": "mock",
            "regulated": "mock",
            "medium": default_provider,
            "low": default_provider,
            "unspecified": default_provider,
        }

    def route(self, context: Dict[str, Any]) -> RouteDecision:
        """
        Choose a provider based on minimal v0.1 rules.

        Expected context keys (optional):
          - intent: str
          - sensitivity: str ("low" | "medium" | "high" | "regulated" | "unspecified")
          - prefer_low_latency: bool
          - prefer_low_cost: bool

        Returns:
          RouteDecision(provider=..., reason=..., strategy=..., metadata=...)
        """
        intent = str(context.get("intent", "unknown"))
        sensitivity = str(context.get("sensitivity", "unspecified")).lower()

        prefer_low_latency = bool(context.get("prefer_low_latency", False))
        prefer_low_cost = bool(context.get("prefer_low_cost", False))

        # Rule 1: sensitivity-based routing (governance-first)
        if sensitivity in self.sensitivity_map:
            provider = self.sensitivity_map[sensitivity]
            return RouteDecision(
                provider=provider,
                reason=f"sensitivity='{sensitivity}' mapped to provider='{provider}'",
                strategy="sensitivity_map",
                metadata={
                    "intent": intent,
                    "sensitivity": sensitivity,
                    "prefer_low_latency": prefer_low_latency,
                    "prefer_low_cost": prefer_low_cost,
                },
            )

        # Rule 2 (fallback): default provider
        return RouteDecision(
            provider=self.default_provider,
            reason=f"no explicit rule matched; using default_provider='{self.default_provider}'",
            strategy="default_fallback",
            metadata={
                "intent": intent,
                "sensitivity": sensitivity,
                "prefer_low_latency": prefer_low_latency,
                "prefer_low_cost": prefer_low_cost,
            },
        )
