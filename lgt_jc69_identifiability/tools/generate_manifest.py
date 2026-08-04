#!/usr/bin/env python3
"""Generate a deterministic SHA-256 manifest for all package files except itself."""
from __future__ import annotations

import hashlib
import sys
from pathlib import Path


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for block in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def main(argv: list[str]) -> int:
    root = Path(argv[0] if argv else ".").resolve()
    out = root / "MANIFEST.sha256"
    files = sorted(
        p for p in root.rglob("*")
        if p.is_file()
        and p != out
        and "__pycache__" not in p.parts
        and p.suffix != ".pyc"
    )
    lines = [f"{digest(p)}  ./{p.relative_to(root).as_posix()}" for p in files]
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"WROTE {out} ({len(files)} files)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
