#!/usr/bin/env python3
"""Own byte custody and ordinary PDF views only; no supplied scientific execution."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import stat
import subprocess
import sys

A = Path(__file__).resolve().parent
S = A.parents[1] / "sources"


def require(ok, why):
    if not ok:
        raise RuntimeError(why)


def pin(p):
    b = p.read_bytes()
    return {"path": str(p), "bytes": len(b), "SHA256": hashlib.sha256(b).hexdigest()}


def prepare():
    require(pin(S / "SOURCE_READY.json")["SHA256"] == "13d913127abab98d78c3758516884b09f7e4849b5e6c07a3e0fd44c502147ec9", "original READY")
    require(pin(S / "SOURCE_READY_SEAL.json")["SHA256"] == "94bd3bbf71c9fd618b6bf12616120aace2a6d3fe04707d6f73bb1bd787dd8ecf", "original source seal")
    manifest = json.loads((S / "SOURCE_READY_MANIFEST.json").read_bytes())
    ready = json.loads((S / "SOURCE_READY.json").read_bytes())
    terminals = ["SOURCE_READY_CLOSURE.json", "SOURCE_READY_MANIFEST.json", "SOURCE_READY_SEAL.json"]
    files, dirs = [], []
    for p in sorted(S.rglob("*")):
        mode = p.lstat().st_mode
        require(not stat.S_ISLNK(mode), "source symlink")
        if stat.S_ISDIR(mode):
            dirs.append(p.relative_to(S).as_posix())
        else:
            require(stat.S_ISREG(mode), "source special file")
            files.append(pin(p))
    require(len(files) == 104 and len(manifest["files"]) == 101 and len(dirs) == 13, "104=101+3 source files/13dirs")
    require(sorted(Path(f["path"]).relative_to(S).as_posix() for f in files) == sorted([f["path"] for f in manifest["files"]] + terminals), "complete exact source namespace")
    require(dirs == manifest["directories"], "complete source directories")
    for entry in manifest["files"]:
        p = pin(S / entry["path"])
        require(p["bytes"] == entry["bytes"] and p["SHA256"] == entry["SHA256"], "whole original payload")
    pdf = Path(ready["selected_actual_PDF"]["path"])
    tex = Path(ready["controlling_TeX"]["extracted_path"])
    require(pin(pdf)["SHA256"] == "9b1b56f516183c309b5510422c51b9b7050660384101f592251f1265c1d38a72", "actual original PDF")
    require(pin(tex)["SHA256"] == "97917390b62c13412f4e5734c3e64e654033f5ca4b8ef05d683b9067ea7e17ea" and len(tex.read_bytes().splitlines()) == 189, "all189 controlling TeX lines")
    require(ready["additional_controlling_TeX_sources"] == [] and len(ready["actual_standalone_readers"]) == 1 and ready["embedded_PDFs"] == [], "complete actual controlling manuscripts")
    (A / "SOURCE_INPUT_MANIFEST.json").write_text(json.dumps({"UTC": datetime.now(timezone.utc).isoformat(), "source_root": str(S), "complete_source_files": files, "exact_complete_source_directories": dirs, "source_payload_count": 101, "source_complete_files_including_three_exact_terminals": 104, "source_exact_terminals": terminals, "root139_gate": "CLOSED", "prior_record139_scientific_exposure": False}, indent=2) + "\n")
    (A / "rasters").mkdir(exist_ok=False)
    runs = []
    for command in [["pdftotext", "-layout", str(pdf), str(A / "published-pdf-text.txt")], ["pdftoppm", "-r", "110", "-f", "1", "-l", "6", "-png", str(pdf), str(A / "rasters/page")], ["pdfinfo", str(pdf)]]:
        started = datetime.now(timezone.utc).isoformat()
        r = subprocess.run(command, capture_output=True, text=True)
        runs.append({"actual_command": command, "UTC_started": started, "UTC_completed": datetime.now(timezone.utc).isoformat(), "exit_code": r.returncode, "stdout": r.stdout, "stderr": r.stderr})
        require(r.returncode == 0, "ordinary Poppler derivation")
    images = [pin(p) for p in sorted((A / "rasters").glob("page-*.png"))]
    require(len(images) == 6, "six own fresh individual rasters")
    (A / "MANUSCRIPT_DERIVATION_RECEIPTS.json").write_text(json.dumps({"actual_PDF": pin(pdf), "actual_controlling_TeX": pin(tex), "actual_ordinary_Poppler_runs": runs, "fresh_own_rasters": images, "scientific_programmes_executed": []}, indent=2) + "\n")
    with (A / "RESEARCH_LOG.md").open("a") as f:
        f.write("\n" + datetime.now(timezone.utc).isoformat() + " —10%: Complete104 original source files/13dirs authenticated; six fresh own PDF page rasters and full text derivative generated. Full6PDF/189TeX/6rasters reading and independent analytic reconstruction next. No native scientific code/results/archived/opinions/foreign exposure. Root139 CLOSED.\n")
    print(json.dumps({"source_files": 104, "source_directories": 13, "PDF_pages": 6, "controlling_TeX_lines": 189, "fresh_rasters": 6, "scientific_execution": False, "root139_gate": "CLOSED"}))


if __name__ == "__main__":
    if sys.argv[1:] != ["--prepare"]:
        raise SystemExit("Inert by default; --prepare creates own ordinary manuscript views only")
    prepare()
