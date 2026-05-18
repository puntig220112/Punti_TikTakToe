from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from ._routes import define_routes
from BACKEND_NAME_PLACEHOLDER.engine import get_engine

_app: FastAPI | None = None


def build_app():
    global _app
    if not _app:
        get_engine()
        _app = FastAPI()
        
        _app.add_middleware(
            CORSMiddleware,
            allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
        
        define_routes(_app)

    return _app