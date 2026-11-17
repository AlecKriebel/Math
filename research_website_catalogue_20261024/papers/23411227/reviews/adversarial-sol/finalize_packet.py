"""One bounded data-only custody closure; no scientific evaluation or subprocesses."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import stat

O = Path('/Users/alec/Documents/Math/research_website_catalogue_20261024/papers/23411227/reviews/adversarial-sol')
S = O.parents[1] / 'sources'
C = Path('/Users/alec/Documents/Math/draft_pr_claimed_solved_800_900_20261012/audits/pr888_30005079')
CONTROLS = {'OWNED_MANIFEST.json', 'FINAL.json'}
RAW = [
    ('private_sources/miao_wang_optimal_v2.pdf', 538390, '85285e55a256fe342d511f716530ed790801d695bdd5f21090ff9d56039b8049', 32),
    ('private_sources/han_li_optimal_arxiv.pdf', 558188, '939691d9bd0c24444f43b944b91c1ac9684fef628d3b23393cc7f6fd3b5db0ff', 48),
    ('private_sources/han_li_gytd.pdf', 641357, 'cd44c6a91351619ffc41aae32bba1d144afb6f9eda11f4dbee74f3677502e9a6', 61),
    ('private_sources/wang_zhu_toric.pdf', 221336, '93aa63348add332cca1df8519bd864065f1956ae5f898e09065651d5f92245b1', 15),
    ('private_sources/owr2022_17.pdf', 1032709, 'c997329409f016d06867ecc06dd38c59cea4919aa9ecf34791ed6a95f63345ec', 68),
    ('private_sources/BLXZ_2103.15278v2.pdf', 443588, '8d56f0d92d9146ea85c53be8c04fc02e90f4b09a57fc3f591a996d1b040c1351', 30),
    ('priority_classical_01/private_tmp/li_li_2103.06439v6.pdf', 530713, '067c12282bed8d0db4865b8b23d92304d16c444dcfeefe71dcde64864fd3459c', 39),
    ('priority_classical_01/private_tmp/miao_wang_2401.13999v1.pdf', 325579, '56026b5035c471db53153c930fd2d100c227e94417a5674be44fe8833d78ec83', 28),
]

def need(test, message):
    if not test:
        raise RuntimeError(message)

def pin(path):
    info = path.lstat()
    need(stat.S_ISREG(info.st_mode), 'Not an ordinary file: ' + str(path))
    data = path.read_bytes()
    return {'bytes': len(data), 'SHA256': hashlib.sha256(data).hexdigest(),
            'mode': oct(stat.S_IMODE(info.st_mode))}

def tree(path):
    need(stat.S_ISDIR(path.lstat().st_mode), 'Nonordinary root: ' + str(path))
    files, dirs = {}, {}
    for node in path.rglob('*'):
        rel = node.relative_to(path).as_posix()
        info = node.lstat()
        if stat.S_ISREG(info.st_mode):
            files[rel] = pin(node)
        else:
            need(stat.S_ISDIR(info.st_mode), 'Symlink/special node: ' + str(node))
            dirs[rel] = oct(stat.S_IMODE(info.st_mode))
    return files, dirs

def check(expected, actual, label):
    need(all(actual[k] == expected[k] for k in ('bytes', 'SHA256', 'mode')), label)

def save(name, value):
    path = O / name
    need(not path.exists(), 'Refusing to replace closure output: ' + name)
    path.write_text(json.dumps(value, indent=2) + '\n')

need(not any((O / x).exists() for x in CONTROLS), 'Packet already sealed')
source_manifest_pin = pin(S / 'SOURCE_MANIFEST.json')
source_final_pin = pin(S / 'SOURCE_FINAL.json')
check({'bytes': 60052, 'SHA256': '3bd41786837658193a0258d1f1a70dc719f0e321647ed885294e9947f64a1e7b', 'mode': '0o644'}, source_manifest_pin, 'Source manifest changed')
check({'bytes': 910, 'SHA256': '46a1f71e118fff3101c7f0af2158658847ad338172d7bd6d119ba041c8613886', 'mode': '0o644'}, source_final_pin, 'Source FINAL changed')
sm = json.loads((S / 'SOURCE_MANIFEST.json').read_bytes())
expected_source = {x['path']: {k: x[k] for k in ('bytes', 'SHA256', 'mode')} for x in sm['files']}
need(len(expected_source) == len(sm['files']), 'Duplicate source path')
expected_source.update({'SOURCE_MANIFEST.json': source_manifest_pin, 'SOURCE_FINAL.json': source_final_pin})
source_files, source_dirs = tree(S)
need(len(source_files) == 196 and source_files == expected_source, 'Whole source bytes/modes/extent changed')
need(len(source_dirs) == 21 and source_dirs == {x['path']: x['mode'] for x in sm['directories']}, 'Source directory topology/modes changed')
need(oct(stat.S_IMODE(S.stat().st_mode)) == sm['root_mode'], 'Source root mode changed')

im_pin = pin(O / 'INITIAL_MANIFEST.json')
is_pin = pin(O / 'INITIAL_SEAL.json')
check({'bytes': 3449, 'SHA256': 'bd01dd866673e3d7742022a49612de952078b508f53dbd46bbb1c1f0fcec7872', 'mode': '0o644'}, im_pin, 'Initial manifest changed')
check({'bytes': 1414, 'SHA256': '144427db7537cfec5e3b4bb4e48ffb7d8c64e3e3b2190469e53abeff71399b5a', 'mode': '0o644'}, is_pin, 'Initial seal changed')
im = json.loads((O / 'INITIAL_MANIFEST.json').read_bytes())
initial_names = {x['path'] for x in im['payloads']} | {'INITIAL_MANIFEST.json', 'INITIAL_SEAL.json'}
need(len(initial_names) == 19, 'Initial extent differs')
for item in im['payloads']:
    check(item, pin(O / item['path']), 'Initial payload changed: ' + item['path'])
for item in im['directories']:
    need(oct(stat.S_IMODE((O / item['path']).lstat().st_mode)) == item['mode'], 'Initial directory mode changed')

raw_pins = []
for rel, count, digest, pages in RAW:
    actual = pin(C / rel)
    need(actual['bytes'] == count and actual['SHA256'] == digest, 'Raw primary changed: ' + rel)
    raw_pins.append({'path': str(C / rel), **actual, 'pages_observed_in_prior_pdfinfo': pages})

extracts = ['miao_wang_optimal_v2', 'han_li_optimal_arxiv', 'han_li_gytd',
            'wang_zhu_toric', 'owr2022_17', 'BLXZ_2103.15278v2',
            'li_li_2103.06439v6', 'miao_wang_2401.13999v1']
images = ['mw12', 'hl21', 'hl33', 'gytd19', 'blxz02']
for name in extracts:
    need((O / 'primaries' / (name + '.txt')).stat().st_size > 0, 'Missing primary extraction')
    for stream in ('stdout', 'stderr'):
        need((O / 'primaries' / (name + '.' + stream + '.txt')).read_bytes() == b'', 'Unexpected extraction stream')
warning = b'Syntax Warning: Bad bounding box in Type 3 glyph\n' * 2
for name in images:
    need((O / 'primary-pages' / (name + '.png')).stat().st_size > 0, 'Missing primary image')
    need((O / 'primary-pages' / (name + '.stdout.txt')).read_bytes() == b'', 'Unexpected render stdout')
    need((O / 'primary-pages' / (name + '.stderr.txt')).read_bytes() == (warning if name == 'blxz02' else b''), 'Render diagnostic not retained exactly')

now = datetime.now(timezone.utc).isoformat()
save('SOURCE_CLOSURE.json', {'schema': 'bounded-adversarial-custody-closure-v1', 'UTC': now,
     'record': 23411227, 'row': 172, 'source_manifest': source_manifest_pin,
     'source_FINAL': source_final_pin, 'whole_source_files': 196, 'source_child_directories': 21,
     'all_source_buffers_modes_topology_unchanged': True, 'all_original19_initial_files_unchanged': True,
     'INITIAL_manifest': im_pin, 'INITIAL_seal': is_pin, 'raw_primary_bodies': raw_pins,
     'scientific_native_executions': 0, 'new_network_operations': 0,
     'primary_extractions': {'count': 8, 'observed_exit_codes': [0] * 8, 'literal_empty_streams_retained': True},
     'selected_primary_renders': {'count': 5, 'observed_exit_codes': [0] * 5,
       'BLXZ_stderr_literal': warning.decode(), 'all_five_images_personally_inspected': True},
     'peer_coordination': False, 'current_root_peer_and_archived_review_judgments_opened': False,
     'source_or_other_namespace_writes': False})
with (O / 'POST_INITIAL_LOG.md').open('a') as log:
    log.write('\n- ' + now + ' — Full bounded review and data-only closure complete, 100%. '
              'All 196 source files/21 directories and all original 19 INITIAL files authenticate unchanged; '
              'eight raw primary PDFs are still bound to exact byte pins. Literal reader streams, including the two '
              'BLXZ font warnings, are retained. Zero scientific/native execution, network operations or peer coordination. '
              'Findings remain sealed locally pending root gate. Final manifest/FINAL are being frozen by this sole closure invocation; '
              'no further writes or executions are planned.\n')

owned_files, owned_dirs = tree(O)
expected_owned = initial_names | {'POST_INITIAL_LOG.md', 'PRIMARY_INTERFACES.md', 'REPORT.md',
    'finalize_packet.py', 'finalize.stdout.txt', 'finalize.stderr.txt', 'SOURCE_CLOSURE.json'}
for name in extracts:
    expected_owned.update('primaries/' + name + suffix for suffix in ('.txt', '.stdout.txt', '.stderr.txt'))
for name in images:
    expected_owned.update('primary-pages/' + name + suffix for suffix in ('.png', '.stdout.txt', '.stderr.txt'))
need(set(owned_files) == expected_owned and len(owned_files) == 65, 'Unexpected owned file extent')
need(owned_dirs == {'rasters': '0o755', 'primaries': '0o755', 'primary-pages': '0o755'}, 'Owned directory topology differs')
need(oct(stat.S_IMODE(O.stat().st_mode)) == '0o755', 'Owned root mode differs')
manifest = {'schema': 'finite-adversarial-whole-packet-manifest-v1', 'UTC': now,
    'root': str(O), 'root_mode': '0o755', 'ordinary_files_including_two_controls': 67,
    'child_directory_count': 3, 'directories': [{'path': k, 'mode': v} for k, v in sorted(owned_dirs.items())],
    'files': [{'path': k, **v} for k, v in sorted(owned_files.items())],
    'exact_root_terminal_exclusions': sorted(CONTROLS), 'ignored_and_empty_files_included': True}
save('OWNED_MANIFEST.json', manifest)
save('FINAL.json', {'schema': 'independent-adversarial-scientific-FINAL-v1', 'UTC': now,
    'record': 23411227, 'row': 172, 'status': 'COMPLETE_FROZEN_QUIESCENT', 'completion_percent': 100,
    'whole_files': 67, 'child_directories': 3, 'manifest': pin(O / 'OWNED_MANIFEST.json'),
    'report': pin(O / 'REPORT.md'), 'primary_interfaces': pin(O / 'PRIMARY_INTERFACES.md'),
    'source_closure': pin(O / 'SOURCE_CLOSURE.json'), 'immutable_INITIAL_seal': is_pin,
    'original_claim_disposition_private_until_root_gate': 'PASS with actual cited primary interfaces; no substantive gap identified',
    'scientific_program_executions': 0, 'new_network_operations': 0, 'peer_coordination': False,
    'reader_warning_preserved': 'BLXZ primary page2: two Type3-glyph bounding-box warnings; readable page personally inspected',
    'root_gate_open': False, 'findings_withheld_from_root': True, 'publication_authority': False,
    'AA': None, 'canonical_url': None, 'follow_up': None,
    'closure_invocation': 'python3 finalize_packet.py > finalize.stdout.txt 2> finalize.stderr.txt',
    'closure_helper_personally_read_whole_before_sole_execution': True})
