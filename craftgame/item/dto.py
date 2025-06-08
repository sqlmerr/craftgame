import datetime
from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True)
class ItemDTO:
    id: UUID
    name: str
    emoji: str
    opened_by_id: UUID | None
    opened_at: datetime.datetime


@dataclass(frozen=True)
class CreateItemDTO:
    name: str
    emoji: str
    opened_by_id: UUID | None
