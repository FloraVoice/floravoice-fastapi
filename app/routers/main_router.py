from fastapi import APIRouter

from app.routers import hello_world


main_router = APIRouter()
main_router.include_router(hello_world.router)
