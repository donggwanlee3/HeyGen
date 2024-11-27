## Documentation: How to Use `VideoTranslationClient`

The `VideoTranslationClient` is a Python client library designed to interact with a video translation server that provides the status of a video translation job. It implements efficient polling with exponential backoff to minimize server load while ensuring timely updates.

---

### **Setup**

1. **Install Dependencies**
 `pip install -r requirements.txt`

2. **Run the Server**
   Make sure your video translation server  is running on the specified base URL. By default, it listens on `http://127.0.0.1:5000/status`.
### **How to Run the Server, Client Library, and Integration Test**

To test the entire setup, including the server, client library, and integration test, follow these steps:

---

### **Run the Server**
The server provides the `/status` endpoint for the client library to query. Make sure the server is running before starting the integration test or using the client library.

1. **Start the Server**:
   Run the following command in your terminal:
   ```bash
   python server.py
   ```

2. **Verify the Server is Running**:
   Open your browser or use `curl` to test the `/status` endpoint:
   ```bash
   curl http://127.0.0.1:5000/status
   ```
   Expected output:
   ```json
   {"result": "pending"}
   ```

3. **Monitor the Server Logs**:
   Check the terminal running `server.py` for logs to ensure it's functioning correctly.

---

### **Run the Client Library**
The client library polls the server to get the job status. You can use it independently or in an integration test.

1. **Write a Script to Use the Client Library**:
   Save the following code in a file, for example, `client_script.py`:
   ```python
   from client_library import VideoTranslationClient

   client = VideoTranslationClient(
       base_url="http://127.0.0.1:5000",  # Server base URL
       max_retries=10,
       backoff_factor=2,
       timeout=30
   )

   try:
       status = client.get_status()
       print(f"Final status: {status}")
   except TimeoutError as e:
       print(f"Timeout occurred: {e}")
   except Exception as e:
       print(f"An error occurred: {e}")
   ```

2. **Run the Script**:
   ```bash
   python client_script.py
   ```

3. **Check the Logs**:
   Logs will appear in the terminal, providing detailed information about retries, status updates, and elapsed time.

---

### **Run the Integration Test**
The integration test combines the server and client to simulate a real-world use case.

2. **Run the Integration Test**:
   Execute the test with:
   ```bash
   python integration_test.py
   ```

3. **Expected Output**:
   The integration test will start the server, use the client library to poll for the job status, and display the final result. Example output:
   ```
   Integration Test: Final status from server: completed
   Integration Test: Completed
   ```

---

### **Final Notes**

1. **Install Dependencies**:
   Ensure all dependencies are installed before running any scripts:
   ```bash
   pip install -r requirements.txt
   ```

2. **Environment Isolation**:
   Use a virtual environment for better dependency management:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. **Debugging**:
   - Check server logs for any issues.
   - Verify the `base_url` in the client library matches the running server’s URL.

This guide ensures you can seamlessly run the server, client library, and integration test to verify the complete setup.
---

### **Using the Library**

1. **Initialize the Client**
   Import the `VideoTranslationClient` class and initialize it with the base URL of the server:
   ```python
   from client_library import VideoTranslationClient

   client = VideoTranslationClient(
       base_url="http://127.0.0.1:5000",  # URL of the server
       max_retries=10,                    # Maximum number of retries
       backoff_factor=2,                  # Exponential backoff factor
       timeout=30                         # Total timeout in seconds
   )
   ```

   - **`base_url`**: URL of the video translation server.
   - **`max_retries`**: Maximum number of retries before giving up.
   - **`backoff_factor`**: Multiplier for exponential backoff (e.g., 2 means 2, 4, 8 seconds).
   - **`timeout`**: Total time (in seconds) before the client stops polling.

2. **Check Job Status**
   Call the `get_status` method to poll the server and retrieve the status:
   ```python
   try:
       status = client.get_status()
       print(f"Final status of the job: {status}")
   except TimeoutError as e:
       print(f"Operation timed out: {e}")
   except Exception as e:
       print(f"An error occurred: {e}")
   ```

   - The `get_status` method polls the server until the job completes (`"completed"`), encounters an error (`"error"`), or exceeds the timeout.
   - Logs will show detailed information about retries, elapsed time, and status.

3. **Logs**
   The client library provides informative logs during execution:
   - **Initial Status**: Logs the first response from the server.
   - **Retries**: Logs each retry attempt with the current status and elapsed time.
   - **Completion**: Logs the final status once the job is completed or fails.

   Example log:
   ```
   10:15:01 - INFO - Initial status: pending
   10:15:01 - INFO - Sleeping for 2s before retry #1. Total elapsed time = 0s
   10:15:03 - INFO - Retry attempt #1: Current status = pending, Elapsed time = 2s
   10:15:03 - INFO - Sleeping for 4s before retry #2. Total elapsed time = 2s
   10:15:07 - INFO - Job completed with status: completed
   ```

---

### **Example Usage**

Here’s a complete example:

```python
from client_library import VideoTranslationClient

# Initialize the client
client = VideoTranslationClient(
    base_url="http://127.0.0.1:5000",  # Server base URL
    max_retries=10,                    # Max retries
    backoff_factor=2,                  # Backoff factor
    timeout=30                         # Timeout in seconds
)

# Poll the server for status
try:
    status = client.get_status()
    print(f"Final status of the job: {status}")
except TimeoutError as e:
    print(f"Operation timed out: {e}")
except Exception as e:
    print(f"An error occurred: {e}")
```

---

### **Client Features**

1. **Efficient Polling**:
   - Implements exponential backoff to optimize polling frequency.

2. **Timeout Handling**:
   - Stops polling after the specified timeout and raises a `TimeoutError`.

3. **Retry Limit**:
   - Prevents infinite retries by capping the number of attempts.

4. **Comprehensive Logs**:
   - Provides detailed logs for each retry and status update.

---

### **Troubleshooting**

- **Timeouts**:
  - Increase the `timeout` value if the server requires more time to process the job.
  
- **Server Not Responding**:
  - Ensure the server is running and accessible at the specified `base_url`.

- **Unexpected Errors**:
  - Check the server logs for any issues if `requests.RequestException` is raised.

---
