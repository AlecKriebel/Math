#!/usr/bin/env python3
"""Strict offline author-packet integrity and scope guard."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys


def pairs(p):
    d = {}
    for k, v in p:
        if k in d:
            raise ValueError('duplicate JSON key: '+k)
        d[k] = v
    return d


def read_json(path):
    return json.loads(path.read_text(encoding='utf-8'), object_pairs_hook=pairs)


def verify(root):
    manifest = read_json(root/'MANIFEST.json')
    if set(manifest) != {'algorithm', 'files', 'schema'} or manifest['schema'] != 1 or manifest['algorithm'] != 'sha256':
        raise ValueError('manifest schema')
    allowed = {'APPROACHES.md', 'PROOF.md', 'README.md', 'RESULTS.json', 'SCOPE.json', 'SOURCE_VERIFICATION.json', 'verify_integrity.py', 'verify_math.py'}
    if {x.get('path') for x in manifest['files']} != allowed:
        raise ValueError('frozen payload allowlist')
    expected = {'MANIFEST.json'}
    for item in manifest['files']:
        if set(item) != {'path', 'bytes', 'sha256'}:
            raise ValueError('entry schema')
        name = item['path']
        if not isinstance(name, str) or '/' in name or '\\' in name or name in expected or name in {'', '.', '..'}:
            raise ValueError('unsafe or duplicate path')
        expected.add(name)
        path = root/name
        if path.is_symlink() or not path.is_file():
            raise ValueError('missing file or symlink: '+name)
        b = path.read_bytes()
        if len(b) != item['bytes'] or hashlib.sha256(b).hexdigest() != item['sha256']:
            raise ValueError('file mismatch: '+name)
    if {p.name for p in root.iterdir()} != expected or any(not p.is_file() or p.is_symlink() for p in root.iterdir()):
        raise ValueError('unexpected file, directory, or symlink')
    scope = read_json(root/'SCOPE.json')
    required = {'problem_id': 5300080, 'problem_code': 'AMR-052-0080', 'rank': 793,
                'disposition': 'unsolved', 'substantive_approaches_used': 5,
                'original_solution_credit': 0, 'novelty_claim': False,
                'full_target_resolved': False, 'arithmetic_checks_prove_analytic_theorems': False,
                'subharmonic_threshold_example_is_henon_counterexample': False}
    for k, v in required.items():
        if scope.get(k) != v or type(scope.get(k)) is not type(v):
            raise ValueError('scope mismatch: '+k)
    run = subprocess.run([sys.executable, '-B', str(root/'verify_math.py')], check=True, text=True, capture_output=True)
    actual = json.loads(run.stdout, object_pairs_hook=pairs)
    if actual != read_json(root/'RESULTS.json'):
        raise ValueError('replay mismatch')
    return {'status': 'PASS', 'manifest_files': len(manifest['files']),
            'math_assertions': actual['assertions'], 'scope': 'unsolved; analytic proofs not certified'}


if __name__ == '__main__':
    try:
        print(json.dumps(verify(Path(__file__).resolve().parent), indent=2, sort_keys=True))
    except (OSError, ValueError, subprocess.CalledProcessError) as exc:
        raise SystemExit('FAIL: '+str(exc))
