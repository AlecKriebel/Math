"""Verify the closed support inventory and reproduce historical finite controls.

This does not formally verify the algebraic-geometric proof.
"""
from pathlib import Path, PurePosixPath
import hashlib
import json
import os
import stat
import subprocess
import sys


def require(condition, message):
    if not condition:
        raise ValueError(message)


def main():
    root = Path(__file__).resolve().parent
    manifest = json.loads((root / 'MANIFEST.json').read_text())
    listed = {}
    for entry in manifest['files']:
        name = entry['path']
        require(not PurePosixPath(name).is_absolute() and '\\' not in name and
                all(part not in ('', '.', '..') for part in name.split('/')) and
                str(PurePosixPath(name)) == name, 'Invalid path')
        require(name not in listed and name != 'MANIFEST.json', 'Duplicate/self path')
        listed[name] = entry
    actual = {}
    for path in root.rglob('*'):
        require(not path.is_symlink(), 'Symlink in package')
        if path.is_dir():
            continue
        require(stat.S_ISREG(path.stat().st_mode), 'Nonregular file')
        actual[path.relative_to(root).as_posix()] = path.read_bytes()
    require(set(actual) == set(listed) | {'MANIFEST.json'}, 'File inventory mismatch')
    for name, entry in listed.items():
        require(len(actual[name]) == entry['bytes'] and
                hashlib.sha256(actual[name]).hexdigest() == entry['sha256'],
                'Content mismatch: ' + name)
    metadata = json.loads(actual['zenodo-metadata.json'])['metadata']
    require(metadata['publication_type'] == 'preprint' and metadata['version'] == '1.0',
            'Wrong publication type/version')
    runs = []
    if '--integrity-only' not in sys.argv:
        env = os.environ.copy()
        env['PYTHONDONTWRITEBYTECODE'] = '1'
        candidate = root / 'historical_candidate/verify_publication.py'
        for flags in ([], ['-O']):
            result = subprocess.run([sys.executable, *flags, str(candidate),
                '98f8b101524ffafa4a533249f5bbc5bed3025c6bb7cb4f982f589bbcef9e58f0'],
                env=env, capture_output=True, text=True)
            require(result.returncode == 0, result.stderr)
            payload = json.loads(result.stdout)
            require(payload['result'] == 'PASS', 'Historical replay did not pass')
            runs.append({'optimized': bool(flags), 'result': payload})
        result = subprocess.run([sys.executable,
            str(root / 'audit/review_pointed_geometry/check_boundary_controls.py')],
            env=env, capture_output=True, text=True)
        require(result.returncode == 0, result.stderr)
        controls = json.loads(result.stdout)
        require(controls == json.loads(actual['audit/review_pointed_geometry/boundary_controls_results.json']),
                'Independent boundary-control result mismatch')
    else:
        controls = None
    print(json.dumps({'result': 'PASS', 'inventory_files': len(actual),
        'historical_runs': runs, 'independent_boundary_controls': controls,
        'scope': 'Exact inventory and reproduced finite/integrity controls; not a formal geometry proof'}, indent=2))


if __name__ == '__main__':
    main()
