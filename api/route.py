from fastapi import APIRouter

from api.auth.signin import router_signin
from api.auth.signup import router_signup
from api.user.users import router_users
from securities.token import router as authorization_router

v1_router = APIRouter(prefix="/api", tags=["api"])

v1_router.include_router(authorization_router)
#v1_router.include_router(router_users)
v1_router.include_router(router_signin)
v1_router.include_router(router_signup)