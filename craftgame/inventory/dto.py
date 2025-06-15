from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True)
class InventoryItemDTO:
    id: UUID
    user_id: UUID
    item_id: UUID
    count: int


@dataclass(frozen=True)
class CreateInventoryItemDTO:
    user_id: UUID
    item_id: UUID
    count: int = 1
