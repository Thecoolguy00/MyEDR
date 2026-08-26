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


app = FastAPI(title="MyEDR", version="0.1.0")


# Database
db = PostgresStore()

device_service = DeviceService(db)


# Create initial schema.
# We'll replace this with migrations later.
db.execute(CREATE_DEVICES_TABLE)


app.include_router(devices_router)


@app.get("/health")
def health():
    db.ping()

    return {
        "status": "ok",
        "service": "myedr-server",
        "database": "ok",
    }


@app.on_event("shutdown")
def shutdown():
    db.close()