"""One data-only row177 INITIAL freeze; no science/support/code import or run."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import stat

P = Path('/Users/alec/Documents/Math/research_website_catalogue_20261024')
S = P / 'papers/23205181/sources'
O = P / 'papers/23205181/reviews/adversarial-sol'

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
    need(not path.exists(), 'Refusing repeated freeze: ' + name)
    path.write_text(json.dumps(value, indent=2) + '\n')

mp, fp = pin(S / 'SOURCE_MANIFEST.json'), pin(S / 'SOURCE_FINAL.json')
need(mp == {'bytes': 15220, 'SHA256': '1ab94ae569aaaeb9f2c4be323a9a9729ca5f96e2b671478af8fc6d537c55c454', 'mode': 420}, 'Source manifest changed')
need(fp == {'bytes': 826, 'SHA256': '92ea655765128b7b1f538bee8c13ecbbc62058f8909ff3afdf3ce4787487a6c0', 'mode': 420}, 'Source FINAL changed')
m = json.loads((S / 'SOURCE_MANIFEST.json').read_bytes())
expected = {x['path']: {k: x[k] for k in ('bytes', 'SHA256', 'mode')} for x in m['files']}
need(len(expected) == len(m['files']) == 67, 'Source duplicate or extent')
expected.update({'SOURCE_MANIFEST.json': mp, 'SOURCE_FINAL.json': fp})
source_files, source_dirs = inventory(S)
need(source_files == expected and len(source_files) == 69, 'Whole source files changed')
need(source_dirs == {x['path']: x['mode'] for x in m['directories']} and len(source_dirs) == 10, 'Source topology changed')
need(stat.S_IMODE(S.stat().st_mode) == m['root_mode'] == 493, 'Source root mode changed')
ready = json.loads((S / 'SOURCE_READY.json').read_bytes())
need([x['key'] for x in ready['native_assets']] == ['paper.pdf', 'source-and-audit.zip'], 'Native order changed')
for asset in ready['native_assets']:
    path = Path(asset['path'])
    need(path.parent == S / 'assets', 'Asset outside source assets')
    need(pin(path)['bytes'] == asset['bytes'] and pin(path)['SHA256'] == asset['SHA256'], 'Native asset differs')
    need(hashlib.md5(path.read_bytes()).hexdigest() == asset['MD5'], 'Native MD5 differs')
tex = S / 'published-source/container-001/tree/main.tex'
need(len(tex.read_bytes().splitlines()) == 448, 'TeX lines differ')
need((O / 'manuscript.txt').read_bytes().count(b'\x0c') == 7, 'PDF text page count differs')
need(sorted(x.name for x in (O / 'rasters').iterdir()) == ['page-' + str(i) + '.png' for i in range(1, 8)], 'Fresh page extent differs')
streams = ['custody.stderr.txt', 'extract.stdout.txt', 'extract.stderr.txt',
           'render.stdout.txt', 'render.stderr.txt', 'freeze.stdout.txt', 'freeze.stderr.txt']
need(all((O / x).read_bytes() == b'' for x in streams), 'Nonempty literal stream; inspect rather than seal')
utc = datetime.now(timezone.utc).isoformat()
source_names = ['SOURCE_FINAL.json', 'SOURCE_MANIFEST.json', 'SOURCE_READY.json',
                'record.response.body', 'files-23205181.response.body',
                'assets/paper.pdf', 'assets/source-and-audit.zip',
                'published-source/container-001/tree/main.tex',
                'published-source/container-001/tree/LICENSES.md',
                'published-source/container-001/tree/LICENSE_CODE.txt',
                'published-source/container-001/tree/sources/UPSTREAM_LICENSE.txt']
save('SOURCE_PINS.json', {'schema': 'row177-source-first-inputs-v1', 'UTC': utc,
     'record': 23205181, 'row': 177, 'whole_source_files': 69, 'child_directories': 10,
     'whole_source_bytes_modes_topology_unchanged': True,
     'native_order': ['paper.pdf', 'source-and-audit.zip'],
     'source_inputs': [{'path': x, **pin(S / x)} for x in source_names],
     'complete_TeX_lines_personally_read': 448, 'native_PDF_text_pages_personally_read': 7,
     'fresh_native_PDF_page_images_personally_inspected': 7,
     'reader_exit_codes': {'pdftotext': 0, 'pdftoppm': 0, 'authenticate_source.py': 0},
     'long_upstream_license_body_not_claimed_wholly_read': True,
     'support_code_archived_results_foreign_proofs_peer_root_findings_opened': False,
     'publication_authority': False})
files, dirs = inventory(O)
need(len(files) == 23 and dirs == {'rasters': 493}, 'Unexpected INITIAL extent')
need(all(v['mode'] == 420 for v in files.values()) and stat.S_IMODE(O.stat().st_mode) == 493, 'Owned modes differ')
need({'INITIAL.md', 'INDEPENDENT_RESULTS.md', 'RESEARCH_LOG.md', 'SOURCE_PINS.json'} <= set(files), 'Missing source-first evidence')
save('INITIAL_MANIFEST.json', {'schema': 'finite-initial-manifest-v1', 'UTC': utc,
     'root': str(O), 'root_mode': 493,
     'files': [{'path': k, **v} for k, v in files.items()],
     'directories': [{'path': k, 'mode': v} for k, v in dirs.items()],
     'exact_terminal_exclusions': ['INITIAL_MANIFEST.json', 'INITIAL_SEAL.json'],
     'no_future_or_subtree_exclusions': True})
save('INITIAL_SEAL.json', {'schema': 'source-first-actual-initial-seal-v1', 'UTC': utc,
     'record': 23205181, 'row': 177,
     'status': 'SOURCE_FIRST_INITIAL_FROZEN_QUIESCENT_FOR_ROOT_CHECKPOINT',
     'manifest': {'path': 'INITIAL_MANIFEST.json', **pin(O / 'INITIAL_MANIFEST.json')},
     'INITIAL': {'path': 'INITIAL.md', **pin(O / 'INITIAL.md')},
     'independent_results': {'path': 'INDEPENDENT_RESULTS.md', **pin(O / 'INDEPENDENT_RESULTS.md')},
     'payload_files': 23, 'actual_files': 25, 'child_directories': 1,
     'source_first_completion_percent': 100, 'whole_review_completion_estimate_percent': 45,
     'support_primary_code_phase_begun': False,
     'root_peer_mathematical_findings_opened': False,
     'postseal_owned_writes_executions_held_until_root_checkpoint_done': True,
     'publication_authority': False})
