#!/usr/bin/env python3
"""Pure offline paired source-custody adoption; no foreign imports or execution."""
from pathlib import Path, PurePosixPath
import hashlib, json, sys
O = Path(__file__).resolve().parent
EXCLUDED = {'OWNED_MANIFEST.json', 'FINAL_SEAL.json'}
N = 0

def need(v, m):
    global N
    N += 1
    if not v:
        raise RuntimeError(m)

def sha(b):
    return hashlib.sha256(b).hexdigest()

def load(p):
    return json.loads(p.read_text())

def typed(a, b):
    if type(a) is not type(b):
        return False
    if isinstance(a, dict):
        return list(a) == list(b) and all((typed(a[k], b[k]) for k in a))
    if isinstance(a, list):
        return len(a) == len(b) and all((typed(x, y) for (x, y) in zip(a, b)))
    return a == b

def bound(r, base):
    p = PurePosixPath(r['path'])
    need(not p.is_absolute() and '..' not in p.parts and (str(p) == r['path']), 'Unsafe relative path')
    p = base / r['path']
    need(p.resolve().is_relative_to(base) and p.is_file() and (not p.is_symlink()), 'Missing, escaped or symlink file')
    b = p.read_bytes()
    need(len(b) == r['bytes'] and sha(b) == r['SHA256'], 'Changed whole payload ' + str(p))
    return b

def main(preseal):
    manifest = load(O / 'OWNED_MANIFEST.json')
    need(manifest['excluded_terminal_files'] == sorted(EXCLUDED), 'Owned terminal boundary')
    seen = set()
    for r in manifest['files']:
        bound(r, O)
        need(r['path'] not in seen, 'Duplicate own payload')
        seen.add(r['path'])
    need(seen == {p.relative_to(O).as_posix() for p in O.rglob('*') if p.is_file()} - EXCLUDED, 'Complete paired packet extent')
    pair = load(O / 'SOURCE_READY_PAIR.json')
    need([r['record_id'] for r in pair['records']] == [23202966, 23205305], 'Only135/136 source records')
    q = load(O / 'FRESH_QUEUE_SELECTION.json')
    need(q['only_ranges_read'] == ["'Full List'!W135:W136", "'Full List'!AB135:AB136"] and q['scientific_assessment_or_old_triage_read'] is False, 'Only fresh native identity/status cells')
    native = load(O / 'NATIVE_SHEET_IDENTITY_SUBRANGES.json')['structuredContent']
    sheet = native['sheets'][0]
    need(sheet['properties']['sheetId'] == 1052646184 and sheet['properties']['title'] == 'Full List', 'Actual visible native tab')
    cells = {}
    for data in sheet['data']:
        for (i, row) in enumerate(data['rowData']):
            for (j, cell) in enumerate(row['values']):
                cells[data['startRow'] + i + 1, data['startColumn'] + j] = cell
    for (row, rid) in [(135, 23202966), (136, 23205305)]:
        need(cells[row, 22]['effectiveValue']['numberValue'] == rid and cells[row, 27]['effectiveValue']['stringValue'] == 'Queued — eligible Zenodo paper', 'Fresh actual native queued record')
    default = load(O / 'ACTUAL_DEFAULT_CLOSURES.json')
    payload_total = 0
    reader_pages = 0
    rasters = 0
    requests = 0
    for r in pair['records']:
        R = Path(r['source_root'])
        ready = load(R / 'SOURCE_READY.json')
        seal = load(R / 'SOURCE_READY_SEAL.json')
        m = load(R / 'SOURCE_READY_MANIFEST.json')
        for (name, key) in [('SOURCE_READY.json', 'SOURCE_READY_SHA256'), ('SOURCE_READY_SEAL.json', 'SOURCE_READY_SEAL_SHA256'), ('SOURCE_READY_MANIFEST.json', 'SOURCE_READY_MANIFEST_SHA256'), ('SOURCE_READY_CLOSURE.json', 'SOURCE_READY_CLOSURE_SHA256')]:
            need(sha((R / name).read_bytes()) == r[key], 'Pinned final immutable source ' + name)
        for (name, key) in [('SOURCE_READY.json', 'SOURCE_READY_SHA256'), ('SOURCE_READY_MANIFEST.json', 'MANIFEST_SHA256'), ('SOURCE_READY_CLOSURE.json', 'CLOSURE_SHA256')]:
            need(sha((R / name).read_bytes()) == seal[key], 'Actual source terminal seal ' + name)
        for f in m['files']:
            bound(f, R)
        need({f['path'] for f in m['files']} == {p.relative_to(R).as_posix() for p in R.rglob('*') if p.is_file()} - set(m['excluded_terminal_files']), 'Complete sealed source extent')
        need(len(m['files']) == seal['owned_payload_count'] == r['source_seal_owned_payloads'], 'Source extent count')
        for f in load(R / 'INPUT_MANIFEST.json')['files']:
            p = Path(f['path'])
            b = p.read_bytes()
            need(len(b) == f['bytes'] and sha(b) == f['SHA256'], 'Whole original bound helper/schema/queue inputs')
        a = load(R / 'ACQUIRED_NATIVE.json')
        record = load(R / 'record.response.body')
        need(record['id'] == ready['record_id'] == r['record_id'] and record['status'] == 'published' and (record['state'] == 'done'), 'Actually published native record')
        need('version' not in record['metadata'] and ready['version_field_present'] is False and (ready['version'] is None) and typed(ready['native_version_whole_field'], {'present': False, 'original_value': None}), 'Absent native version preserved without1.0')
        need(ready['printed_date'] is None and ready['printed_version'] is None and (ready['scientific_verdict'] is None) and (ready['publication_authority'] is False), 'Unread identity/scientific/publication state')
        need(ready['mathematical_PDF_TeX_or_pixels_read'] is False and ready['TeX_preamble_or_mathematical_body_read'] is False and (ready['source_scientific_proofs_code_results_triage_reviews_or_opinions_read'] is False) and (ready['source_programmes_executed'] == []), 'No target scientific exposure or execution')
        need(len(a['all_assets_in_original_order']) == r['native_assets'] == 4, 'All original assets')
        nativepdf = [x for x in a['all_assets_in_original_order'] if Path(x['path']).suffix.lower() == '.pdf']
        need(len(nativepdf) == len(ready['actual_standalone_readers']) == r['native_readers'], 'Every actual native reader')
        for (original, reader) in zip(nativepdf, ready['actual_standalone_readers']):
            need(all((k in reader and typed(v, reader[k]) for (k, v) in original.items())), 'Whole native reader object/order')
        need(sum((x['pages'] for x in ready['actual_standalone_readers'])) == r['all_native_reader_pages'] == len(ready['fresh_page_rasters']), 'Every reader page has fresh unread raster')
        need([x['opaque_byte_splitlines_count'] for x in ready['all_TeX_candidates']] == r['all_archived_TeX_lines_in_original_order'], 'Every TeX source and original order')
        for t in ready['all_TeX_candidates']:
            b = Path(t['extracted_path']).read_bytes()
            need(len(b) == t['bytes'] and sha(b) == t['SHA256'] and (len(b.splitlines()) == t['opaque_byte_splitlines_count']) and (t['preamble_or_mathematical_body_read'] is False), 'Whole opaque TeX source identity')
        if r['record_id'] == 23205305:
            need([x['original_api_file_object']['key'] for x in ready['actual_standalone_readers']] == ['paper.pdf', 'height-repair.pdf'] and [x['pages'] for x in ready['actual_standalone_readers']] == [6, 4], 'Both complete136PDFreaders in native order')
            need(len(ready['additional_controlling_TeX_sources']) == 1 and len(ready['native_reader_source_structural_associations']) == 2 and (ready['all_native_reader_total_pages'] == 10), 'Additional136source/links directly preserved')
        for mode in default['source135' if r['record_id'] == 23202966 else 'source136']:
            need(mode['status'] == 'fulfilled' and mode['value']['exit_code'] == 0, 'Actual default pure closure exit')
            result = json.loads(mode['value']['output'])
            need(result['record_id'] == r['record_id'] and result['status'] == 'SOURCE_CUSTODY_PASS' and (result['mode'] == 'sealed') and (result['network_requests'] == result['writes'] == 0) and (result['scientific_reading_or_execution'] is False), 'Actual neutral pure default result')
        payload_total += ready['whole_regular_payload_occurrences']
        reader_pages += ready['all_native_reader_total_pages']
        rasters += len(ready['fresh_page_rasters'])
        requests += ready['actual_ordinary_native_HTTP_requests']
    need(payload_total == 89 and reader_pages == rasters == 16 and (requests == 18), 'Whole paired source custody totals')
    if not preseal:
        s = load(O / 'FINAL_SEAL.json')
        need(s['OWNED_MANIFEST_SHA256'] == sha((O / 'OWNED_MANIFEST.json').read_bytes()), 'Paired terminal manifest seal')
        for (name, h) in s['selected_payload_SHA256'].items():
            need(sha((O / name).read_bytes()) == h, 'Paired selected payload seal')
    print(json.dumps({'status': 'PAIRED_SOURCE_CUSTODY_PASS', 'mode': 'preseal' if preseal else 'sealed', 'checks': N, 'paired_owned_payloads': len(seen), 'records': [23202966, 23205305], 'original_native_assets': 8, 'actual_native_PDF_readers': 3, 'total_native_PDF_pages': 16, 'unviewed_fresh_rasters': 16, 'TeX_source_occurrences': 3, 'regular_archive_payloads': 89, 'actual_transport_responses': 18, 'target_scientific_reading_or_execution': False, 'project_imports': 0, 'subprocesses': 0, 'network_requests': 0, 'writes': 0}, sort_keys=True))
if __name__ == '__main__':
    need(sys.argv[1:] in [[], ['--preseal']], 'Usage: verify_read_only.py [--preseal]')
    main(sys.argv[1:] == ['--preseal'])
