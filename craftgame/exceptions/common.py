from typing import ClassVar


class AppError(Exception):
    status: ClassVar[int] = 500
    message: ClassVar[str] = "Some error occurred"


class ServerError(AppError):
    status = 500
    message = "Unexpected error occurred"


class NotFound(AppError):
    status = 404
    message = "Not found"
