from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True)
class CraftDTO:
    id: UUID
    result_item_id: UUID
    ingredients_ids: list[UUID]


@dataclass(frozen=True)
class CreateCraftDTO:
    result_item_id: UUID
    ingredients_ids: list[UUID]
