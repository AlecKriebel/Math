#!/usr/bin/env python3
"""Run assertion-enforcement and strict-inventory tamper tests in temporary copies.

Prints JSON to standard output. Does not change any packaged file. The assertion
probes deliberately alter an in-memory AST only; they are not mathematical tests.
"""
import sys
sys.dont_write_bytecode = True
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import tempfile
from validate_packet import validate, require

MODES = [('normal', []), ('-O', ['-O']), ('-OO', ['-OO'])]


def execute(script, flags, *args):
    return subprocess.run([sys.executable, '-B', *flags, str(script), *map(str, args)],
                          text=True, capture_output=True, timeout=180)


def manifest_write(root, data):
    (root/'MANIFEST.json').write_text(json.dumps(data, indent=2)+'\n')


def rehash(root, name):
    data = json.loads((root/'MANIFEST.json').read_text())
    raw = (root/name).read_bytes()
    for row in data['files']:
        if row['path'] == name:
            row['bytes'] = len(raw)
            row['sha256'] = hashlib.sha256(raw).hexdigest()
    manifest_write(root, data)


def mutate(root, case):
    manifest = root/'MANIFEST.json'
    data = json.loads(manifest.read_text())
    if case == 'changed_proof':
        with (root/'PROOF.md').open('ab') as out: out.write(b'\n')
    elif case == 'changed_proof_and_rehashed_manifest':
        with (root/'PROOF.md').open('ab') as out: out.write(b'\n')
        rehash(root, 'PROOF.md')
    elif case == 'changed_checker_and_rehashed_manifest':
        with (root/'verify_exact.py').open('ab') as out: out.write(b'\n')
        rehash(root, 'verify_exact.py')
    elif case == 'missing_file':
        (root/'CHECKS.md').unlink()
    elif case == 'extra_file':
        (root/'extra.txt').write_text('unexpected')
    elif case == 'extra_directory':
        (root/'unexpected').mkdir()
    elif case == 'symlink':
        (root/'CHECKS.md').unlink()
        (root/'CHECKS.md').symlink_to('README.md')
    elif case == 'duplicate_json_key':
        manifest.write_text(manifest.read_text().replace('{', '{"schema_version": 1,', 1))
    elif case == 'duplicate_file_record':
        data['files'].append(data['files'][0]); manifest_write(root, data)
    elif case == 'unsorted_file_records':
        data['files'].reverse(); manifest_write(root, data)
    elif case == 'unsafe_parent_path':
        data['files'][0]['path'] = '../PROOF.md'; manifest_write(root, data)
    elif case == 'absolute_path':
        data['files'][0]['path'] = '/PROOF.md'; manifest_write(root, data)
    elif case == 'boolean_byte_count':
        data['files'][0]['bytes'] = True; manifest_write(root, data)
    elif case == 'nonfinite_byte_count':
        data['files'][0]['bytes'] = float('nan'); manifest_write(root, data)
    elif case == 'unexpected_manifest_key':
        data['extra'] = 'unrecognized'; manifest_write(root, data)
    elif case == 'changed_target':
        data['target']['id'] = 'wrong'; manifest_write(root, data)
    elif case == 'preservation_map_rehashed':
        p = root/'PRESERVATION_MAP.json'; content=json.loads(p.read_text())
        content['artifacts'][0]['sha256'] = '0'*64
        p.write_text(json.dumps(content)+'\n'); rehash(root, p.name)
    elif case == 'missing_manifest_record':
        data['files'].pop(); manifest_write(root, data)
    else:
        raise ValueError('unknown mutation')


CASES = ['changed_proof', 'changed_proof_and_rehashed_manifest',
         'changed_checker_and_rehashed_manifest', 'missing_file', 'extra_file',
         'extra_directory', 'symlink', 'duplicate_json_key', 'duplicate_file_record',
         'unsorted_file_records', 'unsafe_parent_path', 'absolute_path',
         'boolean_byte_count', 'nonfinite_byte_count', 'unexpected_manifest_key',
         'changed_target', 'preservation_map_rehashed', 'missing_manifest_record']


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--skip-assertion-probes', action='store_true',
                        help='Inventory-only rerun; reports the omission explicitly.')
    args = parser.parse_args()
    root = Path(__file__).resolve().parent
    validate(root)
    positives, tamper, probes = [], [], []
    for label, flags in MODES:
        result = execute(root/'validate_packet.py', flags)
        require(result.returncode == 0, 'positive validator failed in ' + label)
        positives.append({'mode': label, 'status': 'PASS', 'result': json.loads(result.stdout)})
        for case in CASES:
            with tempfile.TemporaryDirectory(prefix='crossing-reader-tamper-') as tmp:
                target = Path(tmp)/'public'
                shutil.copytree(root, target)
                mutate(target, case)
                result = execute(root/'validate_packet.py', flags, target)
                require(result.returncode == 1 and result.stderr.startswith('FAIL: '),
                        'tamper was not explicitly rejected: ' + label + '/' + case)
                tamper.append({'mode': label, 'case': case, 'status': 'REJECTED'})
        if not args.skip_assertion_probes:
            for index in range(16):
                result = execute(root/'replay_checks.py', flags, '--probe-assertion', index)
                require(result.returncode == 3, 'assertion probe did not fail: ' + label + '/' + str(index))
                row = json.loads(result.stdout)
                require(row['status'] == 'EXPECTED_ASSERTION_FAILURE' and row['site'] == index,
                        'assertion probe result mismatch')
                probes.append({'mode': label, **row})
    print(json.dumps({'schema_version': 1, 'status': 'PASS', 'positive_validations': positives,
                      'tamper_tests': tamper, 'tamper_rejections': len(tamper),
                      'assertion_probes': probes, 'assertion_failures_confirmed': len(probes),
                      'assertion_probes_skipped': args.skip_assertion_probes,
                      'mathematical_passes_added': 0}, indent=2))


if __name__ == '__main__':
    try:
        main()
    except (OSError, ValueError, KeyError, TypeError, subprocess.TimeoutExpired) as error:
        print('FAIL: ' + str(error), file=sys.stderr)
        raise SystemExit(1)
