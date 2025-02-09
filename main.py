#!/usr/bin/env python3
from colorama import Fore
import pickle
import traceback
import urllib.parse
from args import parse_args
from config import parse_config
from webserver import run_webserver

import redactedapi
from redactedbetter import find_and_upload_missing_transcodes

def server_mode(api, seen):
    print("Running webserver...")
    run_webserver(api, seen, data_dirs, output_dir, torrent_dir)

def script_mode(api, seen):
    print("Searching for transcode candidates...")
    if args.release_urls:
        print("You supplied one or more release URLs, ignoring your configuration's media types.")
        candidates = [(int(query['id']), int(query['torrentid'])) for query in\
                [dict(urllib.parse.parse_qsl(urllib.parse.urlparse(url).query)) for url in args.release_urls]]
    else:
        candidates = api.seeding(skip=seen)

    find_and_upload_missing_transcodes(candidates, api, seen, data_dirs, output_dir, torrent_dir, args.upload, args.single)

def main():
    api = redactedapi.RedactedAPI(api_key)

    try:
        seen = pickle.load(open(args.cache))
    except:
        seen = set()
        pickle.dump(seen, open(args.cache, 'wb'))

    try:
        if args.script:
            script_mode(api, seen)
        else:
            server_mode(api, seen)
    except Exception as e:
        print(traceback.format_exc())
        print(f"{Fore.RED}{str(e)}{Fore.RESET}")
        exit(1)


if __name__ == "__main__":
    args = parse_args()
    config = parse_config(args.config)
    api_key = config['redacted']['api_key']
    data_dirs = config['redacted']['data_dirs']
    output_dir = config['redacted']['output_dir']
    torrent_dir = config['redacted']['torrent_dir']
    main()
