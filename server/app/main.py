from contextlib import asynccontextmanager
import logging

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException

from app.api.auth import router as auth_router
from app.api.devices import router as devices_router
from app.db.postgres import PostgresStore
from app.models.device import CREATE_TABLES
from app.services.auth_service import AuthService
from app.services.device_service import DeviceService

from fastapi.middleware.cors import CORSMiddleware

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting MyEDR server")

    db = PostgresStore()

    app.state.db = db
    app.state.auth_service = AuthService(db)
    app.state.device_service = DeviceService(db)

    db.execute(CREATE_TABLES)

    logger.info("MyEDR server startup complete")

    try:
        yield

    finally:
        logger.info("Shutting down MyEDR server")

        db.close()

        logger.info("MyEDR server shutdown complete")


app = FastAPI(title="MyEDR", version="0.1.0",lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
    ],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(devices_router)


@app.get("/health")
def health():
    db: PostgresStore = app.state.db

    db.ping()

    return {
        "status": "ok",
        "service": "myedr-server",
        "database": "ok",
    }