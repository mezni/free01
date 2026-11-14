
from agentic_ai.tools.support_tools import (
    get_order,
    get_shipping_status,
)


def test_get_order():
    result = get_order(4821)

    assert result["order_id"] == 4821
    assert result["status"] == "shipped"


def test_order_not_found():
    result = get_order(9999)

    assert "error" in result


def test_shipping_status():
    result = get_shipping_status(4821)

    assert result["status"] == "delayed"

