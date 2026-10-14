#!/usr/bin/env python3
"""Test the packaging validator on isolated mutated copies in all Python modes.

This harness never changes the sealed reader or its accepted original files.
The controls exercise selected rejection paths, not every possible fault.
"""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parent
MODES = [('normal', []), ('O', ['-O']), ('OO', ['-OO'])]
CASES = ['changed_proof', 'missing_proof', 'unexpected_pdf', 'expanded_scope',
         'nonboolean_scope', 'changed_anchor_rehashed', 'duplicate_json_key',
         'duplicate_manifest_member', 'escaping_path', 'symbolic_link',
         'boolean_byte_count', 'failed_replay_rehashed', 'private_marker_rehashed',
         'publication_flag', 'missing_reader_resealed', 'false_replay_value_rehashed',
         'wrong_replay_mode_rehashed', 'wrong_replay_stdout_rehashed',
         'nested_proof_pins_rehashed', 'nested_scope_manifest_rehashed',
         'input_manifest_rehashed', 'copy_map_rehashed', 'wrong_han_author_rehashed',
         'extra_manifest_field', 'reindexed_disposition', 'unlisted_text_file']


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def mutate(root, case):
    manifest_path = root / 'MANIFEST.json'
    manifest = json.loads(manifest_path.read_text())
    proof_name = 'accepted/core/COUNTEREXAMPLE.md'
    proof = root / proof_name

    def rehash(name):
        data = (root / name).read_bytes()
        for item in manifest['files']:
            if item['path'] == name:
                item['bytes'] = len(data)
                item['sha256'] = hashlib.sha256(data).hexdigest()

    if case == 'changed_proof':
        proof.write_bytes(proof.read_bytes() + b'\n')
        expected = 'Byte count mismatch'
    elif case == 'missing_proof':
        proof.unlink()
        expected = 'File membership differs'
    elif case == 'unexpected_pdf':
        (root / 'unexpected.pdf').write_bytes(b'Packaging negative control only')
        expected = 'Unexpected file type'
    elif case == 'expanded_scope':
        manifest['scope_flags']['arbitrary_reindexing_claim'] = True
        expected = 'Scope flags exceed'
    elif case == 'nonboolean_scope':
        manifest['scope_flags']['single_generator'] = 1
        expected = 'Scope flags must be booleans'
    elif case == 'changed_anchor_rehashed':
        proof.write_bytes(proof.read_bytes() + b'\n')
        rehash(proof_name)
        expected = 'Frozen original anchor mismatch'
    elif case == 'duplicate_json_key':
        text = manifest_path.read_text()
        manifest_path.write_text(text.replace('{', '{"schema_version": 1,', 1))
        return 'Duplicate JSON object key'
    elif case == 'duplicate_manifest_member':
        manifest['files'].append(manifest['files'][0].copy())
        expected = 'Duplicate manifest member'
    elif case == 'escaping_path':
        manifest['files'][0]['path'] = '../outside.md'
        expected = 'Unsafe or noncanonical relative path'
    elif case == 'symbolic_link':
        (root / 'unexpected_link.md').symlink_to(proof)
        expected = 'Symbolic links are not admitted'
    elif case == 'boolean_byte_count':
        manifest['files'][0]['bytes'] = True
        expected = 'Invalid byte count'
    elif case == 'failed_replay_rehashed':
        name = 'REPLAY_EVIDENCE.json'
        path = root / name
        data = json.loads(path.read_text())
        key = next(iter(data['runs'][0]['report']['checks']))
        data['runs'][0]['report']['checks'][key] = False
        path.write_text(json.dumps(data))
        rehash(name)
        expected = 'Failed recorded arithmetic'
    elif case == 'private_marker_rehashed':
        # Build the marker from parts so the control source itself remains clean.
        name = 'README.md'
        path = root / name
        path.write_text(path.read_text() + '\n/' + 'work' + 'space/example\n')
        rehash(name)
        expected = 'Private-path/material marker found'
    elif case == 'publication_flag':
        manifest['publication_performed'] = True
        expected = 'Publication state differs'
    elif case == 'missing_reader_resealed':
        (root / 'README.md').unlink()
        manifest['files'] = [r for r in manifest['files'] if r['path'] != 'README.md']
        expected = 'Required reader membership differs'
    elif case in {'false_replay_value_rehashed', 'wrong_replay_mode_rehashed', 'wrong_replay_stdout_rehashed'}:
        name = 'REPLAY_EVIDENCE.json'
        path = root / name
        data = json.loads(path.read_text())
        if case == 'false_replay_value_rehashed':
            data['runs'][0]['report']['values']['lower_frame_bound'] = '-1'
            expected = 'Recorded scalar values differ'
        elif case == 'wrong_replay_mode_rehashed':
            data['runs'][1]['report']['optimization_flag'] = 0
            expected = 'Recorded optimization flag differs'
        else:
            data['runs'][0]['stdout_sha256'] = '0' * 64
            expected = 'Recorded stdout digest differs'
        path.write_text(json.dumps(data))
        rehash(name)
    elif case in {'nested_proof_pins_rehashed', 'nested_scope_manifest_rehashed'}:
        name = ('scope_adjudication/PROOF_PINS.json' if case == 'nested_proof_pins_rehashed'
                else 'scope_adjudication/PUBLIC_MANIFEST.json')
        path = root / name
        data = json.loads(path.read_text())
        data['artifacts'][0]['sha256'] = '0' * 64
        path.write_text(json.dumps(data))
        rehash(name)
        expected = 'Frozen original anchor mismatch'
    elif case == 'input_manifest_rehashed':
        name = 'INPUT_MANIFEST.json'
        path = root / name
        data = json.loads(path.read_text())
        data['files'][0]['sha256'] = '0' * 64
        path.write_text(json.dumps(data))
        rehash(name)
        expected = 'Preserved input manifest differs'
    elif case == 'copy_map_rehashed':
        name = 'ORIGINAL_ARTIFACTS.json'
        path = root / name
        data = json.loads(path.read_text())
        data['originals'][0]['source_collection'] = 'changed'
        path.write_text(json.dumps(data))
        rehash(name)
        expected = 'Byte count mismatch'
    elif case == 'wrong_han_author_rehashed':
        name = 'SOURCE_METADATA.json'
        path = root / name
        data = json.loads(path.read_text())
        data['sources'][-1]['authors'][-1] = 'Deguang Han'
        path.write_text(json.dumps(data))
        rehash(name)
        expected = 'Daubechies-Han authorship metadata differs'
    elif case == 'extra_manifest_field':
        manifest['unsupported'] = True
        expected = 'Manifest fields differ'
    elif case == 'reindexed_disposition':
        manifest['disposition'] = 'Arbitrary reindexing excluded'
        expected = 'Disposition differs'
    elif case == 'unlisted_text_file':
        (root / 'extra.md').write_text('Unsealed test file')
        expected = 'File membership differs'
    else:
        raise RuntimeError('Unknown control')
    manifest_path.write_text(json.dumps(manifest))
    return expected


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    if args.output:
        output = args.output.resolve()
        require(output != ROOT and ROOT not in output.parents, 'Control output must be outside sealed reader')
    successful = []
    controls = []
    for mode, flags in MODES:
        result = subprocess.run([sys.executable, *flags, str(ROOT / 'verify_bundle.py')],
                                capture_output=True, text=True, timeout=30)
        require(result.returncode == 0 and not result.stderr.strip(), 'Baseline failed: ' + mode)
        successful.append({'mode': mode, 'result': json.loads(result.stdout)})
        for case in CASES:
            with tempfile.TemporaryDirectory(prefix='wavelet_package_control_') as temporary:
                root = Path(temporary) / 'reader'
                shutil.copytree(ROOT, root)
                expected = mutate(root, case)
                result = subprocess.run([sys.executable, *flags, str(root / 'verify_bundle.py')],
                                        capture_output=True, text=True, timeout=30)
                require(result.returncode != 0 and expected in result.stderr,
                        'Expected rejection missing: ' + mode + ', ' + case)
                controls.append({'mode': mode, 'case': case, 'expected_rejection': expected,
                                 'exit_code': result.returncode, 'expected_rejection_observed': True})
    report = {'status': 'PASS', 'baseline_successful_runs': successful,
              'case_count': len(CASES), 'successful_negative_controls': len(controls),
              'originals_modified': False, 'controls': controls,
              'scope': 'Packaging validator rejection paths only; no mathematical proof certification.'}
    payload = json.dumps(report, indent=2, sort_keys=True) + '\n'
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(payload)
        print(json.dumps({'status': 'PASS', 'successful_negative_controls': len(controls)}))
    else:
        print(payload, end='')


if __name__ == '__main__':
    main()
