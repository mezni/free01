from datetime import datetime, timezone

from support_agent.database import get_connection, initialize_database
from support_agent.memory_repository import MemoryRepository
from support_agent.models import MemorySource, MemoryType
import uuid

# Initialize database table when module is imported
initialize_database()

# Backward-compatible module-level list (deprecated, uses repository internally)
MEMORIES: list = []

repository = MemoryRepository()


def _init_memories():
    """Initialize MEMORIES list from repository for backward compatibility."""
    global MEMORIES
    # Clear and repopulate from repository
    # Since repository.get_by_customer("") doesn't work well,
    # we just keep MEMORIES as a simple list for backward compat
    # The real data is in SQLite via repository


_init_memories()


def _find_memory(
    customer_id: str,
    key: str,
) -> object | None:

    # Try repository first (SQLite)
    memories = repository.get_by_customer(customer_id)
    for memory in memories:
        if memory.key == key and not memory.is_expired():
            return memory

    # Fall back to MEMORIES list for backward compatibility
    for memory in MEMORIES:
        if memory.key == key:
            return memory

    return None


def add_or_update_memory(
    customer_id: str,
    key: str,
    value: str,
    source: MemorySource,
    memory_type: MemoryType,
    confidence: float,
) -> object:

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

        # Also add to MEMORIES list for backward compatibility
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

        # Update in repository too
        repository.save(existing)

    return existing


def get_customer_memories(
    customer_id: str,
) -> list:

    # Try repository first (SQLite with expiration filtering)
    memories = repository.get_by_customer(customer_id)

    # Also check MEMORIES list for backward compatibility
    now = datetime.now(timezone.utc)
    for memory in MEMORIES:
        if memory.customer_id == customer_id:
            if memory.expires_at is None or memory.expires_at > now:
                # Add to results if not already there
                if memory not in memories:
                    memories.append(memory)

    # Apply expiration filtering
    result = [
        memory
        for memory in memories
        if memory.is_expired() is False
    ]

    return result


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

    # Delete from repository
    result = repository.delete(memory.memory_id)

    # Also remove from MEMORIES list for backward compatibility
    if memory in MEMORIES:
        MEMORIES.remove(memory)

    return result


# Add is_expired method to CustomerMemory check
def _is_expired(memory) -> bool:
    """Check if a memory is expired."""
    if memory.expires_at is None:
        return False
    from datetime import datetime, timezone
    now = datetime.now(timezone.utc)
    return memory.expires_at <= now