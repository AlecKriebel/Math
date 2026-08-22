#!/usr/bin/env python3
"""Create a timestamp-valid hostile pyc beside an unchanged source file."""

from __future__ import annotations

import importlib.util
import os
from pathlib import Path
import py_compile
import sys


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit("usage: build_timestamp_cache_fixture.py TARGET.py")
    target = Path(sys.argv[1]).resolve()
    original = target.read_text(encoding="utf-8")
    original_stat = target.stat()
    old_line = '    """Raised when an explicit certificate check fails."""\n'
    if original.count(old_line) != 1:
        raise RuntimeError("expected class docstring line not found exactly once")
    statement = '    open("PYCACHE_EXECUTED", "w").close()'
    width = len(old_line.rstrip("\n"))
    if len(statement) > width:
        raise RuntimeError("fixture statement is unexpectedly too long")
    new_line = statement + " " * (width - len(statement)) + "\n"
    hostile = original.replace(old_line, new_line)
    if len(hostile.encode("utf-8")) != original_stat.st_size:
        raise RuntimeError("hostile source size differs from original")

    temporary = target.with_name(f".{target.name}.hostile-source")
    temporary.write_text(hostile, encoding="utf-8")
    os.utime(
        temporary,
        ns=(original_stat.st_atime_ns, original_stat.st_mtime_ns),
    )
    cache = Path(importlib.util.cache_from_source(str(target)))
    cache.parent.mkdir(parents=True, exist_ok=True)
    py_compile.compile(
        str(temporary),
        cfile=str(cache),
        dfile=str(target),
        doraise=True,
        invalidation_mode=py_compile.PycInvalidationMode.TIMESTAMP,
    )
    temporary.unlink()
    if target.read_text(encoding="utf-8") != original:
        raise RuntimeError("target source changed while constructing fixture")
    print(cache)


if __name__ == "__main__":
    main()
