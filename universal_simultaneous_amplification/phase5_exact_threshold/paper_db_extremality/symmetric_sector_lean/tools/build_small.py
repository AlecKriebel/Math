#!/usr/bin/env python3
"""Resource-bounded invocation of ordinary Lean/Lake kernel-checked builds."""
import argparse, concurrent.futures, subprocess, time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
p=argparse.ArgumentParser();p.add_argument('--workers',type=int,default=2);p.add_argument('--start',type=int,default=3);p.add_argument('--end',type=int,default=39);a=p.parse_args()
(ROOT/'reports/build_small').mkdir(parents=True,exist_ok=True)
def run(N):
    start=time.monotonic()
    r=subprocess.run(['lake','build',f'SymmetricSector.Small{N:02}'],cwd=ROOT,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    (ROOT/'reports/build_small'/f'N{N:02}.log').write_text(r.stdout)
    print(f'N={N}: {"PASS" if r.returncode==0 else "FAIL"} ({time.monotonic()-start:.1f}s)',flush=True)
    if r.returncode: print(r.stdout[-4000:],flush=True)
    return r.returncode
with concurrent.futures.ThreadPoolExecutor(max_workers=a.workers) as e:
    codes=list(e.map(run,range(a.start,a.end+1)))
raise SystemExit(any(codes))
