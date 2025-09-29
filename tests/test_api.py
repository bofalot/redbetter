import unittest
from unittest.mock import patch, MagicMock, mock_open
import json

from redbetter import api
from redbetter import redactedbetter


class TestAPI(unittest.TestCase):

    @patch('api.requests.session')
    def setUp(self, mock_session):
        self.mock_session = mock_session
        self.mock_response = MagicMock()
        self.mock_response.text = json.dumps({'status': 'success', 'response': {'id': 123, 'passkey': 'abc'}})
        self.mock_session.return_value.get.return_value = self.mock_response
        self.api = api.RedAPI(api_key='test_key')

    def test_init(self):
        """Test that the RedAPI class is initialized correctly."""
        self.assertEqual(self.api.site_url, 'https://redacted.sh')
        self.assertEqual(self.api.tracker_url, 'https://flacsfor.me')

    def test_seeding(self):
        """Test that the seeding method correctly fetches and parses the list of seeding torrents."""
        self.api.get_account_info = MagicMock(return_value={'status': 'success', 'response': {'id': 123, 'passkey': 'abc'}})
        mock_response = MagicMock()
        mock_response.text = json.dumps({'status': 'success', 'response': {'seeding':[{'groupId':1,'torrentId':2},{'groupId':3,'torrentId':4}]}})
        self.mock_session.return_value.get.return_value = mock_response
        
        seeding_torrents = self.api.seeding()

        self.assertEqual(list(seeding_torrents), [[1, 2], [3, 4]])
        
    def test_torrent_group(self):
        """Test that the torrent_group method correctly fetches and parses a torrent group."""
        mock_response = MagicMock()
        mock_response.text = json.dumps({'status': 'success', 'response': {'group':{'name':'Test Group','musicInfo':{'artists':[{'name':'Test Artist'}]},'year':2023},'torrents':[]}})
        self.mock_session.return_value.get.return_value = mock_response

        group = self.api.torrent_group(1)

        self.assertEqual(group['name'], 'Test Group')

    def test_torrent(self):
        """Test that the torrent method correctly fetches a single torrent."""
        mock_response = MagicMock()
        mock_response.text = json.dumps({'status': 'success', 'response': {'id':1}})
        self.mock_session.return_value.get.return_value = mock_response

        torrent = self.api.torrent(1)

        self.assertEqual(torrent['id'], 1)

    @patch('builtins.open', new_callable=mock_open, read_data=b'torrent_data')
    def test_upload(self, mock_file):
        """Test that the upload method correctly constructs and sends the upload request."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        self.mock_session.return_value.post.return_value = mock_response

        group = {"group": {"id": 1}}
        torrent = {
            'remasterYear': 2023,
            'remasterTitle': 'Test Remaster',
            'remasterRecordLabel': 'Test Label',
            'remasterCatalogueNumber': '123',
            'media': 'CD'
        }
        new_torrent = 'path/to/new.torrent'
        format = 'FLAC'
        description = ['Test description']

        response = self.api.upload(group, torrent, new_torrent, format, description, dry_run=False)

        self.assertEqual(response.status_code, 200)
        self.mock_session.return_value.post.assert_called_once()

    def test_allowed_transcodes(self):
        """Test the allowed_transcodes function."""
        torrent_with_preemphasis = {'remasterTitle': 'with pre-emphasis'}
        torrent_without_preemphasis = {'remasterTitle': 'normal'}

        self.assertEqual(redactedbetter.allowed_transcodes(torrent_with_preemphasis), [])
        self.assertNotEqual(redactedbetter.allowed_transcodes(torrent_without_preemphasis), [])

    def test_release_url(self):
        """Test the release_url function."""
        self.assertEqual(self.api.release_url(1, 2), 'https://redacted.sh/torrents.php?id=1&torrentid=2#torrent2')

    def test_permalink(self):
        """Test the permalink function."""
        self.assertEqual(self.api.permalink(1), 'https://redacted.sh/torrents.php?torrentid=1')

if __name__ == '__main__':
    unittest.main()