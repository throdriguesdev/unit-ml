import pytest
from app import app


@pytest.fixture
def client():
    with app.test_client() as client:
        yield client




def test_ping_route(client):
    response = client.get('/ping')
    assert response.status_code == 200
    assert b'{"status":"up"}' in response.data


def test_predict_route(client, requests_mock):
    requests_mock.get('https://job-salary-data.p.rapidapi.com/job-salary', json={"status": "OK", "data": []})
    response = client.post('/predict', json={
        'experience_level': 'SE',
        'employment_type': 'FT',
        'job_title': 'Data Scientist',
        'employee_residence': 'US',
        'remote_ratio': 100
    })
    assert response.status_code == 302  # Redirect status code


def test_result_route(client, requests_mock):
    requests_mock.get('https://job-salary-data.p.rapidapi.com/job-salary', json={
        "status": "OK",
        "data": [
            {
                "job_title": "Data Scientist",
                "location": "US",
                "median_salary": 100000,
                "publisher_name": "Indeed",
                "publisher_link": "https://www.indeed.com"
            }
        ]
    })
    response = client.get('/result?predicted_salary=100000&job_title=Data+Scientist&employee_residence=US')
    assert response.status_code == 200
    assert b"$100,000" in response.data
    assert b"Indeed" in response.data
