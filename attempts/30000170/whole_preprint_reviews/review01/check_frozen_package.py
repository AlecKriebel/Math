#!/usr/bin/env python3
"""Independent read-only freeze, extraction, verifier and consistency checks."""
from pathlib import Path, PurePosixPath
import hashlib
import json
import subprocess
import sys
import zipfile

W = Path(__file__).resolve().parent.parent
K = W / 'preprint_package_v02'
R = Path(__file__).resolve().parent
def sha(body):
    return hashlib.sha256(body).hexdigest()

manifest_body = (K / 'PACKAGE_MANIFEST.json').read_bytes()
assert sha(manifest_body) == 'f7c88aaaf5f2e0b9358d141c70582aafe046989392bb23edb1537436bbd239fa'
manifest = json.loads(manifest_body)
seen = set()
pins = {}
for entry in manifest['files']:
    p = PurePosixPath(entry['path'])
    assert not p.is_absolute() and '..' not in p.parts and str(p) == entry['path']
    assert str(p) not in seen
    seen.add(str(p))
    path = K.joinpath(*p.parts)
    assert path.is_file() and not path.is_symlink()
    b = path.read_bytes()
    assert len(b) == entry['bytes'] and sha(b) == entry['sha256'], str(p)
    pins[str(p)] = {'bytes': len(b), 'sha256': sha(b)}
assert len(seen) == 21

archive = K / 'output/nonunique_nearest_stable_complex_quadratics_verification.zip'
dest = R / 'independent_archive_extraction'
dest.mkdir(exist_ok=True)
members = []
archive_prefix = 'nonunique_nearest_stable_complex_quadratics_verification'
with zipfile.ZipFile(archive) as z:
    assert z.testzip() is None
    for info in z.infolist():
        p = PurePosixPath(info.filename)
        assert not p.is_absolute() and '..' not in p.parts and str(p) == info.filename
        assert not info.is_dir() and info.filename not in members
        assert len(p.parts) == 2 and p.parts[0] == archive_prefix
        data = z.read(info)
        assert data == (K / 'verification' / p.name).read_bytes(), info.filename
        (dest / p.name).write_bytes(data)
        members.append(p.name)
assert len(members) == 12
assert set(members) == {p.name for p in (K / 'verification').iterdir() if p.is_file()}

hashes = json.loads((dest / 'HASHES.json').read_bytes())
declared = {e['path'] for e in hashes['files']}
assert declared == set(members) - {'HASHES.json'}
for e in hashes['files']:
    b = (dest / e['path']).read_bytes()
    assert len(b) == e['bytes'] and sha(b) == e['sha256']

runs = {}
for script, expected in [('verify_exact.py', 'expected_exact.json'),
                         ('verify_function_boundary.py', 'expected_function_boundary.json'),
                         ('check_archive_hashes.py', None)]:
    run = subprocess.run([sys.executable, script], cwd=dest, capture_output=True, check=True)
    assert run.stderr == b'', script
    if expected:
        assert run.stdout == (dest / expected).read_bytes(), (script, 'byte-exact output mismatch')
    (R / (script + '.stdout')).write_bytes(run.stdout)
    runs[script] = {'exit': run.returncode, 'stdout_sha256': sha(run.stdout),
                    'stdout_bytes': len(run.stdout), 'expected_byte_exact': bool(expected)}

for a,b in [('nonunique_nearest_stable_complex_quadratics.tex','nonunique_nearest_stable_complex_quadratics.tex'),
            ('VERIFICATION_README.md','README.md'),('SOURCE_PRIORITY.md','SOURCE_PRIORITY.md'),
            ('SOURCE_PROVENANCE.json','SOURCE_PROVENANCE.json'),
            ('publication_metadata.json','publication_metadata.json'),('LICENSE.md','LICENSE.md')]:
    assert (K / a).read_bytes() == (dest / b).read_bytes(), (a,b)
metadata = json.loads((K / 'publication_metadata.json').read_bytes())
deposit = json.loads((K / 'zenodo-deposit.json').read_bytes())
assert deposit['metadata'] == metadata
assert deposit['files'] == manifest['published_files']
for f in deposit['files']:
    assert (K / f['path']).is_file()

final_pins = {}
for p in pins:
    b = (K / p).read_bytes()
    assert sha(b) == pins[p]['sha256']
    final_pins[p] = pins[p]
assert (K / 'PACKAGE_MANIFEST.json').read_bytes() == manifest_body
out = {'status': 'PASS', 'manifest_sha256': sha(manifest_body), 'frozen_file_count': 21,
       'pins': final_pins, 'archive_member_count': len(members), 'archive_members': members,
       'archive_hashes_coverage': len(declared), 'runs': runs,
       'metadata_deposit_equal': True, 'six_outer_archive_duplicates_byte_exact': True,
       'package_unchanged_at_end': True, 'python_version': sys.version}
(R / 'INDEPENDENT_PACKAGE_CHECK.json').write_text(json.dumps(out, indent=2, sort_keys=True)+'\n')
print(json.dumps({k:v for k,v in out.items() if k != 'pins'}, indent=2, sort_keys=True))
