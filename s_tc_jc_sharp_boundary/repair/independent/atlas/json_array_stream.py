#!/usr/bin/env python3
"""Bounded-memory reader for top-level arrays in pretty-printed JSON files.

The atlas assignment files are hundreds of megabytes but their top-level
arrays are formatted with four-space-indented object members.  This helper
uses a read-only mmap and C-level delimiter searches, retaining only one JSON
object at a time.  It intentionally fails if the expected formatting is not
present instead of silently accepting a partial array.
"""

from __future__ import annotations

import json
import mmap
from pathlib import Path
from typing import Iterator


_BETWEEN = b"\n    },\n    {"
_LAST = b"\n    }\n  ]"


def iter_top_level_object_array(path: Path, key: str) -> Iterator[dict]:
    marker = (f'\n  "{key}": [' if key else "").encode("utf-8")
    with path.open("rb") as handle:
        with mmap.mmap(handle.fileno(), 0, access=mmap.ACCESS_READ) as data:
            where = data.find(marker)
            if where < 0:
                raise KeyError(f"top-level array {key!r} not found in {path}")
            start = data.find(b"{", where + len(marker))
            close = data.find(b"]", where + len(marker))
            if close < 0:
                raise ValueError(f"unterminated top-level array {key!r}")
            if start < 0 or close < start:
                return

            last = data.find(_LAST, start)
            if last < 0:
                raise ValueError(f"cannot locate final object in {key!r}")
            while True:
                between = data.find(_BETWEEN, start)
                if 0 <= between < last:
                    end = between + len(b"\n    }")
                    raw = data[start:end]
                    start = between + len(b"\n    },\n    ")
                else:
                    end = last + len(b"\n    }")
                    raw = data[start:end]
                value = json.loads(raw)
                if not isinstance(value, dict):
                    raise TypeError(f"{key!r} member is not an object")
                yield value
                if not (0 <= between < last):
                    break


def top_level_integer(path: Path, key: str) -> int:
    marker = f'\n  "{key}": '.encode("utf-8")
    with path.open("rb") as handle:
        with mmap.mmap(handle.fileno(), 0, access=mmap.ACCESS_READ) as data:
            where = data.find(marker)
            if where < 0:
                raise KeyError(key)
            pos = where + len(marker)
            end = pos
            while end < len(data) and 48 <= data[end] <= 57:
                end += 1
            if end == pos:
                raise ValueError(f"{key!r} is not a nonnegative integer")
            return int(data[pos:end])
