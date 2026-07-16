from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.routers import routers


@asynccontextmanager
async def lifespan(_: FastAPI):

    print("Lifespan")
    yield


app = FastAPI(lifespan=lifespan)

for router in routers:
    app.include_router(router)