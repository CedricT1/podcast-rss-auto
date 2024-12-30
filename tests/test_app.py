import pytest
from app import app, scan_podcasts, parse_date_from_filename
import os
from datetime import datetime, timezone

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_index_page(client):
    """Test if the index page loads correctly"""
    rv = client.get('/')
    assert rv.status_code == 200
    assert b'Liste des Podcasts' in rv.data

def test_scan_podcasts():
    """Test if podcast scanning works"""
    podcasts = scan_podcasts()
    assert isinstance(podcasts, list)
    if podcasts:  # If there are podcasts
        assert all('title' in p and 'url' in p for p in podcasts)

def test_parse_date():
    """Test date parsing from filename"""
    test_filename = "emission-301224_1516.mp3"
    date = parse_date_from_filename(test_filename)
    assert isinstance(date, datetime)
    assert date.tzinfo == timezone.utc

def test_rss_feed(client):
    """Test if RSS feed is generated correctly"""
    rv = client.get('/feed.xml')
    assert rv.status_code == 200
    assert rv.headers['Content-Type'] == 'application/rss+xml'
    assert b'<?xml' in rv.data