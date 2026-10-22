#!/usr/bin/env python3
"""Anchored, source-free byte gate and exact algebra replays; not a proof assistant."""
import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import stat
import subprocess
import sys
import tempfile
import zipfile

ROOT = Path(__file__).resolve().parent
ARCHIVES = {
    'AUTHOR_FREEZE.zip': ('author', 14746, '2257767b04521b39bc59ccd62bfc03321d0ec87d81532b35d09d0d98bc263670'),
    'AUDIT_FREEZE.zip': ('audit', 21275, 'ee4c85b685e93ca46baa8008514dfb124ce6ad80f37d8b18f791c4c5a66a539a'),
}
INNER = {
    'author/AUTHOR_MANIFEST.json': '94982f8c61b72fb17ee09af7b4217a438ec324e87096750a7c40a4f335e955f3',
    'audit/AUDIT_MANIFEST.json': '39d0eec936e7b6e3782e28034120dc399190eec3a4802ffb0964982a6367f0c6',
}

def require(ok, message):
    if not ok:
        raise RuntimeError(message)

def digest(data):
    return {'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()}

def safe(name):
    p = PurePosixPath(name)
    require(isinstance(name, str) and not p.is_absolute() and '..' not in p.parts
            and str(p) == name and name != '.' and '\\' not in name, 'Unsafe path')

def verify(anchor):
    require(ROOT.is_dir() and not ROOT.is_symlink(), 'Invalid packet root')
    manifest_path = ROOT / 'PUBLIC_MANIFEST.json'
    require(stat.S_ISREG(manifest_path.lstat().st_mode), 'Manifest must be regular')
    raw = manifest_path.read_bytes()
    require(hashlib.sha256(raw).hexdigest() == anchor, 'External manifest anchor mismatch')
    manifest = json.loads(raw)
    require(manifest['problem_id'] == 30005994 and manifest['status'] == 'unsolved'
            and manifest['turns'] == '5/5' and manifest['mathematical_changes'] == 0, 'Disposition mismatch')
    require('PUBLIC_MANIFEST.json' not in manifest['files'], 'Self-manifest entry')
    expected = set(manifest['files']) | {'PUBLIC_MANIFEST.json'}
    expected_dirs = set()
    for name in expected:
        safe(name)
        expected_dirs.update(str(p) for p in PurePosixPath(name).parents if str(p) != '.')
    files, dirs = set(), set()
    for path in ROOT.rglob('*'):
        name = path.relative_to(ROOT).as_posix()
        mode = path.lstat().st_mode
        if stat.S_ISREG(mode):
            files.add(name)
        elif stat.S_ISDIR(mode):
            dirs.add(name)
        else:
            raise RuntimeError('Nonregular or linked member: ' + name)
    require(files == expected and dirs == expected_dirs, 'Packet inventory mismatch')
    for name, meta in manifest['files'].items():
        require(digest((ROOT / name).read_bytes()) == meta, 'Payload mismatch: ' + name)
    for name, sha in INNER.items():
        require(digest((ROOT / name).read_bytes())['sha256'] == sha, 'Frozen manifest mismatch')
    for name, (directory, size, sha) in ARCHIVES.items():
        require(digest((ROOT / name).read_bytes()) == {'bytes': size, 'sha256': sha}, 'Frozen archive mismatch')
        wanted = {p.name for p in (ROOT / directory).iterdir()}
        with zipfile.ZipFile(ROOT / name) as z:
            members = z.infolist()
            names = [i.filename for i in members]
            require(len(names) == len(set(names)) and set(names) == wanted and not z.comment, 'Archive inventory mismatch')
            for info in members:
                safe(info.filename)
                require('/' not in info.filename and not info.is_dir() and not info.flag_bits & 1, 'Unsafe archive member')
                require(stat.S_IFMT(info.external_attr >> 16) in (0, stat.S_IFREG), 'Nonregular archive member')
                require(z.read(info) == (ROOT / directory / info.filename).read_bytes(), 'Archive and loose bytes differ')
    audit_manifest = json.loads((ROOT / 'audit/AUDIT_MANIFEST.json').read_bytes())
    require(audit_manifest['disposition'] == 'ACCEPT_PARTIAL_UNSOLVED_GENERAL_POTENTIAL_5_OF_5', 'Audit disposition mismatch')
    runs = []
    with tempfile.TemporaryDirectory(prefix='gradient-publication-replay-') as cwd:
        for optimized in (False, True):
            cmd = [sys.executable, '-I', '-B'] + (['-O'] if optimized else [])
            gate = subprocess.run(cmd + [str(ROOT / 'audit/verify_audit.py'), str(ROOT / 'author'), str(ROOT / 'AUTHOR_FREEZE.zip')], cwd=cwd, capture_output=True, text=True, timeout=120)
            require(gate.returncode == 0, 'Audit gate failed: ' + gate.stderr)
            result = json.loads(gate.stdout)
            require(result['result'] == 'PASS' and result['checks_per_suite'] == 43, 'Audit replay mismatch')
            controls = subprocess.run(cmd + [str(ROOT / 'audit/test_controls.py'), str(ROOT / 'author'), str(ROOT / 'AUTHOR_FREEZE.zip')], cwd=cwd, capture_output=True, text=True, timeout=120)
            require(controls.returncode == 0, 'Audit controls failed: ' + controls.stderr)
            require(json.loads(controls.stdout) == json.loads((ROOT / 'audit/CONTROL_RESULTS.json').read_bytes()), 'Control replay mismatch')
            runs.append({'optimized_wrapper': optimized, 'author_exact_checks': 43, 'independent_exact_checks': 43, 'audit_controls': 19, 'different_cwd': True})
    return {'result': 'PASS_SOURCE_FREE_PUBLICATION', 'problem_id': 30005994, 'status': 'unsolved', 'turns': '5/5', 'mathematical_changes': 0, 'packet_files': len(expected), 'manifest_sha256': anchor, 'frozen_archives_byte_identical': True, 'runs': runs, 'scope': 'Integrity and exact algebra only; original general C1 convex-potential question remains unresolved; quartic theorem is credited to its authors.'}

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--manifest-sha256', required=True)
    args = parser.parse_args()
    print(json.dumps(verify(args.manifest_sha256), indent=2, sort_keys=True))
