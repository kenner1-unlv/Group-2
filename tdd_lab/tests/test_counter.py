"""
Test Cases for Counter Web Service

Create a service that can keep a track of multiple counters
- API must be RESTful - see the status.py file. Following these guidelines, you can make assumptions about
how to call the web service and assert what it should return.
- The endpoint should be called /counters
- When creating a counter, you must specify the name in the path.
- Duplicate names must return a conflict error code.
- The service must be able to update a counter by name.
- The service must be able to read the counter
"""

import pytest
from src import app
from src import status

@pytest.fixture()
def client():
    """Fixture for Flask test client"""
    return app.test_client()

@pytest.mark.usefixtures("client")
class TestCounterEndpoints:
    """Test cases for Counter API"""

    def test_create_counter(self, client):
        """It should create a counter"""
        result = client.post('/counters/foo')
        assert result.status_code == status.HTTP_201_CREATED

    def test_list_counters(self, client):
        """It should list all counters and their values"""
        client.post('/counters/test1')
        client.post('/counters/test2')

        result = client.get('/counters')
        assert result.status_code == status.HTTP_200_OK

        # Other tests share the COUNTERS dict, so assert on the counters
        # this test created rather than on the whole response.
        data = result.get_json()
        assert data['test1'] == 0
        assert data['test2'] == 0

    def test_increment_counter(self, client):
        """It should increment an existing counter's value"""
        # Starting point: creating a counter starting at 0
        client.post('/counters/inc')

        # Implementation via PUT
        result = client.put('/counters/inc')

        # Assert: request success and value increased
        assert result.status_code == status.HTTP_200_OK
        data = result.get_json()
        assert data['inc'] == 1

