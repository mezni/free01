from datetime import datetime, timezone

from support_agent.memory_repository import MemoryRepository
from support_agent.models import MemorySource, MemoryType
import uuid

repository = MemoryRepository()

# Backward-compatible module-level list (deprecated, uses repository internally)
MEMORIES: list = []


def _init_memories():
    """Initialize MEMORIES list from repository for backward compatibility."""
    global MEMORIES
    all_memories = repository.get_by_customer("")
    # This is a simplification - in practice, we'd need to track all customer IDs
    # For backward compat, we'll just keep it empty or synced


_init_memories()


def _find_memory(
    customer_id: str,
    key: str,
) -> object | None:

    memories = repository.get_by_customer(customer_id)
    for memory in memories:
        if memory.key == key:
            return memory
    return None


def add_or_update_memory(
    customer_id: str,
    key: str,
    value: str,
    source: MemorySource,
    confidence: float,
) -> object:

    memory_type = MemoryType.PREFERENCE

    existing = _find_memory(
        customer_id=customer_id,
        key=key,
    )

    now = datetime.now(timezone.utc)
    expires_at = None

    if existing is None:
        from support_agent.models import CustomerMemory

        memory = CustomerMemory(
            memory_id=f"M-{uuid.uuid4().hex[:8].upper()}",
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

        repository.save(memory)

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
) -> list:

    memories = repository.get_by_customer(customer_id)

    now = datetime.now(timezone.utc)

    return [
        memory
        for memory in memories
        if (
            memory.expires_at is None
            or memory.expires_at > now
        )
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

    return repository.delete(memory.memory_id)