from sqlalchemy import BigInteger
from sqlalchemy.orm import Mapped, mapped_column

from craftgame.database.base import Base


class User(Base):
    __tablename__ = "users"

    tg_id: Mapped[int] = mapped_column(BigInteger, nullable=False, unique=True)
