"""Filesystem path utility skeletons."""

from pathlib import Path


def ensure_directory(path: Path) -> Path:
    """
    Ensure a directory exists for generated artifacts.

    Args:
        path: Directory path that should exist.

    Returns:
        The directory path.
    """
    path = Path(path)
    path.mkdir(parents=True, exist_ok=True)
    return path
