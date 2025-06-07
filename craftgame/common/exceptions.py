from typing import ClassVar


class AppError(Exception):
    status: ClassVar[int] = 500
    message: ClassVar[str] = "Some error occurred"
