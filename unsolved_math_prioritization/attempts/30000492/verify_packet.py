#!/usr/bin/env python3
"""Verify fixed author/audit bindings and replay without modifying this package."""
import argparse
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import shutil
import subprocess
import sys
import tempfile
import zipfile

ANCHORS = {
    'author-packet.zip': '25f0cd6997fc0d2774588030e98f902d2b16b8817eaf44b6f3c815826a7c7783',
    'independent-audit.zip': '3ec5f5ec3221344893ca6289f5689650bec1e03bd5da80b72be2ba5a28431d4d',
}

def require(ok, message):
    if not ok:
        raise RuntimeError(message)

def describe(path):
    b = path.read_bytes()
    return {'bytes': len(b), 'sha256': hashlib.sha256(b).hexdigest()}

def archive_check(root, name, prefix, count):
    with zipfile.ZipFile(root / name) as z:
        names = z.namelist()
        expected = sorted(p.relative_to(root).as_posix() for p in (root / prefix).rglob('*') if p.is_file())
        require(len(names) == len(set(names)) == count and sorted(names) == expected, 'ZIP inventory mismatch: ' + name)
        for n in names:
            p = PurePosixPath(n)
            require(not p.is_absolute() and '..' not in p.parts, 'Unsafe ZIP path')
            require(z.read(n) == (root / n).read_bytes(), 'ZIP member mismatch: ' + n)

def integrity(root):
    require(sys.flags.optimize == 0, 'Optimized Python is unsupported; remove -O, -OO and PYTHONOPTIMIZE.')
    m = json.loads((root / 'PUBLICATION_MANIFEST.json').read_text())
    require(m['problem_id'] == 30000492 and m['status'] == 'unsolved' and m['turns'] == '5/5', 'Wrong disposition')
    require(m['general_odd_characteristic_resolution'] is False and m['novelty_certified'] is False and m['human_peer_review'] is False, 'Overstated result')
    actual = {}
    for p in root.rglob('*'):
        require(not p.is_symlink(), 'Symlinks forbidden: ' + str(p))
        if p.is_file() and p != root / 'PUBLICATION_MANIFEST.json':
            actual[p.relative_to(root).as_posix()] = describe(p)
    require(actual == m['files'], 'Publication inventory or hash mismatch')
    for name, digest in ANCHORS.items():
        require(describe(root / name)['sha256'] == digest, 'Frozen archive binding mismatch: ' + name)
    archive_check(root, 'author-packet.zip', 'packet', 13)
    archive_check(root, 'independent-audit.zip', 'audit', 12)
    for prefix in ['packet', 'audit']:
        manifest = json.loads((root / prefix / 'MANIFEST.json').read_text())
        require(manifest['problem_id'] == 30000492, 'Wrong frozen target')
        for f in manifest['files']:
            require(describe(root / prefix / f['path']) == {k: f[k] for k in ['bytes', 'sha256']}, 'Frozen member mismatch')
    a = json.loads((root / 'AUTHOR_FREEZE.json').read_text())
    d = json.loads((root / 'AUDIT_FREEZE.json').read_text())
    bind = json.loads((root / 'audit/BINDING.json').read_text())
    require(a['sha256'] == ANCHORS['author-packet.zip'] and a['bytes'] == 23273 and a['file_count'] == 13, 'Wrong author freeze')
    require(d['sha256'] == ANCHORS['independent-audit.zip'] and d['bytes'] == 19725 and d['file_count'] == 12, 'Wrong audit freeze')
    require(bind['audited_author_archive']['sha256'] == ANCHORS['author-packet.zip'], 'Audit bound to wrong author')
    require(bind['verdict'] == d['verdict'] == 'PASS_PARTIAL_RESULTS_UNSOLVED', 'Wrong audit verdict')
    require(bind['research_status'] == 'unsolved' and bind['approaches_completed'] == 5 and bind['required_corrections'] == 0, 'Wrong audit disposition')
    for member in bind['audited_author_archive']['members']:
        require(describe(root / member['path']) == {k: member[k] for k in ['bytes', 'sha256']}, 'Audit author-member mismatch')
    return len(actual)

def compare_output(raw, expected, runtime_locations):
    if raw == expected:
        return 'byte-identical'
    got, want = json.loads(raw), json.loads(expected)
    for location in runtime_locations:
        gg, ww = got, want
        for key in location[:-1]:
            gg, ww = gg[key], ww[key]
        require(isinstance(gg.pop(location[-1]), str) and isinstance(ww.pop(location[-1]), str), 'Missing runtime field')
    require(got == want, 'Mathematical replay result mismatch')
    return 'identical except declared runtime-version strings'

def replay(root):
    checks = [
        ('author_exact', ['packet/verify.py'], 'packet/EXACT_RESULTS.json', [('software', 'python'), ('software', 'sympy')]),
        ('author_controls', ['packet/test_controls.py'], 'packet/CONTROL_RESULTS.json', []),
        ('independent_full_iterates', ['audit/independent_checks.py', '--author-results', 'packet/EXACT_RESULTS.json'], 'audit/INDEPENDENT_RESULTS.json', [('python',), ('sympy',)]),
        ('independent_certificates', ['audit/certificate_checks.py', 'packet/EXACT_RESULTS.json'], 'audit/CERTIFICATE_RESULTS.json', []),
    ]
    results = {}
    with tempfile.TemporaryDirectory(prefix='settled-quadratic-replay-') as td:
        scratch = Path(td) / 'packet'
        shutil.copytree(root, scratch)
        env = os.environ.copy()
        env.pop('PYTHONOPTIMIZE', None)
        env['PYTHONDONTWRITEBYTECODE'] = '1'
        for name, args, output, runtime in checks:
            proc = subprocess.run([sys.executable, '-E', '-B', *args], cwd=scratch, env=env, capture_output=True)
            require(proc.returncode == 0, name + ' failed: ' + proc.stderr.decode(errors='replace'))
            results[name] = compare_output(proc.stdout, (scratch / output).read_bytes(), runtime)
        integrity(scratch)
    return results

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--integrity-only', action='store_true')
    args = ap.parse_args()
    root = Path(__file__).resolve().parent
    count = integrity(root)
    result = dict(passed=True, problem_id=30000492, status='unsolved', turns='5/5', files_verified=count,
                  archive_member_count=25, frozen_archive_bindings='exact', assertions_enabled=True)
    if not args.integrity_only:
        result['replay'] = replay(root)
    print(json.dumps(result, indent=2, sort_keys=True))

if __name__ == '__main__':
    main()
