import requests

url = "https://job-salary-data.p.rapidapi.com/job-salary"

querystring = {"job_title":"nodejs developer","location":"new york, usa","radius":"200"}

headers = {
	"X-RapidAPI-Key": "2d562a2038msh442eec8c1d9f5a7p1049a4jsn6954b73a715c",
	"X-RapidAPI-Host": "job-salary-data.p.rapidapi.com"
}
    
response = requests.get(url, headers=headers, params=querystring)

print(response.json())