from fastapi import APIRouter


router = APIRouter(prefix="/hello-world")


@router.get("/", response_model=dict)
async def hello_world():
    return {"message": "Hello world!"}
