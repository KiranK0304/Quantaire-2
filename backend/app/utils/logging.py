"""Logging configuration skeletons."""

import logging


"""Logging configuration."""

import logging


def configure_logging(level: int = logging.INFO) -> None:
    """
    Configure application-wide logging.

    This function should be called exactly once during application startup
    before any business logic executes.

    Args:
        level: Minimum logging level for the application.

    Returns:
        None.
    """
    # Prevent duplicate handlers if called multiple times.
    if logging.getLogger().handlers:
        return

    logging.basicConfig(
        level=level,
        format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )