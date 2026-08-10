#!/usr/bin/env python3
"""Small deterministic JSON loader for plain or gzip-compressed artifacts."""

from __future__ import annotations

import gzip
import json
from pathlib import Path


def load_json(path: Path):
    if path.suffix == ".gz":
        with gzip.open(path, "rt", encoding="utf-8") as handle:
            return json.load(handle)
    return json.loads(path.read_text())

