from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers.main_router import main_router


app = FastAPI()
app.include_router(main_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
