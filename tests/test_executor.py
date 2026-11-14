
from agentic_ai.tools.executor import ToolExecutor


def test_execute_valid_tool():

    executor = ToolExecutor()

    result = executor.execute(
        "get_order",
        '{"order_id": 4821}',
    )

    assert result["order_id"] == 4821


def test_unknown_tool():

    executor = ToolExecutor()

    result = executor.execute(
        "delete_database",
        "{}",
    )

    assert result["error"] == "Unknown tool"


def test_invalid_arguments():

    executor = ToolExecutor()

    result = executor.execute(
        "get_order",
        '{"order_id": "invalid"}',
    )

    assert result["error"] == "Tool execution failed"

