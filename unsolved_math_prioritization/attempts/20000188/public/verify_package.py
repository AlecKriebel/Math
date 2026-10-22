#!/usr/bin/env python3
"""Offline package integrity and clean-copy replay. No general reconstruction solver."""
from __future__ import annotations
import argparse
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import shutil
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parent
ACCEPTED = '713520104c62adf26b0a6437b1ce1f2a1540e1489d4ec71b8eb15c9f0564a3af'
REQUIRED = {
    'README.md', 'CONTRACT.md', 'RESULTS_AND_SCOPE.md', 'SOURCES.md', 'requirements.txt',
    'global/GLOBAL_CLASSIFICATION.md', 'local/EMBEDDED_SMOOTHNESS_CRITERION.md',
    'local/SHARPNESS_FAMILIES.md', 'exceptions/EXCEPTIONAL_CLASSIFICATION.md',
    'exceptions/check_monomials.py', 'exceptions/FINITE_MONOMIAL_CHECK.json',
    'algorithm/authored/FINITE_ALGEBRAIC_CRITERION.md',
    'algorithm/authored/PRIOR_ART_AND_MONODROMY_AUDIT.md',
    'exact/EXACT_EXAMPLES_AUDIT.md', 'exact/certify_examples.py',
    'exact/CERTIFICATE_RESULTS.json', 'audit/INDEPENDENT_AUDIT.md', 'audit/ACCEPTANCE.json',
    'sources/CORPUS_BINDINGS.json', 'sources/PREPARATION_SOURCE_MANIFEST.json',
    'sources/ADDITIONAL_SOURCE_INSPECTION.json', 'REPLAY_REPORT.json',
    'TAMPER_CONTROLS.json', 'verify_package.py',
}

def digest(data):
    return hashlib.sha256(data).hexdigest()

def require(ok, message):
    if not ok:
        raise ValueError(message)

def inventory():
    result = {}
    for path in sorted(ROOT.rglob('*')):
        require(not path.is_symlink(), 'Symlink is not allowed: ' + path.relative_to(ROOT).as_posix())
        if path.is_file():
            result[path.relative_to(ROOT).as_posix()] = path.read_bytes()
        else:
            require(path.is_dir(), 'Nonregular object in package')
    return result

def integrity(expected_manifest=None):
    files = inventory()
    require('MANIFEST.json' in files, 'Missing MANIFEST.json')
    manifest_bytes = files['MANIFEST.json']
    if expected_manifest is not None:
        require(digest(manifest_bytes) == expected_manifest, 'Manifest digest does not match supplied trust anchor')
    manifest = json.loads(manifest_bytes)
    require(manifest.get('schema') == 'fixed_camera_public_package_v1', 'Wrong manifest schema')
    require(manifest.get('disposition') == 'scoped_resolved1/5', 'Wrong disposition')
    require(manifest.get('accepted_source_manifest_sha256') == ACCEPTED, 'Wrong accepted-source binding')
    entries = manifest.get('files')
    require(isinstance(entries, list), 'Manifest files must be a list')
    names = []
    for e in entries:
        name = e.get('path')
        require(isinstance(name, str), 'Nonstring path')
        p = PurePosixPath(name)
        require(not p.is_absolute() and p.as_posix() == name and '..' not in p.parts and '\\' not in name,
                'Unsafe or noncanonical manifest path')
        require(name != 'MANIFEST.json' and name not in names, 'Duplicate or self-referential manifest path')
        names.append(name)
        require(name in files, 'Missing file: ' + name)
        require(e.get('bytes') == len(files[name]), 'Byte count mismatch: ' + name)
        require(e.get('sha256') == digest(files[name]), 'Hash mismatch: ' + name)
    require(set(names) == REQUIRED, 'Manifest must list the exact disclosed package')
    require(set(files) == REQUIRED | {'MANIFEST.json'}, 'Unexpected file in package')
    a = json.loads(files['audit/ACCEPTANCE.json'])
    require(a.get('accepted_source_manifest_sha256') == ACCEPTED, 'Acceptance binding mismatch')
    require(a.get('status') == 'scoped_resolved1/5' and a.get('remaining_mathematical_obligations_within_contract') == [], 'Acceptance status mismatch')
    bindings = a.get('artifact_bindings', [])
    require(len(bindings) == 13 and len({e['path'] for e in bindings}) == 13, 'Wrong accepted artifact count')
    for e in bindings:
        b = files[e['path']]
        require(e['public_sha256'] == digest(b) and e['public_bytes'] == len(b), 'Public acceptance artifact mismatch: ' + e['path'])
        if e['edition'] == 'byte-identical':
            require(e['accepted_sha256'] == digest(b) and e['accepted_bytes'] == len(b), 'Exact-copy source mismatch')
    return files, digest(manifest_bytes)

def replay(files):
    env = dict(os.environ)
    for k in ['PYTHONOPTIMIZE', 'PYTHONPATH', 'PYTHONHOME']:
        env.pop(k, None)
    rows = []
    with tempfile.TemporaryDirectory(prefix='fixed-camera-replay-') as name:
        tmp = Path(name)
        for script, output in [('exact/certify_examples.py', 'exact/CERTIFICATE_RESULTS.json'),
                               ('exceptions/check_monomials.py', 'exceptions/FINITE_MONOMIAL_CHECK.json')]:
            p = tmp / script
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_bytes(files[script])
            proc = subprocess.run([sys.executable, '-I', str(p)], cwd=tmp, env=env,
                                  capture_output=True, text=True, timeout=600)
            require(proc.returncode == 0, script + ' failed:\n' + proc.stdout + proc.stderr)
            out = (tmp / output).read_bytes()
            require(out == files[output], 'Replay output differs byte for byte: ' + output)
            obj = json.loads(out)
            if script.startswith('exact/'):
                require(obj['summary']['fixture_groups'] == 13 and len(obj['checks']) == 13, 'Wrong fixture count')
                require(obj['summary']['status'] == 'ALL ASSERTIONS PASSED', 'Fixture failure')
                require(obj['summary']['sympy_version'] == '1.14.0', 'Use SymPy 1.14.0 for the frozen replay')
                count = {'fixture_groups': 13}
            else:
                require(obj['count'] == 430 and obj['all_passed'] is True and obj['maximum_degree'] == 12, 'Wrong monomial result')
                count = {'monomial_tuples': 430, 'degree_range': [1, 12]}
            rows.append({'script': script, 'status': 'PASS', 'output_sha256': digest(out),
                         'byte_identical_to_frozen_output': True, **count})
    return rows

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--integrity-only', action='store_true')
    parser.add_argument('--manifest-sha256', help='Optional externally trusted SHA-256 of MANIFEST.json')
    args = parser.parse_args()
    require(sys.flags.optimize == 0, 'Run without -O/-OO: fixture assertions must remain enabled')
    files, manifest_hash = integrity(args.manifest_sha256)
    result = {'status': 'PASS', 'package_files': len(files), 'manifest_sha256': manifest_hash,
              'accepted_source_manifest_sha256': ACCEPTED, 'integrity': 'PASS'}
    if not args.integrity_only:
        result['replay'] = replay(files)
        require(inventory() == files, 'Package changed during replay')
        result['package_unchanged'] = True
    print(json.dumps(result, indent=2))

if __name__ == '__main__':
    try:
        main()
    except Exception as exc:
        print('FAIL: ' + str(exc), file=sys.stderr)
        sys.exit(1)
