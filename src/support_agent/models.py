from datetime import datetime


class ExtractedTicket:
    def __init__(
        self,
        customer_id: str | None = None,
        product: str | None = None,
        sentiment: str | None = None,
        priority: str | None = None,
        category: str | None = None,
    ):
        self.customer_id = customer_id
        self.product = product
        self.sentiment = sentiment
        self.priority = priority
        self.category = category


class CustomerMemory:
    def __init__(
        self,
        memory_id: str,
        customer_id: str,
        key: str,
        value: str,
        source: str,
        confidence: float,
        created_at: datetime,
        updated_at: datetime,
    ):
        self.memory_id = memory_id
        self.customer_id = customer_id
        self.key = key
        self.value = value
        self.source = source
        self.confidence = confidence
        self.created_at = created_at
        self.updated_at = updated_at