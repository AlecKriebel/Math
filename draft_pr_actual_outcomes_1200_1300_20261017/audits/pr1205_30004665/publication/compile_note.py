#!/usr/bin/env python3
"""Compile the note with the available Homebrew Tectonic, recording provenance."""
from pathlib import Path
import datetime
import hashlib
import json
import os
import shutil
import subprocess

ROOT = Path(__file__).resolve().parent
PROGRAM = ROOT.parents[2]

def main():
    compiler = shutil.which("tectonic")
    if not compiler:
        raise RuntimeError("Install Tectonic or use the saved TeX project compiler")
    version = subprocess.check_output([compiler, "--version"], text=True).strip()
    out = ROOT / "output/pdf"
    out.mkdir(parents=True, exist_ok=True)
    env = dict(os.environ, XDG_CACHE_HOME=str(PROGRAM / "_local/texcache"))
    result = subprocess.run([compiler, "--keep-logs", "--outdir", str(out),
                             str(ROOT / "manuscript/main.tex")],
                            capture_output=True, text=True, env=env)
    (ROOT / "COMPILE_STDOUT.txt").write_text(result.stdout)
    (ROOT / "COMPILE_STDERR.txt").write_text(result.stderr)
    if result.returncode:
        raise RuntimeError(result.stderr)
    receipt = {"at_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
               "compiler": str(Path(compiler).resolve()), "version": version,
               "compiler_sha256": hashlib.sha256(Path(compiler).read_bytes()).hexdigest(),
               "source_sha256": hashlib.sha256((ROOT / "manuscript/main.tex").read_bytes()).hexdigest(),
               "pdf_sha256": hashlib.sha256((out / "main.pdf").read_bytes()).hexdigest(),
               "returncode": result.returncode}
    (ROOT / "COMPILE_RECEIPT.json").write_text(json.dumps(receipt, indent=2) + "\n")
    print(json.dumps(receipt, indent=2))

if __name__ == "__main__":
    main()
