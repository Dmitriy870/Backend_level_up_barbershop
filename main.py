from contextlib import asynccontextmanager

from fastapi import FastAPI
import uvicorn
from specialist.views import router as specialist_router
from database.db_helper import db_helper
from models.base import Base


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with db_helper.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield







app = FastAPI(lifespan=lifespan)


app.include_router(specialist_router)
@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
