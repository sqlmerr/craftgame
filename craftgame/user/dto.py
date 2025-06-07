from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True)
class UserDTO:
    id: UUID
    tg_id: int


@dataclass(frozen=True)
class CreateUserDTO:
    tg_id: int

@dataclass(frozen=True)
class UpdateUserDTO:
    tg_id: int | None = None
