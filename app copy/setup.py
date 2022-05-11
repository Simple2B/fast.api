from fastapi import FastAPI
from fastapi_pagination import add_pagination
from starlette.responses import RedirectResponse
from app.routers import router
from app.config import settings


def create_app() -> FastAPI:
    """Create the application instance"""
    app = FastAPI(title=settings.SERVER_NAME)
    app.include_router(router)

    @app.get("/")
    async def root():
        return RedirectResponse(url="/docs")

    add_pagination(app)
    return app
