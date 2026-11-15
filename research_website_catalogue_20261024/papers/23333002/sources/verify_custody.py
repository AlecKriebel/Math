#!/usr/bin/env python3
"""Read-only metadata/byte/CRC closure. Never reads scientific text or runs source."""
from pathlib import Path
from hashlib import sha256, new
from datetime import datetime, timezone
import io, json, re, stat, subprocess, sys, tarfile, unicodedata, zipfile, zlib

S = Path(__file__).resolve().parent
EXCLUDED = {'SOURCE_READY_MANIFEST.json', 'SOURCE_READY_CLOSURE.json', 'SOURCE_READY_SEAL.json'}


def need(ok, message):
    if not ok:
        raise ValueError(message)


def h(body):
    return sha256(body).hexdigest()


def load(path):
    return json.loads(path.read_bytes())


def bound(item):
    p = Path(item['path'])
    need(p.is_relative_to(S) and not p.is_symlink(), 'dedicated immutable source input')
    body = p.read_bytes()
    need(len(body) == item['bytes'] and h(body) == item['SHA256'], 'whole input size/SHA256')
    return body


def field(obj, key):
    return {'present': True, 'original_value': obj[key]} if key in obj else {'present': False}


def main():
    args = sys.argv[1:]
    need(args in ([], ['--inputs-only'], ['--preseal']), 'arguments')
    ready = load(S / 'SOURCE_READY.json')
    rid = ready['record_id']
    objects = {x['role']: json.loads(bound(x)) for x in ready['whole_native_API_objects']}
    r, latest, f = (objects[k] for k in ['record', 'latest', 'files'])
    versions = [x for key, obj in objects.items() if key.startswith('versions_') for x in obj['hits']['hits']]
    need(r['id'] == latest['id'] == rid and ready['latest_record_id'] == rid
         and ready['all_enumerated_version_ids'] == [x['id'] for x in versions] == [rid], 'actual selected/latest/version identity')
    pages = [obj for key, obj in objects.items() if key.startswith('versions_')]
    need(len(pages) == 1 and type(pages[0]['hits']['total']) is int and pages[0]['hits']['total'] == 1
         and 'next' not in pages[0]['links'], 'exhaustive actual version enumeration')
    q = json.loads(bound(ready['queue_binding']))['whole_selected_original_queue_entry']
    need(q['record_id'] == rid and q['sheet_row'] == ready['sheet_row']
         and q['eligibility'] == 'published_paper_record_with_manuscript'
         and q['title'] == r['metadata']['title'] == ready['title']
         and q['version'] == r['metadata']['version'] == ready['version']
         and q['publication_date'] == r['metadata']['publication_date'] == ready['publication_date']
         and q['doi'] == r['doi'] == ready['DOI'], 'queue and actual published metadata')
    need(r.get('status') == 'published' or r.get('state') == 'done', 'published record eligibility')
    sheet = json.loads(bound(ready['current_native_sheet_identity_subset']))['structuredContent']
    cells = {}
    for tab in sheet['sheets']:
        need(tab['properties']['title'] == 'Full List' and tab['properties']['sheetId'] == 1052646184, 'actual native tab')
        for data in tab['data']:
            for ro, row in enumerate(data.get('rowData', [])):
                for co, cell in enumerate(row.get('values', [])):
                    cells[(data.get('startRow', 0) + ro + 1, data.get('startColumn', 0) + co)] = cell
    text = lambda col: cells[(q['sheet_row'], col)].get('formattedValue', '')
    need(text(0) == str(q['inventory_index']) and text(1) == ready['title']
         and text(11).endswith(ready['DOI']) and text(12) == q['record_url']
         and text(13) == ready['publication_date'] and text(14) == ready['version']
         and text(22) == str(rid) and text(23) == q['work_id'], 'current native identity fields')
    distinctions = ready['native_schema_distinctions']
    need(distinctions['record_swh'] == field(r, 'swh') and distinctions['latest_swh'] == field(latest, 'swh')
         and distinctions['version_hit_swh_fields'] == [field(x, 'swh') for x in versions]
         and distinctions['files_order'] == field(f, 'order')
         and distinctions['files_default_preview'] == field(f, 'default_preview'), 'literal heterogeneous native fields')
    json.loads(bound(ready['native_schema_types']))
    assets = ready['all_native_assets_in_original_order']
    need([x['original_api_file_object'] for x in assets] == r['files'], 'original native record asset order')
    entries = list(f['entries'].values()) if isinstance(f['entries'], dict) else f['entries']
    for asset in assets:
        body = bound(asset)
        original = asset['original_api_file_object']
        algorithm, digest = original['checksum'].split(':', 1)
        need(len(body) == original['size'] and new(algorithm.lower(), body).hexdigest().lower() == digest.lower(),
             'native whole asset checksum and size')
        need(asset['whole_original_native_files_entry'] in entries and asset['cached_bytes_reused'] is False
             and asset['fresh_native_asset_GET_claimed'] is True, 'native files entry and actual acquisition mechanism')
    transport = json.loads(bound(ready['actual_transport_receipts']))
    receipts = transport['receipts']
    need([x['HTTP_status'] for x in receipts] == ready['HTTP_status_sequence'] == [200, 301, 200, 200, 200, 200, 200],
         'all actual ordinary transports, including original latest redirect')
    need(transport['initial_record_GET_invocations'] == 1 and transport['failed_responses'] == [], 'bounded successful acquisition')
    for receipt in receipts:
        bound({'path': receipt['body_path'], 'bytes': receipt['body_bytes'], 'SHA256': receipt['body_SHA256']})
        need(receipt['whole_response_body_captured'] is True and receipt['custom_request_headers'] == []
             and receipt['custom_proxy_or_authentication_or_query'] is False
             and isinstance(receipt['response_headers_in_received_order'], list), 'whole original response and ordered headers')
    custody = json.loads(bound(ready['whole_archive_custody']))
    payloads = custody['all_safe_regular_occurrences']
    total = count = 0
    for container in custody['containers']:
        body = bound(container)
        regular = {x['ordinal_zero_based']: x for x in payloads if x['container_id'] == container['container_id']}
        names = set()
        if container['kind'] == 'zip':
            with zipfile.ZipFile(io.BytesIO(body)) as archive:
                members = archive.infolist()
                need(len(members) == container['native_member_count_including_directories']
                     == len(container['whole_original_central_directory']), 'whole central directory')
                for ordinal, member in enumerate(members):
                    parts = Path(member.filename).parts
                    key = unicodedata.normalize('NFC', '/'.join(parts)).casefold()
                    need(not Path(member.filename).is_absolute() and '..' not in parts
                         and '\\' not in member.filename and ':' not in member.filename and key not in names,
                         'safe distinct native member names')
                    names.add(key)
                    native = container['whole_original_central_directory'][ordinal]
                    need(native['filename'] == member.filename and native['CRC32'] == '%08x' % member.CRC
                         and native['extra_hex'] == member.extra.hex() and native['comment_hex'] == member.comment.hex(),
                         'original central-directory fields')
                    if member.is_dir():
                        continue
                    need(not member.flag_bits & 1 and stat.S_IFMT(member.external_attr >> 16) in (0, stat.S_IFREG), 'safe regular ZIP body')
                    item = regular.pop(ordinal)
                    value = archive.read(member)
                    need(item['original_member_name'] == member.filename and len(value) == member.file_size == item['bytes']
                         and h(value) == item['SHA256'] and zlib.crc32(value) & 0xffffffff == member.CRC
                         and Path(item['extracted_path']).read_bytes() == value, 'complete native CRC/hash/extracted bytes')
                    total += len(value); count += 1
                need(not regular, 'no invented payload occurrences')
        else:
            with tarfile.open(fileobj=io.BytesIO(body), mode='r:*') as archive:
                members = archive.getmembers()
                need(len(members) == container['native_member_count_including_directories'], 'whole TAR directory')
                for ordinal, member in enumerate(members):
                    if member.isdir():
                        continue
                    need(member.isfile(), 'regular TAR body')
                    value = archive.extractfile(member).read(); item = regular.pop(ordinal)
                    need(len(value) == member.size == item['bytes'] and h(value) == item['SHA256']
                         and Path(item['extracted_path']).read_bytes() == value, 'whole TAR payload hash/copy')
                    total += len(value); count += 1
                need(not regular, 'complete TAR payload set')
    need(count == len(payloads) == custody['safe_regular_occurrences'] == ready['whole_regular_payload_occurrences']
         and total == custody['expanded_bytes_all_depths'] == ready['expanded_bytes_all_depths'], 'whole recursive inventory counts')
    need(len(custody['containers']) == ready['recursive_archive_container_count']
         and custody['nested_archives'] == ready['nested_archive_count'], 'complete nested container counts')
    manuscript = json.loads(bound(ready['manuscript_custody']))
    need(len(manuscript['all_TeX_candidates']) == 1 and manuscript['all_TeX_candidates'][0] == ready['controlling_TeX'], 'sole structural TeX candidate')
    tex = ready['controlling_TeX']; body = Path(tex['extracted_path']).read_bytes()
    need(len(body) == tex['bytes'] and h(body) == tex['SHA256']
         and len(body.splitlines()) == tex['opaque_byte_splitlines_count'] and tex['preamble_or_body_read'] is False,
         'opaque complete TeX byte/line identity')
    pdf = ready['selected_actual_PDF']; bound(pdf)
    need(pdf['SHA256'] in text(25), 'current native Sheet manuscript hash')
    info = subprocess.run(['pdfinfo', '-isodates', pdf['path']], capture_output=True, text=True, check=True).stdout
    need(int(re.search(r'^Pages:\s+(\d+)', info, re.M).group(1)) == pdf['pages'], 'actual PDF metadata page count without text extraction')
    for embedded in ready['embedded_PDFs']:
        need(Path(embedded['path']).read_bytes() == Path(pdf['path']).read_bytes(), 'actual embedded PDF identity')
    for flag in ['printed_title_date_version_inspected', 'target_PDF_text_extracted', 'target_PDF_pages_rendered',
                 'TeX_preamble_or_mathematical_body_read', 'source_scientific_proofs_code_results_triage_reviews_or_opinions_read']:
        need(ready[flag] is False, 'paper-first unread exposure boundary')
    need(ready['printed_date'] is None and ready['printed_version'] is None and ready['scientific_verdict'] is None
         and ready['source_programmes_executed'] == [] and ready['cached_bytes_reused'] is False, 'honest acquisition-only limits')
    for item in load(S / 'INPUT_MANIFEST.json')['files']:
        bound(item)
    owned = None
    if args != ['--inputs-only']:
        listed = set()
        for item in load(S / 'SOURCE_READY_MANIFEST.json')['files']:
            bound(dict(item, path=str(S / item['path']))); listed.add(item['path'])
        actual = {str(x.relative_to(S)) for x in S.rglob('*') if x.is_file() and str(x.relative_to(S)) not in EXCLUDED}
        need(actual == listed, 'exact owned custody membership'); owned = len(listed)
    if not args:
        seal = load(S / 'SOURCE_READY_SEAL.json')
        for name, key in [('SOURCE_READY.json', 'SOURCE_READY_SHA256'), ('SOURCE_READY_MANIFEST.json', 'MANIFEST_SHA256'),
                          ('SOURCE_READY_CLOSURE.json', 'CLOSURE_SHA256')]:
            need(h((S / name).read_bytes()) == seal[key], 'terminal custody seal')
        closure = load(S / 'SOURCE_READY_CLOSURE.json')
        need(closure['exit_code'] == 0 and closure['result']['verdict'] == 'PASS'
             and closure['verifier_SHA256'] == h(Path(__file__).read_bytes()), 'actual read-only closure receipt')
    print(json.dumps({'UTC': datetime.now(timezone.utc).isoformat(), 'verdict': 'PASS', 'record_id': rid,
        'mode': args[0] if args else 'terminal-read-only', 'PDF_pages': pdf['pages'],
        'TeX_bytes': tex['bytes'], 'TeX_lines': tex['opaque_byte_splitlines_count'],
        'archive_containers': len(custody['containers']), 'regular_payloads_all_depths': count,
        'expanded_bytes_all_depths': total, 'owned_manifest_payloads': owned,
        'scientific_text_preamble_code_results_opinions_read': False, 'printed_date_version_uninspected': True,
        'network_requests': [], 'native_source_programmes_executed': [], 'writes': []}, indent=2))


if __name__ == '__main__':
    main()
