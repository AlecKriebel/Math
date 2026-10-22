#!/usr/bin/env python3
"""Compile the standalone source outside frozen package contents."""
import argparse, os, shutil, subprocess, sys
sys.dont_write_bytecode=True
from pathlib import Path
from package_paths import fresh_output,safe_path
p=argparse.ArgumentParser();p.add_argument('--out',type=Path,required=True);p.add_argument('--tectonic',default='tectonic');a=p.parse_args()
root=Path(__file__).resolve().parents[1];dest=fresh_output(a.out,root)
dest.mkdir()
source=dest/'paper.tex';shutil.copyfile(safe_path(root,'paper.tex'),source)
env=os.environ.copy();env['SOURCE_DATE_EPOCH']='1791936000';env['FORCE_SOURCE_DATE']='1'
proc=subprocess.run([a.tectonic,'--outdir',str(dest),'--keep-logs',str(source)],env=env,text=True,capture_output=True,cwd=dest)
(dest/'compile.stdout.txt').write_text(proc.stdout);(dest/'compile.stderr.txt').write_text(proc.stderr)
print(proc.stdout);print(proc.stderr)
if proc.returncode:raise SystemExit(proc.returncode)
if not (dest/'paper.pdf').is_file():raise SystemExit('Compiler returned success without PDF.')
log=(dest/'paper.log').read_text(errors='replace')
if 'Overfull \\hbox' in log or 'Overfull \\vbox' in log:raise SystemExit('Overfull layout detected.')
print('Standalone PDF compiled; no overfull boxes. SOURCE_DATE_EPOCH=1791936000.')
