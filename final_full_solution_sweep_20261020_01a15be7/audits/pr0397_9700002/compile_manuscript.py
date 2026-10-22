#!/usr/bin/env python3
"""Build this manuscript and render fresh pages for required visual inspection."""
import argparse
import datetime as dt
import hashlib
import os
from pathlib import Path
import subprocess
import sys

AUDIT = Path(__file__).resolve().parent
EFFORT = AUDIT.parents[1]
sys.path.insert(0, str(EFFORT))
from sweep_io import atomic_json

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--qa-directory", required=True)
args = parser.parse_args()
q = AUDIT / "preprint"
src, build = q / "main.tex", q / "build"
before = hashlib.sha256(src.read_bytes()).hexdigest()
env = dict(os.environ, TECTONIC_CACHE_DIR=str(EFFORT / "private/tectonic-0.17.0/cache"))
cmd = [str(EFFORT / "private/tectonic-0.17.0/tectonic"), "--keep-logs",
       "--keep-intermediates", "--outdir", str(build), str(src)]
run = subprocess.run(cmd, capture_output=True, text=True, env=env)
(build / "compiler_stdout.txt").write_text(run.stdout)
(build / "compiler_stderr.txt").write_text(run.stderr)
if run.returncode:
    raise RuntimeError(run.stderr)
pdf = build / "main.pdf"
receipt = {"timestamp": dt.datetime.now(dt.timezone.utc).isoformat(),
           "returncode": run.returncode, "source_sha256": before,
           "source_unchanged": hashlib.sha256(src.read_bytes()).hexdigest() == before,
           "compiler": "Tectonic0.17.0 official digest-verified local runtime",
           "cache_directory": env["TECTONIC_CACHE_DIR"], "command": cmd,
           "stderr_tail": run.stderr[-2000:], "pdf_bytes": pdf.stat().st_size,
           "pdf_sha256": hashlib.sha256(pdf.read_bytes()).hexdigest()}
atomic_json(build / "BUILD_RECEIPT.json", receipt)
out = q / args.qa_directory
if Path(args.qa_directory).name != args.qa_directory:
    raise RuntimeError("QA directory must be a simple new child name")
out.mkdir(exist_ok=False)
subprocess.run(["pdftoppm", "-scale-to", "1500", "-png", str(pdf), str(out / "page")],
               check=True)
print(receipt)
print(subprocess.check_output(["pdfinfo", str(pdf)], text=True))
print("PAGES", [str(f) for f in sorted(out.glob("page-*.png"))])
print("WARNINGS", [s for s in (build / "main.log").read_text().splitlines()
                   if "Overfull" in s or "Underfull" in s or "undefined" in s.lower()])
