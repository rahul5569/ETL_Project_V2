# Docker Load Tester with Locust

This repository contains a load testing setup using Locust to test an API. The test simulates POST requests with random text file URLs, hosted within a shared directory. It allows you to specify the target URL and configure the payload for the test.

## Requirements

- Python 3.x
- Locust
- Docker (optional, if using containerized setup)

### Python dependencies:

To install the required Python dependencies, run the following command:

```
pip install -r requirements.txt
```

If you don't have a `requirements.txt` file, you can manually install Locust with:

```
pip install locust
```

## Setup

1. **Configure the target API URL** in the `locustfile.py` file. The configuration file contains the URL and parameters to be used in the load test.

2. **Ensure your content directory** is populated with the files you want to simulate POST requests for. The text files in this directory will be used for generating the URLs for the test.

## Running the Test

### Locust Command

To run the load test, execute the following command:

```
locust -f locustfile.py
```

This will start the Locust load testing web interface at `http://localhost:8089`.

### Locust Web Interface

- **Number of Users**: Set the number of virtual users (clients) to simulate.
- **Spawn Rate**: Define how quickly users are spawned.
- **Host**: Specify the base URL of your API.

Click **Start swarming** to begin the load test.

## Test Configuration

### `locustfile.py`

The `locustfile.py` contains the load testing script. The script generates random file URLs from the `content` directory and sends POST requests to your API.

### Example Payload

Each request will post the URL of a random file in the following format:

```
{
  "url": "http://yourserver.com/path/to/file.txt"
}
```

## Troubleshooting

If you encounter any issues, please ensure that:
- The target API is reachable.
- The content directory contains text files for the test.
- The correct configuration is set in `locustfile.py`.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
