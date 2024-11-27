import threading
import time
from client_library import VideoTranslationClient
from server import app  # Import the Flask app from server.py

# Function to run the Flask server
def run_server():
    app.run(debug=False, use_reloader=False)

# Integration test
def integration_test():
    # Start the server in a separate thread
    server_thread = threading.Thread(target=run_server, daemon=True)
    server_thread.start()
    time.sleep(1)  # Give the server time to start

    # Use the client library to interact with the server
    client = VideoTranslationClient(base_url="http://127.0.0.1:5000", timeout=30)
    try:
        status = client.get_status()
        print(f"Integration Test: Final status from server: {status}")
    except Exception as e:
        print(f"Integration Test: An error occurred - {e}")

    # Shut down the server thread
    print("Integration Test Over")

if __name__ == "__main__":
    integration_test()
