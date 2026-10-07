#!/usr/bin/env python3
"""Run independently checkable finite tests; leave original audit reports intact."""
import argparse,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
p=argparse.ArgumentParser();p.add_argument('--upstream',action='store_true',help='Also fetch pinned external sections and run NumPy supplementary checks');args=p.parse_args()
commands=[['checks/tsp_reduction_check.py','--output','checks/tsp_reduction_results.json'],['checks/independent_geometry_checks.py'],['checks/source_bridge_audit.py','--finite-only']]
if args.upstream:commands += [['checks/fetch_pinned_sections.py'],['agent_notes/upstream_adversary_checks.py']]
for command in commands:
    r=subprocess.run([sys.executable,*command],cwd=ROOT,capture_output=True,text=True)
    if r.returncode:
        print(r.stdout);print(r.stderr,file=sys.stderr);sys.exit(r.returncode)
    print('PASS '+command[0])
print('Finite checks are supplemental evidence, not an asymptotic proof or Lean certification.')
