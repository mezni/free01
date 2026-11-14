import json

from agentic_ai.llm_client import LLMClient
from agentic_ai.state import AgentState
from agentic_ai.tools.executor import ToolExecutor


class AgentController:
    def __init__(self, max_steps: int = 5):
        self.llm = LLMClient()
        self.executor = ToolExecutor()
        self.max_steps = max_steps

    def run(self, user_message: str) -> str:

        state = AgentState(
            user_message=user_message,
            input_items=[
                {
                    "role": "user",
                    "content": user_message,
                }
            ],
        )

        while state.iteration < self.max_steps:
            state.iteration += 1

            print(f"\nAgent iteration: {state.iteration}")

            response = self.llm.decide(state.input_items)

            # Preserve model output in conversation history.
            state.input_items.extend(response.output)

            tool_calls = [
                item for item in response.output if item.type == "function_call"
            ]

            # No tool call means the model has finished
            # responding to the user.
            if not tool_calls:
                state.final_response = response.output_text

                state.status = "completed"

                return state.final_response

            # Execute each requested tool.
            for tool_call in tool_calls:
                result = self.executor.execute(
                    tool_call.name,
                    tool_call.arguments,
                )

                state.observations.append(
                    {
                        "tool": tool_call.name,
                        "result": result,
                    }
                )

                print(f"Tool: {tool_call.name}")

                print(f"Result: {result}")

                # Return observation to the model.
                state.input_items.append(
                    {
                        "type": "function_call_output",
                        "call_id": tool_call.call_id,
                        "output": json.dumps(result),
                    }
                )

        state.status = "max_steps_reached"

        return (
            "The agent reached its maximum execution steps without completing the task."
        )
