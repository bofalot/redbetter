import os
import sys
import configparser
import logging


class _Config:
    def __init__(self):
        self.config = None
        self.redacted_api_key = None
        self.orpheus_api_key = None
        self.data_dirs = None
        self.output_dir = None
        self.torrent_dir = None
        self.qbittorrent = None

    def load_config(self, config_file_path):
        if not os.path.exists(config_file_path):
            print(f"Config file not found: {config_file_path}")
            sys.exit(2)

        self.config = configparser.RawConfigParser()
        self.config.read(config_file_path)

        self.redacted_api_key = self.config.get('api_keys', 'redacted')
        self.orpheus_api_key = self.config.get('api_keys', 'orpheus')
        self.data_dirs = self.config.get('directories', 'data_dirs').split(',')
        self.output_dir = self.config.get('directories', 'output_dir')
        self.torrent_dir = self.config.get('directories', 'torrent_dir')

        if self.config.has_section('qbittorrent'):
            self.qbittorrent = {
                'host': self.config.get('qbittorrent', 'host'),
                'port': self.config.get('qbittorrent', 'port'),
                'username': self.config.get('qbittorrent', 'username'),
                'password': self.config.get('qbittorrent', 'password'),
            }
        logging.info("Loaded configuration:")
        logging.info(f"  Redacted API Key: {self.redacted_api_key[:4]}..."
                     f"{self.redacted_api_key[-4:] if self.redacted_api_key else 'N/A'}")
        logging.info(f"  Orpheus API Key: {self.orpheus_api_key[:4]}..."
                     f"{self.orpheus_api_key[-4:] if self.orpheus_api_key else 'N/A'}")
        logging.info(f"  Data Dirs: {self.data_dirs}")
        logging.info(f"  Output Dir: {self.output_dir}")
        logging.info(f"  Torrent Dir: {self.torrent_dir}")
        logging.info(f"  qBittorrent Config: {self.qbittorrent}")

    def get_redacted_api_key(self):
        return self.redacted_api_key

    def get_orpheus_api_key(self):
        return self.orpheus_api_key

    def get_data_dirs(self):
        return self.data_dirs

    def get_output_dir(self):
        return self.output_dir

    def get_torrent_dir(self):
        return self.torrent_dir

    def get_qbittorrent_config(self):
        return self.qbittorrent

    def get_sanitized_config(self):
        sanitized = {
            "data_dirs": self.data_dirs,
            "output_dir": self.output_dir,
            "torrent_dir": self.torrent_dir,
            "qbittorrent": self.qbittorrent,
        }

        # Mask API keys
        if self.redacted_api_key:
            sanitized["redacted_api_key"] = f"{self.redacted_api_key[:4]}...{self.redacted_api_key[-4:]}"
        else:
            sanitized["redacted_api_key"] = "N/A"

        if self.orpheus_api_key:
            sanitized["orpheus_api_key"] = f"{self.orpheus_api_key[:4]}...{self.orpheus_api_key[-4:]}"
        else:
            sanitized["orpheus_api_key"] = "N/A"

        # Mask qBittorrent password
        if self.qbittorrent and self.qbittorrent.get("password"):
            sanitized["qbittorrent"]["password"] = \
                f"{self.qbittorrent['password'][:4]}...{self.qbittorrent['password'][-4:]}"

        return sanitized


config = _Config()


def load_config(config_file_path):
    config.load_config(config_file_path)


def get_redacted_api_key():
    return config.get_redacted_api_key()


def get_orpheus_api_key():
    return config.get_orpheus_api_key()


def get_data_dirs():
    return config.get_data_dirs()


def get_output_dir():
    return config.get_output_dir()


def get_torrent_dir():
    return config.get_torrent_dir()


def get_qbittorrent_config():
    return config.get_qbittorrent_config()


def get_sanitized_config():
    return config.get_sanitized_config()
