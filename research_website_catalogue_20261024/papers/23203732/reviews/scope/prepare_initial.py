#!/usr/bin/env python3
"""Own initial metadata/hash and ordinary Poppler derivatives; no supplied science."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import stat
import subprocess

A = Path(__file__).resolve().parent
S = A.parents[1] / "sources"


def pin(p):
    b = p.read_bytes()
    return {"path": str(p), "bytes": len(b), "SHA256": hashlib.sha256(b).hexdigest()}


def require(ok, reason):
    if not ok:
        raise RuntimeError(reason)


def main():
    require(pin(S / "SOURCE_READY.json")["SHA256"] == "bd5708d6fa77da017786d34952a3d689b5b5fb2703086bc4d33a1093430ed4cb", "original READY")
    require(pin(S / "SOURCE_READY_SEAL.json")["SHA256"] == "cf9ffb0b5f509af974aa3e7a368c2672e000f2665aecf772a0df57f658145287", "original seal")
    ready = json.loads((S / "SOURCE_READY.json").read_bytes())
    manifest = json.loads((S / "SOURCE_READY_MANIFEST.json").read_bytes())
    terminals = ["SOURCE_READY_MANIFEST.json", "SOURCE_READY_CLOSURE.json", "SOURCE_READY_SEAL.json"]
    files, dirs = [], []
    for p in sorted(S.rglob("*")):
        mode = p.lstat().st_mode
        require(not stat.S_ISLNK(mode), "source symlink")
        if stat.S_ISDIR(mode):
            dirs.append(str(p.relative_to(S)))
        else:
            require(stat.S_ISREG(mode), "source special member")
            files.append(pin(p))
    require(len(files) == 101 and len(manifest["files"]) == 98, "exact101=98payloads+3terminals")
    require(sorted(str(Path(x["path"]).relative_to(S)) for x in files) == sorted([x["path"] for x in manifest["files"]] + terminals), "whole source files")
    require(dirs == manifest["directories"], "whole source directories")
    for x in manifest["files"]:
        q = pin(S / x["path"])
        require(q["bytes"] == x["bytes"] and q["SHA256"] == x["SHA256"], "whole original source payload")
    pdf = Path(ready["selected_actual_PDF"]["path"])
    tex = Path(ready["controlling_TeX"]["extracted_path"])
    require(pin(pdf)["SHA256"] == "d2af46715d94a23d4c51b25a4b78e5e2dab64cd7cae3fa61f2349194e5fc6f75", "actual PDF")
    require(pin(tex)["SHA256"] == "7475979d063f5ad6e9e85f09fca5eca6f1beb83a83f654bc9011854dc8c4182a", "actual TeX")
    require(len(tex.read_bytes().splitlines()) == 198, "complete controlling TeX")
    require(ready["additional_controlling_TeX_sources"] == [] and len(ready["actual_standalone_readers"]) == 1, "no unaccounted manuscript source")
    for item in ready["embedded_PDFs"]:
        require(Path(item["extracted_path"]).read_bytes() == pdf.read_bytes(), "embedded original reader identical to standalone")
    (A / "SOURCE_INPUT_MANIFEST.json").write_text(json.dumps({"UTC": datetime.now(timezone.utc).isoformat(), "source_root": str(S), "complete_source_files": files, "exact_complete_source_directories": dirs, "source_payload_count": 98, "source_complete_files_including_three_exact_terminals": 101, "source_exact_terminals": terminals, "root137_gate": "CLOSED", "prior_record137_scientific_exposure": False}, indent=2) + "\n")
    out = A / "rasters"
    out.mkdir(exist_ok=False)
    receipts = []
    for cmd in [["pdftotext", "-layout", str(pdf), str(A / "published-pdf-text.txt")], ["pdftoppm", "-r", "110", "-f", "1", "-l", "6", "-png", str(pdf), str(out / "page")], ["pdfinfo", str(pdf)]]:
        start = datetime.now(timezone.utc).isoformat()
        result = subprocess.run(cmd, capture_output=True, text=True)
        receipts.append({"command": cmd, "UTC_started": start, "UTC_completed": datetime.now(timezone.utc).isoformat(), "exit_code": result.returncode, "stdout": result.stdout, "stderr": result.stderr})
        require(result.returncode == 0, "ordinary Poppler derivation")
    images = [pin(p) for p in sorted(out.glob("page-*.png"))]
    require(len(images) == 6, "six own fresh individual rasters")
    (A / "MANUSCRIPT_DERIVATION_RECEIPTS.json").write_text(json.dumps({"actual_published_PDF": pin(pdf), "actual_controlling_TeX": pin(tex), "ordinary_Poppler_only_not_scientific_programmes": True, "actual_commands": receipts, "fresh_own_individual_rasters": images}, indent=2) + "\n")
    with (A / "RESEARCH_LOG.md").open("a") as f:
        f.write("\n" + datetime.now(timezone.utc).isoformat() + " —10%: Exact101 source files/98payloads+3controls authenticated without source helper execution. Own full PDF text and six fresh individual rasters generated; full reading/reconstruction is next, before foreign/code/results/opinions. Root137 CLOSED.\n")
    print(json.dumps({"source_files": 101, "source_payloads": 98, "PDF_pages": 6, "TeX_lines": 198, "fresh_rasters": 6, "scientific_programmes_executed": False}))


if __name__ == "__main__":
    main()
