#!/usr/bin/env python3
"""Capture original program native streams; do not install or edit candidate."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import os
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
PACKET = ROOT.parent/'snapshot'/'problems'/'30001370_basin_boundaries'
CAPTURE = ROOT/'private'/'replays'
CAPTURE.mkdir(parents=True, exist_ok=True)

def utc():
    return datetime.now(timezone.utc).isoformat()

def sha(b):
    return hashlib.sha256(b).hexdigest()

def capture(label, cmd, expected=None):
    start = utc()
    result = subprocess.run(cmd, cwd=CAPTURE, env={**os.environ, 'PYTHONDONTWRITEBYTECODE':'1'}, capture_output=True)
    end = utc()
    (CAPTURE/(label+'.stdout')).write_bytes(result.stdout)
    (CAPTURE/(label+'.stderr')).write_bytes(result.stderr)
    record = dict(label=label, command=cmd, start_utc=start, end_utc=end,
                  exit_code=result.returncode, stdout_bytes=len(result.stdout),
                  stdout_sha256=sha(result.stdout), stderr_bytes=len(result.stderr),
                  stderr_sha256=sha(result.stderr))
    if expected is not None:
        old = expected.read_bytes()
        (CAPTURE/(label+'.expected')).write_bytes(old)
        first = next((i for i,(a,b) in enumerate(zip(old,result.stdout)) if a != b), None)
        if first is None and len(old) != len(result.stdout):
            first = min(len(old),len(result.stdout))
        record['complete_old_byte_comparison'] = {
            'expected_path':str(expected.relative_to(PACKET)), 'expected_bytes':len(old),
            'expected_sha256':sha(old), 'byte_exact':old == result.stdout,
            'first_difference_offset':first,
        }
    (CAPTURE/(label+'.json')).write_text(json.dumps(record,indent=2)+'\n')
    return record

before = {str(p.relative_to(PACKET)):p.read_bytes() for p in PACKET.rglob('*') if p.is_file()}
records = []
scripts = [(f'check_turn_{i}.py', f'TURN_{i}_CHECKS.json') for i in (1,2,3)]
scripts += [('review/check_independent.py','review/INDEPENDENT_CHECKS.json'), ('verify_packet.py',None)]
for name, receipt in scripts:
    records.append(capture('system_'+name.replace('/','_').replace('.py',''),
                           [sys.executable,str(PACKET/name)],PACKET/receipt if receipt else None))
GOOD = '/opt/homebrew/bin/python3.11'
records.append(capture('existing_python_environment',[GOOD,'-c','import sys,sympy; print(sys.version); print(sympy.__version__)']))
for name, receipt in scripts:
    records.append(capture('existing_'+name.replace('/','_').replace('.py',''),
                           [GOOD,str(PACKET/name)],PACKET/receipt if receipt else None))
source_dir = ROOT/'private'/'candidate_source_aliases'
if source_dir.exists():
    records.append(capture('existing_verify_packet_with_sources',
                           [GOOD,str(PACKET/'verify_packet.py'),'--source-dir',str(source_dir)]))
records.append(capture('independent_backward_feedback', [sys.executable,str(ROOT/'public'/'check_backward_feedback.py')]))
after = {str(p.relative_to(PACKET)):p.read_bytes() for p in PACKET.rglob('*') if p.is_file()}
summary = {
    'created_utc':utc(), 'candidate_before_after_full_bytes_unchanged':before == after,
    'candidate_file_count':len(before), 'records':records,
    'scope':'Complete native stdout/stderr and UTC/exit metadata retained privately; failures are retained. Counts are custody evidence, not proof.',
}
(ROOT/'public'/'REPLAY_RECEIPTS.json').write_text(json.dumps(summary,indent=2)+'\n')
print(json.dumps({'records':len(records),'exits':[(r['label'],r['exit_code']) for r in records],
                  'candidate_unchanged':before == after},indent=2))
