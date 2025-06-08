from craftgame.common.exceptions import AppError


class InventoryError(AppError):
    pass


class InventoryAlreadyExists(InventoryError):
    status = 400
    message = "inventory item already exists"
