#!/usr/bin/env python3
"""Independent round-1 archive checks, isolated replays and tamper controls.

Writes only within this review folder. No Git, GitHub, Zenodo or GWS mutations.
"""
from pathlib import Path, PurePosixPath
import hashlib
import json
import os
import shutil
import subprocess
import sys
import zipfile

HERE = Path(__file__).resolve().parent
AUDIT = HERE.parents[1]
PUB = AUDIT / 'publication'
TMP = HERE / 'tmp'
PYTHON = Path('/Users/alec/Documents/Math/draft_pr_claimed_solved_600_700_20261012/tooling/math-venv/bin/python')


def require(condition, message):
    if not condition:
        raise ValueError(message)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def invoke(args, cwd, name):
    env = os.environ.copy()
    env['TMPDIR'] = str(TMP)
    env['PYTHONOPTIMIZE'] = '2'
    p = subprocess.run([str(PYTHON), *args], cwd=cwd, env=env,
                       text=True, capture_output=True, timeout=120)
    (HERE / (name + '.stdout')).write_text(p.stdout)
    (HERE / (name + '.stderr')).write_text(p.stderr)
    return p


def main():
    files = [PUB / n for n in ['gns_generation_counterexample.tex', 'gns_generation_counterexample.pdf',
        'gns_verification.zip', 'verify_package.py', 'build_package.py', 'PACKAGE_README.md',
        'CURRENT_PRIORITY_AND_STATUS.md', 'requirements.txt', 'zenodo-deposit.json']]
    files += [AUDIT / n for n in ['prepare_integration.py', 'record_tracker.py',
        'reviews/operations_01/check_helpers.py', 'INTEGRATION_HELPER_NOTES.md', 'INTEGRATION_HELPER_CHECKS.json']]
    inputs = {str(p.relative_to(AUDIT)): digest(p.read_bytes()) for p in files}
    (HERE / 'INPUT_SHA256.json').write_text(json.dumps(inputs, indent=2) + '\n')
    with zipfile.ZipFile(PUB / 'gns_verification.zip') as z:
        entries = z.infolist()
        names = [e.filename for e in entries]
        require(len(names) == len(set(names)) == 88, 'wrong ZIP inventory')
        for e in entries:
            p = PurePosixPath(e.filename)
            require(not p.is_absolute() and '..' not in p.parts and str(p) == e.filename and '\\' not in e.filename, 'unsafe path')
            require(not e.is_dir() and (e.external_attr >> 16) & 0o170000 == 0o100000, 'nonregular ZIP member')
        require(z.testzip() is None, 'CRC failure')
        members = {n: z.read(n) for n in names}
    m = json.loads(members['PACKAGE_MANIFEST.json'])
    require(m['file_count'] == 87 and m['raw_third_party_fulltexts_included'] is False, 'manifest count/disclosure')
    require({e['path'] for e in m['files']} == set(names) - {'PACKAGE_MANIFEST.json'}, 'manifest inventory')
    require(len(m['files']) == len({e['path'] for e in m['files']}), 'duplicate manifest paths')
    for e in m['files']:
        require(e['bytes'] == len(members[e['path']]) and e['sha256'] == digest(members[e['path']]), 'member digest')
    native = AUDIT / 'native/unsolved_math_prioritization/attempts/30001184'
    native_files = {p.relative_to(native).as_posix(): p.read_bytes() for p in native.rglob('*') if p.is_file()}
    require(len(native_files) == 29 and {n[10:] for n in names if n.startswith('candidate/')} == set(native_files), 'native inventory')
    require(all(members['candidate/' + n] == d for n, d in native_files.items()), 'native byte binding')
    for n in ('gns_generation_counterexample.pdf', 'gns_generation_counterexample.tex', 'CURRENT_PRIORITY_AND_STATUS.md', 'verify_package.py', 'requirements.txt'):
        require(members[n] == (PUB / n).read_bytes(), 'local/ZIP binding: ' + n)
    require(members['README.md'] == (PUB / 'PACKAGE_README.md').read_bytes(), 'README binding')
    forbidden = [n for n in names if 'sources.private' in n or '/tmp/' in n or '/.git/' in n or n.endswith('.env') or n.rsplit('/', 1)[-1] in {'prepare_integration.py', 'record_tracker.py', 'zenodo-deposit.json'}]
    require(not forbidden, 'forbidden ZIP paths')
    require([n for n in names if n.endswith('.pdf')] == ['gns_generation_counterexample.pdf'], 'third party PDF')
    root = TMP / 'extracted'
    root.mkdir()
    for n, d in members.items():
        p = root / n
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_bytes(d)
    replays = {}
    for label, flags in [('normal', []), ('optimized', ['-O'])]:
        p = invoke(['-I', *flags, str(root / 'verify_package.py')], root, 'REPLAY_' + label)
        require(p.returncode == 0, 'portable full replay failed: ' + label)
        replays[label] = json.loads(p.stdout)
    require(replays['normal'] == replays['optimized'], 'optimization changes full result')
    require(all((root / n).read_bytes() == d for n, d in members.items()), 'replay modified archive')
    # Control independent package inventory failures, in both wrapper modes.
    cases = ['changed_bytes', 'missing', 'extra', 'duplicate_path', 'duplicate_json_key', 'traversal',
             'absolute', 'wrong_size', 'wrong_hash', 'wrong_count', 'empty_directory', 'symlink', 'bool_size', 'malformed_schema']
    controls = {}
    for case in cases:
        target = TMP / ('control_' + case)
        shutil.copytree(root, target)
        mp = target / 'PACKAGE_MANIFEST.json'
        doc = json.loads(mp.read_text())
        changed_manifest = True
        if case == 'changed_bytes': (target / 'README.md').write_bytes(members['README.md'] + b'!'); changed_manifest = False
        elif case == 'missing': (target / 'README.md').unlink(); changed_manifest = False
        elif case == 'extra': (target / 'EXTRA.txt').write_text('x'); changed_manifest = False
        elif case == 'duplicate_path': doc['files'].append(doc['files'][0].copy()); doc['file_count'] += 1
        elif case == 'duplicate_json_key': mp.write_text(mp.read_text().replace('"schema":', '"schema": 0, "schema":', 1)); changed_manifest = False
        elif case == 'traversal': doc['files'][0]['path'] = '../escape'
        elif case == 'absolute': doc['files'][0]['path'] = '/tmp/escape'
        elif case == 'wrong_size': doc['files'][0]['bytes'] += 1
        elif case == 'wrong_hash': doc['files'][0]['sha256'] = '0' * 64
        elif case == 'wrong_count': doc['file_count'] += 1
        elif case == 'empty_directory': (target / 'extra_empty').mkdir(); changed_manifest = False
        elif case == 'symlink': (target / 'README.md').unlink(); (target / 'README.md').symlink_to(root / 'README.md'); changed_manifest = False
        elif case == 'bool_size': doc['files'][0]['bytes'] = True
        elif case == 'malformed_schema': doc['schema'] = 2
        if changed_manifest: mp.write_text(json.dumps(doc))
        controls[case] = {}
        for label, flags in [('normal', []), ('optimized', ['-O'])]:
            p = invoke(['-I', *flags, str(target / 'verify_package.py'), '--integrity-only'], target, 'CONTROL_' + case + '_' + label)
            require(p.returncode != 0, 'control incorrectly accepted: ' + case + '/' + label)
            controls[case][label] = 'REJECT'
    # Reconstruct the builder's exact authored-source tree, then rerun it.
    clone = TMP / 'build_clone'
    for n, d in members.items():
        if n.startswith('candidate/'):
            dest = clone / 'native/unsolved_math_prioritization/attempts/30001184' / n[10:]
        elif n.startswith('chronology_and_reproduction/'):
            dest = clone / n.split('/', 1)[1]
        elif n.startswith('reviews/'):
            dest = clone / n
        elif n != 'PACKAGE_MANIFEST.json':
            dest = clone / 'publication' / ('PACKAGE_README.md' if n == 'README.md' else n)
        else:
            continue
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(d)
    builder = clone / 'publication/build_package.py'
    builder.write_bytes((PUB / 'build_package.py').read_bytes())
    p = invoke(['-I', str(builder)], clone, 'BUILDER_REPLAY')
    require(p.returncode == 0, 'builder replay failed')
    require((clone / 'publication/gns_verification.zip').read_bytes() == (PUB / 'gns_verification.zip').read_bytes(), 'builder not byte-reproducible')
    # Fixture copy redirects all self-selected temp directories into this review.
    ops = TMP / 'operations_clone'
    for n in ('prepare_integration.py', 'record_tracker.py', 'reviews/operations_01/check_helpers.py'):
        dest = ops / n
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes((AUDIT / n).read_bytes())
    for n, d in native_files.items():
        dest = ops / 'native/unsolved_math_prioritization/attempts/30001184' / n
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(d)
    operations = {}
    for label, flags in [('normal', []), ('optimized', ['-O'])]:
        p = invoke(['-I', *flags, str(ops / 'reviews/operations_01/check_helpers.py')], ops, 'OPERATIONS_' + label)
        require(p.returncode == 0, 'operational fixture failure: ' + label)
        operations[label] = json.loads(p.stdout)
    require(all(digest(p.read_bytes()) == inputs[str(p.relative_to(AUDIT))] for p in files), 'original input changed during checks')
    result = {'result': 'PASS', 'archive_members': len(names), 'manifested_files': m['file_count'],
        'manifest_sha256': digest(members['PACKAGE_MANIFEST.json']), 'original_native_files_identical': len(native_files),
        'full_replays': replays, 'negative_package_inventory_controls': controls,
        'builder_byte_identical_zip': True, 'operations_final_fixture_replays': operations,
        'input_files_unchanged': True, 'service_calls_or_mutations': 0}
    (HERE / 'PACKAGE_CHECK_RESULTS.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
