from apscheduler.schedulers.asyncio import AsyncIOScheduler
from app.core.database import SessionLocal
from app.services.online_checker import OnlineChecker
from app.services.bedmage_timer import BedmageTimerService

async def job_check_everything(client):
    db = SessionLocal()
    try:
        checker = OnlineChecker()
        await checker.update_online_status(db, client)

        await BedmageTimerService.check_timers(db, client)
    finally:
        db.close()

def start_scheduler(client):
    scheduler = AsyncIOScheduler()
    scheduler.add_job(job_check_everything, 'interval', minutes=1, args=[client])
    scheduler.start()
    return scheduler