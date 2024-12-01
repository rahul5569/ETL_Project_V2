# locust.py

import os
import random
from locust import HttpUser, task, between
import json

class APILoadTestUser(HttpUser):
    wait_time = between(1, 5)  # Wait between 1 to 5 seconds between tasks

    # Load configuration from a JSON file
    def on_start(self):
        config_path = "./config.json"
        if not os.path.exists(config_path):
            raise FileNotFoundError(f"Config file not found at {config_path}")
        
        with open(config_path, "r") as config_file:
            config = json.load(config_file)
        
        self.target_url = config.get("target_url")
        self.content_directory = config.get("content_directory", "./content")

        if not self.target_url:
            raise ValueError("target_url is not specified in the config file.")
        
        if not os.path.exists(self.content_directory):
            raise ValueError(f"Content directory '{self.content_directory}' does not exist.")

    @task
    def upload_file(self):
        # Get all text files from the content directory
        files = [f for f in os.listdir(self.content_directory) if f.endswith(".txt")]
        if not files:
            print("No text files found in the content directory!")
            return
        
        # Pick a random text file
        random_file = random.choice(files)
        
        # Read the file content
        file_path = os.path.join(self.content_directory, random_file)
        if not os.path.isfile(file_path):
            print(f"File '{file_path}' does not exist or is not accessible!")
            return
        
        with open(file_path, "rb") as file:
            file_content = file.read()

        # Prepare multipart form data (only the file)
        files = {
            "file": (random_file, file_content, "text/plain")
        }

        # Send a POST request to the /upload/ endpoint
        with self.client.post("/upload/", files=files, catch_response=True) as response:
            if response.status_code == 200:
                print(f"Successfully uploaded '{random_file}'")
                response.success()
            else:
                print(f"Failed to upload '{random_file}': {response.status_code} - {response.text}")
                response.failure(f"Failed to upload '{random_file}': {response.status_code} - {response.text}")

# Main function for running the script standalone (optional)
if __name__ == "__main__":
    import sys
    from locust import events, runners

    # Standalone Locust runner for debugging
    class DebugAPILoadTestUser(APILoadTestUser):
        def on_start(self):
            super().on_start()
            print("Debug mode: Configuration loaded and user initialized.")
        
        def run_single_task(self):
            try:
                self.upload_file()
            except Exception as e:
                print(f"Error while running task: {e}")

    # Run a single instance of the user for testing
    user = DebugAPILoadTestUser(runners.MasterRunner(env=None))
    user.on_start()
    print("Running a single task...")
    user.run_single_task()
