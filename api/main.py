import logging
from contextlib import asynccontextmanager
import os

from fastapi import FastAPI

from redbetter import config


@asynccontextmanager
async def lifespan(app: FastAPI):
    logging.info("Starting up...")
    config_file_path = os.environ.get("CONFIG_FILE_PATH", "config.ini")
    config.load_config(config_file_path)
    yield
    logging.info("Shutting down...")

app = FastAPI(lifespan=lifespan)

from api.routers import config as config_router, transcode as transcode_router

from fastapi.staticfiles import StaticFiles

app.include_router(config_router.router, prefix="/api")
app.include_router(transcode_router.router, prefix="/api")

app.mount("/", StaticFiles(directory="frontend/build", html=True), name="static")
