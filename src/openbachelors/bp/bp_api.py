from fastapi import APIRouter
from fastapi import Request

from ..const.json_const import true, false, null
from ..const.filepath import CONFIG_JSON, VERSION_JSON
from ..util.const_json_loader import const_json_loader
from ..util.player_data import player_data_decorator

router = APIRouter()


@router.get("/api/game/get_latest_game_info")
async def api_game_get_latest_game_info(request: Request):
    client_version = const_json_loader[VERSION_JSON]["version"]["clientVersion"]

    response = {
        "version": request.query_params.get("version", ""),
        "action": 0,
        "update_type": 0,
        "update_info": {
            "package": null,
            "patch": null,
            "custom_info": "",
            "source_package": null,
        },
        "client_version": client_version,
    }
    return response


@router.get("/api/remote_config/101/prod/default/Android/ak_sdk_config")
async def api_remote_config_101_prod_default_android_ak_sdk_config(request: Request):
    response = {}
    return response
