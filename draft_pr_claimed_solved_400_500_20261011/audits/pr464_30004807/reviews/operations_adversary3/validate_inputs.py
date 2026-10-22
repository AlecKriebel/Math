#!/usr/bin/env python3
"""Reviewer 3 read-only byte inventory and genuine absent-gate controls."""
import hashlib
import json
import socket
import sys
import zipfile
from pathlib import Path
from unittest.mock import patch

HERE = Path(__file__).resolve().parent
AUDIT = HERE.parent.parent
REPO = AUDIT.parents[2]
sys.path.insert(0, str(AUDIT / 'operations'))
import common as c
import zenodo_pr464 as z
import register_pr464_tracker as t
import integrate_pr464_publication as i

EXPECTED = {
    'operations/common.py': 'ba508397f2999c90f1d6e8bc1ef327f4258cc3a6e9acb4a7fe255051506a74ac',
    'operations/zenodo_pr464.py': 'f9bf46bb315cb62687504a261ef007f5b94e1ac3812137ff6af1866a09b50995',
    'operations/register_pr464_tracker.py': '6454154cc7a24fac9e5b85a0147ddfccc58e3db4f72b5f855c39ef0080e70d44',
    'operations/integrate_pr464_publication.py': '1f5629b7aea5c6de4dda3b67655540c9fae0a434130b872f485a662388f2ba5b',
    'build_preprint_package.py': '3a893ba4f11fa6681e6dbd7c92366dfacde8658eefb67a25acddfd8e8c17c7f5',
}
KIT = 'a91f961bcabadb15f92bb738c3194f0277cd47f1f87167ac8db8eb7c4fd3b9ca'
FREEZE = '6354507a17d9eca504e5db085621b645fc4afb9cd00291e74ee0e5a145c8a352'

def require(value, message):
    if not value:
        raise RuntimeError(message)

def sha(data):
    return hashlib.sha256(data).hexdigest()

def spec(path):
    data = path.read_bytes()
    return {'sha256': sha(data), 'bytes': len(data)}

def save(name, value):
    (HERE / name).write_bytes(c.json_bytes(value))

def main():
    inventory = {name: spec(AUDIT / name) for name in EXPECTED}
    for name, digest in EXPECTED.items():
        require(inventory[name]['sha256'] == digest, 'Reviewed source changed: ' + name)
    kit_spec = spec(REPO / 'zenodo_deposit_tool/zenodo.py')
    require(kit_spec['sha256'] == KIT, 'Unchanged repository kit differs')
    for name in ['operations/README.md', 'operations/check_operations.py', 'operations/REPAIR_RECEIPT.json',
                 'ARCHIVE_OUTPUT_REPAIR_RECEIPT.json', 'SOURCE_RECEIPT.json', 'MATHEMATICAL_ACCEPTANCE_GATE.json',
                 'BRANCH_INSTALL_PLAN.json', 'PACKAGE_REVIEW_INPUT_2.json',
                 'reviews/package_round1/FULL_PACKAGE_REVIEW.md', 'reviews/package_round1/RESULT.json',
                 'reviews/package_round2/FULL_PACKAGE_REVIEW.md', 'reviews/package_round2/RESULT.json']:
        inventory[name] = spec(AUDIT / name)
    require(inventory['PACKAGE_REVIEW_INPUT_2.json']['sha256'] == FREEZE, 'Reviewed freeze changed')
    save('REVIEWED_INPUTS.json', {'pr': 464, 'problem_id': '30004807', 'original_head': c.ORIGINAL,
         'files': inventory, 'unchanged_repository_kit': kit_spec, 'real_external_calls': 0,
         'scope': 'Exact input inventory; not a publication acceptance gate.'})
    receipt, sources = c.validate_source_local()
    refs = []
    frozen = json.loads(sources[c.PREFIX + 'audit/FROZEN_INPUTS.json'])
    for item in frozen['files']:
        name = c.PREFIX + 'release/' + item['path']
        data = sources[name]
        require(sha(data) == item['sha256'] and len(data) == item['bytes'], 'Available release reference changed')
        refs.append({'path': name, 'sha256': sha(data), 'bytes': len(data)})
    historical = json.loads(sources[c.PREFIX + 'audit/AUDIT_MANIFEST.json'])
    for name, item in historical['portable_files'].items():
        name = c.PREFIX + 'audit/' + name
        data = sources[name]
        require(sha(data) == item['sha256'] and len(data) == item['bytes'], 'Available audit reference changed')
        refs.append({'path': name, 'sha256': sha(data), 'bytes': len(data)})
    require(len(refs) == 11 and len(sources) == 13, 'Historical reference counts differ')
    unattested = frozen['author_manifest_sha256']
    require(unattested not in {sha(data) for data in sources.values()}, 'Unattested author manifest unexpectedly supplied')
    freeze = json.loads((AUDIT / 'PACKAGE_REVIEW_INPUT_2.json').read_bytes())
    require((freeze['pr'], freeze['problem'], freeze['original_head']) == (464, '30004807', c.ORIGINAL), 'Freeze identity mismatch')
    for field, name in [('source_receipt_sha256', 'SOURCE_RECEIPT.json'),
                        ('mathematical_acceptance_gate_sha256', 'MATHEMATICAL_ACCEPTANCE_GATE.json'),
                        ('branch_install_plan_sha256', 'BRANCH_INSTALL_PLAN.json')]:
        require(freeze[field] == sha((AUDIT / name).read_bytes()), 'Freeze cross-binding mismatch')
    for name, item in freeze['files'].items():
        c.checked_bytes(c.PACKAGE, name, item)
    manifest = json.loads((c.PACKAGE / 'SHA256SUMS.json').read_bytes())['files']
    with zipfile.ZipFile(c.PACKAGE / c.ZIP_NAME) as archive:
        entries = archive.infolist()
        names = [entry.filename for entry in entries]
        require(len(names) == len(set(names)) and set(names) == set(manifest) | {'SHA256SUMS.json'}, 'ZIP exact selection mismatch')
        require(archive.testzip() is None, 'ZIP CRC mismatch')
        for entry in entries:
            c.relative(entry.filename)
            require(not entry.is_dir() and (entry.external_attr >> 16) & 0o170000 != 0o120000, 'Unsafe ZIP entry')
            require(archive.read(entry) == c.safe_file(c.PACKAGE, entry.filename).read_bytes(), 'ZIP/local bytes differ')
        for name, item in manifest.items():
            c.checked_bytes(c.PACKAGE, name, item)
    plan = json.loads((AUDIT / 'BRANCH_INSTALL_PLAN.json').read_bytes())
    installs = {}
    for item in plan['entries']:
        path = c.safe_file(REPO, item['local_program_path'])
        require(path.is_relative_to(c.PACKAGE), 'Install source outside package')
        name = path.relative_to(c.PACKAGE).as_posix()
        require(name not in installs and item['repository_destination'] == c.PREPRINT + name, 'Duplicate or changed mapping')
        installs[name] = c.checked_bytes(REPO, item['local_program_path'], item)
    require(set(installs) == set(names) | set(freeze['files']), 'Exact install selection mismatch')
    for name, data in sources.items():
        require(installs['verification/frozen_history/' + name.removeprefix(c.PREFIX)] == data, 'Bundled historical source changed')
    metadata = json.loads((c.PACKAGE / 'metadata.json').read_bytes())
    deposit = json.loads((c.PACKAGE / 'deposit.json').read_bytes())
    require(deposit == {'metadata': metadata, 'files': [{'path': 'manuscript.pdf', 'name': 'regular_zas_bianchi_defect.pdf'}, {'path': c.ZIP_NAME}]}, 'Canonical metadata/upload mapping mismatch')
    for round_number in [1, 2]:
        result = json.loads((AUDIT / f'reviews/package_round{round_number}/RESULT.json').read_bytes())
        require(result.get('verdict') == 'PASS', 'Actual package review is not PASS')
        for key in ['blocking_issue_count', 'required_correction_count']:
            require(type(result.get(key)) is int and result[key] == 0, 'Actual package review issue count invalid')
        require(result.get('input_manifest_sha256') == FREEZE, 'Actual package review binds a different input')
    require(not (AUDIT / 'FINAL_ACCEPTANCE_GATE.json').exists(), 'Absent-gate prerequisite changed')
    calls = []
    def deny(*args, **kwargs):
        calls.append('service dispatch')
        raise RuntimeError('REAL SERVICE BOUNDARY DENIED')
    probes = [('validate_gate', c.validate_gate), ('local_check', lambda: z.run()),
              ('stage_apply', lambda: z.run('stage', True)), ('publish_apply', lambda: z.run('publish', True, 123456)),
              ('tracker_apply', lambda: t.run(True)), ('integration_apply', lambda: i.run(True)),
              ('integration_reconcile', i.reconcile)]
    controls = []
    with patch.object(c, 'github', deny), patch.object(c, 'gws', deny), \
         patch.object(c.subprocess, 'run', deny), patch.object(socket, 'create_connection', deny), \
         patch.object(z, 'build_opener', deny):
        for name, fn in probes:
            try:
                fn()
            except RuntimeError as error:
                require('Missing or escaping file: FINAL_ACCEPTANCE_GATE.json' in str(error), 'Incidental missing-gate rejection')
            else:
                raise RuntimeError('Missing final gate accepted')
            controls.append({'case': name, 'passed': True, 'real_external_calls': 0})
    require(not calls, 'Actual missing gate dispatched a service')
    save('ACTUAL_INPUT_VALIDATION.json', {'all_passed': True, 'pr': 464, 'problem_id': '30004807',
         'input_manifest_sha256': FREEZE, 'frozen_top_level_files': len(freeze['files']),
         'zip_entries': len(names), 'manifest_payloads': len(manifest), 'install_targets': len(installs),
         'historical_files': len(sources), 'available_internal_references': refs,
         'unattested_standalone_author_manifest_sha256': unattested, 'standalone_manifest_bytes_or_path_supplied': False,
         'current_metadata_and_upload_mapping_exact': True, 'two_distinct_actual_clean_package_review_results_checked': True,
         'missing_final_gate_probes': controls, 'real_external_calls': 0,
         'publication_stage_append_or_branch_write_performed': False})
    print(json.dumps({'all_passed': True, 'historical_files': len(sources), 'available_references': len(refs),
                      'zip_entries': len(names), 'install_targets': len(installs), 'actual_missing_gate_probes': len(probes),
                      'real_external_calls': 0}, sort_keys=True))

if __name__ == '__main__':
    main()
