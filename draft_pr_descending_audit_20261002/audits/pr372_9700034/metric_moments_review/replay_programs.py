#!/usr/bin/env python3
"""Read-only candidate replay in an audit-private copy; retain complete streams."""
from pathlib import Path
import datetime
import hashlib
import json
import os
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
SNAPSHOT = ROOT.parent / 'snapshot/problems/9700034_sirsn_maximal_routes'
COPY = ROOT / 'private/candidate_copy'
STREAMS = ROOT / 'private/replay_streams'
COPY.parent.mkdir(exist_ok=True)
if not COPY.exists():
    shutil.copytree(SNAPSHOT, COPY)
STREAMS.mkdir(exist_ok=True)
SOURCE = ROOT / 'private/sources'
commands = [(f'check_turn_{i}', [sys.executable, f'check_turn_{i}.py']) for i in range(1, 6)]
commands += [
    ('verify_packet', [sys.executable, 'verify_packet.py']),
    ('verify_packet_sources', [sys.executable, 'verify_packet.py', '--source-dir', str(SOURCE)]),
    ('verify_publication', [sys.executable, 'verify_publication.py']),
    ('verify_publication_sources', [sys.executable, 'verify_publication.py', '--source-dir', str(SOURCE)]),
    ('old_review_independent_check', [sys.executable, 'review/independent_check.py']),
    ('old_review_replay_author', [sys.executable, 'review/replay_author.py', str(COPY)]),
]
env = os.environ.copy()
env['PYTHONHASHSEED'] = '0'
env['PYTHONDONTWRITEBYTECODE'] = '1'
results = []
for name, command in commands:
    start = datetime.datetime.now(datetime.timezone.utc).isoformat()
    run = subprocess.run(command, cwd=COPY, env=env, stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE, timeout=180)
    (STREAMS / f'{name}.stdout').write_bytes(run.stdout)
    (STREAMS / f'{name}.stderr').write_bytes(run.stderr)
    entry = dict(name=name, command=command, cwd=str(COPY), started_utc=start,
                 finished_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                 exit_code=run.returncode, stdout_bytes=len(run.stdout),
                 stderr_bytes=len(run.stderr),
                 stdout_sha256=hashlib.sha256(run.stdout).hexdigest(),
                 stderr_sha256=hashlib.sha256(run.stderr).hexdigest())
    try:
        entry['stdout_json'] = json.loads(run.stdout)
    except json.JSONDecodeError:
        entry['stdout_text'] = run.stdout.decode('utf-8', errors='replace')
    entry['stderr_text'] = run.stderr.decode('utf-8', errors='replace')
    if name.startswith('check_turn_'):
        receipt = COPY / f'TURN_{name.rsplit("_",1)[1]}_CHECKS.json'
        entry['stored_receipt_byte_exact'] = run.stdout == receipt.read_bytes()
    results.append(entry)
    print(json.dumps(entry, sort_keys=True), flush=True)
(ROOT / 'REPLAY_RESULTS.json').write_text(json.dumps(results, indent=2) + '\n')
if any(e['exit_code'] for e in results):
    raise SystemExit(1)
