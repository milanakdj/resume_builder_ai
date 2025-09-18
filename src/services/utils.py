
from functools import wraps
import requests
import time
import random



def retry_with_backoff(max_retries=3, backoff_seconds=1):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except requests.Timeout as e:
                    # Raise immediately on timeout
                    raise Exception(f"API request failed due to: {e}")

                except Exception as e:
                    last_exception = e
                    wait = backoff_seconds * (2 * attempt) + random.uniform(0, 0.1)
                    print(f"Retry {attempt + 1} failed: {e} - retrying in {wait:.2f}s")
                    time.sleep(wait)

            raise Exception(f"API request failed after {max_retries} retries: {last_exception}")

        return wrapper

    return decorator