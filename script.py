from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from app.routers import routers
from app.scheduler.meteo_info import update_all_forecasts
from app.scheduler.scheduler import scheduler


@asynccontextmanager
async def lifespan(_: FastAPI):
    scheduler.start()

    await update_all_forecasts()

    print("Lifespan")
    yield

    scheduler.shutdown()


app = FastAPI(lifespan=lifespan)

for router in routers:
    app.include_router(router)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)