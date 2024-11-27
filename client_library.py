import requests
import time
import logging

class VideoTranslationClient:
    def __init__(self, base_url, max_retries=10, backoff_factor=2, timeout=30):
        self.base_url = base_url
        self.max_retries = max_retries
        self.backoff_factor = backoff_factor
        self.timeout = timeout
        self.completed = False
        self.status = None
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            datefmt='%H:%M:%S'
        )

    def get_status(self):
        retries = 0
        elapsed_time = 0
        if self.completed:
            logging.info(f"Job already finished with {self.status}")
            return self.status
        while elapsed_time <= self.timeout:
            try:
                response = requests.get(f"{self.base_url}/status", timeout=5)
                response.raise_for_status()
                self.status = response.json().get("result")
                if self.status in ["completed", "error"]:
                    self.completed = True
                    logging.info(f"Job completed with status: {self.status}")
                    return self.status
                else:
                    if retries == 0:
                        logging.info(f"Initial status: {self.status}")
                    else:
                        logging.info(f"Retry attempt #{retries}: Current status = {self.status}, Elapsed time = {elapsed_time}s")

                    retries += 1
                    time_remaining = self.timeout - elapsed_time
                    sleep_time = min(self.backoff_factor ** retries, 20, time_remaining)
                    logging.info(f"Sleeping for {sleep_time}s before retry #{retries}. Total elapsed time = {elapsed_time}s")
                    time.sleep(sleep_time)  # Sleep for the backoff duration
                    elapsed_time += sleep_time  # Increment elapsed time after sleeping

            except requests.RequestException as e:
                logging.error(f"Error during request on retry #{retries}: {e}")
                retries += 1
                if retries >= self.max_retries:
                    raise Exception("Max retries reached") from e

        raise TimeoutError(f"Timeout reached after {elapsed_time}s while polling for status")
