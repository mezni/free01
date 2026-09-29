from support_agent.customer_memory import (
    MEMORIES,
    add_or_update_memory,
)
from support_agent.models import (
    MemorySource,
    MemoryType,
)
from support_agent.memory_retrieval import (
    retrieve_relevant_memories,
)


def test_retrieve_relevant_memory():
    MEMORIES.clear()

    add_or_update_memory(
        customer_id="C002",
        key="preferred_contact_method",
        value="email",
        source=MemorySource.CUSTOMER_STATEMENT,
        memory_type=MemoryType.PREFERENCE,
        confidence=0.95,
    )

    add_or_update_memory(
        customer_id="C002",
        key="preferred_language",
        value="English",
        source=MemorySource.CUSTOMER_STATEMENT,
        memory_type=MemoryType.PREFERENCE,
        confidence=0.95,
    )

    results = retrieve_relevant_memories(
        customer_id="C002",
        query="Please send the update by email.",
    )

    assert len(results) == 1
    assert (
        results[0].memory.key
        == "preferred_contact_method"
    )


def test_memories_are_isolated_by_customer():
    MEMORIES.clear()

    add_or_update_memory(
        customer_id="C001",
        key="preferred_contact_method",
        value="phone",
        source=MemorySource.CUSTOMER_STATEMENT,
        memory_type=MemoryType.PREFERENCE,
        confidence=0.95,
    )

    add_or_update_memory(
        customer_id="C002",
        key="preferred_contact_method",
        value="email",
        source=MemorySource.CUSTOMER_STATEMENT,
        memory_type=MemoryType.PREFERENCE,
        confidence=0.95,
    )

    results = retrieve_relevant_memories(
        customer_id="C002",
        query="Please contact me by email.",
    )

    assert len(results) == 1
    assert results[0].memory.customer_id == "C002"
    assert results[0].memory.value == "email"