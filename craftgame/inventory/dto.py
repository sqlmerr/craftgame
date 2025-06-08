from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True)
class InventoryDTO:
    id: UUID
    user_id: UUID
    item_id: UUID


@dataclass(frozen=True)
class CreateInventoryDTO:
    user_id: UUID
    item_id: UUID
