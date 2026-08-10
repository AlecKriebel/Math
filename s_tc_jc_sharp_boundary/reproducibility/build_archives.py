#!/usr/bin/env python3
"""Build deterministic journal source and supplementary-code archives."""
from __future__ import annotations

import hashlib
from pathlib import Path
import zipfile

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "submission"
TIMESTAMP = (2026, 8, 9, 0, 0, 0)


def zip_info(name: str, executable: bool = False) -> zipfile.ZipInfo:
    info = zipfile.ZipInfo(name, TIMESTAMP)
    info.compress_type = zipfile.ZIP_DEFLATED
    mode = 0o100755 if executable else 0o100644
    info.external_attr = mode << 16
    info.create_system = 3
    return info


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def build(path: Path, files: list[tuple[str, Path]], generated: list[tuple[str, bytes]] | None = None) -> None:
    entries: list[tuple[str, bytes, bool]] = []
    for name, source in files:
        entries.append((name, source.read_bytes(), bool(source.stat().st_mode & 0o111)))
    for name, data in generated or []:
        entries.append((name, data, False))
    entries.sort(key=lambda row: row[0])
    checksums = "".join(f"{digest(data)}  {name}\n" for name, data, _ in entries).encode()
    entries.append(("SHA256SUMS.txt", checksums, False))
    with zipfile.ZipFile(path, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for name, data, executable in entries:
            archive.writestr(zip_info(name, executable), data)
    print(f"BUILT {path.name} {digest(path.read_bytes())}")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    build(
        OUT / "Weakly_Tree_Child_Level2_JC_Ambiguity_Source.zip",
        [
            ("source/paper/main.tex", ROOT / "source/paper/main.tex"),
            ("LICENSE-MANUSCRIPT.txt", ROOT / "LICENSE-MANUSCRIPT.txt"),
        ],
        [("README.txt", b"Compile source/paper/main.tex with Tectonic 0.16.0 or a compatible LaTeX installation.\n")],
    )
    build(
        OUT / "Weakly_Tree_Child_Level2_JC_Ambiguity_Reproducibility.zip",
        [
            ("reproducibility/README.md", ROOT / "reproducibility/README.md"),
            ("reproducibility/requirements.txt", ROOT / "reproducibility/requirements.txt"),
            ("reproducibility/networks.json", ROOT / "reproducibility/networks.json"),
            ("reproducibility/verify_primary.py", ROOT / "reproducibility/verify_primary.py"),
            ("reproducibility/verify_math.py", ROOT / "reproducibility/verify_math.py"),
            ("reproducibility/independent/verify_sharpness.py", ROOT / "reproducibility/independent/verify_sharpness.py"),
            ("reproducibility/independent/instance.json", ROOT / "reproducibility/independent/instance.json"),
            ("reproducibility/independent/expected_certificate.json", ROOT / "reproducibility/independent/expected_certificate.json"),
            ("docs/THEOREM_CERTIFICATE_CROSSWALK.md", ROOT / "docs/THEOREM_CERTIFICATE_CROSSWALK.md"),
            ("repair/reviews/SHARPNESS_GATE_REVIEW.md", ROOT / "repair/reviews/SHARPNESS_GATE_REVIEW.md"),
            ("LICENSE-CODE.txt", ROOT / "LICENSE-CODE.txt"),
        ],
        [("README.txt", b"Install reproducibility/requirements.txt, then run: python3 reproducibility/verify_math.py\n")],
    )


if __name__ == "__main__":
    main()
