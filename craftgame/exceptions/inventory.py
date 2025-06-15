from craftgame.exceptions.common import AppError


class InventoryError(AppError):
    pass


class InventoryItemAlreadyExists(InventoryError):
    status = 400
    message = "inventory item already exists"
