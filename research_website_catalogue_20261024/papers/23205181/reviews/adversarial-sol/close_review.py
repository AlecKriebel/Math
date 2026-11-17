"""Single finite data closure only; never execute/import scientific source code."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import stat
import sys

P = Path('/Users/alec/Documents/Math/research_website_catalogue_20261024')
S = P / 'papers/23205181/sources'
O = P / 'papers/23205181/reviews/adversarial-sol'
C = Path('/Users/alec/Documents/Math/openai_followon_kaplansky_idempotents')

def need(ok, message):
    if not ok:
        raise RuntimeError(message)

def pin(path):
    info = path.lstat()
    need(stat.S_ISREG(info.st_mode), 'Nonordinary file: ' + str(path))
    data = path.read_bytes()
    return {'bytes': len(data), 'SHA256': hashlib.sha256(data).hexdigest(),
            'mode': stat.S_IMODE(info.st_mode)}

def inventory(root):
    files, dirs = {}, {}
    need(stat.S_ISDIR(root.lstat().st_mode), 'Nonordinary root')
    for path in sorted(root.rglob('*')):
        info = path.lstat()
        rel = path.relative_to(root).as_posix()
        if stat.S_ISREG(info.st_mode):
            files[rel] = pin(path)
        else:
            need(stat.S_ISDIR(info.st_mode), 'Symlink/special node')
            dirs[rel] = stat.S_IMODE(info.st_mode)
    return files, dirs

def save(name, value):
    path = O / name
    need(not path.exists(), 'Refusing repeated closure: ' + name)
    path.write_text(json.dumps(value, indent=2) + '\n')

initial_manifest = O / 'INITIAL_MANIFEST.json'
initial_seal = O / 'INITIAL_SEAL.json'
need(pin(initial_manifest)['SHA256'] == '80726848258081708b650450d90c644a6dc25394236231ea72cdf581f8ba9766', 'INITIAL manifest changed')
need(pin(initial_seal)['SHA256'] == '3f0ada45f5112b64c713514fd54962db766e3deb8404d2337ec3ae1a116e3850', 'INITIAL seal changed')
im = json.loads(initial_manifest.read_bytes())
for row in im['files']:
    need(pin(O / row['path']) == {k: row[k] for k in ('bytes', 'SHA256', 'mode')}, 'INITIAL payload changed: ' + row['path'])
need(len(im['files']) == 23 and im['directories'] == [{'path': 'rasters', 'mode': 493}], 'INITIAL boundary differs')
need(stat.S_IMODE((O / 'rasters').stat().st_mode) == 493, 'INITIAL raster directory mode changed')
need(sorted(x.name for x in (O / 'rasters').iterdir()) == ['page-' + str(i) + '.png' for i in range(1, 8)], 'INITIAL raster extent changed')
mp, fp = pin(S / 'SOURCE_MANIFEST.json'), pin(S / 'SOURCE_FINAL.json')
need(mp == {'bytes': 15220, 'SHA256': '1ab94ae569aaaeb9f2c4be323a9a9729ca5f96e2b671478af8fc6d537c55c454', 'mode': 420}, 'Source manifest changed')
need(fp == {'bytes': 826, 'SHA256': '92ea655765128b7b1f538bee8c13ecbbc62058f8909ff3afdf3ce4787487a6c0', 'mode': 420}, 'Source FINAL changed')
sm = json.loads((S / 'SOURCE_MANIFEST.json').read_bytes())
expected = {x['path']: {k: x[k] for k in ('bytes', 'SHA256', 'mode')} for x in sm['files']}
need(len(expected) == len(sm['files']) == 67, 'Source duplicate/extent')
expected.update({'SOURCE_MANIFEST.json': mp, 'SOURCE_FINAL.json': fp})
source_files, source_dirs = inventory(S)
need(source_files == expected and len(source_files) == 69, 'Whole source bytes/modes changed')
need(source_dirs == {x['path']: x['mode'] for x in sm['directories']} and len(source_dirs) == 10, 'Source topology changed')
need(stat.S_IMODE(S.stat().st_mode) == sm['root_mode'] == 493, 'Source root changed')
ready = json.loads((S / 'SOURCE_READY.json').read_bytes())
need([x['key'] for x in ready['native_assets']] == ['paper.pdf', 'source-and-audit.zip'], 'Asset order differs')
for asset in ready['native_assets']:
    path = Path(asset['path'])
    need(path.parent == S / 'assets', 'Asset outside source')
    need(pin(path)['bytes'] == asset['bytes'] and pin(path)['SHA256'] == asset['SHA256'], 'Asset pin differs')
    need(hashlib.md5(path.read_bytes()).hexdigest() == asset['MD5'], 'Native MD5 differs')
foreign_manifest = json.loads((S / 'published-source/container-001/tree/sources/SOURCE_MANIFEST.json').read_bytes())
foreign_expected = {x['path']: x for x in foreign_manifest['files']}
prefix = 'sources/preprints/A-Torsion-Free-Group-Algebra-That-Is-Not-Directly-Finite-October-4-2026/build/'
proof_names = [prefix + 'paper.tex', prefix + 'references.bib']
proof_names += [prefix + 'sections/' + x + '.tex' for x in ('introduction', 'algebra', 'random', 'patterns', 'planar', 'topology', 'assembly')]
proof_pins = []
for name in proof_names:
    actual = pin(C / name)
    need(actual['bytes'] == foreign_expected[name]['bytes'] and actual['SHA256'] == foreign_expected[name]['sha256'], 'Cached exact primary differs: ' + name)
    proof_pins.append({'path': str(C / name), **actual, 'deposited_expected_SHA256_matches': True})
extra_names = ['sources/provenance/gardam_kaplansky_ec842e6.tex']
extra_names += ['reviews/refinement_review_two_work/fresh_embedding/' + x for x in ('morozov2018.pdf', 'morozov2018.txt', 'weibel_chapter2.pdf', 'weibel_chapter2.txt', 'oinert_v3.pdf', 'oinert_v3.txt')]
extra_pins = [{'path': str(C / name), **pin(C / name)} for name in extra_names]
native = json.loads((O / 'native.stdout.json').read_bytes())
need(len(native['optional_local_source_hash_checks']) == 4 and all(x['status'] == 'skipped_source_not_packaged' for x in native['optional_local_source_hash_checks'].values()), 'Native skips differ')
need(native['q32']['word_decay_factor_upper_bound'] == '987/1000' and native['q32']['rose_generators'] == 532, 'Native identity differs')
need(json.loads((O / 'NATIVE_RUN.json').read_bytes())['actual_exit'] == 0, 'Native exit receipt differs')
empty_names = ['native.stderr.txt', 'morozov-06.stdout.txt', 'morozov-06.stderr.txt', 'morozov-09.stdout.txt', 'morozov-09.stderr.txt', 'closure.stdout.txt', 'closure.stderr.txt']
need(all((O / name).read_bytes() == b'' for name in empty_names), 'Nonempty literal stream; inspect before closure')
need(sys.flags.optimize == 0, 'Closure interpreter is optimized')
utc = datetime.now(timezone.utc).isoformat()
save('CLOSURE_CUSTODY.json', {'schema': 'row177-finite-review-custody-v1', 'UTC': utc,
     'source_files': 69, 'source_child_directories': 10, 'whole_source_bytes_modes_topology_match': True,
     'original_INITIAL_files': 25, 'original_INITIAL_all_bytes_modes_topology_unchanged': True,
     'exact_primary_proof_inputs': proof_pins, 'targeted_classical_raw_inputs': extra_pins,
     'scientific_native_program': {'path': str(S / 'published-source/container-001/tree/verification/verify_parameter.py'), **pin(S / 'published-source/container-001/tree/verification/verify_parameter.py')},
     'native_run': {'receipt': pin(O / 'NATIVE_RUN.json'), 'stdout': pin(O / 'native.stdout.json'), 'stderr': pin(O / 'native.stderr.txt'), 'actual_exit': 0, 'invocations': 1},
     'closure_interpreter': sys.executable, 'closure_optimize_flag': sys.flags.optimize,
     'network_acquisitions': 0, 'peer_or_archived_review_opinion_bodies_opened': False,
     'source_oldpacket_website_Git_Sheet_contact_mutations': False,
     'publication_authority': False})
files, dirs = inventory(O)
need(len(files) == 41 and dirs == {'primary-pages': 493, 'rasters': 493}, 'Unexpected owned closure extent')
need(all(x['mode'] == 420 for x in files.values()) and stat.S_IMODE(O.stat().st_mode) == 493, 'Owned mode differs')
save('OWNED_MANIFEST.json', {'schema': 'finite-whole-review-manifest-v1', 'UTC': utc,
     'root': str(O), 'root_mode': 493,
     'files': [{'path': k, **v} for k, v in files.items()],
     'directories': [{'path': k, 'mode': v} for k, v in dirs.items()],
     'exact_terminal_exclusions': ['FINAL.json', 'OWNED_MANIFEST.json'],
     'no_future_or_subtree_exclusions': True, 'ignored_and_empty_files_included': True})
save('FINAL.json', {'schema': 'independent-scientific-review-final-v1', 'UTC': utc,
     'row': 177, 'record': 23205181, 'family': 'adversarial-sol',
     'status': 'COMPLETE_FROZEN_QUIESCENT', 'scientific_disposition': 'PASS_FULL_ORIGINAL_STATED_CLAIM',
     'completion_percent': 100, 'substantive_unresolved_gap': None, 'followup': None,
     'manifest': {'path': 'OWNED_MANIFEST.json', **pin(O / 'OWNED_MANIFEST.json')},
     'report': {'path': 'REPORT.md', **pin(O / 'REPORT.md')},
     'initial_seal': {'path': 'INITIAL_SEAL.json', **pin(initial_seal)},
     'payload_files': 41, 'actual_files': 43, 'child_directories': 2,
     'whole_source_and_INITIAL_unchanged': True, 'native_scientific_invocations': 1,
     'native_exit': 0, 'finite_checks_are_not_universal_proof': True,
     'numerical_matching_or_group_ring_certificate_produced': False,
     'publication_authority': False, 'AA': None, 'canonical_url': None,
     'postseal_owned_writes_executions_allowed': False})
