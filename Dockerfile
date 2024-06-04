FROM python:3.11
WORKDIR /app
COPY . /app
RUN apt update && apt upgrade -y
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install pytest
RUN pytest -v > /app/pytest_logs.txt 2>&1
EXPOSE 5000
CMD gunicorn -b 0.0.0.0:5000 --workers=4 app:app && cat /app/pytest_logs.txt