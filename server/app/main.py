from contextlib import asynccontextmanager
import logging

from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI

from app.api.devices import router as devices_router
from app.db.postgres import PostgresStore
from app.models.device import CREATE_DEVICES_TABLE
from app.services.device_service import DeviceService


logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)


db: PostgresStore | None = None
device_service: DeviceService | None = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    global db, device_service

    logger.info("Starting MyEDR server")

    # Initialize database connection pool.
    db = PostgresStore()

    # Initialize services.
    device_service = DeviceService(db)

    # Initialize database schema.
    #
    # Temporary for Goal 1.
    # Replace with migrations once the schema starts evolving.
    db.execute(CREATE_DEVICES_TABLE)

    logger.info("MyEDR server startup complete")

    try:
        yield

    finally:
        logger.info("Shutting down MyEDR server")

        if db is not None:
            db.close()

        db = None
        device_service = None

        logger.info("MyEDR server shutdown complete")


app = FastAPI(title="MyEDR", version="0.1.0", lifespan=lifespan)


app.include_router(devices_router)


@app.get("/health")
def health():
    if db is None:
        return {
            "status": "starting",
            "service": "myedr-server",
        }

    db.ping()

    return {
        "status": "ok",
        "service": "myedr-server",
        "database": "ok",
    }