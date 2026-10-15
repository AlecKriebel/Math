#!/usr/bin/env python3
"""Read-only current input validation and genuine missing-gate guard probes."""
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
import zenodo_pr464 as zenodo
import register_pr464_tracker as tracker
import integrate_pr464_publication as integration

EXPECTED = {
    'operations/common.py': 'ba508397f2999c90f1d6e8bc1ef327f4258cc3a6e9acb4a7fe255051506a74ac',
    'operations/zenodo_pr464.py': 'f9bf46bb315cb62687504a261ef007f5b94e1ac3812137ff6af1866a09b50995',
    'operations/register_pr464_tracker.py': '6454154cc7a24fac9e5b85a0147ddfccc58e3db4f72b5f855c39ef0080e70d44',
    'operations/integrate_pr464_publication.py': '1f5629b7aea5c6de4dda3b67655540c9fae0a434130b872f485a662388f2ba5b',
    'build_preprint_package.py': '960c364c3b3dc10ecc6570f7069ea11150f90f8859f810872837a68161869074',
}
KIT_SHA = 'a91f961bcabadb15f92bb738c3194f0277cd47f1f87167ac8db8eb7c4fd3b9ca'
FREEZE_SHA = '6354507a17d9eca504e5db085621b645fc4afb9cd00291e74ee0e5a145c8a352'


def require(ok, message):
    if not ok:
        raise RuntimeError(message)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def spec(path):
    data = path.read_bytes()
    return {'sha256': sha(data), 'bytes': len(data)}


def save(name, value):
    (HERE / name).write_bytes(c.json_bytes(value))


def main():
    reviewed = {name: spec(AUDIT / name) for name in EXPECTED}
    for name, expected in EXPECTED.items():
        require(reviewed[name]['sha256'] == expected, 'Reviewed helper/builder changed: ' + name)
    kit = spec(REPO / 'zenodo_deposit_tool/zenodo.py')
    require(kit['sha256'] == KIT_SHA, 'Repository kit changed')
    for name in ('operations/README.md', 'operations/check_operations.py', 'check_archive_builder_guards.py',
                 'SOURCE_RECEIPT.json', 'MATHEMATICAL_ACCEPTANCE_GATE.json', 'BRANCH_INSTALL_PLAN.json', 'PACKAGE_REVIEW_INPUT_2.json'):
        reviewed[name] = spec(AUDIT / name)
    require(reviewed['PACKAGE_REVIEW_INPUT_2.json']['sha256'] == FREEZE_SHA, 'Accepted review candidate changed')
    save('REVIEWED_INPUTS.json', {'scope': 'Exact read-only operational inputs. No actual final gate exists; this is not paper acceptance.',
         'pr': 464, 'problem_id': '30004807', 'original_pr_head': c.ORIGINAL,
         'files': reviewed, 'unchanged_repository_kit': kit, 'real_external_calls': 0})
    source, payloads = c.validate_source_local()
    base = c.PREFIX
    refs = []
    inputs = json.loads(payloads[base + 'audit/FROZEN_INPUTS.json'])
    for item in inputs['files']:
        name = base + 'release/' + item['path']; data = payloads[name]
        require(len(data) == item['bytes'] and sha(data) == item['sha256'], 'Historical release reference changed')
        refs.append({'path': name, 'sha256': sha(data), 'bytes': len(data)})
    manifest = json.loads(payloads[base + 'audit/AUDIT_MANIFEST.json'])
    for name, item in manifest['portable_files'].items():
        name = base + 'audit/' + name; data = payloads[name]
        require(len(data) == item['bytes'] and sha(data) == item['sha256'], 'Historical audit reference changed')
        refs.append({'path': name, 'sha256': sha(data), 'bytes': len(data)})
    require(len(refs) == 11, 'Available reference count is not eleven')
    unattested = inputs['author_manifest_sha256']
    require(unattested not in {sha(data) for data in payloads.values()}, 'Unexpected standalone manifest bytes appeared')
    save('SOURCE_VALIDATION.json', {'pr': 464, 'problem_id': '30004807', 'head_sha': c.ORIGINAL,
         'scope_gate': 'exact claimed_solved', 'original_attempt_count': '1/5',
         'verified_snapshot_files': [{'path': p, 'sha256': sha(b), 'bytes': len(b)} for p, b in sorted(payloads.items())],
         'available_internal_reference_count': 11, 'available_internal_references': refs,
         'unattested_standalone_author_manifest_sha256': unattested,
         'standalone_bytes_or_path_supplied': False, 'all_available_verified': True, 'real_external_calls': 0})
    freeze = json.loads((AUDIT / 'PACKAGE_REVIEW_INPUT_2.json').read_text())
    require(freeze['pr'] == 464 and freeze['problem'] == '30004807' and freeze['original_head'] == c.ORIGINAL,
            'Actual reviewed candidate identity differs')
    for field, name in [('source_receipt_sha256', 'SOURCE_RECEIPT.json'),
                        ('mathematical_acceptance_gate_sha256', 'MATHEMATICAL_ACCEPTANCE_GATE.json'),
                        ('branch_install_plan_sha256', 'BRANCH_INSTALL_PLAN.json')]:
        require(freeze[field] == sha((AUDIT / name).read_bytes()), 'Actual reviewed candidate cross-binding differs')
    for name, item in freeze['files'].items():
        c.checked_bytes(AUDIT / 'package', name, item)
    sums = json.loads((AUDIT / 'package/SHA256SUMS.json').read_text())['files']
    package = AUDIT / 'package'
    with zipfile.ZipFile(package / c.ZIP_NAME) as archive:
        members = archive.infolist(); names = [m.filename for m in members]
        require(len(set(names)) == len(names) and set(names) == set(sums) | {'SHA256SUMS.json'}, 'Actual ZIP selection differs')
        require(archive.testzip() is None, 'Actual ZIP CRC failure')
        for member in members:
            c.relative(member.filename)
            require(not member.is_dir() and (member.external_attr >> 16) & 0o170000 != 0o120000,
                    'Actual ZIP has directory or symlink')
            require(archive.read(member) == c.safe_file(package, member.filename).read_bytes(), 'Actual ZIP byte drift')
        for name, item in sums.items():
            c.checked_bytes(package, name, item)
        plan = json.loads((AUDIT / 'BRANCH_INSTALL_PLAN.json').read_text())
        expected = set(names) | set(freeze['files'])
        installs = {}
        for item in plan['entries']:
            local = c.safe_file(REPO, item['local_program_path'])
            require(local.is_relative_to(package), 'Actual install escapes package')
            name = local.relative_to(package).as_posix()
            require(item['repository_destination'] == c.PREPRINT + name and name not in installs,
                    'Actual install mapping differs or duplicates')
            installs[name] = c.checked_bytes(REPO, item['local_program_path'], item)
        require(set(installs) == expected, 'Actual positive install selection differs')
    for path, data in payloads.items():
        history = 'verification/frozen_history/' + path.removeprefix(base)
        require(installs[history] == data, 'Actual historical package copy differs')
    metadata = json.loads((package / 'metadata.json').read_text())
    deposit = json.loads((package / 'deposit.json').read_text())
    require(deposit['metadata'] == metadata, 'Actual canonical deposit metadata differs')
    require(deposit['files'] == [{'path': 'manuscript.pdf', 'name': 'regular_zas_bianchi_defect.pdf'}, {'path': c.ZIP_NAME}],
            'Actual public deposit mapping differs')
    save('ACTUAL_CANDIDATE_VALIDATION.json', {'pr': 464, 'reviewed_manifest': 'PACKAGE_REVIEW_INPUT_2.json',
         'reviewed_manifest_sha256': FREEZE_SHA, 'frozen_top_level_file_count': len(freeze['files']),
         'verified_zip_entries': len(names), 'verified_manifest_payloads': len(sums),
         'verified_install_targets': len(installs), 'all_current_payload_bytes_verified': True,
         'source_math_plan_cross_bindings_verified': True, 'historical_sources_unchanged': 13,
         'deposit_exact_canonical_metadata': True, 'final_publication_gate_absent': not (AUDIT / 'FINAL_ACCEPTANCE_GATE.json').exists(),
         'real_external_calls': 0, 'full_paper_review_or_publication_acceptance': False})
    require(not (AUDIT / 'FINAL_ACCEPTANCE_GATE.json').exists(), 'Actual absent-gate probe prerequisite changed')
    calls = []
    def denied(*args, **kwargs):
        calls.append('service dispatch'); raise RuntimeError('OFFLINE BOUNDARY DENIED')
    probes = [('gate', c.validate_gate), ('default_local_check', lambda: zenodo.run()),
              ('stage_apply', lambda: zenodo.run('stage', True)),
              ('publish_apply', lambda: zenodo.run('publish', True, 123456)),
              ('tracker_apply', lambda: tracker.run(True)), ('integration_apply', lambda: integration.run(True))]
    rows = []
    with patch.object(c, 'github', denied), patch.object(c, 'gws', denied), \
         patch.object(c.subprocess, 'run', denied), patch.object(socket, 'create_connection', denied), \
         patch.object(zenodo, 'build_opener', denied):
        for name, function in probes:
            try:
                function()
            except RuntimeError as error:
                require('Missing or escaping file: FINAL_ACCEPTANCE_GATE.json' in str(error), 'Wrong actual absent-gate rejection')
                rows.append({'probe': name, 'intended_missing_final_gate_rejection': True, 'real_external_calls': 0})
            else:
                raise RuntimeError('Actual absent final gate accepted')
    require(not calls, 'Actual absent final gate reached a service dispatch')
    save('ACTUAL_ABSENT_GATE_PROBES.json', {'all_passed': True, 'case_count': len(rows), 'cases': rows,
         'actual_gate_absent': True, 'before_any_dispatch': True, 'real_external_calls': 0})
    print(json.dumps({'all_passed': True, 'snapshot_files': 13, 'references': 11,
                      'zip_entries': len(names), 'install_targets': len(installs), 'absent_gate_probes': 6,
                      'real_external_calls': 0}, sort_keys=True))


if __name__ == '__main__':
    main()
