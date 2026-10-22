#!/usr/bin/env python3
"""Adversarial verifier controls in this packet's own disposable fixture only."""
import datetime
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import shutil
import sys
import tempfile

BASE = Path(__file__).absolute().parent
spec = importlib.util.spec_from_file_location("custody", BASE / "verify_custody.py")
custody = importlib.util.module_from_spec(spec)
spec.loader.exec_module(custody)


def main():
    scratch = BASE / "ownignoredscratch"
    if scratch.is_symlink():
        raise ValueError("scratch cannot be a symlink")
    scratch.mkdir(exist_ok=True)
    results = []
    try:
        with tempfile.TemporaryDirectory(dir=scratch, prefix="custody-") as tmp:
            root = Path(tmp)
            def reset():
                for p in list(root.iterdir()):
                    if p.is_dir() and not p.is_symlink():
                        shutil.rmtree(p)
                    else:
                        p.unlink()
                (root / ".hidden").write_bytes(b"hidden\n")
                (root / "evidence").write_bytes(b"authored\n")
                files = [{"path": p.name, "bytes": len(p.read_bytes()),
                          "sha256": hashlib.sha256(p.read_bytes()).hexdigest()}
                         for p in sorted(root.iterdir())]
                manifest = {"schema": "exact-recursive-authored-inventory-v1", "files": files,
                            "sealed_at_utc": datetime.datetime.now(datetime.timezone.utc).isoformat()}
                raw = (json.dumps(manifest, sort_keys=True) + "\n").encode()
                (root / "MANIFEST.json").write_bytes(raw)
                return hashlib.sha256(raw).hexdigest()
            pinned = reset()
            if custody.verify(root, pinned).get("files") != 2:
                raise ValueError("positive fixture failed")
            results.append({"case": "exact_hidden_inventory", "result": "PASS"})
            controls = [
                ("wrong_external_pin", lambda: None, "0" * 64),
                ("extra_hidden_file", lambda: (root / ".extra").write_bytes(b"extra"), None),
                ("missing_file", lambda: (root / "evidence").unlink(), None),
                ("altered_bytes", lambda: (root / "evidence").write_bytes(b"changed"), None),
                ("rewritten_manifest", lambda: (root / "MANIFEST.json").write_bytes(b"{}"), None),
                ("symlink", lambda: (root / "link").symlink_to("/dev/null"), None),
                ("special_fifo", lambda: os.mkfifo(root / "fifo"), None),
                ("empty_directory", lambda: (root / "empty").mkdir(), None),
            ]
            for label, mutate, substitute in controls:
                pinned = reset()
                mutate()
                try:
                    custody.verify(root, substitute or pinned)
                except (OSError, ValueError, TypeError, KeyError):
                    results.append({"case": label, "result": "REJECTED"})
                else:
                    raise ValueError("accepted negative fixture: " + label)
    finally:
        if scratch.exists() and not any(scratch.iterdir()):
            scratch.rmdir()
    print(json.dumps({"status": "PASS", "controls": results,
                      "scratch_cleaned": not scratch.exists()}, indent=2, sort_keys=True))


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError, TypeError, KeyError) as error:
        print(json.dumps({"status": "FAIL", "error": str(error)}))
        sys.exit(1)
