"""Finite COPY-1 fact envelope closure; does not replay the data comparison."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import stat

P = Path('/Users/alec/Documents/Math/research_website_catalogue_20261024')
O = P / 'verification/low-exponent-supersolvability-charzero-fact-sol-20261116'
F = P / 'verification/low-exponent-supersolvability-fact-sol-20261116'
S = P / 'papers/23331709/sources'

def need(test, message):
    if not test:
        raise RuntimeError(message)

def pin(path):
    info = path.lstat()
    need(stat.S_ISREG(info.st_mode), 'Nonordinary file: ' + str(path))
    data = path.read_bytes()
    return {'bytes': len(data), 'SHA256': hashlib.sha256(data).hexdigest(), 'mode': oct(stat.S_IMODE(info.st_mode))}

def check(expected, actual, message):
    need(all(expected[k] == actual[k] for k in ('bytes', 'SHA256', 'mode')), message)

def save(name, obj):
    path = O / name
    need(not path.exists(), 'Refusing repeated closure/replacement: ' + name)
    path.write_text(json.dumps(obj, indent=2) + '\n')

need(not (O / 'FINAL.json').exists() and not (O / 'OWNED_MANIFEST.json').exists(), 'Already closed')
check({'bytes': 787, 'SHA256': '83c4d58fe90312dca7a5ce43231788187f7840080388fef94534be60e94cdd58', 'mode': '0o644'}, pin(O / 'INITIAL_SEAL.json'), 'Initial seal changed')
check({'bytes': 618, 'SHA256': '6f33be3f5c3d7694e3f21df98c136e69aba2da5bd57bb8beeef10ef5a49f4d1f', 'mode': '0o644'}, pin(O / 'INITIAL_MANIFEST.json'), 'Initial manifest changed')
im = json.loads((O / 'INITIAL_MANIFEST.json').read_bytes())
for row in im['files']:
    check(row, pin(O / row['path']), 'Initial payload changed')
initial_names = {x['path'] for x in im['files']} | {'INITIAL_MANIFEST.json', 'INITIAL_SEAL.json'}
need(len(initial_names) == 4, 'Initial extent differs')
execution = json.loads((O / 'EXECUTION.json').read_bytes())
for key in ('helper', 'stdout', 'stderr'):
    row = execution[key]
    actual = pin(O / row['path'])
    need(actual['bytes'] == row['bytes'] and actual['SHA256'] == row['SHA256'], 'Comparison body/streams changed')
need(execution['ordinary_comparison_invocations'] == 1 and execution['exit'] == 0, 'Actual execution history differs')
need((O / 'check.stderr.txt').read_bytes() == b'', 'Comparison stderr differs')
result = json.loads((O / 'check.stdout.json').read_bytes())
need(result['status'] == 'PASS_EXACT_APPROVED_COPY1_CORRECTION' and result['total_replacements'] == 5, 'Actual comparison did not pass')
for key in ('old_fact_packet', 'old_writer_packet', 'revised_writer_packet'):
    row = result[key]
    root = Path(row['path'])
    check(row['FINAL'], pin(root / 'FINAL.json'), 'External FINAL changed after comparison')
    check(row['manifest'], pin(root / 'OWNED_MANIFEST.json'), 'External manifest changed after comparison')
expect = json.loads((F / 'SOURCE_EXPECTATIONS.json').read_bytes())
check(expect['source_manifest'], pin(S / 'SOURCE_MANIFEST.json'), 'Source manifest changed after comparison')
check(expect['source_FINAL'], pin(S / 'SOURCE_FINAL.json'), 'Source FINAL changed after comparison')
now = datetime.now(timezone.utc).isoformat()
with (O / 'POST_INITIAL_LOG.md').open('a') as log:
    log.write('\n- ' + now + ' — Actual independent continuation PASS,100%; COPY-1 closed. '
        'The sole fully read comparison exited0 with8280-byte literal stdout/empty stderr and personally read exact unified diffs. '
        'Exactly2/2/1 approved replacements; all other edited-buffer bytes, entire body/MAIN/abstract/Bib/PDF/ZIP preserved. '
        'Old fact20/old writer22/revised writer21/source120files17dirs and continuation INITIAL4 authenticated. '
        'Historical run streams/limits remain distinct and no reviewed helper was replayed. '
        'Finite15-file/zero-child-directory envelope is now frozen; quiescent afterward. No publication/AA/install authority.\n')
expected_names = initial_names | {'POST_INITIAL_LOG.md', 'check_exact_revision.py', 'check.stdout.json',
    'check.stderr.txt', 'EXECUTION.json', 'REPORT.md', 'seal_final.py', 'seal.stdout.txt', 'seal.stderr.txt'}
owned = {}
for path in O.iterdir():
    need(stat.S_ISREG(path.lstat().st_mode), 'Unexpected owned directory/special node')
    owned[path.name] = pin(path)
need(set(owned) == expected_names and len(owned) == 13, 'Owned closure extent differs')
need(oct(stat.S_IMODE(O.stat().st_mode)) == '0o755', 'Owned root mode differs')
save('OWNED_MANIFEST.json', {'schema': 'finite-independent-correction-fact-manifest-v1', 'UTC': now,
    'root': str(O), 'root_mode': '0o755', 'whole_files_including_controls': 15, 'child_directories': [],
    'files': [{'path': k, **v} for k, v in sorted(owned.items())],
    'exact_root_terminal_exclusions': ['OWNED_MANIFEST.json', 'FINAL.json'],
    'all_hidden_ignored_empty_files_modes_included': True})
save('FINAL.json', {'schema': 'independent-private-correction-fact-final-v1', 'UTC': now,
    'record': 23331709, 'row': 167, 'status': 'PASS_EXACT_COPY1_CLOSED_FROZEN_QUIESCENT',
    'completion_percent': 100, 'whole_files': 15, 'child_directories': 0,
    'manifest': pin(O / 'OWNED_MANIFEST.json'), 'report': pin(O / 'REPORT.md'),
    'comparison_result': pin(O / 'check.stdout.json'), 'execution_receipt': pin(O / 'EXECUTION.json'),
    'independent_initial_seal': pin(O / 'INITIAL_SEAL.json'),
    'revised_writer_packet': result['revised_writer_packet'],
    'old_fact_and_writer_packets_whole_authenticated_unchanged': True,
    'source_all120_buffers_modes17_dirs_unchanged_at_actual_comparison': True,
    'exact_replacements': {'index.html': 2, 'HEAD.html': 2, 'model.json': 1},
    'all_other_edited_buffer_bytes_and_preserved_deliverables_unchanged': True,
    'source_contract_reused_no_PDF_scientific_replay': True,
    'new_scientific_native_producer_helper_browser_render_network_Git_W_Sheet_contact_actions': False,
    'publication_authority': False, 'AA': None, 'canonical_url': None, 'follow_up': None,
    'quiescent': True, 'post_final_writes_or_executions': False})
