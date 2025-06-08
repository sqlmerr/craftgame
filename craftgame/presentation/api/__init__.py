from fastapi import FastAPI
from starlette.types import Lifespan

from craftgame.presentation.api.routes import router


def create_app(lifespan: Lifespan) -> FastAPI:
    app = FastAPI(lifespan=lifespan)
    app.include_router(router)

    return app
