import logging
import os

def setup_logging(log_file="logger.log"):
    """Configures logging to file and console."""
    # Clean up previous log
    if os.path.exists(log_file):
        os.remove(log_file)
        print(f"🧹 Cleaned up {log_file}")

    logging.basicConfig(
        filename=log_file,
        level=logging.DEBUG,
        format="%(filename)s:%(lineno)s %(levelname)s:%(message)s",
        force=True # Force reconfiguration
    )
    print(f"✅ Logging configured to {log_file}")

def cleanup_logs(log_files=["logger.log", "web.log", "tunnel.log"]):
    """Removes old log files."""
    for log_file in log_files:
        if os.path.exists(log_file):
            os.remove(log_file)
            print(f"🧹 Cleaned up {log_file}")
