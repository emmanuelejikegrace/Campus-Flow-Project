"""JSON persistence for CampusFlow tickets."""

import json
import os

DEFAULT_PATH = os.path.join("data", "tickets.json")


def load(path=DEFAULT_PATH):
    """Return list of tickets. Missing file -> []. Corrupt -> RuntimeError."""
    if not os.path.exists(path):
        return []
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        raise RuntimeError(
            f"Could not parse {path}: {e}. Refusing to overwrite. "
            "Fix or remove the file and restart."
        )
    if not isinstance(data, list):
        raise RuntimeError(f"{path} must contain a JSON list of tickets.")
    return data


def save(tickets, path=DEFAULT_PATH):
    """Write tickets to disk as pretty JSON."""
    directory = os.path.dirname(path)
    if directory:
        os.makedirs(directory, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(tickets, f, indent=2)