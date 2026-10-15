#!/usr/bin/env python3
"""Capture one unchanged, read-only live gate attempt in a separate owned tree.

This wrapper does not alter the gate or any input. Raw Git/API streams stay in
the attempt's ignored private tree; complete top-level streams and their binding
receipt are public. An unsuccessful attempt is retained rather than normalized.
"""
import argparse
import datetime
import hashlib
import json
import pathlib
import subprocess
import sys

GATE_SHA = '2b613efcc4d41616277c7fd259d1357dbcc69e0aeb4d330efb9618167442a2de'

def bind(path, relative):
    data = path.read_bytes()
    return {'path': relative, 'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()}

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--inputs', required=True)
    parser.add_argument('--own', required=True)
    parser.add_argument('--source-dir', required=True)
    parser.add_argument('--git', required=True)
    parser.add_argument('--gate-code', required=True)
    args = parser.parse_args()
    own = pathlib.Path(args.own)
    public = own / 'public'
    public.mkdir(parents=True, exist_ok=True)
    assert not (public / 'live_attempt_receipt.json').exists(), 'Use a new attempt directory'
    gate = pathlib.Path(args.gate_code)
    assert hashlib.sha256(gate.read_bytes()).hexdigest() == GATE_SHA
    argv = [sys.executable, str(gate), '--inputs', args.inputs, '--own', args.own,
            '--source-dir', args.source_dir, '--git', args.git,
            '--require-exact-api-body', '--require-ready']
    started = datetime.datetime.now(datetime.timezone.utc).isoformat()
    result = subprocess.run(argv, capture_output=True)
    (public / 'final_gate_live.stdout').write_bytes(result.stdout)
    (public / 'final_gate_live.stderr').write_bytes(result.stderr)
    raw = own / 'private' / 'final_gate'
    streams = [bind(p, p.relative_to(own).as_posix()) for p in sorted(raw.rglob('*')) if p.is_file()]
    receipt = {
        'started_utc': started,
        'finished_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'exit': result.returncode,
        'unchanged_gate_sha256': GATE_SHA,
        'command_template': ['python3', 'GATE_CODE', '--inputs', 'INPUT_ROOT', '--own', 'OWN_ATTEMPT',
                             '--source-dir', 'SOURCE_DIR', '--git', 'GIT_LOCATION',
                             '--require-exact-api-body', '--require-ready'],
        'argv_private_paths': argv,
        'complete_top_level_streams': [bind(public / name, 'public/' + name)
                                     for name in ['final_gate_live.stdout', 'final_gate_live.stderr']],
        'raw_private_streams': streams,
        'raw_streams_stay_private': True,
        'permitted_reproduction_differences': ['started_utc', 'finished_utc', 'argv_private_paths',
                                              'gate_receipt.observed_utc'],
        'result': 'PASS' if result.returncode == 0 else 'FAILED_ATTEMPT_PRESERVED',
    }
    (public / 'live_attempt_receipt.json').write_text(json.dumps(receipt, indent=2) + '\n')
    print(json.dumps({'exit': result.returncode, 'result': receipt['result'],
                      'stdout_bytes': len(result.stdout), 'stderr_bytes': len(result.stderr)}, sort_keys=True))
    sys.exit(result.returncode)

if __name__ == '__main__':
    main()
