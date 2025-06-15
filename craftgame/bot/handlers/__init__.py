from aiogram import Router
from . import common, inventory, craft


def init_routers() -> Router:
    r = Router()
    r.include_routers(common.router, inventory.router, craft.router)

    return r
