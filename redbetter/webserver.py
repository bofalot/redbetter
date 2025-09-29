import logging
import pickle
import re

from flask import Flask, request

from api import RedAPI, OpsAPI
import config
from redactedbetter import find_and_upload_missing_transcodes, find_transcode_candidates

app = Flask(__name__)


@app.before_request
def log_request_info():
  app.logger.info(f"Incoming webhook with body: {request.get_data()}")


@app.after_request
def log_response_info(response):
  app.logger.info(f"Responding: {response.get_data()}")
  return response


@app.route("/api/transcode/all", methods=["POST"])
def transcode_all():
    config = app.config
    red_api = config["red_api"]
    ops_api = config["ops_api"]
    seen = config["seen"]
    red_candidates = find_transcode_candidates(red_api, seen)
    ops_candidates = find_transcode_candidates(ops_api, seen)
    red_results = _transcode_and_upload(red_candidates, red_api, seen)
    ops_results = _transcode_and_upload(ops_candidates, ops_api, seen)
    return {"message": "Success", "results": {"red": red_results, "ops": ops_results}}, 200


def _transcode_and_upload(candidates, api, seen):
    request_form = request.form.to_dict()
    upload = request_form.get("upload", "false").lower() == "true"
    single = request_form.get("single", "false").lower() == "true"
    add_to_qbittorrent = request_form.get("add_to_qbittorrent", "false").lower() == "true"

    try:
        new_torrents = find_and_upload_missing_transcodes(
            candidates, api, seen, upload, single, add_to_qbittorrent)

        if len(new_torrents) == 0:
            result = {"message": "No available transcodes to better", "torrent_files": new_torrents}
        else:
            result = {"message": "Success", "torrent_files": new_torrents}
        return result
    except Exception as e:
        return http_error(str(e), 500)


@app.route("/api/transcode", methods=["POST"])
def transcode():
  config = app.config
  seen = config["seen"]
  request_form = request.form.to_dict()
  torrent_url = request_form.get("torrent_url")

  def get_api_from_url(url):
      if 'redacted.sh' in url:
          return config['red_api']
      elif 'orpheus.network' in url:
          return config['ops_api']
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

  return _transcode_and_upload(candidates, api, seen)


@app.errorhandler(404)
def page_not_found(_e):
  return http_error("Not found", 404)


def http_error(message, code):
  return {"status": "error", "message": message}, code


def run_webserver(args, host="0.0.0.0", port=9725):
  app.logger.setLevel(logging.INFO)

  red_api = RedAPI(config.get_redacted_api_key())
  ops_api = OpsAPI(config.get_orpheus_api_key())

  try:
      seen = pickle.load(open(args.cache))
  except:
      seen = set()
      pickle.dump(seen, open(args.cache, 'wb'))

  app.config.update({
      'red_api': red_api,
      'ops_api': ops_api,
      'seen': seen,
      'data_dirs': config.get_data_dirs(),
      'output_dir': config.get_output_dir(),
      'torrent_dir': config.get_torrent_dir(),
      'qbittorrent': config.get_qbittorrent_config(),
  })

  app.run(debug=False, host=host, port=port)