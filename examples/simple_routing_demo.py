from __future__ import annotations

from aios.providers.mock_provider import MockModelProvider
from aios.routing.router import Router
from aios.routing.registry import ProviderRegistry
from aios.core.executor import Executor


def main() -> None:
    # 1) Create two mock providers to simulate different “models”
    fast = MockModelProvider(name="fast", latency_ms=10, fixed_confidence=0.70)
    safe = MockModelProvider(name="safe", latency_ms=60, fixed_confidence=0.92)

    # 2) Register them
    registry = ProviderRegistry()
    registry.register("fast", fast)
    registry.register("safe", safe)

    # 3) Router routes by sensitivity
    router = Router(
        default_provider="fast",
        sensitivity_map={
            "low": "fast",
            "medium": "fast",
            "high": "safe",
            "regulated": "safe",
            "unspecified": "fast",
        },
    )

    # 4) Executor ties it all together
    executor = Executor(router=router, registry=registry)

    prompt = "Summarize the meeting notes and extract next steps."

    # Case A: low sensitivity → fast
    result_a = executor.execute(
        prompt=prompt,
        context={"intent": "task_extraction", "sensitivity": "low"},
    )

    print("\n=== Case A (low sensitivity) ===")
    print("request_id:", result_a.request_id)
    print("route.provider:", result_a.route.provider)
    print("route.reason:", result_a.route.reason)
    print("response.provider:", result_a.provider_response.get("provider"))
    print("response.confidence:", result_a.provider_response.get("confidence"))
    print("response.text:", result_a.provider_response.get("output", {}).get("text"))

    # Case B: high sensitivity → safe
    result_b = executor.execute(
        prompt=prompt,
        context={"intent": "task_extraction", "sensitivity": "high"},
    )

    print("\n=== Case B (high sensitivity) ===")
    print("request_id:", result_b.request_id)
    print("route.provider:", result_b.route.provider)
    print("route.reason:", result_b.route.reason)
    print("response.provider:", result_b.provider_response.get("provider"))
    print("response.confidence:", result_b.provider_response.get("confidence"))
    print("response.text:", result_b.provider_response.get("output", {}).get("text"))


if __name__ == "__main__":
    main()
