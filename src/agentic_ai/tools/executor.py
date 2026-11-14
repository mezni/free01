import json

from pydantic import BaseModel, ConfigDict

from agentic_ai.tools.support_tools import (
    get_order,
    get_shipping_status,
)


class OrderArguments(BaseModel):
    model_config = ConfigDict(extra="forbid")

    order_id: int


class ToolExecutor:
    def __init__(self):
        self._tools = {
            "get_order": (
                get_order,
                OrderArguments,
            ),
            "get_shipping_status": (
                get_shipping_status,
                OrderArguments,
            ),
        }

    def execute(
        self,
        name: str,
        arguments: str,
    ) -> dict:

        if name not in self._tools:
            return {"error": "Unknown tool"}

        function, schema = self._tools[name]

        try:
            parsed = schema.model_validate_json(arguments)

            result = function(**parsed.model_dump())

            return result

        except Exception as exc:
            return {
                "error": "Tool execution failed",
                "details": str(exc),
            }
