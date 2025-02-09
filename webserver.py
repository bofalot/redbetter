import logging
import re

from flask import Flask, request

from redactedbetter import find_and_upload_missing_transcodes

app = Flask(__name__)


@app.before_request
def log_request_info():
  app.logger.info(f"Incoming webhook with body: {request.get_data()}")


@app.after_request
def log_response_info(response):
  app.logger.info(f"Responding: {response.get_data()}")
  return response


@app.route("/api/webhook", methods=["POST"])
def webhook():
  config = app.config
  request_form = request.form.to_dict()
  torrent_url = request_form.get("torrent_url")
  upload = bool(request_form.get("upload"))
  single = bool(request_form.get("single"))

  def is_valid_url(url):
    a = re.findall(r'https://(redacted\.sh|orpheus.network)\/torrents.php\?torrentid=(\d+)', url)
    if len(a) == 0:
      return None
    else:
      return a[0][1]

  torrent_id = is_valid_url(torrent_url)
  if torrent_url is None:
    return http_error("Request must include a 'torrent_url' parameter", 400)

  if torrent_id is None:
    return http_error("Invalid torrent URL (%s)" % torrent_url, 400)

  response = config["api"].torrent(torrent_id)
  group_id = response["group"]["id"]
  candidates = [(int(group_id), int(torrent_id))]

  try:
    new_torrents = find_and_upload_missing_transcodes(
      candidates, config['api'], config['seen'], config['data_dirs'], config['output_dir'], config['torrent_dir'], upload, single)

    if len(new_torrents) == 0:
      result = {"message": "No available transcodes to better", "torrent_files": new_torrents}, 200
    else:
      result = {"message": "Success", "torrent_files": new_torrents}, 201
    return result
  except Exception as e:
    return http_error(str(e), 500)


@app.errorhandler(404)
def page_not_found(_e):
  return http_error("Not found", 404)


def http_error(message, code):
  return {"status": "error", "message": message}, code


def run_webserver(api, seen, data_dirs, output_dir, torrent_dir, host="0.0.0.0", port=9725):
  app.logger.setLevel(logging.INFO)
  app.config.update(
    {
      "api": api,
      "seen": seen,
      "data_dirs": data_dirs,
      "output_dir": output_dir,
      "torrent_dir": torrent_dir
    }
  )

  app.run(debug=False, host=host, port=port)
