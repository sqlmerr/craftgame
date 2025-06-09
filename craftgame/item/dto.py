import datetime
from dataclasses import dataclass
from uuid import UUID

from craftgame.util import normalize_snake_case


@dataclass(frozen=True)
class ItemDTO:
    id: UUID
    name: str
    emoji: str
    opened_by_id: UUID | None
    opened_at: datetime.datetime

    @property
    def item_name(self) -> str:
        return f"{self.emoji} {normalize_snake_case(self.name)}"


@dataclass(frozen=True)
class CreateItemDTO:
    name: str
    emoji: str
    opened_by_id: UUID | None
