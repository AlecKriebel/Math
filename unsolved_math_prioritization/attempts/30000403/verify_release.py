#!/usr/bin/env python3
"""Verify frozen release bytes and replay all exact controls without a network."""
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import subprocess
import sys
import zipfile

ANCHORS = {
    'AUTHOR_FREEZE.json': '060a5eecbd96bacd4ca3e54efe4b3d309c1eae177980281b47a97dace0894d0b',
    'author-packet.zip': 'c8c844e5d1f5ebbfb180ac025e2cd8aad764297f69ef86f8e3f335e678f25e7e',
    'audit/AUDIT_MANIFEST.json': '6a60fac12ddad8ff6cc8fe113007475fff596ad74ac5b886cc7fecd6cd4b97ef',
    'audit-packet.zip': '44d8fcd62fe05c9704196923861b030bcf752144357d5f055d84c31a854a8172',
}

def require(ok, message):
    if not ok:
        raise RuntimeError(message)

def describe(path):
    raw = path.read_bytes()
    return {'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest()}

def check_archive(root, name, members):
    with zipfile.ZipFile(root / name) as z:
        actual = z.namelist()
        require(len(actual) == len(set(actual)), 'Duplicate ZIP members: ' + name)
        require(set(actual) == set(members), 'Unexpected ZIP inventory: ' + name)
        for member in actual:
            p = PurePosixPath(member)
            require(not p.is_absolute() and '..' not in p.parts, 'Unsafe ZIP member')
            require(z.read(member) == (root / member).read_bytes(), 'ZIP member differs: ' + member)

def main():
    require(sys.flags.optimize == 0, 'Optimized Python is unsupported; remove -O, -OO, and PYTHONOPTIMIZE.')
    root = Path(__file__).resolve().parent
    manifest = json.loads((root / 'RELEASE_MANIFEST.json').read_text())
    require(manifest['problem_id'] == 30000403, 'Wrong target')
    require(manifest['status'] == 'claimed_solved' and manifest['turns'] == '3/5', 'Wrong disposition')
    require(manifest['scope'] == 'optimal universal coarse inner Hurwitz lifting constant in characteristic zero, r >= 3', 'Wrong scope')
    require(manifest['novelty_certified'] is False and manifest['external_human_peer_review'] is False, 'Overstated review or novelty')
    inventory = {}
    for p in root.rglob('*'):
        require(not p.is_symlink(), 'Symlinks are forbidden: ' + p.relative_to(root).as_posix())
        if p.is_file() and p != root / 'RELEASE_MANIFEST.json':
            inventory[p.relative_to(root).as_posix()] = describe(p)
    require(inventory == manifest['files'], 'Release inventory mismatch')
    for name, digest in ANCHORS.items():
        require(describe(root / name)['sha256'] == digest, 'Frozen binding mismatch: ' + name)
    freeze = json.loads((root / 'AUTHOR_FREEZE.json').read_text())
    audit = json.loads((root / 'audit/AUDIT_MANIFEST.json').read_text())
    check_archive(root, 'author-packet.zip', ['AUTHOR_FREEZE.json'] + ['packet/' + f['path'] for f in freeze['files']])
    check_archive(root, 'audit-packet.zip', ['audit/AUDIT_MANIFEST.json'] + ['audit/' + f['path'] for f in audit['audit_files']])
    receipt = json.loads((root / 'AUDIT_RECEIPT.json').read_text())
    require(receipt['verdict'] == 'pass_with_nonblocking_notes', 'Wrong audit verdict')
    require(receipt['audit_zip']['sha256'] == ANCHORS['audit-packet.zip'], 'Wrong audit ZIP receipt')
    require(receipt['audit_manifest'] == describe(root / 'audit/AUDIT_MANIFEST.json'), 'Wrong audit manifest receipt')
    env = os.environ.copy()
    env.pop('PYTHONOPTIMIZE', None)
    env['PYTHONDONTWRITEBYTECODE'] = '1'
    replay = subprocess.run([sys.executable, '-E', '-B', str(root / 'audit/verify_audit.py'), '--author-root', str(root), '--replay'], cwd=root, env=env, capture_output=True, text=True)
    require(replay.returncode == 0, 'Frozen replay failed: ' + replay.stderr)
    result = json.loads(replay.stdout)
    require(result['audit_bindings'] == result['author_bindings'] == 'pass', 'Frozen verification did not pass')
    require(result['author_replays'] == 'byte-identical' and result['independent_replay'] == 'certificate-identical', 'Replay mismatch')
    print(json.dumps({'passed': True, 'problem_id': 30000403, 'status': 'claimed_solved', 'turns': '3/5', 'files_verified': len(inventory), 'archives_exact': True, 'assertions_enabled': True, 'replay': result}, indent=2))

if __name__ == '__main__':
    main()
