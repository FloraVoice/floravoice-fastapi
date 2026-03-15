from fastapi import APIRouter

from app.routers import hello_world, flowers_router, auth_router


main_router = APIRouter()
main_router.include_router(hello_world.router)
main_router.include_router(flowers_router.router)
main_router.include_router(auth_router.router)
