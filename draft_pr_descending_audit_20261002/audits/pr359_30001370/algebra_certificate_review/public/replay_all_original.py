#!/usr/bin/env python3
"""Replay frozen original programs; save complete native streams privately."""
import argparse, hashlib, json, os, subprocess, sys
from datetime import datetime, timezone
from pathlib import Path

def utc():
    return datetime.now(timezone.utc).isoformat()

def main():
    p = argparse.ArgumentParser()
    p.add_argument('--snapshot', type=Path, required=True)
    p.add_argument('--python', required=True)
    p.add_argument('--private-output', type=Path, required=True)
    a = p.parse_args()
    folder = a.snapshot / 'problems/30001370_basin_boundaries'
    a.private_output.mkdir(parents=True, exist_ok=True)
    before = {str(f.relative_to(a.snapshot)): hashlib.sha256(f.read_bytes()).hexdigest()
              for f in a.snapshot.rglob('*') if f.is_file()}
    rows = []
    programs = [(f'check_turn_{k}.py', f'TURN_{k}_CHECKS.json') for k in (1, 2, 3)]
    programs += [('review/check_independent.py', 'review/INDEPENDENT_CHECKS.json'),
                 ('verify_packet.py', None)]
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1')
    for i, (name, receipt) in enumerate(programs, 1):
        cmd = [a.python, '-B', str(folder / name)]
        started = utc()
        result = subprocess.run(cmd, cwd=folder, env=env, capture_output=True)
        finished = utc()
        stem = f'{i:02d}_{Path(name).stem}'
        (a.private_output / (stem + '.stdout')).write_bytes(result.stdout)
        (a.private_output / (stem + '.stderr')).write_bytes(result.stderr)
        expected = (folder / receipt).read_bytes() if receipt else None
        rows.append(dict(program=name, argv=cmd, cwd=str(folder), started_utc=started,
                         finished_utc=finished, exit_code=result.returncode,
                         stdout_bytes=len(result.stdout), stderr_bytes=len(result.stderr),
                         stdout_sha256=hashlib.sha256(result.stdout).hexdigest(),
                         stderr_sha256=hashlib.sha256(result.stderr).hexdigest(),
                         saved_receipt=receipt,
                         stdout_byte_exact=(result.stdout == expected) if expected is not None else None,
                         expected_sha256=hashlib.sha256(expected).hexdigest() if expected else None))
    after = {str(f.relative_to(a.snapshot)): hashlib.sha256(f.read_bytes()).hexdigest()
             for f in a.snapshot.rglob('*') if f.is_file()}
    packet = dict(started_utc=rows[0]['started_utc'], finished_utc=utc(),
                  snapshot_unchanged=(before == after), programs=rows,
                  limitation='Exit success and byte equality verify reproduction only, not the theorem.')
    (a.private_output / 'NATIVE_REPLAY_RECEIPT.json').write_text(json.dumps(packet, indent=2) + '\n')
    print(json.dumps(packet, indent=2))
    return 0 if packet['snapshot_unchanged'] and all(
        r['exit_code'] == 0 and r['stderr_bytes'] == 0 and r['stdout_byte_exact'] is not False
        for r in rows) else 1

if __name__ == '__main__':
    sys.exit(main())
