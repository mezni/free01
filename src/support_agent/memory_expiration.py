from datetime import datetime, timedelta, timezone

from support_agent.models import MemoryType


DEFAULT_EXPIRATION_DAYS = {
    MemoryType.PREFERENCE: None,
    MemoryType.PROFILE: None,
    MemoryType.ACCOUNT: 180,
    MemoryType.PRODUCT: 90,
}


def calculate_expiration(
    memory_type: MemoryType,
) -> datetime | None:

    days = DEFAULT_EXPIRATION_DAYS[memory_type]

    if days is None:
        return None

    return (
        datetime.now(timezone.utc)
        + timedelta(days=days)
    )