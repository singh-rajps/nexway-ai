# IoT Device Management System

A simple IoT Device Management REST API built with Python and FastAPI, along with automated tests.

## Features
- Register new IoT devices
- List all connected devices
- Get detailed device information
- Update device status (e.g., heartbeat)
- Delete a device

## Setup and Installation

1. **Install dependencies:**
   Make sure you have Python installed, then run:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the API Server:**
   ```bash
   uvicorn main:app --reload
   ```
   The API will be accessible at `http://127.0.0.1:8000`. You can view the interactive API documentation (Swagger UI) at `http://127.0.0.1:8000/docs`.

## Running the Tests

To run the automated tests, simply use `pytest`:

```bash
pytest test_main.py
```
