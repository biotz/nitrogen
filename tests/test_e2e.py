"""End to End API Tests
"""
import os
import urllib.request
import tests

SERVER_URL = f"http://server:{os.environ['SERVER_PORT']}/"


@tests.e2e
def test_health():
    response = urllib.request.urlopen(SERVER_URL)
    assert response.getcode() == 200
