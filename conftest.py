import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client
        
        ###TEST test_input.py, test_unit-test_routes.py, tests/test_unit.py
        
