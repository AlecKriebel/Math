#!/usr/bin/env python3
"""Extract the persistent archive and run its bundled fail-closed verifier."""

from __future__ import annotations

import argparse
from pathlib import Path
import subprocess
import sys
import tarfile
import tempfile


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("archive", type=Path)
    args = parser.parse_args()
    archive_path = args.archive.resolve()
    if not archive_path.is_file():
        raise FileNotFoundError(archive_path)
    with tempfile.TemporaryDirectory(prefix="stc-jc-extracted-release-") as temp_name:
        temp = Path(temp_name)
        with tarfile.open(archive_path, "r:gz") as archive:
            root = temp.resolve()
            for member in archive.getmembers():
                destination = (temp / member.name).resolve()
                if destination != root and root not in destination.parents:
                    raise AssertionError(f"unsafe archive member: {member.name}")
            archive.extractall(temp, filter="data")
        release_root = temp / "stc_jc_sharp_boundary_reproducibility"
        verifier = (
            release_root
            / "s_tc_jc_landmark_closure/reproducibility/verify_active_release.py"
        )
        completed = subprocess.run(
            [sys.executable, str(verifier)],
            cwd=release_root,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            check=False,
        )
        print(completed.stdout, end="")
        if completed.returncode != 0:
            raise AssertionError(
                f"extracted active verifier failed: {completed.returncode}"
            )
    print("VERIFIED: extracted persistent archive passes its active verifier")


if __name__ == "__main__":
    main()
