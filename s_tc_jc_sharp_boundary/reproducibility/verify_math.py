#!/usr/bin/env python3
"""Run the two independent exact mathematical implementations."""
from __future__ import annotations

import hashlib
import os
from pathlib import Path
import subprocess
import sys
import tempfile

HERE = Path(__file__).resolve().parent
SCRIPT_SHA256 = "7cee6cac60e5ce1208ddf601de33914d1f24d298b6248cbdef48fe63f19bcc35"
INSTANCE_SHA256 = "cca38c3928c7eb768f5dabf480d8eae16ef5a08b7576ffe2780e6a7deaeb337b"
CERTIFICATE_SHA256 = "8d70b47f7ca6bd0b8ea87fab71bf2c6eefb254b410708bbb01ccd3dc0c10b40f"


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def run(label: str, command: list[str]) -> str:
    env = os.environ.copy()
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    env["PYTHONHASHSEED"] = "0"
    completed = subprocess.run(
        command,
        cwd=HERE,
        env=env,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    print(completed.stdout, end="")
    if completed.returncode:
        raise SystemExit(f"{label} failed with exit code {completed.returncode}")
    print(f"VERIFIED {label}")
    return completed.stdout


def main() -> None:
    primary = run("primary symbolic implementation", [sys.executable, str(HERE / "verify_primary.py")])
    if "[PROVED] CERTIFICATE COMPLETE" not in primary:
        raise SystemExit("primary verifier did not emit its proved verdict")

    script = HERE / "independent/verify_sharpness.py"
    instance = HERE / "independent/instance.json"
    expected = HERE / "independent/expected_certificate.json"
    locks = ((script, SCRIPT_SHA256), (instance, INSTANCE_SHA256), (expected, CERTIFICATE_SHA256))
    for path, wanted in locks:
        if digest(path) != wanted:
            raise SystemExit(f"independent artifact hash changed: {path.name}")

    with tempfile.TemporaryDirectory(prefix="stc-jc-independent-") as directory:
        generated = Path(directory) / "certificate.json"
        independent = run(
            "independent standard-library implementation",
            [sys.executable, str(script), "--instance", str(instance), "--output", str(generated)],
        )
        if "PASS final_verdict=PROVED" not in independent:
            raise SystemExit("independent verifier did not emit its proved verdict")
        if digest(generated) != CERTIFICATE_SHA256 or generated.read_bytes() != expected.read_bytes():
            raise SystemExit("independent certificate failed exact byte comparison")
    print("VERIFIED: both exact mathematical implementations passed")


if __name__ == "__main__":
    main()
