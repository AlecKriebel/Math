#!/usr/bin/env python3
"""Authenticate the complete packet and replay frozen checks with assertions enabled."""
import argparse
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import stat
import subprocess
import sys
import tempfile
import zipfile

ARCHIVES = {
    'author': ('AUTHOR', 23857, '6c6762fa475fe36c8c14c81fb9895fe9cee8489794d52cc54b08b6101b54981c'),
    'independent_audit': ('AUDIT', 23399, '3ee4d8c9152392abeb87af427d358770a4763def1b525c017afa9f9f1b13dee9')}
AUTHOR_MANIFEST = '86dad4963c8b21ab475b2ef612c09ac499bfe11437d72ef81fbcb583c1b10553'
AUDIT_MANIFEST = '071afa38ffa81c43bd0b1cd64529a5347806f889643884dc029c2e90ae4bce6d'


def require(ok, message):
    if not ok:
        raise ValueError(message)


def pairs(items):
    result = {}
    for key, value in items:
        require(key not in result, 'duplicate JSON key')
        result[key] = value
    return result


def read_json(path):
    return json.loads(path.read_text(encoding='utf-8'), object_pairs_hook=pairs)


def identity(path):
    data = path.read_bytes()
    return {'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()}


def safe_path(name):
    require(isinstance(name, str), 'non-string path')
    p = PurePosixPath(name)
    require(name and not p.is_absolute() and str(p) == name
            and all(x not in ('', '.', '..') for x in p.parts)
            and '\\' not in name, 'unsafe path')
    return p


def authenticate(root, expected_manifest):
    require(root.is_dir() and not root.is_symlink(), 'publication directory')
    manifest_path = root / 'PUBLICATION_MANIFEST.json'
    require(not manifest_path.is_symlink(), 'manifest symlink')
    require(identity(manifest_path)['sha256'] == expected_manifest, 'external manifest pin mismatch')
    manifest = read_json(manifest_path)
    require(set(manifest) == {'schema', 'algorithm', 'files'}
            and type(manifest['schema']) is int and manifest['schema'] == 1
            and manifest['algorithm'] == 'sha256' and type(manifest['files']) is list, 'manifest schema')
    wanted_files = {'PUBLICATION_MANIFEST.json'}
    wanted_dirs = set()
    for e in manifest['files']:
        require(type(e) is dict and set(e) == {'path', 'bytes', 'sha256'}, 'manifest entry schema')
        p = safe_path(e['path'])
        require(str(p) not in wanted_files, 'duplicate manifest path')
        wanted_files.add(str(p))
        wanted_dirs.update(str(x) for x in p.parents if str(x) != '.')
        path = root / p
        require(p.suffix in {'.md', '.json', '.py', '.txt', '.zip'}, 'forbidden file type')
        require(p.suffix != '.txt' or p.name == 'requirements.txt', 'unexpected text extract')
        require(path.is_file() and not path.is_symlink(), 'missing payload or symlink')
        require(type(e['bytes']) is int and e['bytes'] >= 0 and re.fullmatch('[0-9a-f]{64}', e['sha256']) is not None, 'identity schema')
        require(identity(path) == {k:e[k] for k in ('bytes', 'sha256')}, 'payload identity mismatch: ' + str(p))
    actual_files, actual_dirs = set(), set()
    for p in root.rglob('*'):
        require(not p.is_symlink(), 'recursive symlink')
        rel = p.relative_to(root).as_posix()
        if p.is_dir():
            actual_dirs.add(rel)
        else:
            require(p.is_file(), 'nonregular file')
            actual_files.add(rel)
    require(actual_files == wanted_files and actual_dirs == wanted_dirs, 'recursive inventory mismatch')
    for directory, (label, size, digest) in ARCHIVES.items():
        path = root / 'archives' / ('KAHLER_KOSZUL_30005418_' + label + '_SAFE_FREEZE.zip')
        require(identity(path) == {'bytes': size, 'sha256': digest}, 'frozen ZIP identity')
        with zipfile.ZipFile(path) as archive:
            names = archive.namelist()
            expected = {p.relative_to(root/directory).as_posix() for p in (root/directory).rglob('*') if p.is_file()}
            require(len(names) == len(set(names)) and set(names) == expected, 'ZIP inventory')
            for entry in archive.infolist():
                safe_path(entry.filename)
                require(not entry.is_dir() and not stat.S_ISLNK(entry.external_attr >> 16), 'ZIP member type')
                require(archive.read(entry) == (root/directory/entry.filename).read_bytes(), 'ZIP-expanded mismatch')
    require(identity(root/'author/AUTHOR_MANIFEST.json')['sha256'] == AUTHOR_MANIFEST, 'author manifest pin')
    require(identity(root/'independent_audit/AUDIT_MANIFEST.json')['sha256'] == AUDIT_MANIFEST, 'audit manifest pin')
    status = read_json(root/'PUBLICATION_STATUS.json')
    for key, value in {'problem_id':30005418, 'rank':797, 'disposition':'unsolved',
                       'approach_families_used':5, 'approach_family_limit':5,
                       'full_target_resolved':False, 'mathematical_corrections_required':False,
                       'human_peer_review':False, 'formal_proof_certificate':False,
                       'novelty_claim':False, 'audit_verdict':'PASS_SCOPED_RESULTS'}.items():
        require(status.get(key) == value and type(status.get(key)) is type(value), 'publication scope')
    return len(wanted_files), len(wanted_dirs)


def child_env():
    env = dict(os.environ)
    env.pop('PYTHONOPTIMIZE', None)
    env['PYTHONDONTWRITEBYTECODE'] = '1'
    return env


def run_python(arguments, cwd):
    result = subprocess.run([sys.executable, '-I', '-B', *map(str, arguments)],
                            cwd=cwd, env=child_env(), capture_output=True, text=True)
    require(result.returncode == 0, 'child failed: ' + result.stderr[-4000:])
    return result.stdout


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--expected-manifest-sha256', required=True)
    p.add_argument('--integrity-only', action='store_true')
    args = p.parse_args()
    root = Path(__file__).resolve().parent
    files, dirs = authenticate(root, args.expected_manifest_sha256)
    if args.integrity_only:
        print(json.dumps({'status':'PASS_INTEGRITY_ONLY','files':files,'directories':dirs},sort_keys=True))
        return
    with tempfile.TemporaryDirectory(prefix='kahler-publication-replay-') as tmp:
        sentinel = run_python(['-c', '''import json,sys,sympy
if sys.flags.optimize != 0 or not __debug__: raise SystemExit("optimized child")
try:
    assert False
except AssertionError:
    pass
else:
    raise SystemExit("assertion sentinel failed")
if sympy.__version__ != "1.14.0": raise SystemExit("requires SymPy 1.14.0")
print(json.dumps({"assertions_enabled":True,"optimization":sys.flags.optimize,"sympy":sympy.__version__}))
'''], tmp)
        sentinel = json.loads(sentinel, object_pairs_hook=pairs)
        require(sentinel == {'assertions_enabled':True,'optimization':0,'sympy':'1.14.0'}, 'sentinel result')
        result = run_python([root/'independent_audit/verify_audit.py', root/'author',
                             '--author-zip',root/'archives/KAHLER_KOSZUL_30005418_AUTHOR_SAFE_FREEZE.zip',
                             '--expected-manifest', AUDIT_MANIFEST], tmp)
        result = json.loads(result, object_pairs_hook=pairs)
        require(result['status'] == 'PASS' and result['general_target'] == 'UNSOLVED', 'audit disposition')
        require(result['author_math_replay'] == result['independent_math_replay'] == 'byte-identical', 'replay result')
    print(json.dumps({'status':'PASS_PORTABLE_PUBLICATION','problem_id':30005418,
       'disposition':'unsolved','approach_families_used':5,'audit_verdict':'PASS_SCOPED_RESULTS',
       'publication_files':files,'publication_directories':dirs,'frozen_archives':2,
       'child_assertion_sentinel':sentinel,'author_math_replay':'byte-identical',
       'independent_math_replay':'byte-identical','author_manifest_sha256':AUTHOR_MANIFEST,
       'audit_manifest_sha256':AUDIT_MANIFEST,
       'optional_source_rehash':'NOT_RUN_MISSING_OPTIONAL_SOURCE_INPUTS',
       'fresh_source_inspection':False,'universal_target_certified':False,
       'human_peer_review':False},indent=2,sort_keys=True))


if __name__ == '__main__':
    try:
        main()
    except (OSError, ValueError, KeyError, TypeError, zipfile.BadZipFile, subprocess.CalledProcessError) as exc:
        raise SystemExit('FAIL: ' + str(exc))
