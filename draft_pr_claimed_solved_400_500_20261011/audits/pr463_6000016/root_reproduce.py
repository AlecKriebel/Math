#!/usr/bin/env python3
"""Read-only frozen-source checks and independent normal/optimized replays."""
import datetime
import hashlib
import json
import os
from pathlib import Path
import subprocess

HERE = Path(__file__).resolve().parent
SOURCE = HERE / 'source_snapshot/unsolved_math_prioritization/attempts/6000016'
PYTHON = HERE.parent / 'pr464_30004807/reviews/reproduction/private_sources/venv/bin/python'

def require(condition, message):
    if not condition:
        raise RuntimeError(message)

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
    receipt = json.loads((HERE / 'SOURCE_RECEIPT.json').read_text())
    checks = []
    def frozen():
        for entry in receipt['files']:
            p = HERE / 'source_snapshot' / entry['path']
            require(p.is_file() and not p.is_symlink(), 'missing/nonregular frozen source')
            require(p.stat().st_size == entry['bytes'] and digest(p) == entry['sha256'], entry['path'])
    frozen()
    for name, base, count in [('FROZEN_AUTHOR_MANIFEST.json', SOURCE, 6),
                              ('audit/AUDIT_MANIFEST.json', SOURCE / 'audit', 4),
                              ('PUBLICATION_MANIFEST.json', SOURCE, 13)]:
        manifest = json.loads((SOURCE / name).read_text())
        require(len(manifest['files']) == count, 'manifest entry count')
        require(len({e['path'] for e in manifest['files']}) == count, 'duplicate manifest path')
        for entry in manifest['files']:
            p = base / entry['path']
            require(p.resolve().is_relative_to(SOURCE.resolve()), 'manifest path escape')
            require(p.stat().st_size == entry['bytes'] and digest(p) == entry['sha256'], name + ':' + entry['path'])
            checks.append({'manifest': name, 'path': entry['path'], 'sha256': entry['sha256']})
    audit = json.loads((SOURCE / 'audit/AUDIT_MANIFEST.json').read_text())
    require(audit['frozen_author_manifest_sha256'] == digest(SOURCE / 'FROZEN_AUTHOR_MANIFEST.json'), 'standalone author binding')
    require(audit['frozen_proof_sha256'] == digest(SOURCE / 'PROOF.md'), 'standalone proof binding')
    output = HERE / 'root_reproduction'
    output.mkdir(exist_ok=True)
    runs = []
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1')
    for label, script, arguments, expected, count_key, count in [
            ('author', SOURCE / 'check_exact.py', [], SOURCE / 'exact_results.json', 'exact_identity_count', 41),
            ('audit', SOURCE / 'audit/check_audit.py', ['--author-dir', str(SOURCE)], SOURCE / 'audit/audit_results.json', 'audit_control_count', 61)]:
        for optimized in (False, True):
            cmd = [str(PYTHON)] + (['-O'] if optimized else []) + [str(script)] + arguments
            run_env = dict(env, PYTHONOPTIMIZE='1' if optimized else '0')
            result = subprocess.run(cmd, cwd='/tmp', env=run_env, capture_output=True, timeout=120)
            require(result.returncode == 0 and not result.stderr, label + ' process failed')
            require(result.stdout == expected.read_bytes(), label + ' output differs from frozen result')
            parsed = json.loads(result.stdout)
            require(parsed['status'] == 'PASS' and type(parsed[count_key]) is int and parsed[count_key] == count, label + ' count/status')
            require(len(parsed['checks']) == count and len(set(parsed['checks'])) == count, label + ' names/count mismatch')
            dest = output / (label + ('_optimized.json' if optimized else '_normal.json'))
            dest.write_bytes(result.stdout)
            runs.append({'label': label, 'optimized': optimized, 'exact_named_checks': count,
                         'stdout_sha256': digest(dest), 'byte_identical_to_frozen': True,
                         'returncode': result.returncode, 'cwd': '/tmp',
                         'nested_subprocess_optimization_propagated': True})
    frozen()
    result = {'timestamp_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
              'status': 'PASS', 'source_files_unchanged': len(receipt['files']),
              'manifest_references_verified': len(checks), 'standalone_bindings_verified': 2,
              'manifest_checks': checks, 'runs': runs,
              'scope': 'Named algebraic/integrity checks; analytical positivity, compactness, Stokes, source interpretation and priority require separate review.'}
    (HERE / 'ROOT_REPRODUCTION_RECEIPT.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({k: result[k] for k in ('status', 'source_files_unchanged', 'manifest_references_verified', 'standalone_bindings_verified', 'runs')}, indent=2))

if __name__ == '__main__':
    main()
