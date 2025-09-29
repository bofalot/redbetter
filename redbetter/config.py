import os
import sys
import configparser

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
