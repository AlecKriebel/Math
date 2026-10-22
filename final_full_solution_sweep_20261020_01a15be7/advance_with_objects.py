#!/usr/bin/env python3
"""Resume the reviewed exclusion tool after read-only missing-object fetches.

Eligibility decisions remain entirely in advance_clear_exclusions.py. Any
non-object binding problem, missing status, or candidate stops for root review.
"""
import json
from pathlib import Path
import subprocess
from checkpoint import ensure_commit

ROOT=Path(__file__).resolve().parent


def main():
    while True:
        state=json.loads((ROOT/'STATE.json').read_text())
        inventory=json.loads((ROOT/'rest_inventory.json').read_text())
        pr=next((p for p in inventory['pull_requests'] if p['number']==state['next_pr']),None)
        if pr is None:return
        for sha in (pr['baseRefOid'],pr['headRefOid']):ensure_commit(sha)
        result=subprocess.run(['python3',str(ROOT/'advance_clear_exclusions.py')],capture_output=True,text=True)
        print(result.stdout,end='',flush=True)
        if result.returncode:raise RuntimeError(result.stderr)
        after=json.loads((ROOT/'STATE.json').read_text())
        if after['next_pr']==state['next_pr']:return
        following=next((p for p in inventory['pull_requests'] if p['number']==after['next_pr']),None)
        if following is None:return
        missing=any(subprocess.run(['git','cat-file','-e',sha+'^{commit}'],capture_output=True).returncode
                    for sha in (following['baseRefOid'],following['headRefOid']))
        if not missing:return


if __name__=='__main__':main()
