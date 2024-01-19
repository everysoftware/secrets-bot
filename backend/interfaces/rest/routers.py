from interfaces.rest.auth.router import router as auth_router
from interfaces.rest.password.router import router as record_router
from interfaces.rest.user.router import router as user_router

routers = (record_router, auth_router, user_router)
