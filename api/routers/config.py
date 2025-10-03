
from fastapi import APIRouter
from redbetter import config

router = APIRouter()

@router.get("/config")
async def get_config():
    return config.get_sanitized_config()
