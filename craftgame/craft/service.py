from dataclasses import dataclass
from uuid import UUID

from craftgame.common.exceptions import NotFound, AppError
from craftgame.craft.dto import CreateCraftDTO, CraftDTO
from craftgame.craft.interfaces.deleter import CraftDeleter
from craftgame.craft.interfaces.reader import CraftReader
from craftgame.craft.interfaces.repo import CraftRepo
from craftgame.craft.interfaces.writer import CraftWriter
from craftgame.craft.model import Craft


@dataclass(frozen=True)
class CraftService(CraftDeleter, CraftReader, CraftWriter):
    repo: CraftRepo

    async def create_craft(self, data: CreateCraftDTO) -> CraftDTO:
        if len(data.ingredients_ids) != 2:
            raise AppError

        craft = await self.repo.find_one_craft_by_ingredients(
            data.ingredients_ids[0], data.ingredients_ids[1]
        )
        if craft:
            return CraftDTO(
                id=craft.id,
                result_item_id=craft.result_item_id,
                ingredients_ids=[craft.ingredient1_id, craft.ingredient2_id],
            )

        craft_id = await self.repo.create_craft(
            {
                "result_item_id": data.result_item_id,
                "ingredient1_id": data.ingredients_ids[0],
                "ingredient2_id": data.ingredients_ids[1],
            }
        )
        return await self.get_craft_by_id(craft_id)

    async def get_craft_by_id(self, craft_id: UUID) -> CraftDTO | None:
        craft = await self.repo.find_one_craft_filtered(Craft.id == craft_id)
        if not craft:
            raise NotFound
        return CraftDTO(
            id=craft.id,
            result_item_id=craft.result_item_id,
            ingredients_ids=[craft.ingredient1_id, craft.ingredient2_id],
        )

    async def get_item_crafts(self, item_id: UUID) -> list[CraftDTO]:
        crafts = await self.repo.find_all_crafts(Craft.result_item_id == item_id)
        dtos = []
        for craft in crafts:
            dtos.append(
                CraftDTO(
                    id=craft.id,
                    result_item_id=craft.result_item_id,
                    ingredients_ids=[craft.ingredient1_id, craft.ingredient2_id],
                )
            )

        return dtos

    async def delete_craft(self, craft_id: UUID) -> None:
        await self.repo.delete_craft(craft_id)
