#!/usr/bin/env python3
"""Portable, fail-closed integrity and exact replay for the unchanged partials."""
import argparse
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import subprocess
import sys
import zipfile

ROOT = Path(__file__).absolute().parent
AUTHOR = 'geometry_7000003'
AUDIT = 'geometry_7000003_independent_audit'
ARCHIVE = 'GEOMETRY_7000003_AUTHOR_SAFE_FREEZE.zip'
PINS = {
    AUTHOR + '/MANIFEST.json': '4d6bf3e3bd1197e2ab5f8c910fa16bced508c614c2b58bda113bd5ea97198259',
    AUDIT + '/MANIFEST.json': '9ee0dc3ce60214a2b9ae92e42cb7c38e031a394da4383a503f498f3eb57d9c21',
    ARCHIVE: 'fd97db7181994876f78dbc2afc20d497bdd2fd34becdf2f20c10c8ea66cb4b48',
}

def require(ok, why):
    if not ok:
        raise RuntimeError(why)

def digest(raw):
    return hashlib.sha256(raw).hexdigest()

def integrity():
    require(ROOT.is_dir() and not ROOT.is_symlink(), 'Regular packet root required')
    mf = ROOT / 'PUBLICATION_MANIFEST.json'
    require(mf.is_file() and not mf.is_symlink(), 'Regular publication manifest required')
    before = {'PUBLICATION_MANIFEST.json': mf.read_bytes()}
    m = json.loads(before['PUBLICATION_MANIFEST.json'])
    require(m['problem_id'] == '7000003' and m['status'] == 'unsolved' and m['turns'] == '5/5', 'Wrong scope')
    rows = {r['path']: r for r in m['files']}
    require(len(rows) == len(m['files']) == 20, 'Duplicate or incorrect file count')
    for name in rows:
        p = PurePosixPath(name)
        require(not p.is_absolute() and '..' not in p.parts and str(p) == name, 'Unsafe path')
    for p in ROOT.rglob('*'):
        require(not p.is_symlink(), 'Symlink input: ' + p.name)
        require(p.is_file() or p.is_dir(), 'Special input')
    actual = {p.relative_to(ROOT).as_posix() for p in ROOT.rglob('*') if p.is_file()}
    dirs = {p.relative_to(ROOT).as_posix() for p in ROOT.rglob('*') if p.is_dir()}
    require(actual == set(rows) | {'PUBLICATION_MANIFEST.json'}, 'Unexpected or missing file')
    require(dirs == {AUTHOR, AUDIT}, 'Unexpected or missing directory')
    for name, r in rows.items():
        b = (ROOT/name).read_bytes()
        require(len(b) == r['bytes'] and digest(b) == r['sha256'], 'Integrity failure: ' + name)
        before[name] = b
    for name, expected in PINS.items():
        require(digest(before[name]) == expected, 'Frozen binding: ' + name)
    for folder, count in [(AUTHOR, 7), (AUDIT, 8)]:
        inner = json.loads(before[folder + '/MANIFEST.json'])
        records = inner['files']
        names = {r['path'] for r in records} | {'MANIFEST.json'}
        require(len(records) == count - 1 and len(names) == count, 'Frozen manifest count')
        require({p.name for p in (ROOT/folder).iterdir()} == names, 'Frozen file inventory')
        for r in records:
            b = before[folder + '/' + r['path']]
            require(len(b) == r['bytes'] and digest(b) == r['sha256'], 'Frozen member mismatch')
    snapshot = json.loads(before[AUDIT + '/AUTHOR_SNAPSHOT.json'])
    for r in snapshot['author_files']:
        b = before[AUTHOR + '/' + r['path']]
        require(len(b) == r['bytes'] and digest(b) == r['sha256'], 'Author snapshot mismatch')
    require(len(before[ARCHIVE]) == 15539, 'Archive size')
    with zipfile.ZipFile(ROOT/ARCHIVE) as z:
        names = {AUTHOR + '/' + p.name for p in (ROOT/AUTHOR).iterdir()}
        require(len(z.infolist()) == 7 and set(z.namelist()) == names, 'Archive inventory')
        for name in names:
            require(z.read(name) == before[name], 'Archive member bytes')
    v = json.loads(before[AUDIT + '/VERDICT.json'])
    require(v['verdict'] == 'SCOPED_PASS' and v['mathematical_disposition'] == 'no_resolution' and v['mandatory_corrections'] == [], 'Audit gate')
    s = json.loads(before['PUBLICATION_STATUS.json'])
    require(s['problem_id'] == '7000003' and s['status'] == 'unsolved' and s['turns'] == '5/5', 'Publication status')
    require(s['mathematical_disposition'] == 'no_resolution' and s['full_target_resolved'] is False and s['novelty_claim'] is False, 'Unwarranted promotion')
    require(s['audit_verdict'] == 'SCOPED_PASS' and s['mandatory_corrections'] == [] and s['frozen_pins'] == PINS, 'Status pins')
    return before

def run(name, optimized=False):
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1', PYTHONOPTIMIZE='0')
    env.pop('PYTHONPATH', None)
    env.pop('PYTHONHOME', None)
    return subprocess.check_output([sys.executable, '-B', *(['-O'] if optimized else []), str(ROOT/name)], cwd=ROOT, env=env)

def main():
    p = argparse.ArgumentParser()
    p.add_argument('--integrity-only', action='store_true')
    args = p.parse_args()
    before = integrity()
    result = {'result':'PASS', 'problem_id':'7000003', 'status':'unsolved', 'turns':'5/5', 'packet_files':21, 'frozen_files_preserved':15, 'author_archive_preserved':True, 'publication_manifest_sha256':digest(before['PUBLICATION_MANIFEST.json'])}
    if not args.integrity_only:
        run(AUTHOR+'/verify_manifest.py')
        run(AUDIT+'/verify_manifest.py')
        for optimized in [False, True]:
            a = run(AUTHOR+'/verify.py', optimized)
            require(a == before[AUTHOR+'/EXPECTED_RESULTS.json'], 'Author replay mismatch')
            b = run(AUDIT+'/independent_verify.py', optimized)
            require(b == before[AUDIT+'/EXPECTED_RESULTS.json'], 'Independent replay mismatch')
        result.update(author_assertions=24, author_negative_controls=8, independent_assertions=45, independent_negative_controls=9, normal_and_optimized=True, author_replay_byte_equal=True, independent_replay_byte_equal=True)
    require(integrity() == before, 'Input changed during replay')
    result['scope'] = 'Restricted theorems and obstruction controls only; fixed convex-planar-boundary global rigidity unresolved.'
    print(json.dumps(result, indent=2, sort_keys=True))

if __name__ == '__main__':
    main()
