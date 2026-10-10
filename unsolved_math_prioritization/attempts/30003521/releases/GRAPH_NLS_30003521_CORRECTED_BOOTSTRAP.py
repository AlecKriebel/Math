"""Fail-closed pinned replay. Invoke with Python -I -S, with or without -O."""
import hashlib
import io
import json
import pathlib
import stat
import subprocess
import sys
import tempfile
import zipfile

ROOT = pathlib.Path(__file__).resolve().parent
MANIFEST = ROOT / 'GRAPH_NLS_30003521_CORRECTED_EXTERNAL_MANIFEST.json'
PINNED_MANIFEST_SHA256 = '05386fd90e97e008c580fe90fc1fbffe7cf037a20bde7541085eedadbc6fabfc'

def require(condition, label):
    if not condition:
        raise RuntimeError('validation failed: ' + label)

manifest_bytes = MANIFEST.read_bytes()
require(hashlib.sha256(manifest_bytes).hexdigest() == PINNED_MANIFEST_SHA256, 'manifest_sha256')
manifest = json.loads(manifest_bytes)
require(manifest['archive']['name'] == 'GRAPH_NLS_30003521_CORRECTED_SAFE.zip', 'archive_name')
archive = ROOT / manifest['archive']['name']
archive_bytes = archive.read_bytes()
require(len(archive_bytes) == manifest['archive']['bytes'], 'archive_bytes')
require(hashlib.sha256(archive_bytes).hexdigest() == manifest['archive']['sha256'], 'archive_sha256')
expected = {r['name']: r for r in manifest['files']}
require(len(expected) == len(manifest['files']) == 4, 'manifest_members')
require(set(expected) == {'PROOF_AND_STATUS.md', 'SOURCE_METADATA.json', 'STATUS.json', 'check_identities.py'}, 'expected_member_names')
verified = {}
# Parse the already hashed bytes, never reopen the archive after verification.
with zipfile.ZipFile(io.BytesIO(archive_bytes)) as z:
    names = z.namelist()
    require(len(names) == len(set(names)), 'duplicate_zip_members')
    require(set(names) == set(expected), 'zip_members')
    for name in names:
        require(pathlib.PurePosixPath(name).name == name and '\\' not in name, 'member_basename')
        info = z.getinfo(name)
        require(not info.is_dir() and not stat.S_ISLNK(info.external_attr >> 16), 'member_file_type')
        require(info.file_size == expected[name]['bytes'], 'member_declared_bytes:' + name)
        data = z.read(name)
        require(len(data) == expected[name]['bytes'], 'member_actual_bytes:' + name)
        require(hashlib.sha256(data).hexdigest() == expected[name]['sha256'], 'member_sha256:' + name)
        verified[name] = data
# No payload import or execution occurs until all members pass the explicit gate.
with tempfile.TemporaryDirectory(prefix='graph-nls-corrected-replay-') as td:
    work = pathlib.Path(td)
    for name, data in verified.items():
        (work/name).write_bytes(data)
    result = subprocess.run(
        [sys.executable, '-I', '-S', str(work/'check_identities.py')],
        cwd=work, env={'PATH': '/usr/bin:/bin', 'LC_ALL': 'C.UTF-8'},
        capture_output=True, text=True, timeout=30, check=True)
    checks = json.loads(result.stdout)
    require(checks['passed'] is True, 'checker_passed')
    require(checks['count'] == 11 and len(checks['checks']) == 11, 'checker_count')
    require(all(value is True for value in checks['checks'].values()), 'checker_checks')
    print(json.dumps({
        'integrity_before_payload_execution': True,
        'fail_closed_with_optimization': True,
        'manifest_sha256': PINNED_MANIFEST_SHA256,
        'archive_sha256': manifest['archive']['sha256'],
        'verified_member_count': len(verified),
        'isolation': 'Caller -I -S; fresh temporary payload cwd; Python -I -S child; minimal environment; stdlib only.',
        'checker': checks,
        'stderr': result.stderr,
        'scope': 'Corrected integrity replay and finite identities, not a proof of the open theorem.'
    }, indent=2, sort_keys=True))
