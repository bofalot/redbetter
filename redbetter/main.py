#!/usr/bin/env python3
import logging
from colorama import Fore
import traceback
from args import parse_args
import config
from redbetter.webserver import run_webserver
from http.client import HTTPConnection

logging.basicConfig(level=logging.INFO)
logging.getLogger("urllib3.connectionpool").setLevel(logging.DEBUG)
logging.getLogger("http.client").setLevel(logging.DEBUG)
HTTPConnection.debuglevel = 1
requests_log = logging.getLogger("requests.packages.urllib3")
requests_log.setLevel(logging.DEBUG)
requests_log.propagate = True


def main():
    try:
        run_webserver(config)
    except Exception as e:
        print(traceback.format_exc())
        print(f"{Fore.RED}{str(e)}{Fore.RESET}")
        exit(1)


if __name__ == "__main__":
    args = parse_args()
    config.load_config(args.config)
    main()
