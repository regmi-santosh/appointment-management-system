from fastapi import FastAPI
from fastapi import FastAPI
from .users import router as users_router

app = FastAPI()

app.include_router(users_router, prefix="/users", tags=["users"])


@app.get("/")
async def read_root():
    return {"status": "ok"}
