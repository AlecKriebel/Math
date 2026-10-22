#!/usr/bin/env python3
"""Capture normal, optimized and deliberate false-expectation controls."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys
from datetime import datetime, timezone

BASE = Path(__file__).resolve().parent
REPLAY = BASE/'replays'
REPLAY.mkdir(exist_ok=True)
receipts = []
summaries = []
for optimized in (False, True):
    label = 'optimized' if optimized else 'normal'
    prefix = [sys.executable] + (['-O'] if optimized else [])
    cases = [None,'group_order','gl_commutes','c_fixes_all','one_unipotent_class']
    for control in cases:
        name = label+('-'+control if control else '')
        cmd = prefix+['exact_hessian_audit.py']
        if control:
            cmd += ['--negative-control',control]
        else:
            cmd += ['--output',str(REPLAY/(label+'_data'))]
        start = datetime.now(timezone.utc).isoformat()
        result = subprocess.run(cmd,cwd=BASE,text=True,capture_output=True)
        (REPLAY/(name+'.stdout')).write_text(result.stdout)
        (REPLAY/(name+'.stderr')).write_text(result.stderr)
        correct = result.returncode != 0 if control else result.returncode == 0
        if control:
            correct = correct and 'CHECK FAILED:' in result.stderr
        if not correct:
            raise RuntimeError('Unexpected replay outcome: '+name)
        receipt = {'case':name,'started_utc':start,'argv':cmd,
                   'returncode':result.returncode,'expected_rejection':bool(control),
                   'stdout_sha256':hashlib.sha256(result.stdout.encode()).hexdigest(),
                   'stderr_sha256':hashlib.sha256(result.stderr.encode()).hexdigest(),
                   'last_error_line':result.stderr.strip().splitlines()[-1] if result.stderr else None}
        receipts.append(receipt)
        if not control:
            summaries.append(json.loads(result.stdout))
        print(name+': '+('EXPECTED REJECTION' if control else 'PASS'),flush=True)
if summaries[0] != summaries[1]:
    raise RuntimeError('Normal and optimized results differ')
for name in ('summary.json','elements.json','cyclic_subgroups.json','checks.json'):
    if (REPLAY/'normal_data'/name).read_bytes() != (REPLAY/'optimized_data'/name).read_bytes():
        raise RuntimeError('Normal and optimized artifact differs: '+name)
receipt_data = {'timestamp_utc':datetime.now(timezone.utc).isoformat(),
                'all_expected_outcomes':True,'normal_optimized_artifacts_identical':True,
                'python':sys.version,'runs':receipts}
(BASE/'REPLAY_RECEIPTS.json').write_text(json.dumps(receipt_data,indent=2)+'\n')
print('All ten runs have their expected outcomes; normal and -O artifacts are identical.')
