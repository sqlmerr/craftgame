from craftgame.common.exceptions import AppError


class InventoryError(AppError):
    pass


class InventoryItemAlreadyExists(InventoryError):
    status = 400
    message = "inventory item already exists"
