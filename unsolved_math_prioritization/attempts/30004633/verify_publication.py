#!/usr/bin/env python3
"""Portable integrity and finite-diagnostic checks; not a proof verifier."""
import argparse
import ast
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import zipfile

ROOT = Path(__file__).resolve().parent
MANIFEST = 'PUBLICATION_MANIFEST.json'
ARCHIVE = 'POROUS_MEDIUM_30004633_AUTHOR_CONTINUATION_A2_A5.zip'
FLAGS = (['-I'] if sys.flags.isolated else []) + (['-O'] if sys.flags.optimize else [])

def require(condition, message):
    if not condition:
        raise RuntimeError(message)

def digest(data):
    return hashlib.sha256(data).hexdigest()

def read_json(name):
    return json.loads((ROOT / name).read_text(encoding='utf-8'))

def check_rows(rows, context):
    require(isinstance(rows, list) and bool(rows), context + ': invalid rows')
    names = [row['file'] for row in rows]
    require(len(names) == len(set(names)), context + ': duplicate file')
    for row in rows:
        name = row['file']
        require(Path(name).name == name and name not in ('', '.', '..'), context + ': unsafe path')
        data = (ROOT / name).read_bytes()
        require(len(data) == row['bytes'] and digest(data) == row['sha256'], context + ': byte/hash mismatch: ' + name)
    return names

def integrity():
    m = read_json(MANIFEST)
    require(m.get('schema') == 'porous-medium-30004633-publication-v1', 'manifest schema')
    names = check_rows(m['files'], 'publication')
    actual = set()
    for path in ROOT.rglob('*'):
        if '__pycache__' in path.parts:
            continue
        require(not path.is_symlink(), 'symlinks are not permitted')
        if path.is_file():
            actual.add(path.relative_to(ROOT).as_posix())
    require(actual == set(names) | {MANIFEST}, 'unexpected or missing public file')
    for name in names:
        if name.endswith('.py'):
            tree = ast.parse((ROOT / name).read_text(encoding='utf-8'))
            require(not any(isinstance(node, ast.Assert) for node in ast.walk(tree)), 'optimization-sensitive assert: ' + name)
    author = read_json('AUTHOR_SAFE_MANIFEST.json')
    author_names = check_rows(author['files'], 'author') + ['AUTHOR_SAFE_MANIFEST.json']
    external = read_json('AUTHOR_EXTERNAL_MANIFEST.json')
    data = (ROOT / ARCHIVE).read_bytes()
    require(len(data) == external['bytes'] == 25960, 'archive size')
    require(digest(data) == external['sha256'] == 'b506b44a188cea5a787ef4736affc74efc5ed5bda1516ab72617401b920b42c5', 'archive hash')
    manifest = (ROOT / external['manifest']['filename']).read_bytes()
    require(len(manifest) == external['manifest']['bytes'] and digest(manifest) == external['manifest']['sha256'], 'author manifest pin')
    with zipfile.ZipFile(ROOT / ARCHIVE) as z:
        require(len(z.infolist()) == 12 and sorted(z.namelist()) == sorted(author_names), 'archive member set')
        for name in author_names:
            require(z.read(name) == (ROOT / name).read_bytes(), 'archive-member mismatch: ' + name)
    audit_data = (ROOT / 'AUDIT_MANIFEST.json').read_bytes()
    require(digest(audit_data) == '8ae5d70a50b0c744f3e594c2a567dd31351b20d4216e399843f3995bac159abe', 'audit manifest pin')
    audit = json.loads(audit_data)
    check_rows(audit['inputs'], 'audited input')
    check_rows(audit['audit_outputs'], 'audit output')
    for row in audit['inputs']:
        require(row['verdict'] == 'ACCEPTED' and row['mathematical_patch_required'] is False, 'audit verdict')
        require(external['frozen_manuscript_hashes_verified'][row['file']] == row['sha256'], 'frozen author pin')
    return {'files': len(actual), 'archive_members': 12, 'audited_inputs': 4, 'audit_outputs': 6}

def diagnostics():
    cases = [
        ('verify_approach_02.py', 669, {'proximal-sign': 'proximal-first-variation-sign', 'pressure-sign': 'signed-relative-energy-cancellation', 'omit-vacuum': 'vacuum-term-is-essential', 'freeze-scale': 'frozen-defect-epsilon-scaling'}),
        ('verify_approach_05.py', 50030, {'mass-scale': 'normalization:1,1.5,2', 'kkt-sign': 'kkt:1,1.5,2,0', 'covariance-sign': 'quadratic-test-exact-cancellation'}),
    ]
    results = []
    for name, count, mutations in cases:
        cmd = [sys.executable, *FLAGS, str(ROOT / name)]
        run = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True, timeout=120)
        require(run.returncode == 0, name + ': diagnostic failed: ' + run.stderr)
        output = json.loads(run.stdout)
        require(output['status'] == 'PASS' and output['checks'] == count and output['mutation'] is None, name + ': unexpected diagnostic result')
        for mutation, expected in mutations.items():
            run = subprocess.run([*cmd, '--mutate', mutation], cwd=ROOT, capture_output=True, text=True, timeout=120)
            require(run.returncode != 0 and 'AssertionError: ' + expected in run.stderr, name + ': mutation not detected: ' + mutation)
        results.append({'script': name, 'checks': count, 'mutations_detected': len(mutations)})
    return results

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--integrity-only', action='store_true')
    args = parser.parse_args()
    result = {'status': 'PASS', 'integrity': integrity(), 'diagnostic_scope': 'Finite/symbolic consistency only; not formal proof verification.'}
    if not args.integrity_only:
        result['diagnostics'] = diagnostics()
    print(json.dumps(result, sort_keys=True))

if __name__ == '__main__':
    main()
