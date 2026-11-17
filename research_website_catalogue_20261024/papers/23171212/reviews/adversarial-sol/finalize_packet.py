"""Sole bounded data-only closure of row 175; no scientific code or subprocess."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import stat

O = Path('/Users/alec/Documents/Math/research_website_catalogue_20261024/papers/23171212/reviews/adversarial-sol')
S = O.parents[1] / 'sources'
C = Path('/Users/alec/Documents/Math/draft_pr_publication_program_20260930/audits/pr85_30001203/isolated_main_integration_20261005/checkout/draft_pr_publication_program_20260930/audits/pr91_30003052')
RAW = [
    ('kuester2015', 'ROOT_source_scope_20261005/kuester2015.pdf', 614785, '4422566d4944d0530e610071c3809566829bf18bf7846265e0f981a31c79f9fb', 74),
    ('owr2016', 'ROOT_source_scope_20261005/owr2016.pdf', 491758, '28a2dc55933344c73a994f7eb50436469c7ddc4bc9ec73166d5cb8b97855aa1d', 44),
    ('efhn2016', 'general_operator_priority_20261005/sources/efhn2016.pdf', 6531412, 'd32573669adf2d0b93718e397e417be3e055655ecbbe8dd6d06c0088c37d7442', 606),
]
CONTROLS = {'OWNED_MANIFEST.json', 'FINAL.json'}

def need(test, message):
    if not test:
        raise RuntimeError(message)

def pin(path):
    info = path.lstat()
    need(stat.S_ISREG(info.st_mode), 'Nonordinary file: ' + str(path))
    data = path.read_bytes()
    return {'bytes': len(data), 'SHA256': hashlib.sha256(data).hexdigest(), 'mode': oct(stat.S_IMODE(info.st_mode))}

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

def check(expected, actual, message):
    need(all(expected[k] == actual[k] for k in ('bytes', 'SHA256', 'mode')), message)

def save(name, value):
    path = O / name
    need(not path.exists(), 'Refusing replacement/repeated seal: ' + name)
    path.write_text(json.dumps(value, indent=2) + '\n')

need(not any((O / x).exists() for x in CONTROLS), 'Already finalized')
mp, fp = pin(S / 'SOURCE_MANIFEST.json'), pin(S / 'SOURCE_FINAL.json')
check({'bytes': 20723, 'SHA256': '842831f3bfeb0d75d810d18fe30dad582d0e2615c5c7db2252d68db4c2aaf428', 'mode': '0o644'}, mp, 'Source manifest changed')
check({'bytes': 909, 'SHA256': '4aaaf545371268d0e4e3014e5ac11498c8482b792581e7afa95fae9412adbb61', 'mode': '0o644'}, fp, 'Source FINAL changed')
sm = json.loads((S / 'SOURCE_MANIFEST.json').read_bytes())
expected_source = {x['path']: {k: x[k] for k in ('bytes', 'SHA256', 'mode')} for x in sm['files']}
need(len(expected_source) == len(sm['files']), 'Duplicate source name')
expected_source.update({'SOURCE_MANIFEST.json': mp, 'SOURCE_FINAL.json': fp})
source_files, source_dirs = tree(S)
need(source_files == expected_source and len(source_files) == 87, 'Source bytes/modes/extent changed')
need(source_dirs == {x['path']: x['mode'] for x in sm['directories']} and len(source_dirs) == 5, 'Source directories changed')
need(oct(stat.S_IMODE(S.stat().st_mode)) == sm['root_mode'], 'Source root mode changed')
im_pin, is_pin = pin(O / 'INITIAL_MANIFEST.json'), pin(O / 'INITIAL_SEAL.json')
check({'bytes': 4393, 'SHA256': '9520fbd5a7926773f075b200431b00dec0aeaef046297aad96457a754481d193', 'mode': '0o644'}, im_pin, 'Initial manifest changed')
check({'bytes': 1327, 'SHA256': 'ac10b5d5a893c8816b0c77e2af331112cb74ce5d5cd2744f51fe4144e9efddee', 'mode': '0o644'}, is_pin, 'Initial seal changed')
im = json.loads((O / 'INITIAL_MANIFEST.json').read_bytes())
initial_names = {x['path'] for x in im['files']} | {'INITIAL_MANIFEST.json', 'INITIAL_SEAL.json'}
need(len(initial_names) == 24, 'Initial file extent differs')
for item in im['files']:
    check(item, pin(O / item['path']), 'Original initial payload changed: ' + item['path'])
for item in im['child_directories']:
    need(oct(stat.S_IMODE((O / item['path']).lstat().st_mode)) == item['mode'], 'Initial directory mode changed')

raw_pins = []
for name, rel, count, digest, pages in RAW:
    actual = pin(C / rel)
    need(actual['bytes'] == count and actual['SHA256'] == digest, 'Raw primary changed: ' + rel)
    raw_pins.append({'path': str(C / rel), **actual, 'pages_observed_in_pdfinfo': pages})
    for suffix in ('.pdfinfo.stderr.txt', '.extract.stderr.txt', '.extract.stdout.txt'):
        need((O / 'primaries' / (name + suffix)).read_bytes() == b'', 'Primary reader diagnostic differs')
    need((O / 'primaries' / (name + '.txt')).stat().st_size > 0, 'Missing primary text')
    need((O / 'primaries' / (name + '.pdfinfo.stdout.txt')).stat().st_size > 0, 'Missing literal PDF metadata')
images = ['kuester52', 'owr25', 'efhn326', 'efhn331']
for name in images:
    need((O / 'primary-pages' / (name + '.png')).stat().st_size > 0, 'Missing primary image')
    for stream in ('stdout', 'stderr'):
        need((O / 'primary-pages' / (name + '.' + stream + '.txt')).read_bytes() == b'', 'Primary render stream differs')

now = datetime.now(timezone.utc).isoformat()
save('SOURCE_CLOSURE.json', {'schema': 'bounded-independent-adversarial-custody-closure-v1',
    'UTC': now, 'record': 23171212, 'row': 175, 'SOURCE_FINAL': fp, 'SOURCE_MANIFEST': mp,
    'all87_source_buffers_modes_five_directories_unchanged': True, 'all24_initial_files_unchanged': True,
    'INITIAL_manifest': im_pin, 'INITIAL_seal': is_pin, 'raw_primary_bodies': raw_pins,
    'separately_observed_primary_pdfinfo_exits': [0, 0, 0],
    'separately_observed_primary_extract_exits': [0, 0, 0],
    'separately_observed_primary_render_exits': [0, 0, 0, 0],
    'all_primary_literal_streams_retained': True, 'all_four_new_primary_images_personally_inspected': True,
    'initial_native_extraction_individual_exit_not_captured': True, 'initial_reader_cell_final_render_exit': 0,
    'scientific_native_program_executions': 0, 'new_network_operations': 0, 'peer_coordination': False,
    'archived_or_current_review_findings_opened': False, 'other_namespace_writes': False})
with (O / 'POST_INITIAL_LOG.md').open('a') as log:
    log.write('\n- ' + now + ' — Full bounded review and custody closure complete, 100%. '
        'All87 source files/five directories and original24 INITIAL files authenticate unchanged. '
        'Three exact raw primary bodies remain at authenticated external paths; all literal reader outputs, '
        'including empty files and the initial extraction-exit reporting limit, are preserved. '
        'No scientific/native execution, network acquisition, peer coordination or outside write occurred. '
        'Final whole-file/mode manifest and FINAL are being frozen by the sole fully read data-only closure invocation; '
        'quiescent afterwards. Scientific findings remain withheld pending root source-first gate.\n')
owned_files, owned_dirs = tree(O)
expected = initial_names | {'POST_INITIAL_LOG.md', 'PRIMARY_INTERFACES.md', 'REPORT.md', 'finalize_packet.py',
    'finalize.stdout.txt', 'finalize.stderr.txt', 'SOURCE_CLOSURE.json'}
for name, *_ in RAW:
    expected.update('primaries/' + name + suffix for suffix in
        ('.txt', '.pdfinfo.stdout.txt', '.pdfinfo.stderr.txt', '.extract.stdout.txt', '.extract.stderr.txt'))
for name in images:
    expected.update('primary-pages/' + name + suffix for suffix in ('.png', '.stdout.txt', '.stderr.txt'))
need(set(owned_files) == expected and len(owned_files) == 58, 'Owned final extent differs')
need(owned_dirs == {'rasters': '0o755', 'primaries': '0o755', 'primary-pages': '0o755'}, 'Owned topology/modes differ')
need(oct(stat.S_IMODE(O.stat().st_mode)) == '0o755', 'Owned root mode differs')
save('OWNED_MANIFEST.json', {'schema': 'finite-independent-adversarial-whole-packet-manifest-v1',
    'UTC': now, 'root': str(O), 'root_mode': '0o755', 'ordinary_files_including_controls': 60,
    'child_directory_count': 3, 'directories': [{'path': k, 'mode': v} for k, v in sorted(owned_dirs.items())],
    'files': [{'path': k, **v} for k, v in sorted(owned_files.items())],
    'exact_root_terminal_exclusions': sorted(CONTROLS), 'all_ignored_and_empty_files_included': True})
save('FINAL.json', {'schema': 'independent-adversarial-scientific-FINAL-v1', 'UTC': now,
    'record': 23171212, 'row': 175, 'status': 'COMPLETE_FROZEN_QUIESCENT', 'completion_percent': 100,
    'whole_files': 60, 'child_directories': 3, 'manifest': pin(O / 'OWNED_MANIFEST.json'),
    'report': pin(O / 'REPORT.md'), 'primary_interfaces': pin(O / 'PRIMARY_INTERFACES.md'),
    'source_closure': pin(O / 'SOURCE_CLOSURE.json'), 'immutable_initial_seal': is_pin,
    'private_original_claim_disposition': 'PASS: full printed analytic classification and exact cited primary interfaces; no substantive gap identified',
    'scientific_program_executions': 0, 'network_operations': 0, 'peer_coordination': False,
    'reader_limits': 'Initial pdftotext individual exit not separately captured; shared reader cell final render exit0, complete text/six actual pages read; all literal streams retained',
    'root_gate_open': False, 'findings_withheld_from_root': True, 'publication_authority': False,
    'AA': None, 'canonical_url': None, 'follow_up': None,
    'closure_invocation': 'python3 finalize_packet.py > finalize.stdout.txt 2> finalize.stderr.txt',
    'closure_body_personally_read_whole_before_sole_execution': True})
