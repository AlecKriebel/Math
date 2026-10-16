#!/usr/bin/env python3
"""Supply an invalid lexical alias through a new caller in a copied producer."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import zipfile


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--expect-accepted", action="store_true")
    args = parser.parse_args()
    audit = Path(__file__).resolve().parents[1]
    original_code = (audit / "publication/make_package.py").read_bytes()
    with tempfile.TemporaryDirectory(prefix="alias-regression-", dir=audit / "root_reproduction/.cache") as tmp:
        copy = Path(tmp) / "audit"
        shutil.copytree(audit, copy, ignore=shutil.ignore_patterns(".cache", "qa", "receipts", "package_preflight*"))
        (copy / "ordinary_alias").mkdir()
        script = copy / "publication/make_package.py"
        src = script.read_text()
        needle = '    registry = json.loads(files["SEALS.json"])'
        if src.count(needle) != 1:
            raise RuntimeError("Producer structure changed")
        script.write_text(src.replace(needle, '    add("alias_probe.txt", AUDIT / "ordinary_alias" / ".." / "CURRENT_CORRECTIONS.md")\n' + needle))
        proc = subprocess.run(["/usr/bin/sandbox-exec", "-p", "(version 1) (allow default) (deny network*)",
                               sys.executable, "-B", str(script)], cwd=script.parent,
                              env=dict(os.environ, PYTHONDONTWRITEBYTECODE="1"), capture_output=True, text=True)
        accepted = proc.returncode == 0
        if accepted != args.expect_accepted:
            raise RuntimeError("Unexpected lexical-alias result: " + proc.stderr)
        if not accepted and "Invalid relative path" not in proc.stderr:
            raise RuntimeError("Rejection was unrelated: " + proc.stderr)
        result = {"status": "PASS", "source_guard_sha256": hashlib.sha256(original_code).hexdigest(),
                  "actual_copied_producer_process": True, "guard_body_modified_in_copy": False,
                  "only_new_caller_added_in_copy": True, "lexical_parent_alias_accepted": accepted,
                  "returncode": proc.returncode,
                  "diagnostic": proc.stderr.strip().splitlines()[-1] if proc.stderr else "accepted"}
        if accepted:
            with zipfile.ZipFile(copy / "publication/verification_package.zip") as archive:
                key = "seshadri_counterexample_verification/alias_probe.txt"
                if archive.read(key) != (copy / "CURRENT_CORRECTIONS.md").read_bytes():
                    raise RuntimeError("Aliased payload differs")
                result.update(archive_contains_alias_payload=True, archive_members=len(archive.infolist()))
    if (audit / "publication/make_package.py").read_bytes() != original_code:
        raise RuntimeError("Original producer was changed by control")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
