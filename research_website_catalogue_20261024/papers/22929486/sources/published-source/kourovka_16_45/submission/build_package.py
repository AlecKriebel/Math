#!/usr/bin/env python3
"""Build deterministic source/Zenodo ZIPs from the frozen publication payload.

No network calls, deposits, releases, or DOI creation. PDF compilation is a
separate step. ZIP entry timestamps and permissions are normalized.
"""
from pathlib import Path
from datetime import date
import hashlib
import json
import zipfile

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "output"
METADATA = json.loads((ROOT / "submission" / "metadata.json").read_text())
VERSION = METADATA["version"]
RELEASE_DATE = date.fromisoformat(METADATA["publication_date"])
FIXED_TIME = (RELEASE_DATE.year, RELEASE_DATE.month, RELEASE_DATE.day, 0, 0, 0)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def archive(path, members):
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for name, data in sorted(members.items()):
            entry = zipfile.ZipInfo(name, FIXED_TIME)
            entry.compress_type = zipfile.ZIP_DEFLATED
            entry.create_system = 3
            entry.external_attr = 0o100644 << 16
            z.writestr(entry, data)


def main():
    OUT.mkdir(exist_ok=True)
    # Enumerated directories keep build outputs and third-party PDFs out.
    names = ["README.md", "Makefile", "proof.tex", "proof.pdf", "progress.json",
             "research_log.md", "CITATION.cff", "LICENSES.md", ".gitignore"]
    names += [str(p.relative_to(ROOT)) for folder in
              ("data", "src", "logs", "references", "audit_2026_09_21",
               "preprint_review_2026_09_23", "submission")
              for p in (ROOT / folder).rglob("*")
              if p.is_file() and "__pycache__" not in p.parts
              and "primary_sources" not in p.parts and p.suffix != ".pyc"
              and not p.name.startswith("input_")
              and p.name not in {"delivery_validation.json", "deployment.json",
                                  "package_replay.log", "release_finalization.md"}]
    # Preserve the original provenance files; only later referee-input snapshots
    # are omitted to keep superseded manuscripts out of the current source ZIP.
    names += [str(p.relative_to(ROOT)) for p in
              (ROOT / "audit_2026_09_21").glob("input_*") if p.is_file()]
    names = sorted(set(names))
    payload = {n: (ROOT / n).read_bytes() for n in names}
    manifest = {"version": VERSION, "scope": "Current source-release payload; excludes manifest and SHA256SUMS themselves",
                "files": [{"path": n, "bytes": len(d), "sha256": digest(d)}
                          for n, d in sorted(payload.items())]}
    (ROOT / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    sums = "".join(f"{digest(d)}  {n}\n" for n, d in sorted(payload.items()))
    (ROOT / "SHA256SUMS").write_text(sums)
    payload["manifest.json"] = (ROOT / "manifest.json").read_bytes()
    payload["SHA256SUMS"] = sums.encode()
    source = OUT / f"Kourovka_16_45_Source_and_Verification_v{VERSION}.zip"
    archive(source, {"kourovka_16_45/" + n: d for n, d in payload.items()})
    pdf_name = f"Kourovka_16_45_Counterexample_v{VERSION}.pdf"
    # Build the kit from an explicit in-memory member map. Never enumerate a
    # persistent output directory: stale files from earlier runs must not enter
    # a later version, and output/zenodo may contain user-edited working files.
    kit = {"upload/" + pdf_name: (ROOT / "proof.pdf").read_bytes(),
           "upload/" + source.name: source.read_bytes()}
    for name in ("UPLOAD_GUIDE.md", "metadata.json", "description.html", "description.txt"):
        kit[name] = (ROOT / "submission" / name).read_bytes()
    for name in ("CITATION.cff", "LICENSES.md"):
        kit[name] = (ROOT / name).read_bytes()
    kit["SHA256SUMS"] = "".join(f"{digest(d)}  {n}\n"
                                 for n, d in sorted(kit.items())).encode()
    archive(OUT / f"Kourovka_16_45_Zenodo_Upload_Kit_v{VERSION}.zip",
            {"Kourovka_16_45_Zenodo_Upload_Kit/" + n: d for n, d in kit.items()})
    print(json.dumps({"status": "PASS", "source_files": len(payload),
                      "source_archive": source.name, "source_sha256": digest(source.read_bytes()),
                      "pdf_sha256": digest((ROOT / "proof.pdf").read_bytes())}, indent=2))


if __name__ == "__main__":
    main()
