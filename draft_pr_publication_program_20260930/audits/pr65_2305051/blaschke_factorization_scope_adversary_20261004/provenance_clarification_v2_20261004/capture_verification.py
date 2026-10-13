#!/usr/bin/env python3
"""Run the new verification and record its actual child PID and streams."""
from pathlib import Path
import datetime
import hashlib
import json
import os
import subprocess
import sys

BASE = Path(__file__).resolve().parent
script = BASE / 'verify_preserved_evidence.py'
argv = [sys.executable, '-E', '-B', str(script)]
started = datetime.datetime.now(datetime.timezone.utc).isoformat()
child = subprocess.Popen(argv, cwd='/Users/alec/Documents/Math', stdout=subprocess.PIPE, stderr=subprocess.PIPE)
actual_pid = child.pid
stdout, stderr = child.communicate()
finished = datetime.datetime.now(datetime.timezone.utc).isoformat()
for name, data in (('verification.stdout.bin', stdout), ('verification.stderr.bin', stderr)):
    (BASE / name).write_bytes(data)
record = {
    'argv': argv,
    'cwd': '/Users/alec/Documents/Math',
    'controller_pid': os.getpid(),
    'actual_child_pid': actual_pid,
    'started_utc': started,
    'finished_utc': finished,
    'exit_code': child.returncode,
    'source_pin': {
        'immutable_head': '5cc1602c05d79502defb07cec7027963149494d2',
        'candidate_sha256': '0a15d03ab92cbd13f17042a4708f75c3d592f4884810c7ffadc6a5f34f1cb6c4',
        'frozen_v1_manifest_sha256': '1c272d87a1b06ed2b3c992a2b47a356ef204998d40da887ef61d4e126dc23f55',
        'root_replay_receipt_sha256': 'a364bf6677ea27664f962d28100670820e0e2fc2f5fc66f3aa985fe476b38d95',
        'executed_script_sha256': hashlib.sha256(script.read_bytes()).hexdigest(),
    },
    'stdout': {'path': 'verification.stdout.bin', 'bytes': len(stdout), 'sha256': hashlib.sha256(stdout).hexdigest()},
    'stderr': {'path': 'verification.stderr.bin', 'bytes': len(stderr), 'sha256': hashlib.sha256(stderr).hexdigest()},
    'scope': 'New read-only preservation/provenance check; no mathematical diagnostic was rerun or extended.',
}
(BASE / 'ACTUAL_VERIFICATION_EXECUTION.json').write_text(json.dumps(record, indent=2) + '\n')
sys.stdout.buffer.write(stdout)
sys.stderr.buffer.write(stderr)
print(json.dumps({'actual_child_pid': actual_pid, 'exit_code': child.returncode}, indent=2))
sys.exit(child.returncode)
