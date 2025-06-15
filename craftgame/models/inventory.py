from uuid import UUID

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, relationship, mapped_column

from craftgame.database.base import Base
from craftgame.models.item import Item
from craftgame.models.user import User


class InventoryItem(Base):
    __tablename__ = "inventory_items"
    user: Mapped[User] = relationship()
    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"))

    item: Mapped[Item] = relationship()
    item_id: Mapped[UUID] = mapped_column(ForeignKey("items.id"))

    count: Mapped[int] = mapped_column(default=1)
