from __future__ import annotations

import os
from datetime import datetime
from pathlib import Path
from typing import Any, Dict

from loguru import logger


SEED: int = 42


def get_project_root() -> Path:
    """Return project root path (directory containing this file's grandparent)."""
    return Path(__file__).resolve().parents[2]


def get_models_dir() -> Path:
    """Return models directory path, creating it if needed."""
    models_dir = get_project_root() / "models"
    models_dir.mkdir(parents=True, exist_ok=True)
    return models_dir


def get_data_dir() -> Path:
    """Return data directory path."""
    return get_project_root() / "data"


def get_timestamp() -> str:
    """Return current timestamp string."""
    return datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")


def configure_logging() -> None:
    """Configure loguru logging."""
    logger.remove()
    logger.add(
        sink=lambda msg: print(msg, end=""),
        level="INFO",
        backtrace=False,
        diagnose=False,
    )

    log_dir = get_project_root() / "logs"
    log_dir.mkdir(exist_ok=True)
    logger.add(
        log_dir / "phishdet.log",
        rotation="1 MB",
        retention="10 files",
        level="INFO",
        backtrace=False,
        diagnose=False,
    )


def save_metadata(metadata: Dict[str, Any]) -> None:
    """Save model metadata JSON next to model file."""
    import json

    models_dir = get_models_dir()
    meta_path = models_dir / "model_metadata.json"
    with meta_path.open("w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2)


def load_metadata() -> Dict[str, Any]:
    """Load model metadata JSON if exists."""
    import json

    models_dir = get_models_dir()
    meta_path = models_dir / "model_metadata.json"
    if not meta_path.exists():
        return {}
    with meta_path.open("r", encoding="utf-8") as f:
        return json.load(f)
