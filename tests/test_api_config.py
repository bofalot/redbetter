

import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
from api.main import app


@pytest.fixture(autouse=True)
def mock_config_load():
    with patch('redbetter.config.get_redacted_api_key', return_value='dummy_key'), \
         patch('redbetter.config.get_orpheus_api_key', return_value='dummy_key'), \
         patch('redbetter.config.get_data_dirs', return_value=['/data']), \
         patch('redbetter.config.get_output_dir', return_value='/output'), \
         patch('redbetter.config.get_torrent_dir', return_value='/torrents'), \
         patch('redbetter.config.get_qbittorrent_config', return_value={}):
        yield


client = TestClient(app)


def test_get_config():
    response = client.get("/api/config")
    assert response.status_code == 200
    data = response.json()
    assert "data_dirs" in data
    assert "output_dir" in data
    assert "torrent_dir" in data
    assert "qbittorrent" in data
