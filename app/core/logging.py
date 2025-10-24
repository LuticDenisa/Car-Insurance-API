import logging
import structlog


def setup_logging(level: str = "DEBUG"):

    logging.basicConfig(
        level = getattr(logging, level.upper(), logging.DEBUG),
        format = "%(message)s",
    )

    structlog.configure(
        processors = [
            structlog.processors.add_log_level,
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.JSONRenderer(),
        ],
        wrapper_class = structlog.make_filtering_bound_logger(getattr(logging, level.upper(), logging.DEBUG)),
        cache_logger_on_first_use = True,
    )
