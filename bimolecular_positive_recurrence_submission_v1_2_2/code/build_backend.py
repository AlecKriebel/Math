"""Dependency-free PEP 517/660 backend for the standalone verifier."""
from __future__ import annotations

import base64
import csv
import hashlib
import io
from pathlib import Path
import stat
import zipfile

NAME = "bimolecular_pr"
VERSION = "1.2.0"
DIST = f"{NAME}-{VERSION}.dist-info"
WHEEL = f"{NAME}-{VERSION}-py3-none-any.whl"
ROOT = Path(__file__).resolve().parent
WHEEL_TIMESTAMP = (2026, 8, 16, 12, 0, 0)


def _metadata() -> bytes:
    return (
        "Metadata-Version: 2.4\n"
        "Name: bimolecular-pr\n"
        f"Version: {VERSION}\n"
        "Summary: Exact verification utilities for a stochastic reaction-network proof\n"
        "Requires-Python: >=3.11\n"
        "License-Expression: MIT\n"
        "License-File: LICENSE\n"
    ).encode()


def _wheel_header() -> bytes:
    return b"Wheel-Version: 1.0\nGenerator: dependency-free-build-backend\nRoot-Is-Purelib: true\nTag: py3-none-any\n"


def _record(entries: dict[str, bytes]) -> bytes:
    out = io.StringIO()
    writer = csv.writer(out, lineterminator="\n")
    for name, data in entries.items():
        digest = base64.urlsafe_b64encode(hashlib.sha256(data).digest()).rstrip(b"=").decode()
        writer.writerow([name, f"sha256={digest}", len(data)])
    writer.writerow([f"{DIST}/RECORD", "", ""])
    return out.getvalue().encode()


def _zip_info(name: str) -> zipfile.ZipInfo:
    info = zipfile.ZipInfo(name, WHEEL_TIMESTAMP)
    info.create_system = 3
    info.compress_type = zipfile.ZIP_STORED
    info.external_attr = (stat.S_IFREG | 0o644) << 16
    return info


def _write_wheel(wheel_directory: str, editable: bool) -> str:
    entries: dict[str, bytes] = {
        f"{DIST}/METADATA": _metadata(),
        f"{DIST}/WHEEL": _wheel_header(),
        f"{DIST}/licenses/LICENSE": (ROOT / "LICENSE").read_bytes(),
    }
    if editable:
        entries[f"{NAME}.pth"] = (str(ROOT / "src") + "\n").encode()
    else:
        for path in sorted((ROOT / "src" / NAME).glob("*.py")):
            entries[f"{NAME}/{path.name}"] = path.read_bytes()
    entries[f"{DIST}/RECORD"] = _record(entries)
    destination = Path(wheel_directory) / WHEEL
    destination.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(destination, "w", compression=zipfile.ZIP_STORED) as archive:
        for name, data in entries.items():
            archive.writestr(_zip_info(name), data)
    return destination.name


def build_wheel(wheel_directory, config_settings=None, metadata_directory=None):
    return _write_wheel(wheel_directory, editable=False)


def build_editable(wheel_directory, config_settings=None, metadata_directory=None):
    return _write_wheel(wheel_directory, editable=True)


def prepare_metadata_for_build_wheel(metadata_directory, config_settings=None):
    path = Path(metadata_directory) / DIST
    path.mkdir(parents=True, exist_ok=True)
    (path / "METADATA").write_bytes(_metadata())
    (path / "WHEEL").write_bytes(_wheel_header())
    licenses = path / "licenses"
    licenses.mkdir(parents=True, exist_ok=True)
    (licenses / "LICENSE").write_bytes((ROOT / "LICENSE").read_bytes())
    return DIST


def prepare_metadata_for_build_editable(metadata_directory, config_settings=None):
    return prepare_metadata_for_build_wheel(metadata_directory, config_settings)


def get_requires_for_build_wheel(config_settings=None):
    return []


def get_requires_for_build_editable(config_settings=None):
    return []
