#!/usr/bin/env python3
"""Read-only candidate audit; all outputs remain in this review folder."""
import datetime, hashlib, json, pathlib, re, shutil, subprocess, sys, zipfile

ROOT = pathlib.Path('/Users/alec/Documents/Math/openai_followon_multispecies_vlasov_maxwell')
VERSION = sys.argv[1] if len(sys.argv) > 1 else 'v2'
assert VERSION in ['v2', 'v3', 'v4']
PACKET = ROOT / f'reviews/package_{VERSION}'
OUT = ROOT / 'reviews/package_review_02' / f'mechanics_{VERSION}'
OUT.mkdir(exist_ok=True)
SRC = PACKET / 'source-and-verification'
UPSTREAM = ROOT / 'sources/upstream_pinned'

def sha(data):
    return hashlib.sha256(data).hexdigest()

inventory = json.loads((PACKET / 'REVIEW_INVENTORY.json').read_text())
checks = []
reviewed = {}
for rel, row in inventory['files'].items():
    data = (PACKET / rel).read_bytes()
    reviewed[rel] = {'bytes': len(data), 'sha256': sha(data)}
    assert reviewed[rel] == row, rel
checks.append({'name': 'all frozen inventory entries match', 'count': len(reviewed)})
actual = {str(p.relative_to(PACKET)) for p in PACKET.rglob('*') if p.is_file()}
assert actual == set(reviewed) | {'REVIEW_INVENTORY.json'}, actual ^ set(reviewed)
checks.append({'name': 'no uninventory files', 'count': len(actual)})

internal = json.loads((SRC / 'SHA256SUMS.json').read_text())
for name, val in internal.items():
    assert sha((SRC / name).read_bytes()) == val, name
checks.append({'name': 'internal SHA256SUMS match', 'count': len(internal)})

with zipfile.ZipFile(PACKET / 'upload-kit/source-and-verification.zip') as z:
    names = z.namelist()
    assert len(names) == len(set(names)), 'duplicate ZIP entries'
    assert set(names) == {'source-and-verification/' + p.name for p in SRC.iterdir() if p.is_file()}, names
    for name in names:
        path = pathlib.PurePosixPath(name)
        assert not path.is_absolute() and '..' not in path.parts and '\\' not in name, name
        assert z.read(name) == (PACKET / name).read_bytes(), name
    assert z.testzip() is None
checks.append({'name': 'ZIP members exact and safe', 'count': len(names)})

manifest = json.loads((PACKET / 'zenodo-deposit.json').read_text())
for entry in manifest['files']:
    rel = pathlib.Path(entry['path'])
    assert not rel.is_absolute() and '..' not in rel.parts
    mutable = ROOT / rel
    frozen = PACKET / 'upload-kit' / rel.name
    assert mutable.read_bytes() == frozen.read_bytes(), entry
assert (PACKET / 'upload-kit/README.md').read_bytes() == (SRC / 'README.md').read_bytes()
checks.append({'name': 'manifest targets equal frozen kit', 'count': len(manifest['files'])})

pinned = json.loads((SRC / 'PINNED_SOURCE.json').read_text())
upstream_hashes = {}
for rel, expected in pinned['sha256'].items():
    data = (UPSTREAM / rel).read_bytes()
    assert sha(data) == expected, rel
    upstream_hashes[rel] = sha(data)
checks.append({'name': 'actual pinned source hashes', 'count': len(upstream_hashes)})

# Read and parse the complete structured receipts, not only their headlines.
json_receipts = {}
for path in SRC.glob('*.json'):
    value = json.loads(path.read_text())
    json_receipts[path.name] = {'keys': list(value), 'sha256': sha(path.read_bytes())}
scan = json.loads((SRC / 'FORMAL_STATIC_SCAN.json').read_text())
assert len(scan['local_import_closure']) == 207
assert scan['external_imports'] == ['Mathlib'] and not scan['missing_local_imports']
assert not scan['textual_untrusted_construct_scan']
limitations = json.loads((SRC / 'FORMAL_BUILD_LIMITATIONS.json').read_text())
assert limitations['formal_certificate'] == 'None reproduced.'
checks.append({'name': 'formal receipts retain unverified build limitation', 'modules': 207})

certificate_results = {}
for name in ['exact_kernel_certificate.py', 'rational_selection_certificate.py', 'verify_pair_identity.py']:
    result = subprocess.run([sys.executable, str(SRC / name)], text=True, capture_output=True)
    assert result.returncode == 0, (name, result.stderr)
    parsed = json.loads(result.stdout)
    certificate_results[name] = {'exit_code': result.returncode, 'stdout': parsed, 'stderr': result.stderr}
checks.append({'name': 'three exact algebra certificates', 'count': len(certificate_results)})

build = OUT / 'build'
build.mkdir(exist_ok=True)
shutil.copyfile(SRC / 'main.tex', build / 'main.tex')
cmd = ['/Applications/ChatGPT.app/Contents/Resources/tectonic/tectonic', '-X', 'compile', '--untrusted', 'main.tex']
result = subprocess.run(cmd, cwd=build, text=True, capture_output=True)
(build / 'compile.log').write_text(result.stdout + result.stderr)
assert result.returncode == 0, result.stderr
checks.append({'name': 'clean exact-source Tectonic build', 'exit_code': result.returncode})

page_counts = []
for label, path in [('candidate', PACKET / 'upload-kit/paper.pdf'), ('rebuilt', build / 'main.pdf')]:
    subprocess.run(['pdftotext', '-layout', str(path), str(OUT / f'{label}.txt')], check=True)
    info = subprocess.run(['pdfinfo', str(path)], capture_output=True, text=True, check=True).stdout
    (OUT / f'{label}_pdfinfo.txt').write_text(info)
    page_counts.append(int(re.search(r'^Pages:\s+(\d+)$', info, re.M).group(1)))
    subprocess.run(['pdftoppm', '-r', '80', '-png', str(path), str(OUT / label)], check=True)
assert (OUT / 'candidate.txt').read_bytes() == (OUT / 'rebuilt.txt').read_bytes()
candidate_renders = sorted(OUT.glob('candidate-*.png'))
rebuilt_renders = sorted(OUT.glob('rebuilt-*.png'))
assert len(candidate_renders) == len(rebuilt_renders) == page_counts[0] == page_counts[1]
for a, b in zip(candidate_renders, rebuilt_renders):
    assert a.read_bytes() == b.read_bytes(), (a.name, b.name)
checks.append({'name': 'all PDF renders and extracted text match rebuild', 'count': page_counts[0]})

receipt = {
    'timestamp_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
    'reviewed_inventory_sha256': sha((PACKET / 'REVIEW_INVENTORY.json').read_bytes()),
    'checks': checks, 'reviewed_files': reviewed,
    'pinned_source_hashes': upstream_hashes, 'structured_receipts_read': json_receipts,
    'certificate_results': certificate_results,
    'candidate_pdf_sha256': sha((PACKET / 'upload-kit/paper.pdf').read_bytes()),
    'rebuilt_pdf_sha256': sha((build / 'main.pdf').read_bytes()),
    'limitations': ['This script checks package mechanics and stated algebra only; the mathematical proof requires separate analytic review.', 'No formal build was reproduced.', 'No publication action or external individual communication occurred.'],
}
(OUT / 'PACKAGE_RECEIPT.json').write_text(json.dumps(receipt, indent=2) + '\n')
print(json.dumps({'status': 'PASS', 'checks': checks, 'receipt': str(OUT / 'PACKAGE_RECEIPT.json')}, indent=2))
