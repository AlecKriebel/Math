"""One row184 data-only INITIAL seal; no support/science code import or run."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import stat

P = Path('/Users/alec/Documents/Math/research_website_catalogue_20261024')
S = P / 'papers/22983519/sources'
O = P / 'papers/22983519/reviews/adversarial-sol'

def need(ok, message):
    if not ok: raise RuntimeError(message)

def pin(path):
    info = path.lstat()
    need(stat.S_ISREG(info.st_mode), 'Nonordinary file: ' + str(path))
    data = path.read_bytes()
    return {'bytes': len(data), 'SHA256': hashlib.sha256(data).hexdigest(), 'mode': stat.S_IMODE(info.st_mode)}

def inventory(root):
    files, dirs = {}, {}
    need(stat.S_ISDIR(root.lstat().st_mode), 'Nonordinary root')
    for path in sorted(root.rglob('*')):
        info = path.lstat()
        rel = path.relative_to(root).as_posix()
        if stat.S_ISREG(info.st_mode): files[rel] = pin(path)
        else:
            need(stat.S_ISDIR(info.st_mode), 'Symlink/special node')
            dirs[rel] = stat.S_IMODE(info.st_mode)
    return files, dirs

def save(name, value):
    path = O / name
    need(not path.exists(), 'Refusing repeated freeze: ' + name)
    path.write_text(json.dumps(value, indent=2) + '\n')

mp, fp = pin(S / 'SOURCE_MANIFEST.json'), pin(S / 'SOURCE_FINAL.json')
need(mp == {'bytes': 17481, 'SHA256': 'e05b1df4559bac1a55fac1cfbda2a6aa6428d675e0ce7fbf708766037d425ace', 'mode': 420}, 'Source manifest differs')
need(fp == {'bytes': 826, 'SHA256': '7449712c5c396fde640b7497b20f97fb174593071fce71ca80ff763a23df4954', 'mode': 420}, 'Source FINAL differs')
m = json.loads((S / 'SOURCE_MANIFEST.json').read_bytes())
expected = {x['path']: {k: x[k] for k in ('bytes', 'SHA256', 'mode')} for x in m['files']}
need(len(expected) == len(m['files']) == 69, 'Source duplicate/extent')
expected.update({'SOURCE_MANIFEST.json': mp, 'SOURCE_FINAL.json': fp})
sf, sd = inventory(S)
need(sf == expected and len(sf) == 71, 'Source whole bytes/modes/extent changed')
need(sd == {x['path']: x['mode'] for x in m['directories']} and len(sd) == 14, 'Source topology changed')
need(stat.S_IMODE(S.stat().st_mode) == m['root_mode'] == 493, 'Source root mode changed')
ready = json.loads((S / 'SOURCE_READY.json').read_bytes())
names = ['SHA256SUMS.txt', 'source-and-verification.zip', 'paper.pdf']
need([x['key'] for x in ready['native_assets']] == names, 'Native order differs')
for asset in ready['native_assets']:
    path = Path(asset['path'])
    need(path.parent == S / 'assets', 'Native asset outside source')
    need(pin(path)['bytes'] == asset['bytes'] and pin(path)['SHA256'] == asset['SHA256'], 'Native asset differs')
    need(hashlib.md5(path.read_bytes()).hexdigest() == asset['MD5'], 'Native MD5 differs')
base = 'published-source/container-001/tree/radial_statistical_counterexample/'
need(len((S / (base + 'manuscript/paper.tex')).read_bytes().splitlines()) == 257, 'TeX line count differs')
need((O / 'manuscript.txt').read_bytes().count(b'\x0c') == 4, 'PDF text page count differs')
need(sorted(x.name for x in (O / 'rasters').iterdir()) == ['page-' + str(i) + '.png' for i in range(1, 5)], 'Raster page extent differs')
need(pin(S / (base + 'output/pdf/paper.pdf'))['SHA256'] == pin(S / 'assets/paper.pdf')['SHA256'], 'PDF copies differ')
empty = ['custody.stderr.txt', 'extract.stdout.txt', 'extract.stderr.txt', 'render.stdout.txt', 'render.stderr.txt', 'freeze.stdout.txt', 'freeze.stderr.txt']
need(all((O / name).read_bytes() == b'' for name in empty), 'Nonempty literal stream; inspect rather than seal')
utc = datetime.now(timezone.utc).isoformat()
input_names = ['SOURCE_FINAL.json', 'SOURCE_MANIFEST.json', 'SOURCE_READY.json', 'record.response.body', 'files-22983519.response.body',
               'assets/SHA256SUMS.txt', 'assets/source-and-verification.zip', 'assets/paper.pdf',
               base + 'manuscript/paper.tex', base + 'LICENSES.md']
save('SOURCE_PINS.json', {'schema': 'source-first-row184-inputs-v1', 'UTC': utc,
     'row': 184, 'record': 22983519, 'whole_source_files': 71, 'child_directories': 14,
     'whole_source_unchanged_since_pre_science_authentication': True,
     'native_order': names, 'source_inputs': [{'path': x, **pin(S / x)} for x in input_names],
     'whole_manuscript_TeX_lines_personally_read': 257,
     'native_PDF_distinct_text_pages_personally_read': 4, 'fresh_own_native_page_pixels_personally_inspected': 4,
     'reader_exits': {'pdftotext': 0, 'pdftoppm': 0, 'authenticate_source.py': 0},
     'support_native_code_archived_opinions_foreign_primary_peer_root_bodies_read': False,
     'publication_authority': False})
files, dirs = inventory(O)
need(len(files) == 20 and dirs == {'rasters': 493}, 'Unexpected INITIAL extent')
need(all(x['mode'] == 420 for x in files.values()) and stat.S_IMODE(O.stat().st_mode) == 493, 'Owned modes differ')
save('INITIAL_MANIFEST.json', {'schema': 'finite-source-first-initial-manifest-v1', 'UTC': utc,
     'root': str(O), 'root_mode': 493, 'files': [{'path': k, **v} for k, v in files.items()],
     'directories': [{'path': k, 'mode': v} for k, v in dirs.items()],
     'exact_terminal_exclusions': ['INITIAL_MANIFEST.json', 'INITIAL_SEAL.json'],
     'ignored_and_empty_files_included': True, 'no_future_or_subtree_exclusions': True})
save('INITIAL_SEAL.json', {'schema': 'source-first-actual-independent-result-seal-v1', 'UTC': utc,
     'row': 184, 'record': 22983519, 'status': 'INITIAL_READY_HOLD_FOR_ROOT_CHECKPOINT',
     'manifest': {'path': 'INITIAL_MANIFEST.json', **pin(O / 'INITIAL_MANIFEST.json')},
     'INITIAL': {'path': 'INITIAL.md', **pin(O / 'INITIAL.md')},
     'independent_results': {'path': 'INDEPENDENT_RESULTS.md', **pin(O / 'INDEPENDENT_RESULTS.md')},
     'payload_files': 20, 'actual_files': 22, 'child_directories': 1,
     'source_first_completion_percent': 100, 'whole_review_completion_estimate_percent': 60,
     'support_primary_native_science_phase_begun': False,
     'peer_root_scientific_findings_opened': False,
     'all_owned_writes_executions_held_until_explicit_root_resume': True,
     'publication_authority': False, 'AA': None})
