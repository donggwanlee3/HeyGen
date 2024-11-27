from flask import Flask, jsonify
import time
import random

app = Flask(__name__)

# Simulated backend status
start_time = time.time()
config_delay = 20  # Time in seconds before the job is marked as "completed"
final_result = None  # Variable to store the final result

@app.route('/status', methods=['GET'])
def status():
    global final_result
    elapsed_time = time.time() - start_time

    # If the delay has passed and the final result is not yet determined, set it
    if elapsed_time > config_delay and final_result is None:
        final_result = random.choice(["completed", "error"])

    # If the delay has passed, return the final result
    if elapsed_time > config_delay:
        result = final_result
    else:
        result = "pending"

    return jsonify({"result": result})

if __name__ == "__main__":
    app.run(debug=True, port=5000)
