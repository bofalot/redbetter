
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
from api.main import app


@pytest.fixture(autouse=True)
def mock_config_load():
    with patch('redbetter.config.get_redacted_api_key', return_value='dummy_key'), \
         patch('redbetter.config.get_orpheus_api_key', return_value='dummy_key'):
        yield


client = TestClient(app)


@patch('api.routers.transcode.get_transcode_candidates')
def test_get_candidates_red(mock_get_candidates):
    mock_get_candidates.return_value = [{'name': 'red_candidate'}]
    response = client.get('/api/getCandidates?site=red')
    assert response.status_code == 200
    data = response.json()
    assert data['candidates'] == [{'name': 'red_candidate'}]
    assert mock_get_candidates.call_count == 1


@patch('api.routers.transcode.get_transcode_candidates')
def test_get_candidates_ops(mock_get_candidates):
    mock_get_candidates.return_value = [{'name': 'ops_candidate'}]
    response = client.get('/api/getCandidates?site=ops')
    assert response.status_code == 200
    data = response.json()
    assert data['candidates'] == [{'name': 'ops_candidate'}]
    assert mock_get_candidates.call_count == 1


@patch('api.routers.transcode.get_transcode_candidates')
def test_get_candidates_all(mock_get_candidates):
    mock_get_candidates.side_effect = [
        [{'name': 'red_candidate'}], [{'name': 'ops_candidate'}]
    ]
    response = client.get('/api/getCandidates?site=all')
    assert response.status_code == 200
    data = response.json()
    assert data['candidates'] == [{'name': 'red_candidate'}, {'name': 'ops_candidate'}]
    assert mock_get_candidates.call_count == 2


@patch('api.routers.transcode.get_transcode_candidates')
def test_get_candidates_with_pagination(mock_get_candidates):
    mock_get_candidates.return_value = []
    response = client.get('/api/getCandidates?site=red&limit=10&offset=5')
    assert response.status_code == 200
    assert mock_get_candidates.call_count == 1
