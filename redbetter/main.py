#!/usr/bin/env python3
from colorama import Fore
import traceback
from args import parse_args
import config
from redbetter.webserver import run_webserver


def main():
    try:
        run_webserver(args)
    except Exception as e:
        print(traceback.format_exc())
        print(f"{Fore.RED}{str(e)}{Fore.RESET}")
        exit(1)


if __name__ == "__main__":
    args = parse_args()
    config.load_config(args.config)
    main()
