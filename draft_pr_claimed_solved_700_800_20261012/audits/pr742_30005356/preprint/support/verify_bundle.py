"""Explicit closed inventory plus normally executed finite negative controls.

Does not formally verify the infinite-model theorem or certify priority.
"""
from pathlib import Path, PurePosixPath
import hashlib
import json
import os
import stat
import subprocess
import sys
import tempfile

PIN = 'c95057a2926693b3051722f614e114c4083c6d1d336d74a4e9b368d3a7d7c3ba'


def require(condition, message):
    if not condition:
        raise ValueError(message)


def main():
    require(set(sys.argv[1:]) <= {'--integrity-only'}, 'Unknown argument')
    root = Path(__file__).resolve().parent
    manifest = json.loads((root / 'MANIFEST.json').read_text())
    listed = {}
    for entry in manifest['files']:
        name = entry['path']
        require(not PurePosixPath(name).is_absolute() and '\\' not in name and
                all(p not in ('', '.', '..') for p in name.split('/')) and
                str(PurePosixPath(name)) == name, 'Invalid manifest path')
        require(name not in listed and name != 'MANIFEST.json', 'Duplicate/self path')
        listed[name] = entry
    actual = {}
    for path in root.rglob('*'):
        require(not path.is_symlink(), 'Symlink in support package')
        if path.is_dir():
            continue
        require(stat.S_ISREG(path.stat().st_mode), 'Nonregular object')
        actual[path.relative_to(root).as_posix()] = path.read_bytes()
    require(set(actual) == set(listed) | {'MANIFEST.json'}, 'File inventory mismatch')
    for name, entry in listed.items():
        raw = actual[name]
        require(len(raw) == entry['bytes'] and
                hashlib.sha256(raw).hexdigest() == entry['sha256'], 'Content mismatch: ' + name)
    metadata = json.loads(actual['zenodo-metadata.json'])['metadata']
    require(metadata['title'] == 'Inverse Frobenius in generic multiplicative fields' and
            metadata['publication_type'] == 'preprint' and metadata['version'] == '1.0',
            'Wrong publication identity')
    require(metadata['creators'][0]['orcid'] == '0009-0001-9320-500X', 'Wrong author ORCID')
    gate = json.loads(actual['audit/PRIORITY_GATE.json'])
    require(gate['result'] == 'PASS_FOR_PUBLIC_VERSION_SPECIFIC_NEGATIVE_ANSWER' and
            gate['original_universal_assertion_fully_negatively_answered'] and
            not gate['historical_first_priority_certified'] and
            not gate['final_journal_body_inspected'], 'Scope gate mismatch')
    candidate = root / 'historical_candidate'
    require(hashlib.sha256((candidate / 'PUBLICATION_MANIFEST.json').read_bytes()).hexdigest()
            == PIN, 'Frozen candidate manifest changed')
    snapshot = json.loads(actual['audit/SNAPSHOT.json'])
    prefix = 'unsolved_math_prioritization/attempts/30005356/'
    require(len(snapshot['files']) == 26, 'Wrong original inventory size')
    for entry in snapshot['files']:
        require(entry['path'].startswith(prefix), 'Wrong original problem path')
        raw = actual['historical_candidate/' + entry['path'][len(prefix):]]
        require(len(raw) == entry['bytes'] and hashlib.sha256(raw).hexdigest() ==
                entry['sha256'], 'Original bytes changed')
    result = {'result': 'PASS', 'inventory_files': len(actual),
              'outer_optimized': not __debug__,
              'scope': 'Exact integrity and finite negative controls; not a formal infinite-model proof or priority certificate'}
    if '--integrity-only' not in sys.argv:
        env = os.environ.copy()
        env.pop('PYTHONOPTIMIZE', None)
        env['PYTHONDONTWRITEBYTECODE'] = '1'
        probe = subprocess.run([sys.executable, '-B', '-c', 'print(__debug__)'],
                               env=env, capture_output=True, text=True)
        require(probe.returncode == 0 and probe.stdout.strip() == 'True',
                'Child assertion mode inactive')
        r = subprocess.run([sys.executable, '-B', str(candidate / 'verify_publication.py'), PIN],
                           env=env, capture_output=True, text=True)
        require(r.returncode == 0, r.stderr)
        historical = json.loads(r.stdout)
        require(historical['status'] == 'PASS' and historical['assertions_active'],
                'Historical replay failed')
        result['historical_replay'] = historical
        r = subprocess.run([sys.executable, '-O', '-B', str(candidate / 'verify_publication.py'), PIN],
                           env=env, capture_output=True, text=True)
        require(r.returncode != 0 and 'Run without -O' in r.stderr,
                'Frozen optimization guard failed')
        result['frozen_optimized_mode_correctly_refused'] = True
        control = root / 'audit/review_operator_algebra/controls.py'
        with tempfile.TemporaryDirectory(prefix='inverse-frobenius-controls-') as temp:
            r = subprocess.run([sys.executable, '-B', str(control)], cwd=temp,
                               env=env, capture_output=True, text=True)
            require(r.returncode == 0, r.stderr)
            controls = json.loads((Path(temp) / 'controls_receipt.json').read_text())
            expected = json.loads(actual['audit/review_operator_algebra/controls_receipt.json'])
            controls.pop('generated_utc', None)
            expected.pop('generated_utc', None)
            require(controls == expected, 'Independent finite controls differ')
            result['independent_finite_controls'] = controls
        # Replay must leave the closed package untouched.
        after = {p.relative_to(root).as_posix(): p.read_bytes()
                 for p in root.rglob('*') if p.is_file()}
        require(after == actual, 'Replay changed support package')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
