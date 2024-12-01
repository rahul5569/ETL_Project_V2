from locust import HttpUser, task, between
import logging
import os

# Configure Logging
logger = logging.getLogger("locust")
logger.setLevel(logging.INFO)

class IngestionUser(HttpUser):
    wait_time = between(1, 5)
    host = os.getenv("LOCUST_HOST")

    def on_start(self):
        if self.host is None:
            logger.error("Host is not set. Please ensure that the host is specified.")
        else:
            logger.info(f"Starting load test against host: {self.host}")

    @task
    def upload_file(self):
        logger.info("Executing upload_file task")
        files = {
            'file': ('test_file.txt', 'This is a test file for upload.', 'text/plain')
        }
        with self.client.post("/upload/", files=files, catch_response=True) as response:
            if response.status_code != 200:
                logger.error(f"Failed to upload file: {response.text}")
                response.failure(f"Failed to upload file: {response.text}")
            else:
                logger.info("File uploaded successfully")
                response.success()
