import os
import sys
import configparser

def parse_config(config_file_path):
    if not os.path.exists(config_file_path):
        print("Config file not found: %s" % config_file_path)
        sys.exit(2)

    config = configparser.RawConfigParser()
    config.read(config_file_path)

    api_key = config.get('redacted', 'api_key')
    data_dirs = config.get('redacted', 'data_dirs').split(',')
    output_dir = config.get('redacted', 'output_dir')
    torrent_dir = config.get('redacted', 'torrent_dir')

    return {
        "redacted": {
            "api_key": api_key,
            "data_dirs": data_dirs,
            "output_dir": output_dir,
            "torrent_dir": torrent_dir
        },
        "orpheus": None
    }