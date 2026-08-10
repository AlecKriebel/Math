#!/usr/bin/env python3
"""Dependency-isolated replay of regressions and exact finite interfaces."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import sys
import unittest


ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / "src"
TESTS = ROOT / "tests"
READ_ONLY_SCOPE = tuple(
    sorted(
        {
            ROOT / "verify_read_only.py",
            ROOT / "README.md",
            ROOT / "STATUS.md",
            ROOT / "CERTIFICATION_REPORT.md",
            ROOT / "RELEASE_ENGINEERING.md",
            ROOT / "RESEARCH_LOG.md",
            *(ROOT / "research_notes").glob("*.md"),
            *SOURCE.glob("*.py"),
            *TESTS.glob("test_*.py"),
        },
        key=lambda path: str(path.relative_to(ROOT)),
    )
)


def _digests() -> dict[str, str]:
    missing = [path for path in READ_ONLY_SCOPE if not path.is_file()]
    if missing:
        names = ", ".join(str(path.relative_to(ROOT)) for path in missing)
        raise RuntimeError(f"required verification files are missing: {names}")
    return {
        str(path.relative_to(ROOT)): hashlib.sha256(path.read_bytes()).hexdigest()
        for path in READ_ONLY_SCOPE
    }


def _scope_digest(digests: dict[str, str]) -> str:
    payload = "".join(f"{name}\0{digests[name]}\n" for name in sorted(digests))
    return hashlib.sha256(payload.encode("ascii")).hexdigest()


def main() -> int:
    if sys.version_info < (3, 10):
        raise RuntimeError("Python 3.10 or newer is required")
    if not sys.flags.isolated:
        raise RuntimeError("run with isolated mode: python3 -I -B verify_read_only.py")

    # Set before loading project modules.  This prevents bytecode cache writes
    # even if the caller omitted -B after adapting this entry point.
    sys.dont_write_bytecode = True
    before = _digests()

    sys.path.insert(0, str(SOURCE))
    suite = unittest.defaultTestLoader.discover(
        start_dir=str(TESTS),
        pattern="test_*.py",
        top_level_dir=str(TESTS),
    )
    result = unittest.TextTestRunner(verbosity=2).run(suite)

    after = _digests()
    changed = sorted(name for name in before if before[name] != after[name])
    if changed:
        raise RuntimeError("verification mutated its read-only scope: " + ", ".join(changed))
    if not result.wasSuccessful():
        return 1

    report = {
        "claim_scope": (
            "generic regressions, exact finite algebra, global support "
            "enumeration, tier geometry, affine feasibility, and structural "
            "phase classifications only; not the analytic physical-time "
            "proofs or T3-2"
        ),
        "files_mutated": False,
        "isolated_python": True,
        "scope_sha256": _scope_digest(after),
        "status": "pass",
        "tests_run": result.testsRun,
    }
    print(json.dumps(report, sort_keys=True, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
