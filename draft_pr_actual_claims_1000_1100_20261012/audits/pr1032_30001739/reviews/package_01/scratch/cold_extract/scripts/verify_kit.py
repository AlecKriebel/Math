#!/usr/bin/env python3
"""Check allowlist and exact bytes, then finite diagnostics; no theorem/priority oracle.

Python 3.10+, standard library. No network, shell, package installation or file writes.
Run with -B to prevent interpreter caches if manually importing checker modules.
"""
from pathlib import Path, PurePosixPath
import argparse
import hashlib
import json
import stat
import subprocess
import sys
import zipfile

ROOT = Path(__file__).resolve().parents[1]
def require(value, message):
    if not value:
        raise RuntimeError(message)
def digest(data):
    return hashlib.sha256(data).hexdigest()
def safe_name(name):
    p = PurePosixPath(name)
    return bool(name) and not p.is_absolute() and '..' not in p.parts and '\\' not in name and p.as_posix() == name
def validate_bytes(items):
    names = list(items)
    require(len(set(names)) == len(names), 'duplicate members')
    require('MANIFEST.json' in items and 'ALLOWLIST.json' in items, 'missing inventory')
    manifest = json.loads(items['MANIFEST.json'])
    allow = json.loads(items['ALLOWLIST.json'])['files']
    require(allow == sorted(set(allow)), 'allowlist duplicate/order')
    require(all(safe_name(n) for n in allow), 'unsafe allowlist path')
    require(set(items) == set(allow), 'unlisted or missing package member')
    rows = manifest['files']
    require(len(rows) == len(allow)-1, 'manifest row count')
    require({r['path'] for r in rows} == set(allow)-{'MANIFEST.json'}, 'manifest member mismatch')
    require(len({r['path'] for r in rows}) == len(rows), 'duplicate manifest row')
    for r in rows:
        data = items[r['path']]
        require(len(data) == r['bytes'] and digest(data) == r['sha256'], 'content identity: '+r['path'])
    status = json.loads(items['STATUS.json'])
    require(status['priority_overlap_Luo_Zha'] == 'UNKNOWN', 'priority status')
    require(status['publication_ready'] is False, 'premature readiness')
    require(status['minimum_fresh_complete_independent_reviews'] == 2, 'review gate')
    return manifest
def validate_archive(archive):
    with zipfile.ZipFile(archive) as z:
        info = z.infolist()
        require(len({i.filename for i in info}) == len(info), 'duplicate archive member')
        require(all(safe_name(i.filename) and not i.is_dir() for i in info), 'unsafe archive member')
        require(all(stat.S_IFMT(i.external_attr >> 16) != stat.S_IFLNK for i in info), 'archive symlink')
        require(all(i.date_time == (2026,10,16,0,0,0) and i.compress_type == zipfile.ZIP_STORED for i in info), 'noncanonical archive member')
        return validate_bytes({i.filename:z.read(i) for i in info})
def run(root=ROOT, archive=None):
    files = [p for p in root.rglob('*') if p.is_file()]
    require(not any(p.is_symlink() for p in root.rglob('*')), 'symlink in package')
    items = {p.relative_to(root).as_posix():p.read_bytes() for p in files}
    manifest = validate_bytes(items)
    if archive is not None:
        validate_archive(archive)
        with zipfile.ZipFile(archive) as z:
            require(all(z.read(n) == d for n,d in items.items()), 'archive differs from kit')
    expected = json.loads(items['EXPECTED_RESULTS.json'])
    results=[]
    for mode in ([], ['-O'], ['-OO']):
        for script in expected:
            cmd = [sys.executable, '-I', '-B', *mode, str(root/'scripts'/script)]
            proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=60)
            require(proc.returncode == 0 and not proc.stderr, 'finite diagnostic failed: '+script+' '+repr(mode))
            require(digest(proc.stdout) == expected[script]['sha256'] and len(proc.stdout) == expected[script]['bytes'], 'diagnostic output mismatch: '+script)
            results.append({'script':script,'mode':mode or ['normal'],'stdout_bytes':len(proc.stdout),'sha256':digest(proc.stdout)})
    return {'status':'PASS','files':len(items),'diagnostic_runs':len(results),'results':results,
            'computes_Hom_space':False,'certifies_priority':False,'publication_ready':False}
if __name__ == '__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--archive',type=Path)
    args=parser.parse_args()
    print(json.dumps(run(archive=args.archive),indent=2,sort_keys=True))
