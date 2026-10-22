"""Read-only audit of publication files; writes only under this review directory."""
import hashlib, io, json, pathlib, subprocess, sys, zipfile

HERE = pathlib.Path(__file__).resolve().parent
PUB = HERE.parent.parent / 'publication'
def digest(b): return hashlib.sha256(b).hexdigest()
def info(b): return {'bytes': len(b), 'sha256': digest(b)}
def valid(z):
    names = z.namelist()
    assert len(names) == len(set(names)), 'Duplicate member'
    assert all(not pathlib.PurePosixPath(n).is_absolute() and '..' not in pathlib.PurePosixPath(n).parts for n in names)
    assert z.testzip() is None
    return names

paths = ['main.tex', 'PACKAGE_RECEIPT.json', 'zenodo-deposit.json', 'zenodo-metadata.json',
         'output/pdf/cellularization-vanishing.pdf',
         'output/cellularization-vanishing-source-and-verification.zip',
         'output/zenodo-upload-kit.zip']
files = {n: info((PUB / n).read_bytes()) for n in paths}
receipt = json.loads((PUB / 'PACKAGE_RECEIPT.json').read_text())
for n, record in receipt['files'].items(): assert info((PUB / n).read_bytes()) == record, n
outer = zipfile.ZipFile(PUB / 'output/zenodo-upload-kit.zip')
outer_names = valid(outer)
source_name = 'cellularization-vanishing-source-and-verification.zip'
source_bytes = outer.read(source_name)
assert source_bytes == (PUB / 'output' / source_name).read_bytes()
inner = zipfile.ZipFile(io.BytesIO(source_bytes))
inner_names = valid(inner)
source_manifest = json.loads(inner.read('SOURCE_MANIFEST.json'))
assert set(source_manifest) == set(inner_names) - {'SOURCE_MANIFEST.json'}
assert source_manifest == receipt['source_members']
for n, record in source_manifest.items(): assert info(inner.read(n)) == record, n
assert inner.read('main.tex') == (PUB / 'main.tex').read_bytes()
pdf = (PUB / 'output/pdf/cellularization-vanishing.pdf').read_bytes()
assert pdf == outer.read('cellularization-vanishing.pdf') == inner.read('output/pdf/cellularization-vanishing.pdf')
metadata = json.loads(outer.read('zenodo-metadata.json'))
assert metadata == json.loads((PUB / 'zenodo-metadata.json').read_text())
deposit = json.loads(outer.read('zenodo-deposit.json'))
assert deposit['metadata'] == metadata == json.loads((PUB / 'zenodo-deposit.json').read_text())['metadata']
assert {r['path'] for r in deposit['files']} == {'cellularization-vanishing.pdf', source_name}
assert all(r['path'] in outer_names for r in deposit['files'])
assert outer.read('README.md') == inner.read('README.md') == (PUB / 'README.md').read_bytes()
assert inner.read('LICENSE.txt') == (PUB / 'LICENSE.txt').read_bytes()
provenance = json.loads(inner.read('PROVENANCE.json'))
report = HERE.parent.parent / 'input/MATHEMATICAL_REPORT.md'
assert digest(report.read_bytes()) == provenance['source_report_sha256']
extract = HERE / 'extracted'
extract.mkdir(exist_ok=True)
inner.extractall(extract)
(HERE / 'SOURCE_MANIFEST.json').write_bytes(inner.read('SOURCE_MANIFEST.json'))
expected = json.loads(inner.read('verification/expected_results.json'))
verifier = extract / 'verification/check_bosonization.py'
run = subprocess.run([sys.executable, str(verifier)], capture_output=True, text=True)
assert run.returncode == 0 and json.loads(run.stdout) == expected
(HERE / 'verifier_actual.json').write_text(run.stdout)
optimized = subprocess.run([sys.executable, '-O', str(verifier)], capture_output=True, text=True)
assert optimized.returncode != 0 and 'requires assertion checks' in optimized.stderr
result = {'result': 'PASS', 'files': files, 'outer_names': outer_names,
          'inner_names': inner_names, 'source_manifest': info(inner.read('SOURCE_MANIFEST.json')),
          'outer_deposit_manifest': info(outer.read('zenodo-deposit.json')),
          'checks': ['all receipt file hashes', 'all source manifest names, sizes and hashes',
                     'all archive CRCs, no duplicates or traversal', 'all PDF copies byte-identical',
                     'source main.tex byte-identical', 'all metadata equals',
                     'deposit relative paths resolve in actual kit', 'provenance source report hash',
                     'actual archived verifier equals expected output', '-O rejects disabled assertions'],
          'verifier_optimized': {'returncode': optimized.returncode, 'stderr': optimized.stderr}}
(HERE / 'integrity_checks.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps(result, indent=2))
