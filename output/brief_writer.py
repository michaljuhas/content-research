import logging
import os
from datetime import datetime, date

logger = logging.getLogger(__name__)


def write(brief_markdown: str, config: dict) -> str:
    """Save the brief to briefs/YYYY-MM-DD.md. Returns the file path."""
    output_cfg = config.get("output", {})
    briefs_dir = output_cfg.get("briefs_dir", "briefs")
    filename_format = output_cfg.get("filename_format", "%Y-%m-%d.md")

    os.makedirs(briefs_dir, exist_ok=True)
    filename = date.today().strftime(filename_format)
    filepath = os.path.join(briefs_dir, filename)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(brief_markdown)

    _append_log(config, filepath)
    return filepath


def _append_log(config: dict, filepath: str) -> None:
    output_cfg = config.get("output", {})
    logs_dir = output_cfg.get("logs_dir", "logs")
    os.makedirs(logs_dir, exist_ok=True)

    log_path = os.path.join(logs_dir, "run.log")
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(log_path, "a", encoding="utf-8") as f:
        f.write(f"{timestamp} — brief written to {filepath}\n")
