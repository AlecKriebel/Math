#!/usr/bin/env python3
"""Integrity/replay controls only; not an analytic proof certificate."""
import hashlib
import json
import pathlib
import shutil
import subprocess
import sys
import tempfile

PINS = {
    'public_packet/MANIFEST.json': '7ef81a33a9b5d235039cd0d8cee912d23f6fa3bb1e4f67a5e2217ef8c5e1e650',
    'independent_audit/AUDIT_MANIFEST.json': '87128f21837939279b70fcd50c115713f37a5e0d5c7ef13d0dfb7b8926710b1b',
    'independent_audit/INDEPENDENT_AUDIT.md': 'b761d276cf0af8e8c1a2561db4b7f8b5c07eff98cba43d510fbf631be85454c6',
}

def require(condition, message):
    if not condition:
        raise ValueError(message)

def digest(data):
    return hashlib.sha256(data).hexdigest()

def inventory(root, manifest_name):
    manifest = json.loads((root / manifest_name).read_bytes())
    require(manifest['schema'] == 'sha256-file-inventory-v1', 'manifest schema')
    expected = {manifest_name}
    for record in manifest['files']:
        name = record['path']
        p = pathlib.PurePosixPath(name)
        require(not p.is_absolute() and '..' not in p.parts and str(p) == name,
                'unsafe manifest path')
        require(name not in expected, 'duplicate manifest path')
        expected.add(name)
    found = set()
    for p in root.rglob('*'):
        require(not p.is_symlink(), 'symlink')
        if p.is_file():
            found.add(p.relative_to(root).as_posix())
        else:
            require(p.is_dir(), 'special filesystem node')
    require(found == expected, 'inventory mismatch')
    for record in manifest['files']:
        data = (root / record['path']).read_bytes()
        require(len(data) == record['bytes'] and digest(data) == record['sha256'],
                'hash mismatch: ' + record['path'])
    return len(found)

def verify(root, replay=True):
    for name, sha in PINS.items():
        require(digest((root / name).read_bytes()) == sha, 'pinned input mismatch')
    total = inventory(root, 'RELEASE_MANIFEST.json')
    author_files = inventory(root / 'public_packet', 'MANIFEST.json')
    audit_files = inventory(root / 'independent_audit', 'AUDIT_MANIFEST.json')
    result = {'release_files': total, 'author_files': author_files, 'audit_files': audit_files,
              'scope': 'integrity and finite diagnostics only; no analytic proof certification'}
    if not replay:
        return result
    modes = {}
    for label, flags in [('normal', []), ('optimized', ['-O'])]:
        prefix = [sys.executable, '-B'] + flags
        outputs = []
        for folder, script, frozen in [
                ('public_packet', 'controls.py', 'CONTROL_RESULTS.json'),
                ('independent_audit', 'independent_controls.py', 'INDEPENDENT_CONTROL_RESULTS.json')]:
            base = root / folder
            out = subprocess.check_output(prefix + [str(base / script)], cwd=root)
            require(out == (base / frozen).read_bytes(), 'direct replay mismatch')
            outputs.append(json.loads(out))
        out = subprocess.check_output(prefix + [str(root / 'public_packet/verify_packet.py'), '--self-test'], cwd=root)
        check = json.loads(out)
        require(len(check['negative_controls']) == 7 and
                set(check['negative_controls'].values()) == {'rejected'}, 'author corruption controls')
        modes[label] = {'author_assertions': outputs[0]['assertions'],
                        'independent_diagnostics': outputs[1]['passed_checks'],
                        'author_corruption_controls_rejected': 7,
                        'direct_replay_outputs_byte_match': True}
    result['modes'] = modes
    return result

def selftest(root):
    def inner_manifest(p):
        file = p / 'public_packet/MANIFEST.json'
        file.write_bytes(file.read_bytes() + b' ')
    changes = [
        ('changed_author', lambda p: (p / 'public_packet/README.md').write_bytes(b'changed')),
        ('changed_audit', lambda p: (p / 'independent_audit/INDEPENDENT_AUDIT.md').write_bytes(b'changed')),
        ('missing', lambda p: (p / 'README.md').unlink()),
        ('extra', lambda p: (p / 'extra.txt').write_bytes(b'extra')),
        ('nested_extra', lambda p: (p / 'independent_audit/extra.txt').write_bytes(b'extra')),
        ('symlink', lambda p: (p / 'link').symlink_to(p / 'README.md')),
        ('pinned_manifest', inner_manifest),
        ('manifest_traversal', lambda p: (p / 'RELEASE_MANIFEST.json').write_text(json.dumps(
            {'schema': 'sha256-file-inventory-v1', 'files': [{'path': '../escape'}]}))),
        ('manifest_duplicate', lambda p: (p / 'RELEASE_MANIFEST.json').write_text(json.dumps(
            {'schema': 'sha256-file-inventory-v1', 'files': [{'path': 'RELEASE_MANIFEST.json'}]}))),
    ]
    results = {}
    for name, change in changes:
        with tempfile.TemporaryDirectory(prefix='polyhedra-release-control-') as d:
            p = pathlib.Path(d) / 'packet'
            shutil.copytree(root, p)
            change(p)
            try:
                verify(p, replay=False)
            except (ValueError, KeyError, FileNotFoundError):
                results[name] = 'rejected'
            else:
                raise RuntimeError('negative control accepted: ' + name)
    return results

if __name__ == '__main__':
    root = pathlib.Path(__file__).resolve().parent
    result = verify(root)
    if '--self-test' in sys.argv:
        result['release_corruption_controls'] = selftest(root)
    print(json.dumps(result, indent=2, sort_keys=True))
