from support_agent.memory import ConversationMemory


def test_add_user_message():

    memory = ConversationMemory()

    memory.add_user_message(
        "My customer ID is C002."
    )

    messages = memory.get_messages()

    assert len(messages) == 1
    assert messages[0]["role"] == "user"
    assert messages[0]["content"] == (
        "My customer ID is C002."
    )


def test_conversation_history():

    memory = ConversationMemory()

    memory.add_user_message(
        "My customer ID is C002."
    )

    memory.add_assistant_message(
        "How can I help you?"
    )

    messages = memory.get_messages()

    assert len(messages) == 2
    assert messages[0]["role"] == "user"
    assert messages[1]["role"] == "assistant"


def test_clear_memory():

    memory = ConversationMemory()

    memory.add_user_message("Hello")

    memory.clear()

    assert memory.get_messages() == []


from support_agent.models import (
    ExtractedTicket,
)
from support_agent.state import (
    AgentState,
    update_state_from_extraction,
)


def test_update_agent_state():

    state = AgentState()

    extracted = ExtractedTicket(
        customer_id="C002",
        product="subscription",
        sentiment="negative",
        priority="high",
        category="billing",
    )

    update_state_from_extraction(
        state,
        extracted,
    )

    assert state.customer_id == "C002"
    assert state.product == "subscription"
    assert state.category == "billing"
    assert state.priority == "high"

from support_agent.customer_memory import (
    MEMORIES,
    add_memory,
    get_customer_memories,
)


def test_customer_memory():

    MEMORIES.clear()

    add_memory(
        customer_id="C002",
        key="preferred_contact_method",
        value="email",
        source="customer_statement",
        confidence=0.95,
    )

    memories = get_customer_memories("C002")

    assert len(memories) == 1
    assert memories[0].key == (
        "preferred_contact_method"
    )
    assert memories[0].value == "email"