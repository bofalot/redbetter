import logging
from qbittorrentapi import Client

class QBittorrentClient:
    def __init__(self, config):
        self.config = config
        self.client = None

    def connect(self):
        if not self.config or not self.config.get('host'):
            logging.info('qBittorrent is not configured, skipping.')
            return False

        try:
            self.client = Client(**self.config)
            self.client.auth_log_in()
            logging.info('Successfully connected to qBittorrent.')
            return True
        except Exception as e:
            logging.error(f'Failed to connect to qBittorrent: {e}')
            return False

    def add_torrent(self, torrent_file_path, save_path):
        if not self.client:
            if not self.connect():
                return

        try:
            with open(torrent_file_path, 'rb') as f:
                self.client.torrents_add(torrent_files=f, save_path=save_path)
            logging.info(f'Successfully added torrent {torrent_file_path} to qBittorrent.')
        except Exception as e:
            logging.error(f'Failed to add torrent {torrent_file_path} to qBittorrent: {e}')

    def disconnect(self):
        if self.client:
            self.client.auth_log_out()
            logging.info('Disconnected from qBittorrent.')
