"""Prepare administrative source readiness without reading manuscript text."""
from pathlib import Path
from datetime import datetime, timezone
from hashlib import sha256
import json

S = Path(__file__).resolve().parent


def load(path):
    return json.loads(path.read_bytes())


def identity(path):
    body = path.read_bytes()
    return {'path': str(path), 'bytes': len(body), 'SHA256': sha256(body).hexdigest()}


def save(name, obj):
    with (S / name).open('x') as out:
        out.write(json.dumps(obj, indent=2, ensure_ascii=False) + '\n')


def field(obj, key):
    return {'present': True, 'original_value': obj[key]} if key in obj else {'present': False}


def types(value, path, out):
    kind = ('null' if value is None else 'boolean' if type(value) is bool else
            'integer' if type(value) is int else 'number' if type(value) is float else
            'string' if type(value) is str else 'array' if type(value) is list else 'object')
    out.setdefault(path, set()).add(kind)
    if isinstance(value, dict):
        for key, child in value.items():
            types(child, path + '/' + key, out)
    elif isinstance(value, list):
        for child in value:
            types(child, path + '/*', out)


def main():
    acquired = load(S / 'ACQUIRED_NATIVE.json')
    objects = {x['role']: load(Path(x['path'])) for x in acquired['whole_native_API_objects']}
    record, latest, files = (objects[x] for x in ['record', 'latest', 'files'])
    binding = load(S / 'QUEUE_BINDING.json')
    queue = binding['whole_selected_original_queue_entry']
    custody, manuscript = load(S / 'ARCHIVE_CUSTODY.json'), load(S / 'MANUSCRIPT_CUSTODY.json')
    assert record['id'] == latest['id'] == queue['record_id']
    assert record['metadata']['title'] == queue['title']
    assert record['metadata']['version'] == queue['version']
    assert record['metadata']['publication_date'] == queue['publication_date']
    assert record['doi'] == queue['doi']
    assert len(manuscript['all_TeX_candidates']) == 1
    assert len(manuscript['embedded_PDFs']) == 0 or all(x['byte_identical_to_published_manuscript'] for x in manuscript['embedded_PDFs'])
    pdf = manuscript['PDF']
    expected = [x for x in queue['sources'] if x['filename'] == Path(pdf['path']).name]
    assert len(expected) == 1 and expected[0]['sha256'] == pdf['SHA256']
    sheet = load(S / 'NATIVE_SHEET_IDENTITY_SUBRANGES.json')['structuredContent']
    native_cells = {}
    for tab in sheet['sheets']:
        for data in tab['data']:
            for row_offset, row in enumerate(data.get('rowData', [])):
                for col_offset, cell in enumerate(row.get('values', [])):
                    native_cells[(data.get('startRow', 0) + row_offset + 1,
                                  data.get('startColumn', 0) + col_offset)] = cell
    row = queue['sheet_row']
    text = lambda col: native_cells[(row, col)].get('formattedValue', '')
    assert text(0) == str(queue['inventory_index']) and text(1) == record['metadata']['title']
    assert text(11).endswith(record['doi']) and text(12) == queue['record_url']
    assert text(13) == record['metadata']['publication_date'] and text(14) == record['metadata']['version']
    assert text(22) == str(record['id']) and text(23) == queue['work_id']
    assert pdf['SHA256'] in text(25)
    receipts = [load(x) for x in S.rglob('*.transport.json')]
    receipts.sort(key=lambda x: x['started_UTC'])
    assert all(x['HTTP_status'] in (200, 301, 302, 303, 307, 308) for x in receipts)
    save('ALL_TRANSPORT_RECEIPTS.json', {'receipts': receipts,
         'ordinary_native_GET_only': True, 'initial_record_GET_invocations': 1,
         'actual_native_redirect_hops_not_retries': True, 'failed_responses': []})
    schema = {}
    for role, value in objects.items():
        out = {}
        types(value, '', out)
        schema[role] = {path: sorted(kinds) for path, kinds in out.items()}
    save('NATIVE_SCHEMA_TYPES.json', {'objects': schema, 'raw_whole_bodies_authoritative': True,
         'missing_null_empty_and_original_array_orders_not_normalized': True})
    versions = [x for role, obj in objects.items() if role.startswith('versions_') for x in obj['hits']['hits']]
    ready = {'schema': 'metadata-only-native-source-ready-v1', 'status': 'SOURCE_READY',
        'UTC': datetime.now(timezone.utc).isoformat(), 'record_id': record['id'], 'sheet_row': row,
        'title': record['metadata']['title'], 'DOI': record['doi'], 'version': record['metadata']['version'],
        'publication_date': record['metadata']['publication_date'], 'created': record['created'], 'updated': record['updated'],
        'native_conceptrecid_whole_field': field(record, 'conceptrecid'),
        'native_version_whole_field': field(record['metadata'], 'version'),
        'native_license_metadata_whole_field': field(record['metadata'], 'license'),
        'native_resource_type_whole_field': field(record['metadata'], 'resource_type'),
        'latest_record_id': latest['id'], 'all_enumerated_version_ids': acquired['all_enumerated_version_ids'],
        'version_enumeration_exhaustive_no_next_link': True,
        'whole_native_API_objects': acquired['whole_native_API_objects'],
        'all_native_assets_in_original_order': acquired['all_assets_original_record_order'],
        'actual_transport_receipts': identity(S / 'ALL_TRANSPORT_RECEIPTS.json'),
        'HTTP_status_sequence': [x['HTTP_status'] for x in receipts],
        'native_schema_types': identity(S / 'NATIVE_SCHEMA_TYPES.json'),
        'native_schema_distinctions': {'record_swh': field(record, 'swh'), 'latest_swh': field(latest, 'swh'),
            'version_hit_swh_fields': [field(x, 'swh') for x in versions],
            'files_order': field(files, 'order'), 'files_default_preview': field(files, 'default_preview')},
        'current_native_sheet_identity_subset': identity(S / 'NATIVE_SHEET_IDENTITY_SUBRANGES.json'),
        'current_sheet_tab_and_bounds': {'title': 'Full List', 'sheetId': 1052646184, 'rowCount': 1000, 'columnCount': 30},
        'queue_binding': identity(S / 'QUEUE_BINDING.json'),
        'current_native_sheet_and_fresh_published_record_identity_match': True,
        'selected_actual_PDF': pdf, 'controlling_TeX': manuscript['all_TeX_candidates'][0],
        'controlling_TeX_selection_basis': 'sole .tex occurrence across complete recursive native package, filename/structural custody only; no preamble/body read or build correspondence certified',
        'manuscript_custody': identity(S / 'MANUSCRIPT_CUSTODY.json'),
        'whole_archive_custody': identity(S / 'ARCHIVE_CUSTODY.json'),
        'top_level_archive_count': custody['top_level_archives'], 'recursive_archive_container_count': custody['archive_containers'],
        'nested_archive_count': custody['nested_archives'], 'whole_regular_payload_occurrences': custody['safe_regular_occurrences'],
        'expanded_bytes_all_depths': custody['expanded_bytes_all_depths'],
        'embedded_PDFs': manuscript['embedded_PDFs'], 'printed_title_date_version_inspected': False,
        'printed_date': None, 'printed_version': None,
        'target_PDF_text_extracted': False, 'target_PDF_pages_rendered': False,
        'TeX_preamble_or_mathematical_body_read': False,
        'source_scientific_proofs_code_results_triage_reviews_or_opinions_read': False,
        'source_programmes_executed': [], 'cached_bytes_reused': False,
        'all_original_assets_received_by_actual_fresh_native_GET': True,
        'custom_headers_auth_proxy_query_or_retry_tricks_used': False,
        'ignored_assets_and_extraction_paths_established_before_acquisition': True,
        'exposure_limit': 'Native metadata/identity columns, file names and opaque CRC/hash/safe extraction, PDF metadata/page count and TeX byte/line count only. No PDF text or page image, no TeX preamble/body, no scientific code/result/opinion reading. Subsequent scientific lane must personally inspect the complete manuscript and printed edition before imported opinions.',
        'scientific_verdict': None, 'publication_authority': False, 'completion_percent_at_preseal': 95}
    save('SOURCE_READY.json', ready)
    inputs = acquired['whole_native_API_objects'] + [identity(Path(x['path'])) for x in acquired['all_assets_original_record_order']]
    inputs += [identity(Path(x['body_path'])) for x in receipts]
    inputs += [identity(S / name) for name in ['QUEUE_BINDING.json', 'NATIVE_SHEET_METADATA.json', 'NATIVE_SHEET_HEADERS.json', 'NATIVE_SHEET_IDENTITY_SUBRANGES.json']]
    seen, unique = set(), []
    for x in inputs:
        if x['path'] not in seen:
            seen.add(x['path']); unique.append(x)
    save('INPUT_MANIFEST.json', {'files': unique, 'all_original_objects_bytes_preserved': True,
         'external_queue_was_snapshotted_in_binding_not_assumed_immutable': True})
    with (S / 'SOURCE_LOG.md').open('a') as out:
        out.write('- ' + datetime.now(timezone.utc).isoformat() + ' — 95%: Exact native current identities match live Sheet and reconciled queue. Whole record/latest/all-versions/files, all original asset bytes and complete recursive safe CRC/hash package custody closed. Sole TeX candidate identified structurally; PDF pages counted with pdfinfo. Printed date/version remain uninspected; all scientific/preamble/code/result/opinion unread flags remain false. Final read-only seal pending.\n')
    print(json.dumps({'record_id': record['id'], 'SOURCE_READY_SHA256': sha256((S / 'SOURCE_READY.json').read_bytes()).hexdigest(),
         'PDF_pages': pdf['pages'], 'TeX_bytes': ready['controlling_TeX']['bytes'],
         'TeX_lines': ready['controlling_TeX']['opaque_byte_splitlines_count'],
         'recursive_payloads': custody['safe_regular_occurrences'], 'native_statuses': ready['HTTP_status_sequence']}, indent=2))


if __name__ == '__main__':
    main()
