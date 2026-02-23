from __future__ import annotations

import time
from dataclasses import dataclass
from typing import Any, Dict, Optional

from .base import BaseModelProvider


@dataclass
class MockModelProvider(BaseModelProvider):
    """
    A deterministic mock provider for local/dev testing.

    Use this provider to validate:
      - routing decisions
      - policy enforcement flow
      - executor lifecycle
      - audit logging + telemetry hooks

    It returns structured output without calling any external APIs.
    """

    name: str = "mock"
    latency_ms: int = 25
    cost_per_1k_tokens: float = 0.0
    fixed_confidence: float = 0.85
    fixed_text: Optional[str] = None

    def generate(self, prompt: str, context: Dict[str, Any]) -> Dict[str, Any]:
        # Simulate latency
        if self.latency_ms and self.latency_ms > 0:
            time.sleep(self.latency_ms / 1000.0)

        request_id = str(context.get("request_id", "req_mock"))
        intent = context.get("intent", "unknown")
        sensitivity = context.get("sensitivity", "unspecified")

        text = self.fixed_text or (
            f"[{self.name}] mock response | intent={intent} | sensitivity={sensitivity}"
        )

        return {
            "provider": self.name,
            "request_id": request_id,
            "confidence": float(self.fixed_confidence),
            "usage": {
                # Approximate token counts for testing (not real tokenization)
                "prompt_tokens": max(1, len(prompt) // 4),
                "completion_tokens": max(1, len(text) // 4),
                "total_tokens": max(2, (len(prompt) + len(text)) // 4),
                "cost_usd": 0.0,
            },
            "output": {
                "text": text,
                "structured": {
                    "intent": intent,
                    "sensitivity": sensitivity,
                },
            },
            "metadata": {
                "mock": True,
                "latency_ms": self.latency_ms,
            },
        }
