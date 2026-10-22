#!/usr/bin/env python3
"""Reproduce both accepted defects on captured old bytes in disposable scratch."""
import hashlib
import json
import os
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path

WORK = Path(__file__).resolve().parent
AUDIT = WORK.parents[1]
REPO = AUDIT.parents[2]


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def require(test, message):
    if not test:
        raise RuntimeError(message)


def main():
    observations = []
    old_archive = WORK / "before/preprint_v1_0/verification_kit.zip"
    for optimized in [False, True]:
        for fault in ["hardlink-protected-tex", "outside-leaf-symlink"]:
            with tempfile.TemporaryDirectory(prefix="old-defect-", dir=WORK / "tmp") as temp:
                base = Path(temp)
                with zipfile.ZipFile(old_archive) as z:
                    z.extractall(base)
                kit = base / "verification_kit"
                out = base / "alias.zip"
                if fault == "hardlink-protected-tex":
                    target = kit / "preprint.tex"
                    os.link(target, out)
                else:
                    target = base / "sentinel.txt"
                    target.write_text("This old-stage sentinel must not be overwritten.\n")
                    out.symlink_to(target)
                before = sha(target)
                argv = [sys.executable, "-I", "-B"] + (["-O"] if optimized else []) + [str(kit / "build_archive.py"), "--output", str(out)]
                r = subprocess.run(argv, capture_output=True, text=True, timeout=120)
                after = sha(target)
                require(r.returncode == 0 and before != after, "Old defect was not reproduced")
                observations.append({"fault": fault, "optimized": optimized, "argv": argv,
                                     "returncode": r.returncode, "stdout": r.stdout, "stderr": r.stderr,
                                     "target_before_sha256": before, "target_after_sha256": after,
                                     "historical_defect_reproduced": True, "canonical_mutation": False})
    argv = [sys.executable, "-B", str(REPO / "zenodo_deposit_tool/zenodo.py"), "check",
            str(WORK / "before/preprint_v1_0/deposit_metadata.json")]
    r = subprocess.run(argv, cwd=REPO, capture_output=True, text=True, timeout=120)
    require(r.returncode != 0 and "exactly 'metadata' and 'files'" in r.stderr, "Old native-schema defect not reproduced")
    observations.append({"fault": "historical-custom-schema", "argv": argv, "returncode": r.returncode,
                         "stdout": r.stdout, "stderr": r.stderr, "historical_defect_reproduced": True})
    out = {"status": "PASS", "scope": "Accepted defects reproduced only on captured old edition and disposable targets; final current edition separately rejects these aliases and passes local uploader validation.", "observations": observations}
    (WORK / "HISTORICAL_REGRESSION_RESULTS.json").write_text(json.dumps(out, indent=2) + "\n")
    print(json.dumps({"status": "PASS", "historical_defects_reproduced": len(observations)}))


if __name__ == "__main__":
    main()
