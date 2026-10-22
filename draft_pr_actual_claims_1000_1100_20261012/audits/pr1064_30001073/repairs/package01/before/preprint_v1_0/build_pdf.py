#!/usr/bin/env python3
"""Compile the source to a caller-chosen temporary directory; no canonical mutation."""
from pathlib import Path
import argparse, subprocess, shutil, sys
p=argparse.ArgumentParser();p.add_argument('--out-dir',required=True);a=p.parse_args()
root=Path(__file__).resolve().parent;out=Path(a.out_dir).resolve();out.mkdir(parents=True,exist_ok=True)
engine=shutil.which('tectonic')
if engine is None:raise SystemExit('Tectonic required for command-line PDF export')
r=subprocess.run([engine,'--outdir',str(out),str(root/'paper.tex')])
if r.returncode:raise SystemExit(r.returncode)
if not (out/'paper.pdf').is_file():raise SystemExit('PDF export missing')
print(out/'paper.pdf')
