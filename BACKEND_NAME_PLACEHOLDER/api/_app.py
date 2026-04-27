from fastapi import FastAPI

from ._routes import define_routes
from BACKEND_NAME_PLACEHOLDER.engine import get_engine

_app: FastAPI | None = None


def build_app():
    global _app
    if not _app:
        get_engine()
        _app = FastAPI()
        define_routes(_app)

    return _app
