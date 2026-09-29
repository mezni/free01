from support_agent.models import MemoryCandidate


MIN_MEMORY_CONFIDENCE = 0.80


ALLOWED_MEMORY_KEYS = {
    "preferred_contact_method",
    "preferred_language",
    "preferred_timezone",
    "product_preference",
    "communication_preference",
}


def should_store_memory(
    candidate: MemoryCandidate,
) -> bool:

    if not candidate.customer_id:
        return False

    if not candidate.key:
        return False

    if not candidate.value.strip():
        return False

    if candidate.confidence < MIN_MEMORY_CONFIDENCE:
        return False

    if candidate.key not in ALLOWED_MEMORY_KEYS:
        return False

    return True