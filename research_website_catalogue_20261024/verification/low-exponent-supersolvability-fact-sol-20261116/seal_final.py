"""Finite fact/copy envelope closure only; never executes any reviewed helper."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import stat

P = Path('/Users/alec/Documents/Math/research_website_catalogue_20261024')
O = P / 'verification/low-exponent-supersolvability-fact-sol-20261116'
N = P / 'verification/low-exponent-supersolvability-editorial-sol-20261116'
S = P / 'papers/23331709/sources'

def need(test, message):
    if not test:
        raise RuntimeError(message)

def pin(path):
    mode = path.lstat().st_mode
    need(stat.S_ISREG(mode), 'Nonordinary file: ' + str(path))
    data = path.read_bytes()
    return {'bytes': len(data), 'SHA256': hashlib.sha256(data).hexdigest(), 'mode': oct(stat.S_IMODE(mode))}

def check(expected, actual, message):
    need(all(expected[k] == actual[k] for k in ('bytes', 'SHA256', 'mode')), message)

def save(name, obj):
    target = O / name
    need(not target.exists(), 'Refusing replacement/final rerun: ' + name)
    target.write_text(json.dumps(obj, indent=2) + '\n')

need(not (O / 'FINAL.json').exists() and not (O / 'OWNED_MANIFEST.json').exists(), 'Already final')
check({'bytes': 863, 'SHA256': '6bcbfcce8079f31936b2bbbcd37830d3c1fd8d5a344d9fcb1280e5db9e82ccc7', 'mode': '0o644'}, pin(O / 'INITIAL_SEAL.json'), 'Initial seal changed')
check({'bytes': 1708, 'SHA256': '85964177f686fd75c54f15c7364c37174126e8aead0437b23858f2be4a631e50', 'mode': '0o644'}, pin(O / 'INITIAL_MANIFEST.json'), 'Initial manifest changed')
im = json.loads((O / 'INITIAL_MANIFEST.json').read_bytes())
for item in im['files']:
    check(item, pin(O / item['path']), 'Original initial payload changed')
initial_names = {x['path'] for x in im['files']} | {'INITIAL_MANIFEST.json', 'INITIAL_SEAL.json'}
need(len(initial_names) == 9, 'Initial extent changed')
result = json.loads((O / 'check.stdout.json').read_bytes())
need(result['status'] == 'DATA_CUSTODY_PASS_WITH_ONE_HUMAN_COPY_FINDING', 'Data result differs')
need((O / 'check.stderr.txt').read_bytes() == b'', 'Literal data-check stderr differs')
execution = json.loads((O / 'EXECUTION.json').read_bytes())
for key in ('helper', 'stdout', 'stderr'):
    item = execution[key]
    actual = pin(O / item['path'])
    need(item['bytes'] == actual['bytes'] and item['SHA256'] == actual['SHA256'], 'Check body/streams changed')
need(execution['exit'] == 0 and execution['ordinary_invocations'] == 1, 'Execution receipt differs')
need(len(result['writer_file_pins']) == 22, 'Writer extent receipt differs')
need({x.name for x in N.iterdir()} == set(result['writer_file_pins']), 'Writer names changed')
for name, expected in result['writer_file_pins'].items():
    check(expected, pin(N / name), 'Frozen writer bytes/modes changed')
expect = json.loads((O / 'SOURCE_EXPECTATIONS.json').read_bytes())
for key in ('root_clearance', 'root_report', 'controlling_TeX', 'root_PDF_text_read'):
    item = expect[key]
    check(item, pin(Path(item['path'])), 'Source/authority read input changed')
check(expect['source_manifest'], pin(S / 'SOURCE_MANIFEST.json'), 'Source manifest changed')
check(expect['source_FINAL'], pin(S / 'SOURCE_FINAL.json'), 'Source FINAL changed')
sm = json.loads((S / 'SOURCE_MANIFEST.json').read_bytes())
actual_files, actual_dirs = set(), {}
for path in S.rglob('*'):
    info = path.lstat()
    rel = path.relative_to(S).as_posix()
    if stat.S_ISREG(info.st_mode): actual_files.add(rel)
    else:
        need(stat.S_ISDIR(info.st_mode), 'Source symlink/special node')
        actual_dirs[rel] = oct(stat.S_IMODE(info.st_mode))
need(actual_files == {x['path'] for x in sm['files']} | {'SOURCE_MANIFEST.json', 'SOURCE_FINAL.json'} and len(actual_files) == 120, 'Source extent changed')
need(actual_dirs == {x['path']: x['mode'] for x in sm['directories']} and len(actual_dirs) == 17, 'Source topology changed')
for item in sm['files']:
    check(item, pin(S / item['path']), 'Source original byte/mode changed')
now = datetime.now(timezone.utc).isoformat()
with (O / 'POST_INITIAL_LOG.md').open('a') as log:
    log.write('\n- ' + now + ' — Bounded fact/copy family complete100%, one exact short-metadata qualification '
        'COPY-1 retained for root adoption. Full visible copy and assets pass; no repaired candidate is falsely certified. '
        'The sole fully read data/static comparison exited0 with literal5424-byte stdout/empty stderr; no rerun. '
        'Original9 INITIAL, all22 frozen writer and all120 source buffers remain unchanged. '
        'Finite whole-file/mode manifest and FINAL now freeze this20-file/zero-child-directory folder; '
        'quiescent after closure. No publication/AA/installation authority.\n')
expected_owned = initial_names | {'POST_INITIAL_LOG.md', 'check_copy_independently.py', 'check.stdout.json',
    'check.stderr.txt', 'EXECUTION.json', 'REPORT.md', 'seal_final.py', 'seal.stdout.txt', 'seal.stderr.txt'}
owned = {}
for path in O.iterdir():
    need(stat.S_ISREG(path.lstat().st_mode), 'Unexpected owned directory/special node')
    owned[path.name] = pin(path)
need(set(owned) == expected_owned and len(owned) == 18, 'Owned closure extent differs')
need(oct(stat.S_IMODE(O.stat().st_mode)) == '0o755', 'Owned root mode differs')
save('OWNED_MANIFEST.json', {'schema': 'finite-independent-fact-copy-whole-manifest-v1', 'UTC': now,
    'root': str(O), 'root_mode': '0o755', 'whole_files_including_controls': 20, 'child_directories': [],
    'files': [{'path': k, **v} for k, v in sorted(owned.items())],
    'exact_root_terminal_exclusions': ['OWNED_MANIFEST.json', 'FINAL.json'],
    'all_hidden_ignored_empty_files_modes_included': True})
save('FINAL.json', {'schema': 'independent-private-fact-copy-final-v1', 'UTC': now, 'record': 23331709,
    'row': 167, 'status': 'COMPLETE_FROZEN_ONE_COPY_QUALIFICATION_REQUIRED', 'completion_percent': 100,
    'whole_files': 20, 'child_directories': 0, 'manifest': pin(O / 'OWNED_MANIFEST.json'),
    'report': pin(O / 'REPORT.md'), 'actual_data_result': pin(O / 'check.stdout.json'),
    'execution_receipt': pin(O / 'EXECUTION.json'), 'writer_FINAL': result['writer_FINAL'],
    'writer_manifest': result['writer_manifest'], 'original_INITIAL_seal': pin(O / 'INITIAL_SEAL.json'),
    'visible_MAIN_abstract_context_assets_pass': True, 'copy_fix_required_before_promotion': result['copy_findings_from_personal_whole_context_read'],
    'source_scientific_clearance_unchanged': True, 'MAIN_rewrite_required': False,
    'all9_initial_all22_writer_all120_source_files_unchanged': True,
    'new_scientific_native_producer_helper_browser_render_network_or_external_contact': False,
    'W_Git_Sheet_source_or_old_packet_mutations': False, 'publication_authority': False,
    'AA': None, 'canonical_url': None, 'follow_up': None,
    'quiescent': True, 'post_final_writes_or_executions': False})
