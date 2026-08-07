# pyrefly: ignore [missing-import]
import structlog
import logging
from app.config import settings

def setup_logging():
    log_level = getattr(logging,settings.LOG_LEVEL.upper(),logging.INFO)

    # Adds up additional details to the logs
    structlog.configure(
        processors = [
            structlog.processors.add_log_level,
            structlog.processors.TimeStamper(fmt='iso'),
            structlog.processors.JSONRenderer()
        ],
        # Passing those logs which are higher than our log level
        wrapper_class = structlog.make_filtering_bound_logger(log_level),
    )