import logging
import re

from flask import Flask, request

from .api import RedAPI, OpsAPI
from .redactedbetter import find_and_upload_missing_transcodes, find_transcode_candidates, get_transcode_candidates

app = Flask(__name__)


@app.before_request
def log_request_info():
    app.logger.info(f"Incoming webhook with body: {request.get_data()}")


@app.after_request
def log_response_info(response):
    app.logger.info(f"Responding: {response.get_data()}")
    return response


@app.route("/api/getCandidates", methods=["GET"])
def get_candidates():
    site = request.args.get("site", "all")
    limit = request.args.get("limit", type=int)
    offset = request.args.get("offset", type=int)
    if site not in ["red", "ops", "all"]:
        return http_error("Invalid site parameter", 400)

    red_api = app.config["red_api"]
    ops_api = app.config["ops_api"]
    results = []

    if site in ["red", "all"]:
        results.extend(get_transcode_candidates(red_api, limit=limit, offset=offset))
    if site in ["ops", "all"]:
        results.extend(get_transcode_candidates(ops_api, limit=limit, offset=offset))

    return {"candidates": results}, 200


@app.route("/api/transcode/all", methods=["POST"])
def transcode_all():
    app_config = app.config
    red_api = app_config["red_api"]
    ops_api = app_config["ops_api"]
    red_candidates = find_transcode_candidates(red_api)
    ops_candidates = find_transcode_candidates(ops_api)
    red_results = _transcode_and_upload(red_candidates, red_api)
    ops_results = _transcode_and_upload(ops_candidates, ops_api)
    return {"message": "Success", "results": {"red": red_results, "ops": ops_results}}, 200


def _transcode_and_upload(candidates, api):
    request_form = request.form.to_dict()
    upload = request_form.get("upload", "false").lower() == "true"
    single = request_form.get("single", "false").lower() == "true"
    add_to_qbittorrent = request_form.get(
        "add_to_qbittorrent", "false").lower() == "true"

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
        return http_error(str(e), 500)


@app.route("/api/transcode", methods=["POST"])
def transcode():
    app_config = app.config
    request_form = request.form.to_dict()
    torrent_url = request_form.get("torrent_url")

    def get_api_from_url(url):
        if 'redacted.sh' in url:
            return app_config['red_api']
        elif 'orpheus.network' in url:
            return app_config['ops_api']
        return None

    api = get_api_from_url(torrent_url)
    if api is None:
        return http_error("Invalid torrent URL (%s)" % torrent_url, 400)

    match = re.search(r'torrentid=(\d+)', torrent_url)
    if not match:
        return http_error("Invalid torrent URL (%s)" % torrent_url, 400)
    torrent_id = match.group(1)

    response = api.torrent(torrent_id)
    group_id = response["group"]["id"]
    candidates = [(int(group_id), int(torrent_id))]

    return _transcode_and_upload(candidates, api)


@app.errorhandler(404)
def page_not_found(_e):
    return http_error("Not found", 404)


def http_error(message, code):
    return {"status": "error", "message": message}, code


def run_webserver(app_config, host="0.0.0.0", port=9725):
    app.logger.setLevel(logging.INFO)

    red_api = RedAPI(app_config.get_redacted_api_key())
    ops_api = OpsAPI(app_config.get_orpheus_api_key())

    app.config.update({
        'red_api': red_api,
        'ops_api': ops_api,
        'data_dirs': app_config.get_data_dirs(),
        'output_dir': app_config.get_output_dir(),
        'torrent_dir': app_config.get_torrent_dir(),
        'qbittorrent': app_config.get_qbittorrent_config(),
    })

    app.run(debug=False, host=host, port=port)
