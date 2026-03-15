from apscheduler.schedulers.asyncio import AsyncIOScheduler
from app.core.database import SessionLocal
from app.services.deathlist import DeathlistService
from app.services.online_checker import OnlineChecker
from app.services.bedmage_timer import BedmageTimerService
from app.core.config import settings

async def job_check_everything(client):
    db = SessionLocal()
    try:
        checker = OnlineChecker()
        await checker.update_online_status(db, client)
        await BedmageTimerService.check_timers(db, client)
        await DeathlistService.check_and_notify_deaths(db, client)
    except Exception as e:
        print(f"Error in job_check_everything: {e}")
    finally:
        db.close()

def start_scheduler(client):
    scheduler = AsyncIOScheduler()
    scheduler.add_job(job_check_everything, 'interval', minutes=settings.SCHEDULER_TIMER_MINUTES, args=[client])
    scheduler.start()
    return scheduler