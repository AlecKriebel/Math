#!/usr/bin/env python3
"""Relocatable offline integrity verification and frozen TZ partial-control replay."""
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import platform
import subprocess
import sys
import zipfile

ROOT = Path(__file__).resolve().parent
PINS = {
    'author/MANIFEST.json': (1508, '793eff4aec0c86808289fa1ce17d32d95f52c03dd09219d13538a6fa6527d5cd'),
    'audit/MANIFEST.json': (1617, '25337b329f8cb087a391cd161014e614707582fcb5feb71304218470964fc9b0'),
    'audit/AUDIT.md': (28048, '972dda0eaeae5654823ca98a23b75614b70bc71462a6f66fed98a16732365f9f'),
    'archives/tz_curvature_30001631_public_packet.zip': (21262, 'c9a370d76b6ef5cb98214f49098e812eb9c470adfa9e3a694bcbea4bd006298f'),
    'archives/tz_curvature_30001631_independent_audit.zip': (24319, '79fac578564f0939a154925154892c7a940f5dc947004d1c23a4947e93beb3bb'),
}


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def run(script, *args):
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1')
    return subprocess.check_output([sys.executable, '-B', str(ROOT / script), *map(str, args)], env=env)


def main():
    require(platform.python_version() == '3.12.14', 'Exact replay requires Python 3.12.14')
    import sympy
    import mpmath
    require(sympy.__version__ == '1.14.0' and mpmath.__version__ == '1.3.0', 'Dependency versions differ')
    manifest = json.loads((ROOT / 'PUBLICATION_MANIFEST.json').read_bytes())
    require(manifest['target_id'] == '30001631' and manifest['outcome'] == 'unsolved' and manifest['turns'] == '5/5', 'Publication scope differs')
    records = {row['path']: row for row in manifest['files']}
    require(len(records) == len(manifest['files']), 'Duplicate manifest entries')
    for path in ROOT.rglob('*'):
        require(not path.is_symlink(), 'Symlink in publication')
        require(path.is_file() or path.is_dir(), 'Special file in publication')
    actual = {p.relative_to(ROOT).as_posix() for p in ROOT.rglob('*') if p.is_file()}
    require(actual == set(records) | {'PUBLICATION_MANIFEST.json'}, 'Unexpected publication file set')
    expected_dirs = {str(parent) for name in records for parent in PurePosixPath(name).parents if str(parent) != '.'}
    actual_dirs = {p.relative_to(ROOT).as_posix() for p in ROOT.rglob('*') if p.is_dir()}
    require(actual_dirs == expected_dirs, 'Unexpected directory set')
    before = {}
    for name, row in records.items():
        path = PurePosixPath(name)
        require(not path.is_absolute() and '..' not in path.parts, 'Unsafe path')
        data = (ROOT / name).read_bytes()
        require(len(data) == row['bytes'] and digest(data) == row['sha256'], 'Integrity mismatch: ' + name)
        before[name] = data
    for name, (size, sha) in PINS.items():
        require(len(before[name]) == size and digest(before[name]) == sha, 'Immutable input binding differs: ' + name)
    archive_members = 0
    for dirname, archive in [('author', 'tz_curvature_30001631_public_packet.zip'), ('audit', 'tz_curvature_30001631_independent_audit.zip')]:
        files = {p.name: p.read_bytes() for p in (ROOT / dirname).iterdir()}
        with zipfile.ZipFile(ROOT / 'archives' / archive) as z:
            require(len(z.namelist()) == len(set(z.namelist())), 'Duplicate ZIP member')
            require(set(z.namelist()) == set(files), 'Archive allowlist differs')
            for name, data in files.items():
                require(z.read(name) == data, 'Archive member differs: ' + name)
                archive_members += 1
    author_manifest = json.loads(run('author/verify_manifest.py'))
    audit_manifest = json.loads(run('audit/verify_audit_manifest.py'))
    author_bytes = run('author/check_controls.py')
    require(author_bytes == before['author/CONTROL_OUTPUT.json'], 'Original replay bytes differ')
    require(json.loads(author_bytes)['passed'] == 11, 'Original control count differs')
    independent_bytes = run('audit/independent_controls.py', ROOT / 'author', ROOT / 'archives/tz_curvature_30001631_public_packet.zip')
    require(independent_bytes == before['audit/INDEPENDENT_RESULTS.json'], 'Independent replay bytes differ')
    independent = json.loads(independent_bytes)
    require(independent['checks_passed'] == 23 and all(t['passed'] for t in independent['tests']), 'Independent checks failed')
    negative = next(t for t in independent['tests'] if t['name'] == 'independent_deliberate_error_controls')
    require(negative['rejected'] == 8, 'Deliberate-error controls differ')
    require(all((ROOT / name).read_bytes() == data for name, data in before.items()), 'Input changed during replay')
    print(json.dumps({
        'status': 'pass', 'target_id': '30001631', 'outcome': 'unsolved', 'turns': '5/5',
        'controlling_clarifications': ['C1', 'C2'],
        'publication_files_verified': len(records), 'publication_manifest_self_excluded': True,
        'publication_manifest_sha256': digest((ROOT / 'PUBLICATION_MANIFEST.json').read_bytes()),
        'archive_members_verified': archive_members,
        'author_manifest': author_manifest, 'audit_manifest': audit_manifest,
        'author_controls_passed': 11, 'author_replay_byte_equal': True,
        'independent_check_groups_passed': 23, 'independent_replay_byte_equal': True,
        'deliberate_mathematical_errors_rejected': 8,
        'actual_finite_type_TZ_curvature_evaluated': False, 'supplementary_quadrature_is_exact_proof': False,
        'python': platform.python_version(), 'sympy': sympy.__version__, 'mpmath': mpmath.__version__,
        'scope': 'Integrity and finite identity/model checks supporting partial deductions only; no target sign resolution or formal proof certificate.'
    }, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
