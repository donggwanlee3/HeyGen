## Documentation: How to Use `VideoTranslationClient`

The `VideoTranslationClient` is a Python client library designed to interact with a video translation server that provides the status of a video translation job. It implements efficient polling with exponential backoff to minimize server load while ensuring timely updates.

---

### **Setup**

1. **Install Dependencies**
   Ensure you have the following Python packages installed:
   - `requests`
   - `logging`

   Use `pip` to install the required packages:
   ```bash
   pip install requests
   ```

2. **Run the Server**
   Make sure your video translation server (e.g., Flask app) is running on the specified base URL. By default, it listens on `http://127.0.0.1:5000/status`.

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
