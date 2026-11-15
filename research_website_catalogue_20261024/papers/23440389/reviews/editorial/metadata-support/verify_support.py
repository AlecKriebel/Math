#!/usr/bin/env python3
"""Pure offline metadata/custody verification; no manuscript programs imported."""
import copy
import hashlib
import json
from pathlib import Path
import stat
import zipfile

HERE = Path(__file__).resolve().parent
P = HERE.parents[4]
checks = 0


def check(value, label):
    global checks
    checks += 1
    if value is not True:
        raise RuntimeError(label)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def read(path):
    return json.loads(Path(path).read_text())


def strict(a, b):
    if type(a) is not type(b):
        return False
    if isinstance(a, dict):
        return list(a) == list(b) and all(strict(a[k], b[k]) for k in a)
    if isinstance(a, list):
        return len(a) == len(b) and all(strict(x, y) for x, y in zip(a, b))
    return a == b


def valid_core(b, rights):
    s = b['source_ready']['whole_literal_object']
    r = b['native_API_objects'][0]['whole_literal_object']
    l = b['native_API_objects'][1]['whole_literal_object']
    v = b['native_API_objects'][2]['whole_literal_object']
    f = b['native_API_objects'][3]['whole_literal_object']
    t = b['transport_aggregate']['whole_literal_object']
    root = b['root_authority']['whole_literal_object']
    return all([
        s['record_id'] == 23440389,
        type(s['version']) is str and s['version'] == '1.0',
        s['publication_date'] == '2026-10-17',
        s['created'] == '2026-10-17T18:10:27.832798+00:00',
        s['updated'] == '2026-10-17T18:10:28.256431+00:00',
        [x['original_api_file_object']['key'] for x in s['all_native_assets_in_original_order']] ==
            ['Tree_Five_List_Verification_v1.0.zip', 'Tree_Five_List_Note_v1.0.pdf'],
        len(b['native_API_objects']) == 4,
        strict(r, l),
        r['swh'] == {} and type(r['swh']) is dict,
        v['hits']['hits'][0]['swh'] is None,
        type(v['hits']['total']) is int and v['hits']['total'] == 1,
        f['default_preview'] is None and f['order'] == [],
        type(f['entries']) is list,
        strict(s['native_license_object'], {'id': 'cc-by-4.0'}),
        len(t['receipts']) == 7,
        [x['HTTP_status'] for x in t['receipts']] == [200, 301, 200, 200, 200, 200, 200],
        t['custom_header_proxy_auth_query_or_retry_changes'] is False,
        all(x['custom_request_headers'] == [] and x['custom_proxy_or_authentication_or_query'] is False
            and x['automatic_redirect_following'] is False for x in t['receipts']),
        all(type(x['response_headers_in_received_order']) is list for x in t['receipts']),
        sum(h[0].lower() == 'content-type' for h in t['receipts'][5]['response_headers_in_received_order']) == 2,
        len(root['independent_review_packets']) == 2,
        [x['lane'] for x in root['independent_review_packets']] == ['scope', 'adversarial'],
        len(b['scientific_custom_verdicts']) == 2,
        root['followup'] is None,
        root['public_page_or_native_canonical_authorized_yet'] is False,
        root['editorial_preparation_authorized'] is True,
        rights['separate_code_license_grant'] is None,
        rights['authored_package_license'] == 'CC BY 4.0',
        rights['printed_version'] == '1.0',
        rights['printed_date'] == '17 October 2026',
        rights['publication_date'] == '2026-10-17',
        rights['created'] == '2026-10-17T18:10:27.832798+00:00',
        rights['updated'] == '2026-10-17T18:10:28.256431+00:00',
        rights['follow_up'] is None,
        rights['current_native_canonical_or_AA_authority'] is None,
        rights['public_install_authorized'] is False,
        rights['PDF_pages'] == 3,
        rights['complete_ZIP_payloads'] == 61,
    ])


def main():
    b = read(HERE / 'SOURCE_PROTOCOL_BINDINGS.json')
    rights = read(HERE / 'RIGHTS_AND_IDENTITY.json')
    inputs = read(HERE / 'INPUT_MANIFEST.json')
    for x in inputs['files']:
        data = Path(x['path']).read_bytes()
        check(len(data) == x['bytes'] and sha(data) == x['SHA256'], 'input guard ' + x['path'])
    rows = ([b['source_ready'], b['root_authority'], b['transport_aggregate'], b['archive_custody'],
             b['native_schema_types'], b['printed_identity']] + b['source_terminal_objects'] +
            b['native_API_objects'] + b['transport_objects'] + b['scientific_custom_verdicts'] + b['scientific_review_seals'])
    for x in rows:
        data = Path(x['path']).read_bytes()
        check(len(data) == x['bytes'] and sha(data) == x['SHA256'], 'literal bytes ' + x['path'])
        check(strict(x['whole_literal_object'], json.loads(data)), 'literal type/order ' + x['path'])
    for x in b['raw_byte_copies']:
        check((HERE / x['copy_path']).read_bytes() == Path(x['original_path']).read_bytes(), 'byte copy ' + x['copy_path'])
    check(valid_core(b, rights), 'core identity and authorization')
    s = b['source_ready']['whole_literal_object']
    root = b['root_authority']['whole_literal_object']
    check(strict(root['whole_literal_source_ready'], s), 'root whole source')
    check(sha(Path(b['source_ready']['path']).read_bytes()) == root['source_ready_sha256'], 'root source hash')
    for i, x in enumerate(b['scientific_custom_verdicts']):
        packet = root['independent_review_packets'][i]
        check(strict(x['whole_literal_object'], packet['whole_literal_custom_verdict']), 'root whole custom verdict')
        check(x['SHA256'] == packet['verdict_sha256'], 'root verdict hash')
        check(b['scientific_review_seals'][i]['SHA256'] == packet['seal']['sha256'], 'root review seal hash')
    aggregate = b['transport_aggregate']['whole_literal_object']
    for i, x in enumerate(b['transport_objects']):
        check(strict(x['whole_literal_object'], aggregate['receipts'][i]), 'actual dispatch order receipt')
        receipt = x['whole_literal_object']
        data = Path(receipt['body_path']).read_bytes()
        check(len(data) == receipt['body_bytes'] and sha(data) == receipt['body_SHA256'], 'whole response body')
        if 'body_MD5' in receipt:
            check(hashlib.md5(data).hexdigest() == receipt['body_MD5'], 'response body MD5')
    check(strict(json.loads(Path(aggregate['receipts'][1]['body_path']).read_bytes()),
                 {'status': 301, 'message': 'Redirecting...', 'location': 'https://zenodo.org/api/records/23440389'}), 'raw 301 body')
    record = b['native_API_objects'][0]['whole_literal_object']
    files = b['native_API_objects'][3]['whole_literal_object']
    for i, asset in enumerate(s['all_native_assets_in_original_order']):
        data = Path(asset['path']).read_bytes()
        check(len(data) == asset['bytes'] and sha(data) == asset['SHA256'], 'native asset SHA256')
        check(hashlib.md5(data).hexdigest() == asset['MD5'], 'native asset MD5')
        check(strict(asset['original_api_file_object'], record['files'][i]), 'whole native file object')
        check(strict(asset['whole_original_native_files_entry'], files['entries'][i]), 'whole native files entry')
    custody = b['archive_custody']['whole_literal_object']
    check(len(custody['containers']) == 1 and len(custody['all_safe_regular_occurrences']) == 61, 'whole ZIP custody cardinality')
    container = custody['containers'][0]
    with zipfile.ZipFile(container['container_path']) as z:
        infos = z.infolist()
        check(len(infos) == 61, 'native ZIP member count')
        expanded = 0
        for i, (info, x) in enumerate(zip(infos, custody['all_safe_regular_occurrences'])):
            check(info.filename == x['original_member_name'] and i == x['ordinal_zero_based'], 'ZIP order and name')
            check(not info.is_dir() and (stat.S_IFMT(info.external_attr >> 16) in (0, stat.S_IFREG)), 'regular ZIP member')
            check(info.file_size == x['bytes'] and info.compress_size == x['compressed_bytes'], 'ZIP sizes')
            check(f'{info.CRC:08x}' == x['CRC32'] and info.flag_bits == x['zip_flags'], 'ZIP CRC and flags')
            check(info.compress_type == x['compression_method'] and info.external_attr == x['native_external_attr']
                  and list(info.date_time) == x['native_date_time'], 'ZIP native metadata')
            data = z.read(info)
            check(sha(data) == x['SHA256'] and data == Path(x['extracted_path']).read_bytes(), 'ZIP complete body/extracted identity')
            expanded += len(data)
        check(expanded == custody['expanded_bytes_all_depths'] == 386822, 'expanded bytes')
    for x in b['rights_and_requirements_candidates']:
        check(Path(x['path']).read_text() == x['whole_literal_text'], 'README complete text')
    check(rights['grant_quote'] in b['rights_and_requirements_candidates'][0]['whole_literal_text'], 'actual authored grant')
    faults = []
    def reject(name, change):
        bb, rr = copy.deepcopy(b), copy.deepcopy(rights)
        change(bb, rr)
        check(valid_core(bb, rr) is False, 'fault rejected ' + name)
        faults.append(name)
    reject('ZIP/PDF order swapped', lambda bb, rr: bb['source_ready']['whole_literal_object']['all_native_assets_in_original_order'].reverse())
    reject('invented third review', lambda bb, rr: bb['root_authority']['whole_literal_object']['independent_review_packets'].append({'lane': 'invented'}))
    reject('301 response erased', lambda bb, rr: bb['transport_aggregate']['whole_literal_object']['receipts'].pop(1))
    reject('version converted to number', lambda bb, rr: bb['source_ready']['whole_literal_object'].__setitem__('version', 1.0))
    reject('created timestamp substituted for declared date', lambda bb, rr: rr.__setitem__('publication_date', rr['created']))
    reject('MIT default inserted', lambda bb, rr: rr.__setitem__('separate_code_license_grant', 'MIT'))
    reject('null follow-up converted to empty object', lambda bb, rr: rr.__setitem__('follow_up', {}))
    reject('native authorization invented', lambda bb, rr: bb['root_authority']['whole_literal_object'].__setitem__('public_page_or_native_canonical_authorized_yet', True))
    reject('versions null normalized to object', lambda bb, rr: bb['native_API_objects'][2]['whole_literal_object']['hits']['hits'][0].__setitem__('swh', {}))
    reject('duplicate transport header flattened', lambda bb, rr: bb['transport_aggregate']['whole_literal_object']['receipts'][5].__setitem__('response_headers_in_received_order', dict(bb['transport_aggregate']['whole_literal_object']['receipts'][5]['response_headers_in_received_order'])))
    for name, aa, cc in [('bool/int', True, 1), ('dict key order', {'a': 1, 'b': 2}, {'b': 2, 'a': 1}), ('list order', [1, 2], [2, 1]), ('null/empty', None, {})]:
        check(strict(aa, cc) is False, 'strict control ' + name)
        faults.append(name)
    manifest = HERE / 'OWNED_MANIFEST.json'
    if manifest.exists():
        for x in read(manifest)['files']:
            data = (HERE / x['path']).read_bytes()
            check(len(data) == x['bytes'] and sha(data) == x['SHA256'], 'owned guard ' + x['path'])
    seal = HERE / 'SEAL.json'
    if seal.exists():
        check(sha(manifest.read_bytes()) == read(seal)['OWNED_MANIFEST_SHA256'], 'owned manifest seal')
    print(json.dumps({'status': 'QUALIFIED_PASS_METADATA_CUSTODY_ONLY', 'checks': checks,
                      'input_files': len(inputs['files']), 'whole_literal_JSON_objects': len(rows),
                      'native_API_objects': 4, 'actual_transport_objects': 7, 'scientific_custom_verdicts': 2,
                      'native_assets': 2, 'whole_ZIP_payloads': 61, 'raw_byte_copies': len(b['raw_byte_copies']),
                      'in_memory_metadata_faults_rejected': faults, 'network': False, 'writes': False,
                      'scientific_program_execution': False, 'publication_authority': False}, indent=2))


if __name__ == '__main__':
    main()
