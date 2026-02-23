from __future__ import annotations

import uuid
from dataclasses import dataclass
from typing import Any, Dict, Optional

from aios.routing.router import Router, RouteDecision
from aios.routing.registry import ProviderRegistry
from aios.providers.base import BaseModelProvider


@dataclass
class ExecutionResult:
    """
    Structured result of a single AIOS execution.
    """
    request_id: str
    route: RouteDecision
    provider_response: Dict[str, Any]


class Executor:
    """
    v0.1 Executor

    Responsibilities:
      - Assign request_id
      - Call router to select provider
      - Resolve provider via registry
      - Invoke provider.generate()
      - Return structured result including routing metadata
    """

    def __init__(self, router: Router, registry: ProviderRegistry) -> None:
        self.router = router
        self.registry = registry

    def execute(
        self,
        prompt: str,
        context: Optional[Dict[str, Any]] = None,
    ) -> ExecutionResult:
        context = dict(context or {})

        # Ensure stable request id
        request_id = str(context.get("request_id") or uuid.uuid4())
        context["request_id"] = request_id

        # Route
        route = self.router.route(context)

        # Resolve provider
        provider: BaseModelProvider = self.registry.get(route.provider)

        # Execute model/provider
        provider_response = provider.generate(prompt=prompt, context=context)

        return ExecutionResult(
            request_id=request_id,
            route=route,
            provider_response=provider_response,
        )
