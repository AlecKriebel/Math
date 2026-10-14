#!/usr/bin/env python3
"""Strict local file inventory, hash, schema, and preserved-input validation.

No network access or mutation. All required checks use explicit exceptions, not
assert statements. This validator does not claim signature authenticity.
"""
import sys
sys.dont_write_bytecode = True
import hashlib
import json
from pathlib import Path
import re
import stat

# Filled at assembly from the frozen authored-input preservation map.
PRESERVED = {'PROOF.md': (15940, '6ec0d8fbf2e583e02fd775e24be762144d09ae3e8de9a835a80856e27527746e'), 'CHECKS.md': (1646, '69c6243a74ccb5b87fd5a95919d24151d24a1ab80b21183391256ebdc28e6242'), 'verify_exact.py': (7526, 'c86870f318768b0fe9cd89b6b2f83d62dec34640bf402a88aff6af9e2fcd7ca7'), 'exact_checks.json': (14223, '5ea80af62ea2a954e12f49f91f626e8bb9a8749e65e2192edc7cbf01a5228e83'), 'ACCEPTANCE.md': (12735, '210e2af0dec5b1bc0e3a6cf56f63e3ce40335528b251f9502fec62fac89475be'), 'AUDIT_MANIFEST.json': (2963, 'ab5418294d23a290117ff1f47c0dc6cbee99f0661246946026b5e73265362428'), 'SOURCE_SCOPE_CLARIFICATION.md': (12949, '963d36d9d5b970fab8c398ea63758928eeccda878db0eaec83eac421d3829db7'), 'CLARIFICATION_SOURCE_MANIFEST.json': (4095, '065fa407dbe66b5d8ee70ed4c947f769d881fef5b09f377bb5bd5be4bdfd9803'), 'SOURCE_SCOPE_AND_PRIOR_ART.md': (11181, '438a3f0f8a52a154d0598911172b627e6ad78981fb1825b841602f79653fe544'), 'SOURCE_MANIFEST.json': (5215, 'e3cf425ff67a9ea6f5bbb5d0d762eda6f7e2bf84321455c4f5c24a8ba8771250'), 'PROOF_PINS.json': (986, 'a8e89a1ba262b72463408c5d620cd70aea350cbf1948ef0dfca5be441f92e607'), 'SOURCE_PUBLIC_FILES.json': (594, '6bbee93a2e8e0fe96114fc963b86a6bff5850a4295ee6fff82f1a4d1c54081ab')}
REQUIRED = {'SOURCE_SCOPE_CLARIFICATION.md', 'SOURCE_VERSION_NOTES.md', 'ACCEPTANCE.md', 'replay_checks.py', 'REPLAY_REPORT.json', 'validate_packet.py', 'CLARIFICATION_SOURCE_MANIFEST.json', 'PRESERVATION_MAP.json', 'TEST_REPORT.json', 'PROOF.md', 'VERIFICATION.md', 'test_packet.py', 'README.md', 'AUDIT_MANIFEST.json', 'CHECKS.md', 'SOURCE_PUBLIC_FILES.json', 'verify_exact.py', 'SOURCE_MANIFEST.json', 'exact_checks.json', 'SOURCE_SCOPE_AND_PRIOR_ART.md', 'PROOF_PINS.json'}

# Immutable historical evidence: these describe the 22-file prepared input.
# Bind complete bytes so resealing cannot silently relabel test modes or provenance.
FROZEN_HISTORY = {'PRESERVATION_MAP.json': (4302, '29e628a86bdfce5c8870dec9a81744f081ad5ebcee64c7e33f59f4b3cfdff8bd'), 'REPLAY_REPORT.json': (2186, 'e94c7923b01489964d7dbfd6f6bee2495497698c52ad8402a5ab7e3f7bb9cb68'), 'TEST_REPORT.json': (17160, '698ba83590ce6a5b172fac0fb7f4e7734d38aca7c8f55b901200d2c8b1a385e7')}
REQUIRED |= {'INTEGRATION_ACCEPTANCE.md', 'INTEGRATION_EVIDENCE.json', 'SOURCE_LINK_REVIEW.json', 'REVIEW_CHANGE_MAP.json', 'review_checks.py'}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def reject_constant(value):
    raise ValueError('non-finite JSON value: ' + value)


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        require(key not in result, 'duplicate JSON key: ' + key)
        result[key] = value
    return result


def read_json(path):
    return json.loads(path.read_text(encoding='utf-8'), object_pairs_hook=unique_object,
                      parse_constant=reject_constant)


def regular(path):
    require(stat.S_ISREG(path.lstat().st_mode), 'not a regular non-symlink file: ' + path.name)


def validate(root):
    require(root.is_dir() and not root.is_symlink(), 'packet root must be a real directory')
    actual = set()
    for path in root.iterdir():
        regular(path)
        actual.add(path.name)
    require(actual == REQUIRED | {'MANIFEST.json'}, 'file inventory mismatch')
    manifest = read_json(root / 'MANIFEST.json')
    require(type(manifest) is dict and set(manifest) == {'schema_version', 'target', 'scope', 'files'}, 'manifest schema mismatch')
    require(type(manifest['schema_version']) is int and manifest['schema_version'] == 1, 'manifest version mismatch')
    require(type(manifest['target']) is dict and manifest['target'] == {'row': 1782, 'id': '30000215', 'code': 'OWR-822-007'}, 'target mismatch')
    require(type(manifest['target']['row']) is int, 'invalid target row type')
    require(manifest['scope'] == 'Authored reader and supplemental verification only; no new mathematical pass.', 'scope mismatch')
    require(type(manifest['files']) is list, 'file records must be an array')
    rows = {}
    previous = ''
    for row in manifest['files']:
        require(type(row) is dict and set(row) == {'path', 'bytes', 'sha256'}, 'file record schema mismatch')
        name = row['path']
        require(type(name) is str and re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_.-]*', name) is not None, 'unsafe manifest path')
        require(name > previous and name not in rows, 'file records must be unique and sorted')
        previous = name
        require(name in REQUIRED, 'unrecognized manifest artifact')
        require(type(row['bytes']) is int and row['bytes'] >= 0, 'invalid byte count')
        require(type(row['sha256']) is str and re.fullmatch(r'[0-9a-f]{64}', row['sha256']) is not None, 'invalid digest')
        raw = (root / name).read_bytes()
        require(len(raw) == row['bytes'], 'byte count mismatch: ' + name)
        require(hashlib.sha256(raw).hexdigest() == row['sha256'], 'digest mismatch: ' + name)
        rows[name] = row
    require(set(rows) == REQUIRED, 'manifest coverage mismatch')
    for name, (length, digest) in PRESERVED.items():
        require((rows[name]['bytes'], rows[name]['sha256']) == (length, digest), 'preserved source pin mismatch: ' + name)
    for name, expected in FROZEN_HISTORY.items():
        require((rows[name]['bytes'], rows[name]['sha256']) == expected,
                'frozen historical evidence mismatch: ' + name)
    preservation = read_json(root / 'PRESERVATION_MAP.json')
    require(type(preservation) is dict and set(preservation) == {'schema_version', 'statement', 'artifacts'}, 'preservation schema mismatch')
    require(type(preservation['schema_version']) is int and preservation['schema_version'] == 1, 'preservation version mismatch')
    require(type(preservation['artifacts']) is list and len(preservation['artifacts']) == len(PRESERVED), 'preservation record count mismatch')
    seen = set()
    for row in preservation['artifacts']:
        require(type(row) is dict and set(row) == {'artifact', 'source_artifact', 'source_role', 'transformation', 'bytes', 'sha256'}, 'preservation record schema mismatch')
        name = row['artifact']
        require(name in PRESERVED and name not in seen, 'preservation artifact mismatch')
        seen.add(name)
        require(type(row['bytes']) is int and (row['bytes'], row['sha256']) == PRESERVED[name], 'preservation pin mismatch')
        require(row['transformation'] == 'none; byte-for-byte copy; filename may differ', 'preservation transformation mismatch')
        require(type(row['source_artifact']) is str and '/' not in row['source_artifact'] and '\\' not in row['source_artifact'], 'invalid source basename')
        require(type(row['source_role']) is str and bool(row['source_role']), 'invalid source role')
    require(seen == set(PRESERVED), 'preservation coverage mismatch')
    audit = read_json(root / 'AUDIT_MANIFEST.json')
    require(audit['verdict'] == 'ACCEPTED' and audit['outstanding_issues'] == [], 'audit acceptance mismatch')
    require((audit['subject']['bytes'], audit['subject']['sha256']) == PRESERVED['PROOF.md'], 'audit proof binding mismatch')
    require((audit['audit']['bytes'], audit['audit']['sha256']) == PRESERVED['ACCEPTANCE.md'], 'audit report binding mismatch')
    pins = read_json(root / 'PROOF_PINS.json')
    for key, name in [('proof','PROOF.md'), ('mathematical_acceptance','ACCEPTANCE.md'), ('audit_manifest','AUDIT_MANIFEST.json')]:
        require((pins[key]['bytes'], pins[key]['sha256']) == PRESERVED[name], 'source review binding mismatch')
    source_inventory = read_json(root / 'SOURCE_PUBLIC_FILES.json')
    expected_source = {'PROOF_PINS.json', 'SOURCE_MANIFEST.json', 'SOURCE_SCOPE_AND_PRIOR_ART.md'}
    require({r['artifact'] for r in source_inventory['public_files']} == expected_source, 'source inventory mismatch')
    for row in source_inventory['public_files']:
        require((row['bytes'], row['sha256']) == PRESERVED[row['artifact']], 'source inventory pin mismatch')
    for name in REQUIRED:
        if name.endswith('.json'):
            read_json(root / name)
    replays = read_json(root / 'REPLAY_REPORT.json')
    require(replays['status'] == 'PASS' and replays['mathematical_passes_added'] == 0, 'replay report status mismatch')
    require(len(replays['complete_replays']) == 3, 'replay mode count mismatch')
    for row, mode, level in zip(replays['complete_replays'], ['normal', '-O', '-OO'], [0, 1, 2]):
        require(row['mode'] == mode and row['outer_optimization'] == level and row['status'] == 'PASS', 'replay mode mismatch')
        require(row['checker_compilation_optimization'] == 0 and row['compiled_assertion_sites'] == 16, 'replay assertion setting mismatch')
        require(row['compiled_assertion_failure_instructions'] >= 16, 'replay assertion coverage mismatch')
        require(row['byte_identical_result'] is True, 'replay byte equality missing')
        require((row['result_bytes'], row['result_sha256']) == PRESERVED['exact_checks.json'], 'replay result binding mismatch')
        require(row['checker_sha256'] == PRESERVED['verify_exact.py'][1], 'replay source binding mismatch')
        require(row['summary'] == {'status': 'PASS', 'geometry_cases': 60, 'local_k33_subgraphs': 1650, 'seeded_assignments': 1792, 'k33_image_rank': 17, 'k33_minimum_weight': 1}, 'replay coverage mismatch')
    tests = read_json(root / 'TEST_REPORT.json')
    require(tests['status'] == 'PASS' and tests['mathematical_passes_added'] == 0, 'test report status mismatch')
    require(tests['assertion_probes_skipped'] is False and tests['assertion_failures_confirmed'] == 48, 'assertion test coverage mismatch')
    require(len(tests['assertion_probes']) == 48, 'assertion probe record count mismatch')
    require({(r['mode'], r['site']) for r in tests['assertion_probes']} == {(m, i) for m in ['normal', '-O', '-OO'] for i in range(16)}, 'assertion probe identity mismatch')
    require(all(r['status'] == 'EXPECTED_ASSERTION_FAILURE' and r['checker_compilation_optimization'] == 0 for r in tests['assertion_probes']), 'assertion probe result mismatch')
    require(tests['tamper_rejections'] == 54 and len(tests['tamper_tests']) == 54 and all(r['status'] == 'REJECTED' for r in tests['tamper_tests']), 'tamper report mismatch')
    require(len({(r['mode'], r['case']) for r in tests['tamper_tests']}) == 54, 'duplicate tamper record')
    require(len(tests['positive_validations']) == 3 and all(r['status'] == 'PASS' for r in tests['positive_validations']), 'positive validation report mismatch')
    return {'status': 'PASS', 'files': len(rows), 'preserved_artifacts': len(PRESERVED),
            'optimization': sys.flags.optimize, 'mathematical_passes_added': 0}


def main():
    require(len(sys.argv) <= 2, 'usage: validate_packet.py [packet_directory]')
    root = Path(sys.argv[1]).absolute() if len(sys.argv) == 2 else Path(__file__).resolve().parent
    print(json.dumps(validate(root), sort_keys=True))


if __name__ == '__main__':
    try:
        main()
    except (OSError, ValueError, KeyError, TypeError) as error:
        print('FAIL: ' + str(error), file=sys.stderr)
        raise SystemExit(1)
