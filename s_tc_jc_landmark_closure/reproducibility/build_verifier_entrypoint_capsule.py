#!/usr/bin/env python3
"""Build the small deterministic verifier-entrypoint ZIP used by submissions.

The capsule makes the executable entry points and theorem map available with
the submission itself.  It is intentionally not a duplicate of the complete
graph/certificate archive; the README directs readers to the immutable public
release for those inputs and the clean-checkout transcripts.
"""

from __future__ import annotations

import hashlib
from pathlib import Path
import zipfile


PROJECT = Path(__file__).resolve().parents[1]
ZIP_TIME = (2026, 8, 17, 0, 0, 0)
RELEASE_TAG = "stc-jc-sharp-boundary-v1.1.3"
CANONICAL_NAME = "Strong_Tree_Childness_Sharp_Level2_JC_verifier_entrypoints.zip"

MEMBERS = (
    "requirements.txt",
    "STATUS.md",
    "FINAL_OUTCOME.json",
    "CLAIM_DEPENDENCY_GRAPH.md",
    "THEOREM_CERTIFICATE_CROSSWALK.md",
    "PERSISTENT_ARCHIVE_CHECKLIST.md",
    "release/PUBLIC_RELEASE_ASSETS.md",
    "reproducibility/bootstrap.sh",
    "reproducibility/verify_quick.sh",
    "reproducibility/verify_full.sh",
    "reproducibility/verify_regenerate_all.sh",
    "reproducibility/verify_active_release.py",
    "reproducibility/verify_extracted_archive.py",
    "reproducibility/verify_public_release.py",
    "reproducibility/verify_submission_source_archives.py",
)


def digest_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def zip_write(archive: zipfile.ZipFile, name: str, data: bytes, mode: int = 0o100644) -> None:
    info = zipfile.ZipInfo(name, ZIP_TIME)
    info.create_system = 3
    info.external_attr = mode << 16
    info.compress_type = zipfile.ZIP_DEFLATED
    archive.writestr(info, data, compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)


def readme() -> bytes:
    return f"""# Exact verifier entry points

This small submission-support capsule exposes the exact commands, Python dependency
lock, active theorem map, and release-provenance checker used for the
manuscript.  Exact PDF replay additionally requires Bash, checksum utilities,
Tectonic 0.16.9 with default bundle v33, and (for the public-download gate)
GitHub CLI `gh`; these tools are not installed by `requirements.txt`.
It is not the complete proof archive: the graph encodings, regenerated
relations, exact polynomial records, and clean-checkout transcripts are too
large and are published as the hash-bound assets of the immutable release:

https://github.com/AlecKriebel/Math/releases/tag/{RELEASE_TAG}

After cloning that tag, run from the monorepository root:

```bash
bash s_tc_jc_landmark_closure/reproducibility/verify_quick.sh
bash s_tc_jc_landmark_closure/reproducibility/verify_full.sh
bash s_tc_jc_landmark_closure/reproducibility/verify_regenerate_all.sh
python s_tc_jc_landmark_closure/reproducibility/verify_public_release.py
```

The last command downloads and verifies the public release assets.  A plain
archive extraction has no Git history, so its fail-closed gate is instead:

```bash
python s_tc_jc_landmark_closure/reproducibility/verify_active_release.py
```

The public verifier also executes the extracted-archive gate automatically.
The
internal `SHA256SUMS` file authenticates every file in this capsule relative
to the submission package's outer manifest.  No script submits a manuscript,
contacts an editor, chooses a license, or creates a DOI.
""".encode("utf-8")


def build(output: Path) -> None:
    records: list[tuple[str, bytes, int]] = [("README.md", readme(), 0o100644)]
    for relative in MEMBERS:
        path = PROJECT / relative
        if not path.is_file():
            raise FileNotFoundError(path)
        mode = 0o100755 if path.suffix == ".sh" else 0o100644
        records.append((relative, path.read_bytes(), mode))
    sums = "".join(
        f"{digest_bytes(data)}  {name}\n" for name, data, _mode in records
    ).encode("utf-8")
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
