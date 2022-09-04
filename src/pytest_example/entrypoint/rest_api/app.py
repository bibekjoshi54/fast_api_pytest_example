from typing import Union

from fastapi import FastAPI
from fastapi.requests import Request
from starlette.responses import JSONResponse

from ...config import CONFIG_AWS_ENDPOINT
from ...repository.impl.dynamo_event_helper import dynamo_start_up
from .resource import TODO_ROUTER


def get_app():
    app = FastAPI()

    @app.exception_handler(ValueError)
    async def unicorn_exception_handler(request: Request, exc: ValueError):
        return JSONResponse(
            status_code=418,
            content={"message": f"Oops! {exc} did something. There goes a rainbow..."},
        )

    @app.exception_handler(Exception)
    async def unicorn_exception_handler(request: Request, exc: Exception):
        return JSONResponse(
            status_code=418,
            content={"message": f"Oops! There goes a rainbow..."},
        )

    dynamo_start_up(app, CONFIG_AWS_ENDPOINT)
    app.include_router(router=TODO_ROUTER, prefix="/api")
    return app
