#!/usr/bin/env python3
"""Read-only evidence closure, not a formal theorem checker or source runner."""
from pathlib import Path
from hashlib import sha256, md5
from datetime import datetime, timezone
import ast, json, sys, zipfile, zlib

A = Path(__file__).resolve().parent
P = A.parent.parent
S = P / 'source-resume-20261115'
EXCLUDED = {'MANIFEST.json', 'CLOSURE.json', 'SEAL.json'}
INITIAL_SHA = '3bc7f7b9743df0035dcf55c5aa2e39df5af8367b05a1678b2387ae6887ed733f'
READY_SHA = '0795e0631373b473f9d50270532ed8f326f68ba793d4f08c1654ea1a4556a244'
SOURCE_SEAL_SHA = 'b46f46fa3798b80d6382a823f7f8a582af5427028c27e6bac2ef465e5f81929c'


def need(value, message):
    if not value:
        raise ValueError(message)


def h(body):
    return sha256(body).hexdigest()


def load(path):
    return json.loads(path.read_bytes())


def bound(item):
    body = Path(item['path']).read_bytes()
    need(len(body) == item['bytes'] and h(body) == item['SHA256'], 'bound complete bytes')
    return body


def main():
    args = sys.argv[1:]
    need(args in ([], ['--inputs-only'], ['--preseal']), 'arguments')
    need(h((A / 'INITIAL_SEAL.json').read_bytes()) == INITIAL_SHA, 'immutable independent initial')
    initial = load(A / 'INITIAL_SEAL.json')
    for key in ['INITIAL_RECONSTRUCTION', 'INITIAL_READ_RECORD', 'INPUT_BASELINE']:
        bound(initial[key])
    first_read = load(A / 'INITIAL_READ_RECORD.json')
    need(first_read['PDF_pages_personally_read'] == [1, 2, 3, 4]
         and first_read['controlling_TeX_all_157_lines_personally_read'] is True
         and first_read['foreign_scientific_bodies_read_before_initial'] == []
         and first_read['native_code_or_results_read_before_initial'] == []
         and first_read['archived_or_current_peer_scientific_opinions_or_triage_read_before_initial'] == [],
         'declared full-reading and early-exposure record')
    for raster in first_read['fresh_rasters_personally_read']:
        bound(raster)
    baseline = load(A / 'INPUT_BASELINE.json')
    expected = set()
    for item in baseline['files']:
        bound(item)
        expected.add(item['path'])
    actual = {str(q) for root in baseline['source_roots'] for q in Path(root).rglob('*') if q.is_file()}
    need(actual == expected, 'both immutable old and resumed source folders unchanged')
    need(h((S / 'SOURCE_READY.json').read_bytes()) == READY_SHA
         and h((S / 'SOURCE_READY_SEAL.json').read_bytes()) == SOURCE_SEAL_SHA,
         'exact additive source authority')
    ready = load(S / 'SOURCE_READY.json')
    need(ready['version'] == '1.0.0' and ready['cached_ZIP_native_GET_claimed'] is False
         and ready['prior_failed_HTTP_status_sequence'] == [403, 403, 403]
         and ready['new_resumption_HTTP_status_sequence'] == [200, 301, 200, 200, 200, 200],
         'literal version, cache provenance and transport history')
    for asset in ready['all_native_assets_in_original_order']:
        body = bound(asset)
        need('md5:' + md5(body).hexdigest() == asset['original_api_file_object']['checksum'],
             'whole original native asset authentication')
    custody = json.loads(bound(ready['whole_archive_custody']))
    payloads = custody['all_safe_regular_occurrences']
    with zipfile.ZipFile(ready['all_native_assets_in_original_order'][0]['path']) as archive:
        members = archive.infolist()
        need(len(members) == len(payloads) == 20, 'complete supporting package')
        for ordinal, (member, item) in enumerate(zip(members, payloads)):
            body = archive.read(member)
            need(item['ordinal_zero_based'] == ordinal and item['original_member_name'] == member.filename
                 and len(body) == item['bytes'] == member.file_size and h(body) == item['SHA256']
                 and zlib.crc32(body) & 0xffffffff == member.CRC
                 and Path(item['extracted_path']).read_bytes() == body, 'whole payload CRC/hash/copy/order')
    inputs = load(A / 'INPUT_MANIFEST.json')
    for item in inputs['files']:
        bound(item)
    primary = load(A / 'PRIMARY_READ_RECORD.json')
    need(len(primary['primary_records']) == 6 and len(primary['fresh_primary_rasters_personally_read']) == 8
         and primary['root_or_sibling_scientific_opinions_read'] == [], 'exact primary scope and independence')
    for record in primary['primary_records']:
        need(bound(record).startswith(b'%PDF-'), 'whole actual primary PDF')
        bound(record['whole_extracted_text_identity'])
        chain = json.loads(bound(record['whole_transport_chain_identity']))
        need(chain == record['whole_transport_chain'] and len(chain) == 1, 'literal primary transport')
        for receipt in chain:
            need(receipt['HTTP_status'] == 200 and receipt['whole_response_body'] is True
                 and receipt['custom_headers'] == [] and receipt['retry'] is False
                 and isinstance(receipt['ordered_response_headers'], list), 'ordinary complete primary response')
            bound({'path': receipt['body_path'], 'bytes': receipt['bytes'], 'SHA256': receipt['SHA256']})
        need(record['full_physical_pages_personally_read'], 'explicit actual reading range')
    for item in primary['fresh_primary_rasters_personally_read']:
        bound(item)
    bound(primary['root_initial_authority_opaque_identity_only_not_scientific_body_read'])
    child = A / 'sign-check'
    manifest = load(child / 'manifest.json')
    need((child / 'SEAL.sha256').read_text().split()[0] == h((child / 'manifest.json').read_bytes()),
         'immutable child seal')
    need(h((child / 'manifest.json').read_bytes()) ==
         '985768d1025f89a19057a4bdf7554c77e7ec358baf7b5d32448e27e50b324b9a', 'exact child manifest')
    for name, item in manifest['artifacts'].items():
        need(len((child / name).read_bytes()) == item['bytes']
             and h((child / name).read_bytes()) == item['sha256'], 'child completed artifact identity')
    result = load(child / 'results.json')
    need(result['total_equalities'] == 131095 and result['output_truncation'] is False
         and [x['total_equalities'] for x in result['fields']] == [44339, 43378, 43378],
         'bounded independent result counts')
    need(result['checker_sha256'] == h((child / 'check_bosonization.py').read_bytes()), 'child checker binding')
    for field in result['fields']:
        p = int(field['field'].split('_')[1])
        control = field['negative_control']
        residual = control['multiplicativity_residual_left_minus_right']
        need(field['status'] == 'PASS' and field['max_binary_output_word_length'] == 8
             and field['max_associativity_output_word_length'] == 9, 'exact untruncated finite domain')
        need(residual == [] if p == 2 else len(residual) == 1 and residual[0]['coefficient'] == (-2) % p,
             'predicted characteristic-sensitive mutant multiplicativity')
        need(control['antipode_left_residual'] and control['antipode_right_residual'],
             'mutant antipode failures retained')
    native = load(A / 'NATIVE_REPRODUCTION.json')
    canonical = Path(native['canonical_original_path']).read_bytes()
    need(h(canonical) == native['canonical_SHA256']
         and Path(native['isolated_copy_path']).read_bytes() == canonical, 'isolated exact canonical native copy')
    need(native['exit_code'] == 0 and native['stderr_original'] == ''
         and json.loads(native['stdout_original']) == native['result']
         and native['whole_parsed_output_equals_native_expected'] is True, 'actual complete native run')
    expected_result = load(Path(native['native_expected_results_path']))
    need(expected_result == native['result'] and native['result']['result'] == 'PASS',
         'native expected certificate comparison')
    audit = ast.parse((S / 'published-source/audits/hopf_01/check_bosonization.py').read_text())
    canon = ast.parse(canonical.decode())
    need(isinstance(canon.body[0], ast.If) and ast.dump(audit, include_attributes=False) ==
         ast.dump(ast.Module(body=canon.body[1:], type_ignores=[]), include_attributes=False),
         'whole native programme AST comparison')
    verdict = load(A / 'VERDICT.json')
    need(verdict['decision'] == 'SUPPORTED — FULL ORIGINAL CLAIM' and verdict['defect_found'] is False
         and verdict['unresolved_central_mathematical_gap'] is None and verdict['follow_up'] is None
         and verdict['exact_source_ready_whole_object_preserved'] == ready,
         'literal full-scope verdict and unchanged source object')
    owned_count = None
    if args != ['--inputs-only']:
        manifest = load(A / 'MANIFEST.json')
        listed = set()
        for item in manifest['files']:
            path = A / item['path']
            need(path.is_relative_to(A) and not path.is_symlink(), 'owned path')
            bound(dict(item, path=str(path)))
            listed.add(item['path'])
        actual = {str(q.relative_to(A)) for q in A.rglob('*') if q.is_file()
                  and str(q.relative_to(A)) not in EXCLUDED}
        need(actual == listed, 'complete exact owned membership')
        owned_count = len(listed)
    if not args:
        seal = load(A / 'SEAL.json')
        for name, key in [('MANIFEST.json', 'MANIFEST_SHA256'), ('CLOSURE.json', 'CLOSURE_SHA256'),
                          ('REPORT.md', 'REPORT_SHA256'), ('VERDICT.json', 'VERDICT_SHA256')]:
            need(h((A / name).read_bytes()) == seal[key], 'terminal review seal')
        closure = load(A / 'CLOSURE.json')
        need(closure['exit_code'] == 0 and closure['result']['verdict'] == 'PASS'
             and closure['verifier_SHA256'] == h(Path(__file__).read_bytes()), 'actual read-only closure')
    print(json.dumps({'UTC': datetime.now(timezone.utc).isoformat(), 'verdict': 'PASS',
                      'mode': args[0] if args else 'terminal-read-only', 'record_id': 23439582,
                      'protected_source_files': len(expected), 'whole_ZIP_payloads': len(payloads),
                      'actual_primary_PDFs': 6, 'critical_primary_rasters': 8,
                      'target_manuscript_pages': 4, 'controlling_TeX_lines': 157,
                      'initial_seal_unchanged': True, 'independent_finite_equalities': 131095,
                      'complete_native_expected_output_match': True, 'owned_manifest_payloads': owned_count,
                      'mathematical_proof_machine_checked': False,
                      'network_requests': [], 'source_programmes_executed_by_this_closure': [],
                      'writes': []}, indent=2))


if __name__ == '__main__':
    main()
