"""Externally pinned audit replay, fail-closed with or without Python -O.
Invoke: python -I -S GRAPH_NLS_30003521_INDEPENDENT_AUDIT_BOOTSTRAP.py
"""
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
MANIFEST_NAME = 'GRAPH_NLS_30003521_INDEPENDENT_AUDIT_EXTERNAL_MANIFEST.json'
MANIFEST_SHA256 = 'dc130874db62fa94985c753ca4739703fa61372352c3b243ce147484f442acd4'
ARCHIVE_NAME = 'GRAPH_NLS_30003521_INDEPENDENT_AUDIT_SAFE.zip'

def require(condition, label):
    if not condition:
        raise RuntimeError('audit validation failed: ' + label)

mb = (ROOT / MANIFEST_NAME).read_bytes()
require(hashlib.sha256(mb).hexdigest() == MANIFEST_SHA256, 'manifest_sha256')
manifest = json.loads(mb)
require(manifest['archive']['name'] == ARCHIVE_NAME, 'archive_name')
ab = (ROOT / ARCHIVE_NAME).read_bytes()
require(len(ab) == manifest['archive']['bytes'], 'archive_bytes')
require(hashlib.sha256(ab).hexdigest() == manifest['archive']['sha256'], 'archive_sha256')
expected = {entry['name']: entry for entry in manifest['files']}
require(len(expected) == len(manifest['files']) == 15, 'manifest_cardinality')
verified = {}
with zipfile.ZipFile(io.BytesIO(ab)) as z:
    names = z.namelist()
    require(len(names) == len(set(names)), 'duplicate_members')
    require(set(names) == set(expected), 'member_set')
    for name in names:
        require(pathlib.PurePosixPath(name).name == name and '\\' not in name, 'member_basename')
        info = z.getinfo(name)
        require(not info.is_dir() and not stat.S_ISLNK(info.external_attr >> 16), 'member_type')
        require(info.file_size == expected[name]['bytes'], 'declared_member_size')
        data = z.read(name)
        require(len(data) == expected[name]['bytes'], 'actual_member_size')
        require(hashlib.sha256(data).hexdigest() == expected[name]['sha256'], 'member_sha256')
        verified[name] = data
# Every member has been checked; only now materialize and execute the control code.
with tempfile.TemporaryDirectory(prefix='graph-nls-audit-release-') as td:
    work = pathlib.Path(td)
    for name, data in verified.items():
        (work / name).write_bytes(data)
    result = subprocess.run([sys.executable, '-I', '-S', str(work / 'replay_adversarial_controls.py')], cwd=work, env={'PATH': '/usr/bin:/bin', 'LC_ALL': 'C.UTF-8'}, capture_output=True, text=True, timeout=180, check=True)
    replay = json.loads(result.stdout)
    require(replay['all_expected_results'] is True, 'all_control_results')
    require(replay['count'] == 46, 'control_count')
    require(replay['original_failure_confirmed'] is True, 'original_failure_demonstrated')
    require(replay['corrected_release_accepted'] is True, 'corrected_release_accepted')
    print(json.dumps({'archive_sha256': manifest['archive']['sha256'], 'manifest_sha256': MANIFEST_SHA256, 'verified_member_count': len(verified), 'integrity_before_payload_execution': True, 'all_expected_control_results': True, 'control_count': replay['count'], 'original_optimization_failure_confirmed': True, 'corrected_release_accepted': True, 'scope': 'Pinned finite integrity replay only; the independent mathematical report accepts bounded partial results, not the open theorem.', 'stderr': result.stderr}, indent=2, sort_keys=True))
