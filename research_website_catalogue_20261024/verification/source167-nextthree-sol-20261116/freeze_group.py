"""One-use data-only closure of the three immutable source packets and this group."""
from pathlib import Path
import datetime
import hashlib
import json
import stat

G = Path(__file__).resolve().parent
P = G.parents[1]
ROWS = {23331709: 167, 23174156: 169, 23137834: 170}
EXPECTED = {23331709: 'c2fc40cc1154d3aa47ab74e9c7dcfffc202c7238864ff4b86e1ffad094974c25',
            23174156: '153bc99484999f9e5bca8623ee88e9935cf2c42557626112161f8f372a5a4827',
            23137834: '14cbf430570b90574e7c28bba911e7fe2b868c164107591b1783694c30212f80'}
CONTROLS = {'FINAL.json', 'OWNED_MANIFEST.json'}
def pin(path, root):
    raw = path.read_bytes()
    return {'path': path.relative_to(root).as_posix(), 'bytes': len(raw),
            'SHA256': hashlib.sha256(raw).hexdigest(), 'mode': oct(stat.S_IMODE(path.stat().st_mode))}
def match(path, item, root):
    actual = pin(path, root)
    assert actual['bytes'] == item['bytes'] and actual['SHA256'] == item['SHA256'], str(path)
    assert int(actual['mode'], 8) == int(item['mode'], 8), str(path)
def dump(path, value):
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + '\n')

assert pin(G / 'acquire_source.py', G)['SHA256'] == '28c1649a17a4860fb4e911429fa06557a6bffd7f9af61f05dcac4e19af7490f7'
rows = []
totals = dict(source_files=0, source_child_directories=0, native_assets=0, containers=0,
              member_occurrences=0, native_PDF_pages=0, HTTP_GETs=0, ordinary_redirect_responses=0,
              access_or_transport_failures=0, pdfinfo_calls=0)
for record, row in ROWS.items():
    S = P / 'papers' / str(record) / 'sources'
    assert pin(S / 'SOURCE_FINAL.json', S)['SHA256'] == EXPECTED[record]
    final = json.loads((S / 'SOURCE_FINAL.json').read_text())
    assert final['record'] == record and final['acquisition_complete'] is True
    for name in ['SOURCE_MANIFEST', 'SOURCE_READY']:
        match(S / final[name]['path'], final[name], S)
    manifest = json.loads((S / 'SOURCE_MANIFEST.json').read_text())
    ready = json.loads((S / 'SOURCE_READY.json').read_text())
    paths = sorted(S.rglob('*'))
    assert not any(p.is_symlink() for p in paths)
    actual_files = {p.relative_to(S).as_posix() for p in paths if p.is_file()}
    expected_files = {x['path'] for x in manifest['files']} | {'SOURCE_MANIFEST.json', 'SOURCE_FINAL.json'}
    assert actual_files == expected_files and len(actual_files) == final['extent']['ordinary_files']
    actual_dirs = {p.relative_to(S).as_posix() for p in paths if p.is_dir()}
    assert actual_dirs == {x['path'] for x in manifest['directories']}
    assert all(p.is_dir() or stat.S_ISREG(p.stat().st_mode) for p in paths)
    for item in manifest['files']:
        match(S / item['path'], item, S)
    for item in manifest['directories']:
        assert stat.S_IMODE((S / item['path']).stat().st_mode) == int(item['mode'], 8)
    for item in ready['native_assets']:
        path = S / item['asset']['path']
        match(path, item['asset'], S)
        raw = path.read_bytes()
        assert hashlib.md5(raw).hexdigest() == item['native_MD5'][4:]
        assert raw == (S / (item['response_label'] + '.response.body')).read_bytes()
    requests = []
    for path in sorted(S.glob('*.transport.json')):
        event = json.loads(path.read_text())
        status = event['curl_transport']['http_code']
        assert event['exit'] == 0 and status in (200, 301, 302, 303, 307, 308)
        assert event['automatic_retries'] == 0 and event['automatic_redirects'] is False
        assert event['command'][event['command'].index('--request') + 1] == 'GET'
        requests.append({'receipt': pin(path, S), 'exit': event['exit'], 'HTTP': status})
        totals['HTTP_GETs'] += 1
        totals['ordinary_redirect_responses'] += int(status != 200)
    assert all(x['metadata']['exit'] == 0 for x in ready['native_PDFs'])
    execution = json.loads((G / ('SOURCE' + str(record) + '_EXECUTION.json')).read_text())
    assert execution['tool_exit_code'] == 0 and execution['source_sealed_complete'] is True
    assert (G / execution['stderr']).stat().st_size == 0
    output_lines = (G / execution['stdout']).read_text().splitlines()
    sealed = [json.loads(x[7:]) for x in output_lines if x.startswith('SEALED ')]
    assert len(sealed) == 1 and sealed[0]['SOURCE_FINAL']['SHA256'] == EXPECTED[record]
    totals['source_files'] += len(actual_files)
    totals['source_child_directories'] += len(actual_dirs)
    totals['native_assets'] += len(ready['native_assets'])
    totals['containers'] += ready['container_count']
    totals['member_occurrences'] += ready['archive_member_occurrences']
    totals['native_PDF_pages'] += sum(x['metadata']['pages'] for x in ready['native_PDFs'])
    totals['pdfinfo_calls'] += len(list(S.glob('pdfinfo-*.execution.json')))
    metadata_keys = ['title', 'DOI', 'concept_DOI', 'native_version', 'native_version_field_present',
                     'publication_date_declared', 'created', 'modified', 'updated', 'status', 'state',
                     'submitted', 'is_published', 'resource_type', 'access_right', 'license', 'creators',
                     'native_order', 'files_entries_order', 'files_custom_order', 'default_preview',
                     'latest_record_id', 'fixed_record_is_latest', 'version_record_ids']
    rows.append({'record': record, 'sheet_row': row, 'source_root': str(S),
                 'SOURCE_FINAL': pin(S / 'SOURCE_FINAL.json', S), 'SOURCE_MANIFEST': final['SOURCE_MANIFEST'],
                 'SOURCE_READY': final['SOURCE_READY'], 'extent': final['extent'],
                 'native_metadata': {k: ready[k] for k in metadata_keys},
                 'native_assets': ready['native_assets'], 'controlling_TeX': ready['controlling_TeX'],
                 'native_PDFs': ready['native_PDFs'], 'all_materialized_PDFs': ready['all_materialized_PDFs'],
                 'container_count': ready['container_count'], 'archive_member_occurrences': ready['archive_member_occurrences'],
                 'ordinary_requests': requests, 'full_sealed_source_inventory_unchanged': True})

now = datetime.datetime.now(datetime.timezone.utc).isoformat()
handoff = {'schema': 'fixed-three-opaque-native-source-handoff-v1', 'UTC': now,
           'exact_rows': [167, 169, 170], 'row_168_excluded': True, 'records': rows, 'totals': totals,
           'all_native_sizes_MD5_SHA256_and_response_copy_bytes_verified': True,
           'all_source_files_directories_modes_and_seals_unchanged': True,
           'scientific_prose_or_printed_numeric_versions_inspected': False,
           'archived_opinions_results_README_or_native_programs_read_or_executed': False,
           'scientific_verdict': None, 'publication_authority': False, 'completion_percent_acquisition': 100}
dump(G / 'HANDOFF.json', handoff)
files, dirs = [], []
for path in sorted(G.rglob('*')):
    assert not path.is_symlink()
    rel = path.relative_to(G).as_posix()
    if path.is_dir():
        dirs.append(rel)
    else:
        assert stat.S_ISREG(path.stat().st_mode)
        if rel not in CONTROLS:
            files.append(pin(path, G))
assert len(files) == 16 and not dirs
dump(G / 'OWNED_MANIFEST.json', {'schema': 'finite-opaque-source-group-owned-manifest-v1', 'UTC': now,
     'actual_regular_files': 18, 'payload_files': 16, 'child_directories': [], 'files': files,
     'symlinks': [], 'special_files': [], 'exact_root_terminal_controls': sorted(CONTROLS),
     'no_ignored_payload_subtree_runtime_or_future_exclusions': True})
dump(G / 'FINAL.json', {'schema': 'fixed-three-opaque-source-group-final-v1', 'UTC': now,
     'status': 'COMPLETE_FROZEN_QUIESCENT_OPAQUE_ACQUISITION_ONLY', 'completion_percent_acquisition': 100,
     'exact_targets': ROWS, 'row_168_excluded': True, 'actual_group_files': 18, 'group_child_directories': 0,
     'source_totals': totals, 'total_owned_files_including_three_sources': totals['source_files'] + 18,
     'HANDOFF': pin(G / 'HANDOFF.json', G), 'REPORT': pin(G / 'REPORT.md', G),
     'OWNED_MANIFEST': pin(G / 'OWNED_MANIFEST.json', G),
     'scientific_verdict': None, 'scientific_body_reading_or_native_execution': False,
     'printed_versions_uninspected': True, 'publication_authority': False, 'AA': None,
     'canonical_url': None, 'followup': None, 'all_four_owned_roots_quiescent_after_this_seal': True})
for item in files:
    match(G / item['path'], item, G)
assert len([p for p in G.rglob('*') if p.is_file()]) == 18
print(json.dumps({'group_files': 18, 'group_child_dirs': 0, 'totals': totals,
                  'pins': {n: pin(G / n, G) for n in ['FINAL.json', 'OWNED_MANIFEST.json', 'HANDOFF.json', 'REPORT.md']}}, indent=2))
