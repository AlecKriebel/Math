#!/usr/bin/env python3
"""Build the navigation-only verifier capsule supplied with submissions."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import zipfile


PROJECT = Path(__file__).resolve().parents[1]
ZIP_TIME = (2026, 8, 19, 0, 0, 0)
CANONICAL_NAME = "Strong_Tree_Childness_Sharp_Level2_JC_verifier_entrypoints.zip"
ARCHIVE_NAME = "stc_jc_sharp_boundary_atlas_certificates_v1.1.7.tar.gz"
ENVELOPE = PROJECT / "release_artifacts/CERTIFICATE_BUNDLE_ENVELOPE.json"


def digest_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def zip_write(archive: zipfile.ZipFile, name: str, data: bytes, mode: int = 0o100644) -> None:
    info = zipfile.ZipInfo(name, ZIP_TIME)
    info.create_system = 3
    info.external_attr = mode << 16
    info.compress_type = zipfile.ZIP_DEFLATED
    archive.writestr(info, data, compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)


def release_record() -> dict:
    if ENVELOPE.is_file():
        return json.loads(ENVELOPE.read_text(encoding="utf-8"))
    return {
        "archive": ARCHIVE_NAME,
        "archive_sha256": "TO_BE_FILLED_AFTER_FINAL_SEAL",
        "zenodo_doi": "ZENODO_DOI_PENDING",
        "version": "1.1.7",
    }


def readme(record: dict) -> bytes:
    doi = record.get("zenodo_doi", "ZENODO_DOI_PENDING")
    return f"""# Verifier entry points — navigation capsule only

This small ZIP is not the proof archive. It contains the archive identity,
checksum, minimal theorem map, runtime requirements, and a checksum verifier
so a submission reader can locate and authenticate the load-bearing object.

Canonical proof object: `{record['archive']}`
SHA-256: `{record['archive_sha256']}`
Zenodo DOI: `{doi}`

After downloading and extracting the canonical archive, run from its root:

```bash
bash verify.sh quick
bash verify.sh full
bash verify.sh regenerate-all
```

The archive contains the complete finite atlas, every per-relation exact
certificate and transport, restoration and probe records, primitive inputs,
and both primary and separately implemented verifiers. This capsule contains
none of those large proof records and must not be cited as the proof object.
No included script uploads files, creates a DOI, submits a manuscript, or
chooses a license.
""".encode("utf-8")


def archive_verifier(record: dict) -> bytes:
    expected = record["archive_sha256"]
    return f'''#!/usr/bin/env python3
"""Authenticate the downloaded curated proof archive."""
import hashlib
from pathlib import Path
import sys

EXPECTED_NAME = {record["archive"]!r}
EXPECTED_SHA256 = {expected!r}
path = Path(sys.argv[1] if len(sys.argv) > 1 else EXPECTED_NAME)
if path.name != EXPECTED_NAME:
    raise SystemExit(f"expected filename {{EXPECTED_NAME}}, got {{path.name}}")
h = hashlib.sha256()
with path.open("rb") as stream:
    for block in iter(lambda: stream.read(1 << 20), b""):
        h.update(block)
actual = h.hexdigest()
if actual != EXPECTED_SHA256:
    raise SystemExit(f"SHA-256 mismatch: {{actual}}")
print(f"VERIFIED {{path.name}} {{actual}}")
'''.encode("utf-8")


def build(output: Path) -> None:
    record = release_record()
    records: list[tuple[str, bytes, int]] = [
        ("README_FIRST.md", readme(record), 0o100644),
        ("CERTIFICATE_BUNDLE_ENVELOPE.json",
         (json.dumps(record, sort_keys=True, indent=2) + "\n").encode(), 0o100644),
        ("THEOREM_CERTIFICATE_CROSSWALK.md",
         (PROJECT / "THEOREM_CERTIFICATE_CROSSWALK.md").read_bytes(), 0o100644),
        ("RUNTIME_AND_HARDWARE.md",
         (PROJECT / "certificate_bundle/RUNTIME_AND_HARDWARE.md").read_bytes(), 0o100644),
        ("verify_downloaded_archive.py", archive_verifier(record), 0o100755),
    ]
    sums = "".join(f"{digest_bytes(data)}  {name}\n" for name, data, _ in records).encode()
    records.append(("SHA256SUMS", sums, 0o100644))

    output.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED,
                         compresslevel=9) as archive:
        for name, data, mode in records:
            zip_write(archive, name, data, mode)


def main() -> None:
    output = PROJECT / "biorxiv_submission" / CANONICAL_NAME
    build(output)
    print(f"BUILT: {output.relative_to(PROJECT)}")


if __name__ == "__main__":
    main()
