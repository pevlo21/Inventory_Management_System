from fastapi import APIRouter

from api.auth.token import router as authorization_router
from api.user.users import router_users

v1_router = APIRouter(prefix="/api", tags=["api"])

v1_router.include_router(authorization_router)
v1_router.include_router(router_users)