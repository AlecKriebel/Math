#!/usr/bin/env python3
"""Check exact publication bytes, then replay frozen scripts with assertions enabled."""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

PACKET_SHA = '767185ee51afce74a4227eb090aa4e896503ddbf186cc236e5deedadb4b51ab2'
AUDIT_SHA = 'aed1a4ef5836440f76c31e73048f4f3378d91d8b3fc1846a05a6d2e460f8df7f'

def require(ok, message):
    if not ok:
        raise RuntimeError(message)

def entry(path):
    b = path.read_bytes()
    return {'bytes': len(b), 'sha256': hashlib.sha256(b).hexdigest()}

def main():
    require(sys.flags.optimize == 0, 'Optimized Python is unsupported; rerun without -O, -OO, or PYTHONOPTIMIZE.')
    root = Path(__file__).resolve().parent
    inventory = {}
    for p in root.rglob('*'):
        require(not p.is_symlink(), 'Symlinks are not permitted: ' + p.relative_to(root).as_posix())
        if p.is_file() and p != root / 'RELEASE_MANIFEST.json':
            inventory[p.relative_to(root).as_posix()] = entry(p)
    manifest = json.loads((root / 'RELEASE_MANIFEST.json').read_text())
    require(manifest['problem_id'] == 30001988, 'Wrong target')
    require(manifest['status'] == 'unsolved' and manifest['turns'] == '5/5', 'Wrong disposition')
    require(manifest['full_target_verified'] is False and manifest['novelty_verified'] is False, 'Overstated disposition')
    require(inventory == manifest['files'], 'Release inventory mismatch')
    require(entry(root / 'packet/SHA256SUMS.json')['sha256'] == PACKET_SHA, 'Wrong author packet')
    require(entry(root / 'audit/BINDING.json')['sha256'] == AUDIT_SHA, 'Wrong independent audit')
    env = os.environ.copy()
    env.pop('PYTHONOPTIMIZE', None)
    env['PYTHONDONTWRITEBYTECODE'] = '1'
    commands = ('verify_audit.py', 'replay_packet.py', 'independent_controls.py')
    results = {}
    for script in commands:
        proc = subprocess.run([sys.executable, '-E', '-B', str(root / 'audit' / script)],
                              cwd=root, env=env, capture_output=True, text=True)
        require(proc.returncode == 0, script + ' failed: ' + proc.stderr)
        result = json.loads(proc.stdout)
        require(result.get('passed') is True, script + ' did not report success')
        results[script] = result
    require(results['replay_packet.py'] == json.loads((root / 'audit/REPLAY_RESULTS.json').read_text()), 'Recorded author replay differs')
    require(results['independent_controls.py'] == json.loads((root / 'audit/INDEPENDENT_RESULTS.json').read_text()), 'Recorded independent controls differ')
    print(json.dumps({'passed': True, 'status': 'unsolved', 'turns': '5/5',
                      'files_verified': len(inventory), 'assertions_enabled': True,
                      'packet_manifest_sha256': PACKET_SHA, 'audit_binding_sha256': AUDIT_SHA,
                      'replays': results}, indent=2))

if __name__ == '__main__':
    main()
