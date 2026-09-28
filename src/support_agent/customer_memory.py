from datetime import datetime, timezone

from support_agent.models import CustomerMemory


MEMORIES: list[CustomerMemory] = []


def add_memory(
    customer_id: str,
    key: str,
    value: str,
    source: str,
    confidence: float,
) -> CustomerMemory:

    now = datetime.now(timezone.utc)

    memory = CustomerMemory(
        memory_id=f"M-{len(MEMORIES) + 1}",
        customer_id=customer_id,
        key=key,
        value=value,
        source=source,
        confidence=confidence,
        created_at=now,
        updated_at=now,
    )

    MEMORIES.append(memory)

    return memory


def get_customer_memories(
    customer_id: str,
) -> list[CustomerMemory]:

    return [
        memory
        for memory in MEMORIES
        if memory.customer_id == customer_id
    ]