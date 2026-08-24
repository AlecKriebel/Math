#!/usr/bin/env python3
"""Resealed mutations that the outer handoff verifier must reject."""

from __future__ import annotations

import copy
import hashlib
import json
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any, Callable


ROOT = Path(__file__).resolve().parent
MANIFEST = ROOT / "PACKAGE_MANIFEST.json"
VERIFIER = ROOT / "verify_handoff.py"


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()


def reseal(value: dict[str, Any]) -> None:
    value.pop("payload_sha256", None)
    value["payload_sha256"] = hashlib.sha256(canonical(value)).hexdigest()


def first_file(value: dict[str, Any]) -> str:
    return sorted(value["files"])[0]


def main() -> None:
    if not __debug__:
        raise SystemExit("optimized Python is forbidden")
    original = json.loads(MANIFEST.read_text(encoding="utf-8"))
    mutations: list[tuple[str, Callable[[dict[str, Any]], None]]] = [
        ("wrong_file_hash", lambda v: v["files"][first_file(v)].__setitem__("sha256", "0" * 64)),
        ("omitted_file", lambda v: v["files"].pop(first_file(v))),
        ("unsafe_path", lambda v: v["files"].__setitem__("../escape", {"bytes": 0, "sha256": "0" * 64})),
        ("wrong_inner_payload", lambda v: v["inner_manifest"].__setitem__("payload_sha256", "0" * 64)),
        ("false_ready_status", lambda v: v.__setitem__("status", "PASS_WITHOUT_REVIEW")),
    ]
    results = []
    with tempfile.TemporaryDirectory(prefix="k2p-handoff-mutations-") as directory:
        base = Path(directory)
        for name, mutate in mutations:
            value = copy.deepcopy(original)
            mutate(value)
            reseal(value)
            path = base / f"{name}.json"
            path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")
            run = subprocess.run(
                [sys.executable, "-B", str(VERIFIER), "--manifest", str(path)],
                cwd=ROOT,
                capture_output=True,
                text=True,
                check=False,
            )
            if run.returncode == 0:
                raise SystemExit(f"mutation survived: {name}")
            results.append({"mutation": name, "rejected": True})
    optimized = subprocess.run(
        [sys.executable, "-O", str(VERIFIER)],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    if optimized.returncode == 0 or "optimized Python is forbidden" not in optimized.stdout + optimized.stderr:
        raise SystemExit("optimized verifier was not rejected")
    print(json.dumps({
        "status": "PASS",
        "mutations": results,
        "optimized_mode_rejected": True,
    }, sort_keys=True))


if __name__ == "__main__":
    main()

