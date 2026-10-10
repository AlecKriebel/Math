#!/usr/bin/env python3
"""Portable byte, scope, and exact-control replay; public sources are optional."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parent

def require(ok, message):
    if not ok:
        raise SystemExit(message)

def read_json(path):
    return json.loads(path.read_bytes())

def main():
    p = argparse.ArgumentParser(description=__doc__)
    for option in ('problems', 'research', 'catalog', 'pdf-directory'):
        p.add_argument('--' + option, type=Path)
    args = p.parse_args()
    values = [args.problems, args.research, args.catalog, args.pdf_directory]
    require(all(values) or not any(values), 'Supply all four external-source options or none')
    manifest = read_json(ROOT / 'PUBLICATION_MANIFEST.json')
    entries = manifest['files']
    expected = {r['path'] for r in entries} | {'PUBLICATION_MANIFEST.json'}
    require(len(entries) == len(expected) - 1, 'Duplicate manifest path')
    actual = {str(x.relative_to(ROOT)) for x in ROOT.rglob('*') if x.is_file()}
    require(actual == expected, 'File inventory mismatch')
    for row in entries:
        path = ROOT / row['path']
        require(not path.is_symlink() and path.resolve().is_relative_to(ROOT), 'Unsafe member path')
        data = path.read_bytes()
        require(len(data) == row['bytes'] and hashlib.sha256(data).hexdigest() == row['sha256'],
                'Integrity failure: ' + row['path'])
    pins = {
        'author/AUTHOR_MANIFEST.json': 'af41972b5888f937ac69d53a823207f4736064edb6c289eaf1e002fa1acb8b4f',
        'audit/AUDIT_MANIFEST.json': '5db63a8b3c44c1695ec0a11f3346dcb8ec215c6f6c160b96ca409144c7343d46',
    }
    for path, sha in pins.items():
        require(hashlib.sha256((ROOT / path).read_bytes()).hexdigest() == sha, 'Frozen manifest changed')
    status = read_json(ROOT / 'PUBLICATION_STATUS.json')
    require(status['status'] == 'unsolved' and status['turns'] == '3/5', 'Disposition changed')
    require(status['mathematical_audit'] == 'PASS_scoped', 'Audit scope changed')
    require(status['original_target_verified_solved'] is False and status['novelty_established'] is False,
            'Unsupported original-target or novelty promotion')
    verdict = read_json(ROOT / 'audit/VERDICT.json')
    require(verdict['verdict'] == 'PASS' and verdict['original_target_verified_solved'] is False,
            'Unexpected independent verdict')
    env = dict(os.environ)
    env.pop('PYTHONOPTIMIZE', None)
    env['PYTHONDONTWRITEBYTECODE'] = '1'
    def run(script, options=()):
        result = subprocess.run([sys.executable, '-B', str(ROOT / script), *options],
                                check=True, capture_output=True, text=True, cwd=ROOT, env=env)
        return json.loads(result.stdout)
    run('author/verify_integrity.py')
    run('audit/verify_manifest.py')
    author = run('author/verify_math.py')
    independent = run('audit/verify_independent.py')
    require(author == read_json(ROOT / 'author/CHECKS.json'), 'Author controls differ from freeze')
    require(independent == read_json(ROOT / 'audit/INDEPENDENT_CHECKS.json'), 'Independent controls differ')
    require(author['assertions'] == 282118 and independent['assertions'] == 52161, 'Assertion count changed')
    external = 'NOT_RUN: separately supplied public-source bytes required'
    if all(values):
        options = []
        for label, value in zip(('problems', 'research', 'catalog', 'pdf-directory'), values):
            options.extend(['--' + label, str(value.resolve())])
        source = run('audit/verify_source_metadata.py', options)
        require(source == read_json(ROOT / 'audit/SOURCE_METADATA_VERIFICATION.json'), 'Source bindings differ')
        external = 'PASS: supplied bytes match recorded public-source bindings; no fresh retrieval implied'
    print(json.dumps({'status': 'PASS', 'verified_files': len(expected),
        'original_target_status': status['status'], 'turns': status['turns'],
        'mathematical_audit': status['mathematical_audit'],
        'author_assertions': author['assertions'], 'independent_assertions': independent['assertions'],
        'external_source_verification': external, 'novelty_established': False}, indent=2, sort_keys=True))

if __name__ == '__main__':
    main()
