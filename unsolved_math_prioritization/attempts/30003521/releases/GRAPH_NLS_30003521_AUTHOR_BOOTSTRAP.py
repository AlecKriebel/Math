"""Validate externally pinned bytes before executing any payload code."""
import hashlib
import json
import pathlib
import subprocess
import sys
import tempfile
import zipfile

ROOT = pathlib.Path(__file__).resolve().parent
MANIFEST = ROOT / 'GRAPH_NLS_30003521_AUTHOR_EXTERNAL_MANIFEST.json'
PINNED_MANIFEST_SHA256 = '7761f7a28c02e251d926f37ddfc5d51e3bfb326a3d1eb89e4544eee507b10f66'
manifest_bytes = MANIFEST.read_bytes()
assert hashlib.sha256(manifest_bytes).hexdigest() == PINNED_MANIFEST_SHA256
manifest = json.loads(manifest_bytes)
archive = ROOT / manifest['archive']['name']
archive_bytes = archive.read_bytes()
assert len(archive_bytes) == manifest['archive']['bytes']
assert hashlib.sha256(archive_bytes).hexdigest() == manifest['archive']['sha256']
expected = {r['name']: r for r in manifest['files']}
assert len(expected) == len(manifest['files']) == 4
verified = {}
with zipfile.ZipFile(archive) as z:
    names = z.namelist()
    assert len(names) == len(set(names))
    assert set(names) == set(expected)
    for name in names:
        assert pathlib.PurePosixPath(name).name == name
        info = z.getinfo(name)
        assert info.file_size == expected[name]['bytes']
        data = z.read(name)
        assert len(data) == expected[name]['bytes']
        assert hashlib.sha256(data).hexdigest() == expected[name]['sha256']
        verified[name] = data
# No payload is imported or executed before the complete member verification above.
with tempfile.TemporaryDirectory(prefix='graph-nls-audit-') as td:
    work = pathlib.Path(td)
    for name, data in verified.items():
        (work/name).write_bytes(data)
    result = subprocess.run(
        [sys.executable, '-I', '-S', str(work/'check_identities.py')],
        cwd=work, env={'PATH': '/usr/bin:/bin', 'LC_ALL': 'C.UTF-8'},
        capture_output=True, text=True, timeout=30, check=True)
    checks = json.loads(result.stdout)
    assert checks['passed'] is True
    print(json.dumps({
        'integrity_before_payload_execution': True,
        'manifest_sha256': PINNED_MANIFEST_SHA256,
        'archive_sha256': manifest['archive']['sha256'],
        'verified_member_count': len(verified),
        'isolation': 'Fresh temporary cwd, Python -I -S, minimal environment, stdlib-only checker.',
        'checker': checks,
        'stderr': result.stderr,
        'independent_audit': False,
        'scope': 'Author integrity replay and finite identities, not a proof of the open theorem.'
    }, indent=2, sort_keys=True))
