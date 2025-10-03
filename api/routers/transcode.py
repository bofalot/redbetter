
import re
from fastapi import APIRouter, Depends, Form, Query, HTTPException
from redbetter.api import RedAPI, OpsAPI
from redbetter.redactedbetter import find_and_upload_missing_transcodes, find_transcode_candidates, get_transcode_candidates
from api.dependencies import get_red_api, get_ops_api

router = APIRouter()

@router.get("/api/getCandidates")
def get_candidates(site: str = Query(..., enum=["red", "ops", "all"]),
                     limit: int = Query(None),
                     offset: int = Query(None),
                     red_api: RedAPI = Depends(get_red_api),
                     ops_api: OpsAPI = Depends(get_ops_api)):
    results = []
    if site in ["red", "all"]:
        results.extend(get_transcode_candidates(red_api, limit=limit, offset=offset))
    if site in ["ops", "all"]:
        results.extend(get_transcode_candidates(ops_api, limit=limit, offset=offset))
    return {"candidates": results}

@router.post("/api/transcode/all")
def transcode_all(red_api: RedAPI = Depends(get_red_api),
                    ops_api: OpsAPI = Depends(get_ops_api),
                    upload: bool = Form(False),
                    single: bool = Form(False),
                    add_to_qbittorrent: bool = Form(False)):
    red_candidates = find_transcode_candidates(red_api)
    ops_candidates = find_transcode_candidates(ops_api)
    red_results = _transcode_and_upload(red_candidates, red_api, upload, single, add_to_qbittorrent)
    ops_results = _transcode_and_upload(ops_candidates, ops_api, upload, single, add_to_qbittorrent)
    return {"message": "Success", "results": {"red": red_results, "ops": ops_results}}

def _transcode_and_upload(candidates, api, upload, single, add_to_qbittorrent):
    try:
        new_torrents = find_and_upload_missing_transcodes(
            candidates, api, upload, single, add_to_qbittorrent)

        if len(new_torrents) == 0:
            result = {"message": "No available transcodes to better",
                      "torrent_files": new_torrents}
        else:
            result = {"message": "Success", "torrent_files": new_torrents}
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/api/transcode")
def transcode(red_api: RedAPI = Depends(get_red_api),
              ops_api: OpsAPI = Depends(get_ops_api),
              torrent_url: str = Form(...),
              upload: bool = Form(False),
              single: bool = Form(False),
              add_to_qbittorrent: bool = Form(False)):
    def get_api_from_url(url):
        if 'redacted.ch' in url:
            return red_api
        elif 'orpheus.network' in url:
            return ops_api
        return None

    api = get_api_from_url(torrent_url)
    if api is None:
        raise HTTPException(status_code=400, detail=f"Invalid torrent URL ({torrent_url})")

    match = re.search(r'torrentid=(\d+)', torrent_url)
    if not match:
        raise HTTPException(status_code=400, detail=f"Invalid torrent URL ({torrent_url})")
    torrent_id = match.group(1)

    response = api.torrent(torrent_id)
    group_id = response["group"]["id"]
    candidates = [(int(group_id), int(torrent_id))]

    return _transcode_and_upload(candidates, api, upload, single, add_to_qbittorrent)
