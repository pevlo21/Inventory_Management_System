from fastapi import APIRouter

from api.admin.users import router_users
from api.auth.signin import router_signin
from api.auth.signup import router_signup
from securities.token import router as authorization_router


class V1Router(APIRouter):  #custom Router class to include all routers of the API
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.include_router(authorization_router)
        self.include_router(router_signin)
        self.include_router(router_signup)
        self.include_router(router_users)


v1_router = V1Router(prefix="/api", tags=["api"])