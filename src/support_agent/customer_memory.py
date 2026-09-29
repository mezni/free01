from datetime import datetime, timezone

from support_agent.models import CustomerMemory, MemorySource, MemoryType
from support_agent.memory_expiration import calculate_expiration


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
    memory_type: MemoryType,
    confidence: float,
) -> CustomerMemory:

    existing = _find_memory(
        customer_id=customer_id,
        key=key,
    )

    now = datetime.now(timezone.utc)

    expires_at = calculate_expiration(memory_type)

    if existing is None:
        memory = CustomerMemory(
            memory_id=f"M-{len(MEMORIES) + 1}",
            customer_id=customer_id,
            key=key,
            value=value,
            memory_type=memory_type,
            source=source,
            confidence=confidence,
            created_at=now,
            updated_at=now,
            expires_at=expires_at,
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

    now = datetime.now(timezone.utc)

    return [
        memory
        for memory in MEMORIES
        if (
            memory.customer_id == customer_id
            and (
                memory.expires_at is None
                or memory.expires_at > now
            )
        )
    ]


def remove_expired_memories() -> int:

    now = datetime.now(timezone.utc)

    expired = [
        memory
        for memory in MEMORIES
        if (
            memory.expires_at is not None
            and memory.expires_at <= now
        )
    ]

    for memory in expired:
        MEMORIES.remove(memory)

    return len(expired)


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