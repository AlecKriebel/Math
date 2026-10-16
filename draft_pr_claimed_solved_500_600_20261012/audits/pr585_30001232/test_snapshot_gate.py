#!/usr/bin/env python3
"""Actual copied mutations against the acquisition-pinned 18-input gate."""
import hashlib
import json
from pathlib import Path
import shutil
import tempfile
from verify_original_snapshot import verify


def main():
    root = Path(__file__).resolve().parent
    baseline = verify(root)
    before = {p.relative_to(root / "original").as_posix(): p.read_bytes()
              for p in (root / "original").rglob("*") if p.is_file()}
    snapshot = (root / "ORIGINAL_SNAPSHOT.json").read_bytes()
    controls = []
    for mutation in ("changed_original", "missing_original", "extra_original",
                     "changed_and_resealed_snapshot"):
        with tempfile.TemporaryDirectory(prefix="seshadri-snapshot-control-") as tmp:
            copy = Path(tmp)
            shutil.copytree(root / "original", copy / "original")
            (copy / "ORIGINAL_SNAPSHOT.json").write_bytes(snapshot)
            data = json.loads(snapshot)
            record = next(r for r in data["files"] if r["path"].endswith("/author/PROOF.md"))
            target = copy / "original" / record["path"]
            if mutation == "missing_original":
                target.unlink()
            elif mutation == "extra_original":
                (target.parent / "unlisted.txt").write_text("unlisted authored input\n")
            else:
                target.write_bytes(target.read_bytes() + b"\nchanged copied proof\n")
                if mutation == "changed_and_resealed_snapshot":
                    record["size"] = target.stat().st_size
                    record["sha256"] = hashlib.sha256(target.read_bytes()).hexdigest()
                    (copy / "ORIGINAL_SNAPSHOT.json").write_text(json.dumps(data, indent=2)+"\n")
            try:
                verify(copy)
            except (ValueError, OSError):
                controls.append({"mutation": mutation, "rejected": True})
            else:
                raise RuntimeError("Copied mutation was accepted: " + mutation)
    after = {p.relative_to(root / "original").as_posix(): p.read_bytes()
             for p in (root / "original").rglob("*") if p.is_file()}
    if after != before or (root / "ORIGINAL_SNAPSHOT.json").read_bytes() != snapshot:
        raise RuntimeError("Original input changed during controls")
    print(json.dumps({"status": "PASS", "baseline": baseline,
                      "actual_copied_mutations": controls,
                      "originals_unchanged": True}, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
