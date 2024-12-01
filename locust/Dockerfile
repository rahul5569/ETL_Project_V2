FROM python:3.11-slim

WORKDIR /locust

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8089

CMD locust -f locustfile.py --headless -u "${LOCUST_USERS}" -r "${LOCUST_SPAWN_RATE}" --run-time "${LOCUST_RUN_TIME}"
