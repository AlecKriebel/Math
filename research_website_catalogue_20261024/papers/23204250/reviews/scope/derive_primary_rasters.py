#!/usr/bin/env python3
"""Explicit ordinary primary-PDF page views only; no supplied science execution."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import subprocess
import sys

A = Path(__file__).resolve().parent


def pin(p):
    b = p.read_bytes()
    return {"path": str(p), "bytes": len(b), "SHA256": hashlib.sha256(b).hexdigest()}


def derive():
    base = A / "primary/shared-raw/primary"
    out = A / "primary/rasters"
    out.mkdir(exist_ok=False)
    items = [("upstream-06", base / "upstream-PDF-hop0.body", 6), ("upstream-07", base / "upstream-PDF-hop0.body", 7), ("upstream-11", base / "upstream-PDF-hop0.body", 11), ("upstream-12", base / "upstream-PDF-hop0.body", 12), ("upstream-18", base / "upstream-PDF-hop0.body", 18), ("upstream-19", base / "upstream-PDF-hop0.body", 19), ("yannakakis-14", base / "Yannakakis-TIFR-PDF-hop0.body", 14), ("lpdwy-published-05", base / "LPDWY-published-PDF-hop0.body", 5)]
    runs = []
    for label, src, page in items:
        command = ["pdftoppm", "-r", "115", "-f", str(page), "-l", str(page), "-singlefile", "-png", str(src), str(out / label)]
        started = datetime.now(timezone.utc).isoformat()
        r = subprocess.run(command, capture_output=True, text=True)
        runs.append({"source": pin(src), "physical_page": page, "actual_command": command, "UTC_started": started, "UTC_completed": datetime.now(timezone.utc).isoformat(), "exit_code": r.returncode, "stdout": r.stdout, "stderr": r.stderr, "output": pin(out / (label + ".png")) if r.returncode == 0 else None})
        if r.returncode:
            raise RuntimeError("ordinary primary page render failed")
    (A / "primary/PRIMARY_RASTER_RECEIPTS.json").write_text(json.dumps({"actual_runs": runs, "ordinary_Poppler_only": True}, indent=2) + "\n")
    print(json.dumps({"fresh_own_primary_rasters": len(runs), "scientific_execution": False, "own_primary_GETs": 0}))


if __name__ == "__main__":
    if sys.argv[1:] != ["--derive"]:
        raise SystemExit("Inert by default; --derive creates ordinary fresh primary page views only")
    derive()
