#!/usr/bin/env python3
"""Read-only additive row121 source custody; no network or source execution."""
from pathlib import Path, PurePosixPath
from hashlib import sha256, md5
from datetime import datetime, timezone
import json, stat, sys, unicodedata, zipfile, zlib

S = Path(__file__).resolve().parent
READY_SHA = '0795e0631373b473f9d50270532ed8f326f68ba793d4f08c1654ea1a4556a244'
EXCLUDED = {'SOURCE_READY_MANIFEST.json', 'SOURCE_READY_CLOSURE.json', 'SOURCE_READY_SEAL.json'}


def need(ok, message):
    if not ok:
        raise ValueError(message)


def h(body):
    return sha256(body).hexdigest()


def load(path):
    return json.loads(path.read_bytes())


def bound(item):
    body = Path(item['path']).read_bytes()
    need(len(body) == item['bytes'] and h(body) == item['SHA256'], 'bound whole bytes/SHA256')
    return body


def main():
    args = sys.argv[1:]
    need(args in ([], ['--preseal'], ['--inputs-only']), 'arguments')
    need(h((S / 'SOURCE_READY.json').read_bytes()) == READY_SHA, 'SOURCE_READY identity')
    ready = load(S / 'SOURCE_READY.json')
    need(ready['record_id'] == 23439582 and ready['version'] == '1.0.0'
         and ready['publication_date'] == '2026-10-17'
         and ready['created'] == '2026-10-17T16:57:54.532142+00:00', 'literal native identity')
    objects = {x['role']: json.loads(bound(x)) for x in ready['whole_native_API_objects']}
    r, l, v, f = (objects[k] for k in ['record', 'latest', 'versions_page001', 'files'])
    need(r['id'] == l['id'] == 23439582 and type(v['hits']['total']) is int
         and v['hits']['total'] == 1 and [x['id'] for x in v['hits']['hits']] == [23439582]
         and 'next' not in v['links'], 'native latest and exhaustive versions')
    need(r['swh'] == l['swh'] == {} and all('swh' in x and x['swh'] is None for x in v['hits']['hits'])
         and f['order'] == [] and f['default_preview'] is None, 'heterogeneous native schemas')
    need(isinstance(json.loads(bound(ready['native_schema_types'])), dict), 'schema custody')
    assets = ready['all_native_assets_in_original_order']
    need([x['original_api_file_object'] for x in assets] == r['files']
         and [x['whole_original_native_files_entry'] for x in assets] == f['entries'],
         'whole native assets and unchanged ZIP/PDF order')
    need([x['original_api_file_object']['key'] for x in assets] ==
         ['cellularization-vanishing-source-and-verification.zip', 'cellularization-vanishing.pdf'],
         'actual original files')
    for asset in assets:
        body = bound(asset)
        need('md5:' + md5(body).hexdigest() == asset['original_api_file_object']['checksum']
             and len(body) == asset['original_api_file_object']['size'], 'fresh native asset MD5 and size')
    association = json.loads(bound(ready['cache_association']))
    need(association['exact_native_MD5_size_match_before_copy_or_extraction'] is True
         and association['native_GET_of_cached_ZIP_claimed'] is False
         and association['original_native_file_object'] == r['files'][0], 'explicit cache association')
    candidate = Path(association['candidate_original_path']).read_bytes()
    need(candidate == Path(assets[0]['path']).read_bytes(), 'whole authenticated cache copy')
    transport = json.loads(bound(ready['actual_transport_receipts']))
    new = transport['new_resumption_receipts_in_chronological_order']
    need([x['HTTP_status'] for x in new] == [200, 301, 200, 200, 200, 200],
         'actual successful resumption and complete native redirect')
    for receipt in new:
        body = Path(receipt['body_path']).read_bytes()
        need(len(body) == receipt['body_bytes'] and h(body) == receipt['body_SHA256']
             and receipt['whole_response_body_captured'] is True
             and isinstance(receipt['response_headers_in_received_order'], list)
             and receipt['custom_request_headers'] == []
             and receipt['custom_proxy_or_authentication_or_query'] is False,
             'ordinary native response and ordered headers')
    need(new[0]['request_count'] == 1 and new[0]['requested_url'] ==
         'https://zenodo.org/api/records/23439582', 'one authorized initial GET')
    prior = transport['prior_sealed_failed_transport_receipts_unchanged']
    need(len(prior) == 3, 'all three prior failures retained')
    for item in prior:
        literal = json.loads(bound(item['receipt_identity']))
        need(literal == item['whole_literal_original_receipt'] and literal['HTTP_status'] == 403,
             'prior receipt preserved literally')
        bound({'path': literal['body_path'], 'bytes': literal['bytes'], 'SHA256': literal['SHA256']})
    baseline = json.loads(bound(ready['prior_source_baseline']))
    expected = set()
    for item in baseline['files']:
        bound(item)
        expected.add(item['path'])
    old = Path(ready['prior_incomplete_source_folder_preserved'])
    need({str(x) for x in old.rglob('*') if x.is_file()} == expected, 'old sealed source membership')
    need(h(bound(ready['prior_incomplete_seal'])) ==
         '52c000f32fdde4a5fac49014e7e6f76a788d7d318220d11e6ea770b3a1cd8770', 'old incomplete seal unchanged')
    custody = json.loads(bound(ready['whole_archive_custody']))
    payloads = custody['all_safe_regular_occurrences']
    names = set()
    expanded = 0
    with zipfile.ZipFile(Path(assets[0]['path'])) as archive:
        members = archive.infolist()
        need(len(members) == len(payloads) == 20, 'complete ZIP member enumeration')
        for ordinal, (member, item) in enumerate(zip(members, payloads)):
            path = PurePosixPath(member.filename)
            folded = unicodedata.normalize('NFC', member.filename).casefold()
            need(not path.is_absolute() and '..' not in path.parts and '\\' not in member.filename
                 and ':' not in member.filename and folded not in names, 'safe unique archive names')
            names.add(folded)
            need(not member.is_dir() and not member.flag_bits & 1
                 and stat.S_IFMT(member.external_attr >> 16) in (0, stat.S_IFREG), 'regular unencrypted member')
            body = archive.read(member)
            need(len(body) == member.file_size == item['bytes'] and h(body) == item['SHA256']
                 and zlib.crc32(body) & 0xffffffff == member.CRC
                 and item['CRC32'] == '%08x' % member.CRC
                 and item['ordinal_zero_based'] == ordinal and item['original_member_name'] == member.filename
                 and Path(item['extracted_path']).read_bytes() == body, 'whole payload CRC/hash/order/copy')
            expanded += len(body)
    need(expanded == 184835 and custody['nested_archives'] == 0, 'whole expanded package')
    identity = json.loads(bound(ready['printed_identity']))
    tex = ready['controlling_TeX']
    body = Path(tex['extracted_path']).read_bytes()
    need(len(body) == tex['bytes'] == 13093 and h(body) == tex['SHA256']
         and len(body.splitlines()) == tex['lines'] == 157, 'sole controlling TeX')
    need(identity['PDF']['pages'] == ready['selected_actual_PDF']['pages'] == 4
         and identity['controlling_TeX']['date_preamble'] ==
         r'17 October 2026 \quad (version 1.0.0; unrefereed)', 'printed identity and page count')
    need(len(identity['embedded_PDFs']) == 1 and identity['unsupported_archive_magic_occurrences'] == [],
         'complete embedded PDF/archive structural inventory')
    need(Path(identity['embedded_PDFs'][0]['path']).read_bytes() == Path(assets[1]['path']).read_bytes(),
         'embedded and separately published PDF byte identity')
    for flag in ['target_manuscript_scientifically_read', 'controlling_TeX_mathematical_body_read',
                 'source_programs_executed_or_scientifically_read',
                 'archived_current_opinions_or_inventory_triage_read', 'target_PDF_pages_rendered']:
        need(ready[flag] is False, 'source-only exposure contract')
    count = None
    if args != ['--inputs-only']:
        manifest = load(S / 'SOURCE_READY_MANIFEST.json')
        listed = set()
        for item in manifest['files']:
            path = S / item['path']
            need(path.is_relative_to(S) and not path.is_symlink(), 'owned regular path')
            bound(dict(item, path=str(path)))
            listed.add(item['path'])
        actual = {str(x.relative_to(S)) for x in S.rglob('*') if x.is_file()
                  and str(x.relative_to(S)) not in EXCLUDED}
        need(actual == listed, 'complete new packet membership')
        count = len(listed)
    if not args:
        seal = load(S / 'SOURCE_READY_SEAL.json')
        for name, key in [('SOURCE_READY.json', 'SOURCE_READY_SHA256'),
                          ('SOURCE_READY_MANIFEST.json', 'SOURCE_READY_MANIFEST_SHA256'),
                          ('SOURCE_READY_CLOSURE.json', 'SOURCE_READY_CLOSURE_SHA256')]:
            need(h((S / name).read_bytes()) == seal[key], 'terminal source seal')
        closure = load(S / 'SOURCE_READY_CLOSURE.json')
        need(closure['exit_code'] == 0 and closure['result']['verdict'] == 'PASS'
             and closure['verifier_SHA256'] == h(Path(__file__).read_bytes()), 'read-only closure receipt')
    print(json.dumps({'UTC': datetime.now(timezone.utc).isoformat(), 'verdict': 'PASS',
                      'mode': args[0] if args else 'terminal-read-only', 'record_id': 23439582,
                      'native_assets': 2, 'whole_ZIP_payloads': 20, 'expanded_bytes': expanded,
                      'PDF_pages': 4, 'controlling_TeX_bytes': 13093, 'controlling_TeX_lines': 157,
                      'prior_sealed_files_unchanged': len(expected), 'manifest_payloads': count,
                      'new_ordinary_HTTP_statuses': [x['HTTP_status'] for x in new],
                      'prior_failures_preserved': 3, 'cached_ZIP_native_GET_claimed': False,
                      'scientific_body_or_code_read': False, 'source_programs_executed': [],
                      'network_requests': [], 'writes': []}, indent=2))


if __name__ == '__main__':
    main()
