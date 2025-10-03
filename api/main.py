
import logging
from fastapi import FastAPI, Depends
from redbetter import config
from redbetter.api import RedAPI, OpsAPI

from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    logging.info("Starting up...")
    yield
    logging.info("Shutting down...")

app = FastAPI(lifespan=lifespan)

@app.get("/")
async def root():
    return {"message": "RedOpsManager API"}

from api.routers import config as config_router, transcode as transcode_router

from fastapi.staticfiles import StaticFiles

app.include_router(config_router.router)
app.include_router(transcode_router.router)

app.mount("/", StaticFiles(directory="frontend/build", html=True), name="static")

