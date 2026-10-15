#!/usr/bin/env python3
"""Build standalone source with installed Tectonic; no repository mutation."""
import argparse
from pathlib import Path
import shutil
import subprocess

ROOT = Path(__file__).resolve().parent

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--outdir', default='_runs/pdf')
    args = ap.parse_args()
    out = ROOT/args.outdir
    out.resolve().relative_to(ROOT)
    out.mkdir(parents=True, exist_ok=True)
    executable = shutil.which('tectonic')
    if not executable:
        raise SystemExit('Install Tectonic to rebuild paper.tex. The shipped paper.pdf is already compiled.')
    subprocess.run([executable, '--keep-logs', '--outdir', str(out), str(ROOT/'paper.tex')], cwd=ROOT, check=True)

if __name__ == '__main__':
    main()
