# flake8: noqa F401
from fastapi import APIRouter, Request

from .auth import auth_router
from .post import post_router
from .user import user_router

router = APIRouter(prefix="/api", tags=["API"])

router.include_router(auth_router)
router.include_router(post_router)
router.include_router(user_router)


@router.get("/list-endpoints/")
def list_endpoints(request: Request):
    url_list = [
        {"path": route.path, "name": route.name} for route in request.app.routes
    ]
    return url_list
