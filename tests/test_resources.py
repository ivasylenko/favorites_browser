import os
import pytest
from unittest.mock import patch
import json
import tempfile

from app.application import FlaskApplication
FlaskApplication.construct_app()
app = FlaskApplication.APP


mock_photos =  [
    {'farm': '66', 'id': '51150463332', 'isfamily': '0', 'isfriend': '0', 'ispublic': '1', 'owner': '192068950@N02',
    'secret': '4c75af6e8c', 'server': '65535', 'title': 'snapshot'},
    {'farm': '66', 'id': '51150463447', 'isfamily': '0', 'isfriend': '0', 'ispublic': '1', 'owner': '190622906@N05',
    'secret': 'ef1a9d3a06', 'server': '65535', 'title': 'SMART FORTWO 451 ANG...MOUNT CLIP'}
]

mock_favorites = [
  {
    "id": 51151911549,
    "title": "Drew Crochet Zipper Pouch / Clutch Bag 01",
    "owner": "192489650@N02",
    "secret": "c73c316f20",
    "server": "65535"
  },
  {
    "id": 51150451497,
    "title": "Drew Crochet Zipper Pouch / Clutch Bag 02",
    "owner": "192489650@N02",
    "secret": "bd3259538d",
    "server": "65535"
  }
]

@pytest.fixture
def client():
    db_fd, app.config['DATABASE'] = tempfile.mkstemp()
    app.config['TESTING'] = True

    with app.test_client() as client:
        yield client

    os.close(db_fd)
    os.unlink(app.config['DATABASE'])

@patch('app.providers.FlickrProvider.get_photos')
def test_fetch_recent_photos(mock_get_photos, client):
    """Start with a blank database."""
    mock_get_photos.return_value = mock_photos
    response = client.get('/feed')
    result = json.loads(response.data.decode('utf-8'))
    assert mock_get_photos.call_count == 1
    call = mock_get_photos.mock_calls[0]
    assert not call.kwargs
    assert result.get('error') is None
    assert len(result.get('data')) == 2

@patch('app.providers.FlickrProvider.get_photos')
def test_search_photos(mock_get_photos, client):
    """Start with a blank database."""
    mock_get_photos.return_value = mock_photos
    response = client.get('/feed?text=chess')
    result = json.loads(response.data.decode('utf-8'))
    assert mock_get_photos.call_count == 1
    call = mock_get_photos.mock_calls[0]
    assert call.kwargs.get('text') == 'chess'
    assert result.get('error') is None
    assert len(result.get('data')) == 2
