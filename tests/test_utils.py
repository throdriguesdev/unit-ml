import pytest
import pandas as pd
from utils import calculate_mean_salary, get_salary_data_from_api


@pytest.fixture
def sample_data():
    return pd.DataFrame({
        'experience_level': ['SE', 'SE', 'MI', 'EN'],
        'employment_type': ['FT', 'CT', 'FT', 'FT'],
        'job_title': ['Data Scientist', 'Data Scientist', 'Data Analyst', 'Data Analyst'],
        'employee_residence': ['US', 'US', 'US', 'US'],
        'remote_ratio': [100, 100, 100, 100],
        'salary_in_usd': [100000, 110000, 70000, 60000]
    })


def test_calculate_mean_salary(sample_data):
    job_titles = ['Data Scientist', 'Data Analyst']
    mean_salary = calculate_mean_salary(sample_data, job_titles)
    assert mean_salary == 85000  # (100000 + 70000) / 2


def test_get_salary_data_from_api(requests_mock):
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
    data = get_salary_data_from_api("Data Scientist", "US")
    assert len(data) == 1
    assert data[0]['job_title'] == "Data Scientist"
    assert data[0]['location'] == "US"
    assert data[0]['median_salary'] == 100000
    assert data[0]['publisher_name'] == "Indeed"
    assert data[0]['publisher_link'] == "https://www.indeed.com"
