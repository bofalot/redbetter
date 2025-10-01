
import json
from unittest.mock import patch, MagicMock, mock_open

import pytest
from redbetter import api, redactedbetter


@pytest.fixture
def mock_session():
    with patch('redbetter.api.requests.session') as mock_session:
        yield mock_session


@pytest.fixture
def red_api(mock_session):
    mock_response = MagicMock()
    mock_response.text = json.dumps(
        {'status': 'success', 'response': {'id': 123, 'passkey': 'abc'}})
    mock_session.return_value.get.return_value = mock_response
    return api.RedAPI(api_key='test_key')


def test_init(red_api):
    """Test that the RedAPI class is initialized correctly."""
    assert red_api.site_url == 'https://redacted.sh'
    assert red_api.tracker_url == 'https://flacsfor.me'


def test_seeding(red_api, mock_session):
    """Test that the seeding method correctly fetches and parses the list of seeding torrents."""
    red_api.get_account_info = MagicMock(
        return_value={'status': 'success', 'response': {'id': 123, 'passkey': 'abc'}})
    mock_response = MagicMock()
    mock_response.text = json.dumps({'status': 'success', 'response': {'seeding': [
                                    {'groupId': 1, 'torrentId': 2}, {'groupId': 3, 'torrentId': 4}]}})
    mock_session.return_value.get.return_value = mock_response

    seeding_torrents = red_api.seeding()

    assert list(seeding_torrents) == [[1, 2], [3, 4]]


def test_torrent_group(red_api, mock_session):
    """Test that the torrent_group method correctly fetches and parses a torrent group."""
    mock_response = MagicMock()
    mock_response.text = json.dumps({'status': 'success', 'response': {'group': {'name': 'Test Group', 'musicInfo': {
                                    'artists': [{'name': 'Test Artist'}]}, 'year': 2023}, 'torrents': []}})
    mock_session.return_value.get.return_value = mock_response

    group = red_api.torrent_group(1)

    assert group['name'] == 'Test Group'


def test_torrent(red_api, mock_session):
    """Test that the torrent method correctly fetches a single torrent."""
    mock_response = MagicMock()
    mock_response.text = json.dumps(
        {'status': 'success', 'response': {'id': 1}})
    mock_session.return_value.get.return_value = mock_response

    torrent = red_api.torrent(1)

    assert torrent['id'] == 1


@patch('builtins.open', new_callable=mock_open, read_data=b'torrent_data')
def test_upload(mock_file, red_api, mock_session):
    """Test that the upload method correctly constructs and sends the upload request."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_session.return_value.post.return_value = mock_response

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

    response = red_api.upload(
        group, torrent, new_torrent, format, description, dry_run=False)

    assert response.status_code == 200
    mock_session.return_value.post.assert_called_once()


def test_allowed_transcodes():
    """Test the allowed_transcodes function."""
    torrent_with_preemphasis = {'remasterTitle': 'with pre-emphasis'}
    torrent_without_preemphasis = {'remasterTitle': 'normal'}

    assert redactedbetter.allowed_transcodes(torrent_with_preemphasis) == []
    assert redactedbetter.allowed_transcodes(torrent_without_preemphasis) != []


def test_release_url(red_api):
    """Test the release_url function."""
    assert red_api.release_url(
        1, 2) == 'https://redacted.sh/torrents.php?id=1&torrentid=2#torrent2'


def test_permalink(red_api):
    """Test the permalink function."""
    assert red_api.permalink(
        1) == 'https://redacted.sh/torrents.php?torrentid=1'
