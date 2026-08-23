#!/usr/bin/env python3
"""Contaminate a disposable source extraction for fail-closed tree tests."""

from __future__ import annotations

import importlib.util
import os
from pathlib import Path
import py_compile
import sys


HELPER = Path(
    "universal_simultaneous_amplification/phase4_landmark_closure/"
    "obstruction/r2_collision_closure/verify_direct_flow_screen.py"
)


def create_timestamp_bytecode(root: Path) -> Path:
    target = root / HELPER
    original = target.read_text(encoding="utf-8")
    original_stat = target.stat()
    old_line = '    """Raised when an explicit certificate check fails."""\n'
    if original.count(old_line) != 1:
        raise RuntimeError("expected helper docstring line not found exactly once")
    statement = '    open("PYCACHE_EXECUTED", "w").close()'
    width = len(old_line.rstrip("\n"))
    if len(statement) > width:
        raise RuntimeError("negative-control statement is unexpectedly too long")
    new_line = statement + " " * (width - len(statement)) + "\n"
    hostile = original.replace(old_line, new_line)
    if len(hostile.encode("utf-8")) != original_stat.st_size:
        raise RuntimeError("hostile source size differs from original")

    temporary = target.with_name(f".{target.name}.negative-control-source")
    temporary.write_text(hostile, encoding="utf-8")
    os.utime(temporary, ns=(original_stat.st_atime_ns, original_stat.st_mtime_ns))
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
        raise RuntimeError("companion source changed while creating hostile bytecode")
    return cache


def main() -> None:
    if len(sys.argv) != 3:
        raise SystemExit(
            "usage: create_tree_negative_control.py "
            "{bytecode,extra-file,extra-dir,symlink,fifo} ROOT"
        )
    mode = sys.argv[1]
    root = Path(sys.argv[2]).resolve(strict=True)
    if mode == "bytecode":
        created = create_timestamp_bytecode(root)
    elif mode == "extra-file":
        created = root / "UNEXPECTED_REGULAR_FILE"
        created.write_text("negative control\n", encoding="ascii")
    elif mode == "extra-dir":
        created = root / "UNEXPECTED_EMPTY_DIRECTORY"
        created.mkdir()
    elif mode == "symlink":
        created = root / "UNEXPECTED_SYMLINK"
        os.symlink("MANIFEST.sha256", created)
    elif mode == "fifo":
        created = root / "UNEXPECTED_FIFO"
        os.mkfifo(created)
    else:
        raise SystemExit(f"unknown negative-control mode: {mode}")
    print(created)


if __name__ == "__main__":
    main()
