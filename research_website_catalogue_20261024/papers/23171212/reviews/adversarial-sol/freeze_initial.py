"""Data-only source/metadata guard and finite INITIAL seal for exactly row 175."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import stat

O = Path('/Users/alec/Documents/Math/research_website_catalogue_20261024/papers/23171212/reviews/adversarial-sol')
S = O.parents[1] / 'sources'
TERMINALS = {'INITIAL_MANIFEST.json', 'INITIAL_SEAL.json'}

def need(test, message):
    if not test:
        raise RuntimeError(message)

def pin(path):
    info = path.lstat()
    need(stat.S_ISREG(info.st_mode), 'Nonordinary file: ' + str(path))
    data = path.read_bytes()
    return {'bytes': len(data), 'SHA256': hashlib.sha256(data).hexdigest(),
            'mode': oct(stat.S_IMODE(info.st_mode))}

def save(name, data):
    path = O / name
    need(not path.exists(), 'Refusing repeat output: ' + name)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + '\n')

def tree(root):
    need(stat.S_ISDIR(root.lstat().st_mode), 'Nonordinary root')
    files, dirs = {}, {}
    for path in root.rglob('*'):
        rel = path.relative_to(root).as_posix()
        info = path.lstat()
        if stat.S_ISREG(info.st_mode):
            files[rel] = pin(path)
        else:
            need(stat.S_ISDIR(info.st_mode), 'Symlink/special node: ' + str(path))
            dirs[rel] = oct(stat.S_IMODE(info.st_mode))
    return files, dirs

need(not any((O / x).exists() for x in TERMINALS), 'INITIAL already frozen')
mp, fp = pin(S / 'SOURCE_MANIFEST.json'), pin(S / 'SOURCE_FINAL.json')
need(mp == {'bytes': 20723, 'SHA256': '842831f3bfeb0d75d810d18fe30dad582d0e2615c5c7db2252d68db4c2aaf428', 'mode': '0o644'}, 'Source manifest differs')
need(fp == {'bytes': 909, 'SHA256': '4aaaf545371268d0e4e3014e5ac11498c8482b792581e7afa95fae9412adbb61', 'mode': '0o644'}, 'Source FINAL differs')
sm = json.loads((S / 'SOURCE_MANIFEST.json').read_bytes())
expected_source = {x['path']: {k: x[k] for k in ('bytes', 'SHA256', 'mode')} for x in sm['files']}
need(len(expected_source) == len(sm['files']), 'Duplicate source path')
expected_source.update({'SOURCE_MANIFEST.json': mp, 'SOURCE_FINAL.json': fp})
source_files, source_dirs = tree(S)
need(source_files == expected_source and len(source_files) == 87, 'Source file bytes/modes/extent differ')
need(source_dirs == {x['path']: x['mode'] for x in sm['directories']} and len(source_dirs) == 5, 'Source directory modes/topology differ')
need(oct(stat.S_IMODE(S.stat().st_mode)) == sm['root_mode'], 'Source root mode differs')
ready = json.loads((S / 'SOURCE_READY.json').read_bytes())
record = json.loads((S / 'record.response.body').read_bytes())
files_wrapper = json.loads((S / 'files-23171212.response.body').read_bytes())
need(ready['record'] == record['id'] == 23171212, 'Record identity differs')
need([x['key'] for x in record['files']] == ready['native_order'] == [x['key'] for x in files_wrapper['entries']], 'Native order differs')
asset_pins = []
for index, asset in enumerate(ready['native_assets'], 1):
    path = S / asset['asset']['path']
    actual = pin(path)
    need(all(actual[k] == asset['asset'][k] for k in ('bytes', 'SHA256', 'mode')), 'Asset differs')
    md5 = hashlib.md5(path.read_bytes()).hexdigest()
    need('md5:' + md5 == asset['native_MD5'], 'Native MD5 differs')
    asset_pins.append({'native_position': index, 'name': asset['name'], **actual,
                       'actual_MD5': md5, 'source_path': str(path), 'source_url': asset['source_url']})
need(len(asset_pins) == 7, 'Asset count differs')
for stream in ('extract.stdout.txt', 'extract.stderr.txt', 'render.stdout.txt', 'render.stderr.txt'):
    need((O / stream).read_bytes() == b'', 'Reader stream differs from observation')
need((S / 'assets/pr91_note.tex').read_bytes().count(b'\n') == 426, 'TeX line count differs')
need((O / 'manuscript.txt').read_bytes().count(b'\x0c') == 6, 'PDF text page count differs')
now = datetime.now(timezone.utc).isoformat()
save('SOURCE_PINS.json', {'schema': 'actual-source-first-native-identity-v1', 'UTC': now,
    'record': 23171212, 'row': 175, 'source_FINAL': fp, 'source_manifest': mp,
    'all87_source_buffers_modes_five_directories_authenticated_before_science': True,
    'raw_record': {'path': str(S / 'record.response.body'), **pin(S / 'record.response.body')},
    'raw_files_wrapper': {'path': str(S / 'files-23171212.response.body'), **pin(S / 'files-23171212.response.body')},
    'native_metadata_exact': record['metadata'],
    'native_status': {k: record.get(k, 'ABSENT') for k in ('created', 'modified', 'updated', 'status', 'state', 'submitted', 'is_published')},
    'native_order': ready['native_order'], 'native_custom_order': files_wrapper['order'],
    'native_default_preview': files_wrapper['default_preview'], 'native_assets': asset_pins,
    'controlling_TeX': ready['controlling_TeX'], 'native_PDF': ready['native_PDFs'][0],
    'native_version': record['metadata']['version'], 'printed_numeric_version': 'ABSENT after complete actual manuscript reading',
    'printed_date': 'October 5, 2026', 'full426_TeX_and_all6_PDF_text_and6_fresh_pages_personally_read': True,
    'actual_LICENSE_text': (S / 'assets/LICENSE.txt').read_text(),
    'rights_scope': 'CC BY 4.0 for original manuscript, verification code, results and authored documentation; third-party rights retained',
    'reader_exit_custody': {'one_sequential_shell_cell_final_exit': 0, 'pdftotext_individual_exit': None,
       'individual_exit_not_separately_captured': True, 'complete_six_page_text_produced_and_read': True,
       'fresh_six_page_Poppler_render_read': True, 'literal_four_empty_stream_files_retained': True},
    'native_public_Description_author_math_and_old_control_descriptions_exposed': True,
    'standalone_support_results_audit_program_foreign_current_opinions_opened': False,
    'scientific_program_executions': 0, 'network_operations': 0, 'peer_coordination': False,
    'publication_authority': False})
owned, dirs = tree(O)
expected = {'authenticate_source.py', 'SOURCE_CUSTODY.json', 'custody.stdout.json', 'custody.stderr.txt',
    'manuscript.txt', 'extract.stdout.txt', 'extract.stderr.txt', 'render.stdout.txt', 'render.stderr.txt',
    'RESEARCH_LOG.md', 'INITIAL.md', 'INDEPENDENT_RESULTS.md', 'freeze_initial.py',
    'freeze.stdout.txt', 'freeze.stderr.txt', 'SOURCE_PINS.json'}
expected.update('rasters/page-' + str(n) + '.png' for n in range(1, 7))
need(set(owned) == expected and len(owned) == 22, 'Owned INITIAL extent differs')
need(dirs == {'rasters': '0o755'}, 'Owned INITIAL directories differ')
need(oct(stat.S_IMODE(O.stat().st_mode)) == '0o755', 'Owned root mode differs')
save('INITIAL_MANIFEST.json', {'schema': 'actual-source-first-whole-result-manifest-v1',
    'UTC': now, 'root': str(O), 'root_mode': '0o755', 'files_including_two_terminal_controls': 24,
    'child_directories': [{'path': k, 'mode': v} for k, v in sorted(dirs.items())],
    'files': [{'path': k, **v} for k, v in sorted(owned.items())],
    'exact_root_terminal_exclusions': sorted(TERMINALS), 'ignored_and_empty_files_included': True})
save('INITIAL_SEAL.json', {'schema': 'actual-independent-adversarial-source-first-seal-v1',
    'UTC': now, 'record': 23171212, 'row': 175, 'status': 'SOURCE_FIRST_INITIAL_AND_ACTUAL_HAND_RESULTS_FROZEN',
    'whole_files': 24, 'child_directories': 1, 'INITIAL': pin(O / 'INITIAL.md'),
    'independent_results': pin(O / 'INDEPENDENT_RESULTS.md'), 'source_pins': pin(O / 'SOURCE_PINS.json'),
    'manifest': pin(O / 'INITIAL_MANIFEST.json'), 'source_first_complete_percent': 100,
    'full_review_estimate_percent': 60, 'all426_TeX_all6_PDF_text_all6_fresh_pixels_personally_read': True,
    'support_results_audits_programs_foreign_current_peer_root_bodies_opened': False,
    'scientific_program_executions': 0, 'network_operations': 0, 'peer_coordination': False,
    'mathematical_findings_withheld_until_root_gate': True, 'publication_authority': False,
    'AA': None, 'canonical_url': None, 'follow_up': None})
