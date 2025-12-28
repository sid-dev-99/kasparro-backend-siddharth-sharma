import time
import functools
import logging
import random

logger = logging.getLogger(__name__)

def retry_with_backoff(retries: int = 3, backoff_factor: float = 2.0):
    """
    Decorator to retry a function call with exponential backoff.
    
    Args:
        retries: Maximum number of retries.
        backoff_factor: Multiplier for the sleep time.
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            attempt = 0
            current_delay = 1.0 # Start with 1 second
            
            while attempt < retries:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    attempt += 1
                    if attempt >= retries:
                        logger.error(f"Function {func.__name__} failed after {retries} attempts. Error: {e}")
                        raise e
                    
                    sleep_time = current_delay * (1 + random.random() * 0.1) # Add jitter
                    logger.warning(f"Function {func.__name__} failed (Attempt {attempt}/{retries}). Retrying in {sleep_time:.2f}s... Error: {e}")
                    time.sleep(sleep_time)
                    current_delay *= backoff_factor
        return wrapper
    return decorator
