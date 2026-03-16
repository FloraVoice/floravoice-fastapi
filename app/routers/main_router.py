from fastapi import APIRouter

from app.routers import hello_world, flowers_router, auth_router, users_router, admins_router, orders_router


main_router = APIRouter()
main_router.include_router(hello_world.router)
main_router.include_router(flowers_router.router)
main_router.include_router(auth_router.router)
main_router.include_router(users_router.router)
main_router.include_router(admins_router.router)
main_router.include_router(orders_router.router)
