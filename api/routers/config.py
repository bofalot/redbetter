
from fastapi import APIRouter, Depends
from redbetter import config

router = APIRouter()

@router.get("/api/config")
async def get_config():
    # Return a subset of the config, excluding sensitive values
    return {
        "data_dirs": config.get_data_dirs(),
        "output_dir": config.get_output_dir(),
        "torrent_dir": config.get_torrent_dir(),
        "qbittorrent": config.get_qbittorrent_config(),
    }
