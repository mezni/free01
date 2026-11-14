import os

from openai import OpenAI

from agentic_ai.tools.registry import TOOLS


class LLMClient:
    def __init__(self):
        self.client = OpenAI()

        self.model = os.getenv(
            "OPENAI_MODEL",
            "gpt-6-astra",
        )

    def decide(self, input_items: list):

        return self.client.responses.create(
            model=self.model,
            instructions=(
                "You are a customer support agent. "
                "Investigate customer order requests. "
                "Use available tools when necessary. "
                "Never invent order or shipping information. "
                "When sufficient information is available, "
                "provide a concise factual answer."
            ),
            input=input_items,
            tools=TOOLS,
            parallel_tool_calls=False,
        )
