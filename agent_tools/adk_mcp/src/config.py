from google.genai import types

def get_retry_config():
    """Returns the standard retry configuration for Gemini models."""
    return types.HttpRetryOptions(
        attempts=5,  # Maximum retry attempts
        exp_base=7,  # Delay multiplier
        initial_delay=1,
        http_status_codes=[429, 500, 503, 504],  # Retry on these HTTP errors
    )
