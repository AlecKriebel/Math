#!/usr/bin/env python3
"""Replay frozen scripts in ignored scratch without modifying source receipts."""
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
from datetime import datetime, timezone

HERE = Path(__file__).resolve().parent
SNAPSHOT = HERE.parent / 'source_snapshot'
ROOT = HERE.parents[3]
SCRATCH = ROOT / 'tmp' / 'pr13_11000263_reproduction' / 'frozen_replay'
FILES = ['AUDIT.md', 'verify.py', 'verification.json',
         'independent_symbolic_check.py', 'independent_symbolic_check.json']

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
    before = {name: sha(SNAPSHOT/name) for name in FILES}
    SCRATCH.mkdir(parents=True, exist_ok=True)
    for name in FILES:
        shutil.copy2(SNAPSHOT/name, SCRATCH/name)
    runs = []
    for script, receipt in [('verify.py', 'verification.json'),
                            ('independent_symbolic_check.py', 'independent_symbolic_check.json')]:
        run = subprocess.run([sys.executable, str(SCRATCH/script)], cwd=SCRATCH,
                             text=True, capture_output=True, check=False)
        stored = (SNAPSHOT/receipt).read_bytes()
        fresh = (SCRATCH/receipt).read_bytes()
        (HERE/(script+'.stdout.txt')).write_text(run.stdout)
        (HERE/(script+'.stderr.txt')).write_text(run.stderr)
        assert run.returncode == 0, (script, run.returncode, run.stderr)
        assert stored == fresh, (receipt, 'byte mismatch')
        runs.append({'script': script, 'returncode': run.returncode,
                     'output_receipt': receipt, 'exact_bytes_match': stored == fresh,
                     'json_semantics_match': json.loads(stored) == json.loads(fresh),
                     'stored_sha256': hashlib.sha256(stored).hexdigest(),
                     'fresh_sha256': hashlib.sha256(fresh).hexdigest(),
                     'stdout_sha256': hashlib.sha256(run.stdout.encode()).hexdigest(),
                     'stderr': run.stderr})
    after = {name: sha(SNAPSHOT/name) for name in FILES}
    assert before == after, 'immutable snapshot changed'
    out = {'status': 'passed', 'timestamp_utc': datetime.now(timezone.utc).isoformat(),
           'frozen_head': '7a845f7e025a24affe1b712cf7ada648570f9c64',
           'python_executable': sys.executable, 'python_version': sys.version,
           'scratch_path': str(SCRATCH), 'source_hashes_before': before,
           'source_hashes_after': after, 'snapshot_unchanged': before == after,
           'runs': runs}
    (HERE/'replay_receipt.json').write_text(json.dumps(out, indent=2)+'\n')
    print(json.dumps(out, indent=2))

if __name__ == '__main__':
    main()
