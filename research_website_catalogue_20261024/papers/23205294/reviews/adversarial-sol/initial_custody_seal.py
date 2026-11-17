"""Fixed data-only custody/sealing utility. No source imports or science execution."""
import hashlib
import json
import os
import stat
from datetime import datetime, timezone
from pathlib import Path

P = Path('/Users/alec/Documents/Math/research_website_catalogue_20261024')
S = P / 'papers/23205294/sources'
O = P / 'papers/23205294/reviews/adversarial-sol'
ADOPTION = P / 'verification/root-source185186187-adoption-20261116.json'
EXCLUDED = {'INITIAL_MANIFEST.json', 'INITIAL_SEAL.json'}

def sha(data):
    return hashlib.sha256(data).hexdigest()

def pin(path, relative):
    st = path.lstat()
    assert stat.S_ISREG(st.st_mode), str(path)
    data = path.read_bytes()
    return {'path': relative, 'bytes': len(data), 'SHA256': sha(data),
            'mode': stat.S_IMODE(st.st_mode)}

def inventory(root):
    files, directories = [], []
    for path in sorted(root.rglob('*')):
        rel = path.relative_to(root).as_posix()
        st = path.lstat()
        if stat.S_ISREG(st.st_mode):
            files.append(pin(path, rel))
        elif stat.S_ISDIR(st.st_mode):
            directories.append({'path': rel, 'mode': stat.S_IMODE(st.st_mode)})
        else:
            raise AssertionError('Nonregular entry: ' + str(path))
    return files, directories

def exclusive(path, data):
    with path.open('xb') as stream:
        stream.write(data)

def encoded(value):
    return (json.dumps(value, ensure_ascii=False, indent=2) + '\n').encode()

assert S.is_dir() and O.is_dir()
assert sha((S / 'SOURCE_FINAL.json').read_bytes()) == '09da60cf7a73285d2eccac7186d563f8f1e898c5bcc0390761a8a416989064d7'
assert sha((S / 'SOURCE_MANIFEST.json').read_bytes()) == '340a82f34c9cb70a48e60c9bb7db4e1f8a0980e5ca037771c3fe7dc16c6677e7'
assert sha(ADOPTION.read_bytes()) == 'ccb0369dfddcafe22c6a1ec5639a52c997b2d7b5e0ccd17905a8e1001c5680a0'
source_manifest = json.loads((S / 'SOURCE_MANIFEST.json').read_text())
source_files, source_dirs = inventory(S)
assert len(source_files) == 56 and len(source_dirs) == 10
assert stat.S_IMODE(S.lstat().st_mode) == source_manifest['root_mode'] == 0o755
assert source_dirs == source_manifest['directories']
assert [f for f in source_files if f['path'] not in {'SOURCE_FINAL.json', 'SOURCE_MANIFEST.json'}] == source_manifest['files']
assert all(f['mode'] == 0o644 for f in source_files)
snapshots = {}
for line in (O / 'SOURCE_ALL_FILES.sha256').read_text().splitlines():
    digest, name = line.split('  ', 1)
    assert name.startswith('./') and name[2:] not in snapshots
    snapshots[name[2:]] = digest
assert snapshots == {f['path']: f['SHA256'] for f in source_files}
assert (O / 'SOURCE_NONREGULAR.txt').stat().st_size == 0
control = S / 'published-source/container-001/tree/main.tex'
assert control.stat().st_size == 18376 and control.read_bytes().count(b'\n') == 165
assert (S / 'assets/paper.pdf').read_bytes() == (S / 'published-source/container-001/tree/paper.pdf').read_bytes()
native_md5 = {}
for name, expected in [('source-and-verification.zip', 'cb7a71654965b49cf40a4ad876329b81'),
                       ('README.md', '183de89c85c10783624ac66a93e7a583'),
                       ('paper.pdf', 'dd9e8dbb83cf2aa974eb70b3230f1920')]:
    native_md5[name] = hashlib.md5((S / 'assets' / name).read_bytes()).hexdigest()
    assert native_md5[name] == expected
assert (O / 'manuscript.txt').read_bytes().count(b'\x0c') == 6
assert len(list((O / 'source-pdf-pages').glob('page-*.png'))) == 6
for name in ['PDFINFO.stderr.txt', 'PDFTEXT.stderr.txt', 'RASTER.stdout.txt', 'RASTER.stderr.txt']:
    assert (O / name).stat().st_size == 0
copies = {'record.response.body': 'native-record.json',
          'files-23205294.response.body': 'native-files.json',
          'SOURCE_FINAL.json': 'source-SOURCE_FINAL.json',
          'SOURCE_MANIFEST.json': 'source-SOURCE_MANIFEST.json',
          'published-source/container-001/tree/LICENSES.md': 'native-LICENSES.md',
          'published-source/container-001/tree/LICENSE_CODE.txt': 'native-LICENSE_CODE.txt',
          'published-source/container-001/tree/main.tex': 'native-main.tex'}
for original, destination in copies.items():
    exclusive(O / destination, (S / original).read_bytes())
exclusive(O / 'source-adoption.json', ADOPTION.read_bytes())
utc = datetime.now(timezone.utc).isoformat()
exclusive(O / 'SOURCE_CUSTODY.json', encoded({'UTC': utc, 'status': 'EXACT_56_FILES_10_DIRS',
    'source_root': str(S), 'source_root_mode': 0o755, 'files': source_files,
    'directories': source_dirs, 'native_MD5': native_md5, 'embedded_PDF_identical': True,
    'control_TeX_bytes': 18376, 'control_TeX_newlines': 165,
    'root_source_adoption': pin(ADOPTION, ADOPTION.relative_to(P).as_posix()),
    'semantic_reading': 'INITIAL.md; unread support bodies authenticated opaquely only'}))
files, directories = inventory(O)
assert not any(f['path'] in EXCLUDED for f in files)
manifest = {'schema': 'finite-initial-manifest-v1', 'UTC': utc, 'root': str(O),
    'root_mode': stat.S_IMODE(O.lstat().st_mode), 'files': files, 'directories': directories,
    'exact_terminal_exclusions': sorted(EXCLUDED), 'no_future_or_subtree_exclusions': True}
exclusive(O / 'INITIAL_MANIFEST.json', encoded(manifest))
exclusive(O / 'INITIAL_SEAL.json', encoded({'schema': 'source-first-initial-seal-v1', 'UTC': utc,
    'status': 'INITIAL_READY_HOLD', 'record': '23205294', 'family': 'adversarial-sol',
    'payload_files': len(files), 'actual_files_including_two_terminals': len(files) + 2,
    'child_directories': len(directories), 'manifest': pin(O / 'INITIAL_MANIFEST.json', 'INITIAL_MANIFEST.json'),
    'source_files': 56, 'source_child_directories': 10, 'source_exact': True,
    'full_TeX_PDF_text_and_six_fresh_pixels_personally_read': True,
    'closed_body_boundary': 'INITIAL.md', 'independent_hand_derivations': 'INITIAL_HAND_RESULTS.md',
    'overall_completion_percent': 40, 'source_first_phase_percent': 100,
    'scientific_disposition': 'PENDING_POSTSEAL_PRIMARY_REVIEW', 'follow_up': None,
    'scientific_program_executions': 0, 'publication_authority': False,
    'hold_no_further_writes_until_explicit_resume': True}))
