import json
from unittest.mock import patch

import pytest

from redbetter.webserver import app


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        with patch('redbetter.webserver.RedAPI') as mock_red_api, \
                patch('redbetter.webserver.OpsAPI') as mock_ops_api:
            app.config['red_api'] = mock_red_api
            app.config['ops_api'] = mock_ops_api
            yield client


def test_get_candidates_red(client):
    with patch('redbetter.webserver.get_transcode_candidates') as mock_get_candidates:
        mock_get_candidates.return_value = [{'name': 'red_candidate'}]
        response = client.get('/api/getCandidates?site=red')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['candidates'] == [{'name': 'red_candidate'}]
        mock_get_candidates.assert_called_once_with(
            app.config['red_api'], limit=None, offset=None)


def test_get_candidates_ops(client):
    with patch('redbetter.webserver.get_transcode_candidates') as mock_get_candidates:
        mock_get_candidates.return_value = [{'name': 'ops_candidate'}]
        response = client.get('/api/getCandidates?site=ops')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['candidates'] == [{'name': 'ops_candidate'}]
        mock_get_candidates.assert_called_once_with(
            app.config['ops_api'], limit=None, offset=None)


def test_get_candidates_all(client):
    with patch('redbetter.webserver.get_transcode_candidates') as mock_get_candidates:
        mock_get_candidates.side_effect = [
            [{'name': 'red_candidate'}], [{'name': 'ops_candidate'}]]
        response = client.get('/api/getCandidates?site=all')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['candidates'] == [
            {'name': 'red_candidate'}, {'name': 'ops_candidate'}]
        assert mock_get_candidates.call_count == 2


def test_get_candidates_invalid_site(client):
    response = client.get('/api/getCandidates?site=invalid')
    assert response.status_code == 400
    data = json.loads(response.data)
    assert data['status'] == 'error'


def test_get_candidates_with_pagination(client):
    with patch('redbetter.webserver.get_transcode_candidates') as mock_get_candidates:
        mock_get_candidates.return_value = []
        response = client.get('/api/getCandidates?site=red&limit=10&offset=5')
        assert response.status_code == 200
        mock_get_candidates.assert_called_once_with(
            app.config['red_api'], limit=10, offset=5)
