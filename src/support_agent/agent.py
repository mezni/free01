from support_agent.memory import ConversationMemory


class SupportAgent:

    def __init__(self, max_turns: int = 5):
        self.max_turns = max_turns
        self.memory = ConversationMemory()

    def process_message(self, user_message: str, system_prompt: str, tools=None):
        self.memory.add_user_message(user_message)

        response = self._call_llm(
            system_prompt=system_prompt,
            messages=self.memory.get_messages(),
            tools=tools,
        )

        self.memory.messages.append(
            {
                "role": "assistant",
                "content": response.content,
            }
        )

        if hasattr(response, "tool_calls") and response.tool_calls:
            for tool_call in response.tool_calls:
                tool_result = self._execute_tool(tool_call)
                self.memory.messages.append(
                    {
                        "role": "user",
                        "content": tool_result,
                    }
                )

        return response

    def _call_llm(self, system_prompt, messages, tools=None):
        raise NotImplementedError("Subclasses must implement _call_llm")

    def _execute_tool(self, tool_call):
        raise NotImplementedError("Subclasses must implement _execute_tool")