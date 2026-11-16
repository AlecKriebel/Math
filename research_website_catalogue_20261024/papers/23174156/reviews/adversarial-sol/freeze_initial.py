"""Data-only custody for the actual source-first adversarial notes; no scientific execution."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import stat

R = Path(__file__).resolve().parent
S = R.parents[1] / 'sources'
def pin(path):
    raw = path.read_bytes()
    return {'bytes': len(raw), 'SHA256': hashlib.sha256(raw).hexdigest(),
            'mode': oct(stat.S_IMODE(path.stat().st_mode))}
def match(path, item):
    actual = pin(path)
    assert actual['bytes'] == item['bytes'] and actual['SHA256'] == item['SHA256'], str(path)
    assert int(actual['mode'], 8) == int(item['mode'], 8), str(path)

assert pin(S / 'SOURCE_FINAL.json')['SHA256'] == '153bc99484999f9e5bca8623ee88e9935cf2c42557626112161f8f372a5a4827'
final = json.loads((S / 'SOURCE_FINAL.json').read_text())
for name in ['SOURCE_READY', 'SOURCE_MANIFEST']:
    match(S / final[name]['path'], final[name])
manifest = json.loads((S / 'SOURCE_MANIFEST.json').read_text())
paths = sorted(S.rglob('*'))
assert not any(p.is_symlink() for p in paths)
assert {p.relative_to(S).as_posix() for p in paths if p.is_file()} == {x['path'] for x in manifest['files']} | {'SOURCE_FINAL.json', 'SOURCE_MANIFEST.json'}
assert len([p for p in paths if p.is_file()]) == 186
assert len([p for p in paths if p.is_dir()]) == 18
for item in manifest['files']:
    match(S / item['path'], item)
record = json.loads((S / 'record.response.body').read_text())
wrapper = json.loads((S / 'files-23174156.response.body').read_text())
metadata = {k: record.get(k, 'ABSENT') for k in ['id', 'doi', 'conceptdoi', 'created', 'modified', 'updated', 'status', 'state', 'submitted', 'is_published']}
metadata['metadata'] = {k: record['metadata'].get(k, 'ABSENT') for k in ['title', 'publication_date', 'version', 'resource_type', 'access_right', 'license', 'creators']}
native = [{'name': x['key'], 'native_MD5': x['checksum'], 'created': x['created'], 'updated': x['updated'], **pin(S / 'assets' / x['key'])} for x in wrapper['entries']]
pins = {'schema': 'source-first-adversarial-native-reading-pins-v1', 'record_id': 23174156,
        'metadata': metadata, 'printed_date': 'October 5, 2026', 'printed_numeric_version': 'ABSENT',
        'native_assets_in_literal_order': native, 'record_order': [x['key'] for x in record['files']],
        'custom_order': wrapper['order'], 'default_preview': wrapper['default_preview'],
        'source_controls_by_reference': [{'path': 'papers/23174156/sources/' + name, **pin(S / name)} for name in ['SOURCE_FINAL.json', 'SOURCE_MANIFEST.json', 'SOURCE_READY.json', 'record.response.body', 'files-23174156.response.body']],
        'source_extent_files_dirs': [186, 18], 'full_opaque_source_baseline_unchanged': True,
        'native_PDF': {'path': 'papers/23174156/sources/assets/pr95_note.pdf', 'pages': 5, **pin(S / 'assets/pr95_note.pdf')},
        'actual_TeX': {'path': 'papers/23174156/sources/assets/pr95_note.tex', 'lines': 292, **pin(S / 'assets/pr95_note.tex')},
        'actual_license': {'path': 'papers/23174156/sources/assets/LICENSE.txt', 'human_read': True, **pin(S / 'assets/LICENSE.txt')},
        'license_scope': 'CC BY4.0 all original manuscript/code/results/authored documentation; third-party rights separate; no MIT split',
        'all_TeX_native_PDF_pages_and_complete_extracted_text_personally_read': True,
        'fresh_rasters': [{'path': f'rasters/page-{i}.png', 'personally_read': True, **pin(R / f'rasters/page-{i}.png')} for i in range(1, 6)],
        'render': {'utility': 'Trusted installed Poppler pdftoppm', 'dpi': 140, 'exit': 0,
                   'stdout': {'path': 'render.stdout.txt', **pin(R / 'render.stdout.txt')},
                   'stderr': {'path': 'render.stderr.txt', **pin(R / 'render.stderr.txt')}},
        'text': {'path': 'manuscript.txt', 'extraction_exit': 0, 'complete_body_read': True, **pin(R / 'manuscript.txt')},
        'prior_opaque_acquisition_and_manuscript_native_Description_assertions_disclosed': True,
        'support_code_results_README_priority_archived_current_reviews_or_new_foreign_math_bodies_opened': False,
        'scientific_native_executions': 0, 'publication_authority': False, 'AA': None, 'canonical_url': None, 'followup': None}
(R / 'SOURCE_PINS.json').write_text(json.dumps(pins, indent=2, ensure_ascii=False) + '\n')
files = []
for path in sorted(R.rglob('*')):
    assert not path.is_symlink()
    if path.is_file() and path.name != 'INITIAL_SEAL.json':
        files.append({'path': path.relative_to(R).as_posix(), **pin(path)})
assert len(files) == 13
seal = {'schema': 'actual-source-first-adversarial-result-seal-v1', 'record_id': 23174156, 'row': 169,
        'UTC': datetime.now(timezone.utc).isoformat(), 'status': 'ACTUAL_INITIAL_AND_INDEPENDENT_RESULTS_FROZEN',
        'actual_regular_files': 14, 'payload_files': 13, 'child_directories': ['rasters'], 'files': files,
        'exact_root_terminal_exclusion': 'INITIAL_SEAL.json', 'all_actual_manuscript_reading_and_hand_results_complete': True,
        'source_first_completion_percent': 100, 'full_adversarial_completion_estimate_percent': 60,
        'foreign_support_programs_results_README_priority_current_peer_root_and_archived_opinion_bodies_unopened': True,
        'scientific_native_executions': 0, 'findings_withheld_until_root_own_INITIAL': True,
        'publication_authority': False, 'AA': None, 'canonical_url': None, 'followup': None}
(R / 'INITIAL_SEAL.json').write_text(json.dumps(seal, indent=2) + '\n')
print(json.dumps({n: pin(R / n) for n in ['INITIAL_SEAL.json', 'INITIAL.md', 'INDEPENDENT_RESULTS.md', 'SOURCE_PINS.json']}, indent=2))
