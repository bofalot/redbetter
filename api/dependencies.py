
from redbetter import config
from redbetter.api import RedAPI, OpsAPI

def get_red_api() -> RedAPI:
    return RedAPI(config.get_redacted_api_key())

def get_ops_api() -> OpsAPI:
    return OpsAPI(config.get_orpheus_api_key())
