#!/usr/bin/env python3
"""Run each submitted outer-ledger mutation separately and retain its reason."""

from __future__ import annotations

import copy
import hashlib
import json
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any, Callable


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()


def reseal(value: dict[str, Any]) -> None:
    value.pop("payload_sha256", None)
    value["payload_sha256"] = hashlib.sha256(canonical(value)).hexdigest()


def main() -> None:
    if len(sys.argv) != 3:
        raise SystemExit("usage: capture_mutation_reasons.py HANDOFF OUTPUT")
    root = Path(sys.argv[1]).resolve()
    output = Path(sys.argv[2]).resolve()
    verifier = root / "verify_handoff.py"
    original = json.loads((root / "PACKAGE_MANIFEST.json").read_text(encoding="utf-8"))
    first = sorted(original["files"])[0]
    mutations: list[tuple[str, str, Callable[[dict[str, Any]], None]]] = [
        (
            "wrong_file_hash",
            "outer file ledger mismatch",
            lambda v: v["files"][first].__setitem__("sha256", "0" * 64),
        ),
        ("omitted_file", "outer file ledger mismatch", lambda v: v["files"].pop(first)),
        (
            "unsafe_path",
            "unsafe manifest path: '../escape'",
            lambda v: v["files"].__setitem__("../escape", {"bytes": 0, "sha256": "0" * 64}),
        ),
        (
            "wrong_inner_payload",
            "outer-to-inner manifest binding mismatch",
            lambda v: v["inner_manifest"].__setitem__("payload_sha256", "0" * 64),
        ),
        (
            "false_ready_status",
            "outer manifest status mismatch",
            lambda v: v.__setitem__("status", "PASS_WITHOUT_REVIEW"),
        ),
    ]
    rows = []
    with tempfile.TemporaryDirectory(prefix="independent-k2p-mutation-reasons-") as temp:
        base = Path(temp)
        for name, expected, mutate in mutations:
            value = copy.deepcopy(original)
            mutate(value)
            reseal(value)
            manifest = base / f"{name}.json"
            manifest.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")
            run = subprocess.run(
                [sys.executable, "-B", str(verifier), "--manifest", str(manifest)],
                cwd=root,
                capture_output=True,
                text=True,
                check=False,
            )
            combined = run.stdout + run.stderr
            rows.append(
                {
                    "mutation": name,
                    "expected_reason": expected,
                    "returncode": run.returncode,
                    "stdout": run.stdout,
                    "stderr": run.stderr,
                    "reason_matched": run.returncode != 0 and expected in combined,
                }
            )
        optimized = subprocess.run(
            [sys.executable, "-O", str(verifier)],
            cwd=root,
            capture_output=True,
            text=True,
            check=False,
        )
        rows.append(
            {
                "mutation": "optimized_python",
                "expected_reason": "optimized Python is forbidden",
                "returncode": optimized.returncode,
                "stdout": optimized.stdout,
                "stderr": optimized.stderr,
                "reason_matched": optimized.returncode != 0
                and "optimized Python is forbidden" in optimized.stdout + optimized.stderr,
            }
        )
    status = "PASS" if all(row["reason_matched"] for row in rows) else "FAIL"
    result = {"schema": "k2p-outer-mutation-reason-audit-v1", "status": status, "results": rows}
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"status": status, "mutations": len(rows), "output": str(output)}, sort_keys=True))
    raise SystemExit(0 if status == "PASS" else 1)


if __name__ == "__main__":
    main()

