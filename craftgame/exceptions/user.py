from craftgame.exceptions.common import AppError


class UserError(AppError):
    pass


class UserNotFoundError(UserError):
    status = 404
    message = "user not found"


class UserWithThisTelegramIdAlreadyExists(UserError):
    status = 400
    message = "user with this telegram id already exists"
