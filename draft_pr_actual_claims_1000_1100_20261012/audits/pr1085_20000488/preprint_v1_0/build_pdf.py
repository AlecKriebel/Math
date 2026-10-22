#!/usr/bin/env python3
"""Compile a disposable copy of the single-file source with Tectonic."""
import argparse, os, shutil, subprocess, tempfile
from pathlib import Path
from kit_common import ROOT, EPOCH, regular, safe_output, emit, sha, require

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--out-dir", required=True)
    args = parser.parse_args()
    source = regular(ROOT / "paper.tex")
    out = Path(args.out_dir).absolute()
    # Check both directory and every intended child, before ANY write/compiler.
    safe_output(out)
    for name in ["paper.tex", "paper.pdf", "paper.log", "COMPILE_RECEIPT.json"]:
        safe_output(out / name)
    require(not out.exists() or out.is_dir(), "out-dir must be a directory")
    env = dict(os.environ, SOURCE_DATE_EPOCH=EPOCH, FORCE_SOURCE_DATE="1")
    out.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="pr1085-tex-", dir=out) as scratch:
        temp = Path(scratch)
        shutil.copyfile(source, temp / "paper.tex")
        proc = subprocess.run(["tectonic", "--keep-logs", "--outdir", str(temp),
                               str(temp / "paper.tex")], env=env,
                              capture_output=True, text=True)
        require(proc.returncode == 0, "Tectonic failed: " + proc.stderr)
        pdf = regular(temp / "paper.pdf").read_bytes()
        log = regular(temp / "paper.log").read_bytes()
        require(b"Overfull" not in log, "overfull box in compile log")
        (out / "paper.tex").write_bytes(source.read_bytes())
        (out / "paper.pdf").write_bytes(pdf)
        (out / "paper.log").write_bytes(log)
    emit({"passed": True, "engine": "Tectonic", "source_date_epoch": EPOCH,
          "source_sha256": sha(source.read_bytes()), "pdf_sha256": sha(pdf),
          "pdf_bytes": len(pdf), "overfull_boxes": 0,
          "stdout": proc.stdout, "stderr": proc.stderr},
         out / "COMPILE_RECEIPT.json")
if __name__ == "__main__":
    main()
