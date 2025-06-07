import datetime
from uuid import UUID

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, relationship, mapped_column

from craftgame.common.base import Base
from craftgame.user.model import User


class Item(Base):
    __tablename__ = "items"
    name: Mapped[str]

    opened_by_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"), nullable=True)
    opened_by: Mapped[User] = relationship()
    opened_at: Mapped[datetime.datetime] = mapped_column(
        default=lambda: datetime.datetime.now()
    )
