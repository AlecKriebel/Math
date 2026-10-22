#!/usr/bin/env python3
"""Mutation tests of this preparation's verifier, confined to disposable copies."""
from pathlib import Path
import datetime as dt
import hashlib
import json
import shutil
import subprocess
import sys

SUPPORT = Path(__file__).resolve().parent
BASE = SUPPORT.parent / "preprint/package_source/birational-cycle-verification"
FIXTURES = SUPPORT / "guard_selftests"


def require(test, message):
    if not test:
        raise RuntimeError(message)


def main():
    FIXTURES.mkdir(exist_ok=True)
    results = []
    for name in ["valid", "missing", "extra", "source_tamper", "symlink",
                 "duplicate_manifest", "traversal_manifest", "expected_result_tamper"]:
        dest = FIXTURES / name
        if dest.exists():
            shutil.rmtree(dest)
        shutil.copytree(BASE, dest)
        if name == "missing":
            (dest / "paper/main.tex").unlink()
        elif name == "extra":
            (dest / "unlisted.txt").write_text("unexpected\n")
        elif name == "source_tamper":
            with (dest / "paper/main.tex").open("a") as f:
                f.write("% deliberate mutation\n")
        elif name == "symlink":
            (dest / "paper/main.tex").unlink()
            (dest / "paper/main.tex").symlink_to(dest / "README.md")
        elif name in ("duplicate_manifest", "traversal_manifest"):
            p = dest / "MANIFEST.json"
            d = json.loads(p.read_text())
            if name == "duplicate_manifest":
                d["files"].append(d["files"][0])
            else:
                d["files"][0]["path"] = "../outside.txt"
            p.write_text(json.dumps(d))
        elif name == "expected_result_tamper":
            p = dest / "expected_checks.json"
            d = json.loads(p.read_text())
            d["exact_checks"] += 1
            p.write_text(json.dumps(d))
            manifest = dest / "MANIFEST.json"
            m = json.loads(manifest.read_text())
            for f in m["files"]:
                if f["path"] == "expected_checks.json":
                    f.update(bytes=p.stat().st_size, sha256=hashlib.sha256(p.read_bytes()).hexdigest())
            manifest.write_text(json.dumps(m))
        for optimized in (False, True):
            cmd = [sys.executable] + (["-O"] if optimized else []) + ["-B", "verify.py"]
            p = subprocess.run(cmd, cwd=dest, capture_output=True, text=True, timeout=30)
            require((p.returncode == 0) == (name == "valid"), "Guard fixture failed: " + name)
            if name == "valid":
                result = json.loads(p.stdout)
                require(result["finite_checks"] == 147619, "Unexpected valid replay count")
            results.append({"fixture": name, "optimized": optimized, "exit_code": p.returncode,
                            "expected": "PASS" if name == "valid" else "REJECT",
                            "result": "PASS"})
    output = {"timestamp_utc": dt.datetime.now(dt.timezone.utc).isoformat(), "status": "PASS",
              "cases": len(results), "results": results,
              "scope": "Local wrapper mutation tests only; no scientific or publication readiness claim"}
    (SUPPORT / "GUARD_TESTS.json").write_text(json.dumps(output, indent=2) + "\n")
    print(json.dumps({"status": "PASS", "cases": len(results)}, indent=2))


if __name__ == "__main__":
    main()
