from uuid import UUID

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from craftgame.common.base import Base
from craftgame.item.model import Item


class Craft(Base):
    __tablename__ = "crafts"
    result_item_id: Mapped[UUID] = mapped_column(ForeignKey("items.id"))
    result_item: Mapped[Item] = relationship(foreign_keys="Craft.result_item_id")

    ingredient1_id: Mapped[UUID] = mapped_column(ForeignKey("items.id"))
    ingredient1: Mapped[Item] = relationship(foreign_keys="Craft.ingredient1_id")
    ingredient2_id: Mapped[UUID] = mapped_column(ForeignKey("items.id"))
    ingredient2: Mapped[Item] = relationship(foreign_keys="Craft.ingredient2_id")
