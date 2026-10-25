#!/usr/bin/env python3
"""Regression check: stale output files cannot leak into a rebuilt upload kit."""
from pathlib import Path
import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
import zipfile

ROOT = Path(__file__).resolve().parents[1]


def main():
    # The copied source must include this test and all package prerequisites;
    # work takes place outside the canonical certificates and archives.
    with tempfile.TemporaryDirectory(prefix="kourovka-package-test-") as tmp:
        copy = Path(tmp) / "kourovka_16_45"
        shutil.copytree(ROOT, copy, ignore=shutil.ignore_patterns(
            "tmp", "build", "output", "__pycache__", ".git"))
        metadata = json.loads((copy / "submission/metadata.json").read_text())
        version = metadata["version"]
        stale = copy / "output/zenodo/upload/obsolete-upload.txt"
        stale.parent.mkdir(parents=True)
        stale.write_text("This old generated file must never enter the new kit.")
        hashes = []
        for _ in range(2):
            subprocess.run([sys.executable, str(copy / "submission/build_package.py")],
                           check=True, stdout=subprocess.DEVNULL)
            kit = copy / f"output/Kourovka_16_45_Zenodo_Upload_Kit_v{version}.zip"
            hashes.append(hashlib.sha256(kit.read_bytes()).hexdigest())
            with zipfile.ZipFile(kit) as archive:
                names = archive.namelist()
                uploads = [n for n in names if "/upload/" in n]
                if len(uploads) != 2 or any("obsolete" in n for n in names):
                    raise AssertionError("Stale or unexpected upload members")
                prefix = "Kourovka_16_45_Zenodo_Upload_Kit/"
                for line in archive.read(prefix + "SHA256SUMS").decode().splitlines():
                    expected, name = line.split("  ", 1)
                    if hashlib.sha256(archive.read(prefix + name)).hexdigest() != expected:
                        raise AssertionError("Kit checksum mismatch: " + name)
        if hashes[0] != hashes[1]:
            raise AssertionError("Repeated build is not byte-identical")
        if not stale.exists():
            raise AssertionError("Builder altered a pre-existing working file")
        print("PASS: exactly two upload files; stale-file isolation; checksums; deterministic rebuild")


if __name__ == "__main__":
    main()
