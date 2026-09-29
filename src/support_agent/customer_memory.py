from datetime import datetime, timezone

from support_agent.models import CustomerMemory, MemorySource


MEMORIES: list[CustomerMemory] = []


def _find_memory(
    customer_id: str,
    key: str,
) -> CustomerMemory | None:
    for memory in MEMORIES:
        if (
            memory.customer_id == customer_id
            and memory.key == key
        ):
            return memory

    return None


def add_or_update_memory(
    customer_id: str,
    key: str,
    value: str,
    source: MemorySource,
    confidence: float,
) -> CustomerMemory:

    existing = _find_memory(
        customer_id=customer_id,
        key=key,
    )

    now = datetime.now(timezone.utc)

    if existing is None:
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

    if existing.value == value:

        if confidence > existing.confidence:
            existing.confidence = confidence
            existing.source = source
            existing.updated_at = now

        return existing

    existing_source_priority = {
        MemorySource.CUSTOMER_STATEMENT: 4,
        MemorySource.IMPORTED_DATA: 3,
        MemorySource.SUPPORT_AGENT: 2,
        MemorySource.SYSTEM: 1,
    }

    current_priority = existing_source_priority[
        existing.source
    ]

    new_priority = existing_source_priority[
        source
    ]

    should_update = (
        new_priority > current_priority
        or (
            new_priority == current_priority
            and confidence > existing.confidence
        )
    )

    if should_update:
        existing.value = value
        existing.source = source
        existing.confidence = confidence
        existing.updated_at = now

    return existing


def get_customer_memories(
    customer_id: str,
) -> list[CustomerMemory]:

    return [
        memory
        for memory in MEMORIES
        if memory.customer_id == customer_id
    ]


def delete_memory(
    customer_id: str,
    key: str,
) -> bool:

    memory = _find_memory(
        customer_id=customer_id,
        key=key,
    )

    if memory is None:
        return False

    MEMORIES.remove(memory)

    return True