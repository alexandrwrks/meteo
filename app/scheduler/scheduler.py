from apscheduler.schedulers.asyncio import AsyncIOScheduler

from app.scheduler.meteo_info import update_all_forecasts

scheduler = AsyncIOScheduler()

scheduler.add_job(
    update_all_forecasts,
    trigger="interval",
    minutes=15,
    id="meteo_update",
    replace_existing=True,
)
