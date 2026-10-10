#!/usr/bin/env python3
"""Authenticate the complete publication before replaying frozen finite checks."""
import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import stat
import subprocess
import sys
import zipfile

ARCHIVES = {
 'author_v1': ('AUTHOR_SAFE_FREEZE', 17955, 'f603686a4d0a3d22cb26b6f1dbb972a8dd37a746a0738ef43165e3d9ff6d66ed'),
 'independent_audit': ('INDEPENDENT_AUDIT_SAFE', 38655, 'd35d483f06de1771829468e7b2e64b56567254784de0205f98e341f277d54eb7'),
 'author_v2': ('V2_SAFE_FREEZE', 20735, '9194e9059bd3255336a66e707d490c685b2055752a987aca65f099d89aab7c82'),
 'delta_acceptance': ('V2_DELTA_ACCEPTANCE_SAFE', 10463, 'e89df0aeb0a03707ecfa90722762c20aa3f60d8227d118a20830d62a81f1b9c4')}

def require(ok, message):
    if not ok: raise ValueError(message)

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
            and manifest['algorithm'] == 'sha256', 'manifest schema')
    wanted_files = {'PUBLICATION_MANIFEST.json'}
    wanted_dirs = set()
    for e in manifest['files']:
        require(set(e) == {'path', 'bytes', 'sha256'}, 'manifest entry schema')
        p = safe_path(e['path'])
        require(str(p) not in wanted_files, 'duplicate manifest path')
        wanted_files.add(str(p))
        wanted_dirs.update(str(x) for x in p.parents if str(x) != '.')
        path = root / p
        require(p.suffix in {'.md', '.json', '.py', '.patch', '.zip'}, 'forbidden file type')
        require(path.is_file() and not path.is_symlink(), 'missing payload or symlink')
        require(type(e['bytes']) is int and identity(path) == {k:e[k] for k in ('bytes', 'sha256')},
                'payload identity mismatch: ' + str(p))
    actual_files, actual_dirs = set(), set()
    for p in root.rglob('*'):
        require(not p.is_symlink(), 'recursive symlink')
        rel = p.relative_to(root).as_posix()
        if p.is_dir(): actual_dirs.add(rel)
        else:
            require(p.is_file(), 'nonregular file')
            actual_files.add(rel)
    require(actual_files == wanted_files and actual_dirs == wanted_dirs, 'recursive inventory mismatch')
    for directory, (label, size, digest) in ARCHIVES.items():
        path = root / 'archives' / ('JACOBIAN_COCYCLE_5300056_' + label + '.zip')
        require(identity(path) == {'bytes': size, 'sha256': digest}, 'frozen ZIP identity')
        with zipfile.ZipFile(path) as archive:
            names = archive.namelist()
            expected = {p.relative_to(root/directory).as_posix() for p in (root/directory).rglob('*') if p.is_file()}
            require(len(names) == len(set(names)) and set(names) == expected, 'ZIP inventory')
            for entry in archive.infolist():
                safe_path(entry.filename)
                require(not entry.is_dir() and not stat.S_ISLNK(entry.external_attr >> 16), 'ZIP member type')
                require(archive.read(entry) == (root/directory/entry.filename).read_bytes(), 'ZIP-expanded mismatch')
    status = read_json(root/'PUBLICATION_STATUS.json')
    expected_status = {'problem_id':5300056, 'rank':795, 'disposition':'unsolved',
                       'substantive_approaches_used':5, 'substantive_approach_limit':5,
                       'original_solution_credit':0, 'full_target_resolved':False,
                       'required_proof_replacements':3, 'human_peer_review':False,
                       'formal_proof_certificate':False, 'novelty_claim':False,
                       'latest_review':'V2_BOUNDED_DELTA_ACCEPTED'}
    for key,value in expected_status.items():
        require(status.get(key) == value and type(status.get(key)) is type(value), 'publication scope')
    return len(wanted_files), len(wanted_dirs)

def run(path, *arguments):
    args=[sys.executable]
    if sys.flags.optimize: args.append('-O')
    proc=subprocess.run(args+['-B', str(path), *map(str,arguments)], capture_output=True, text=True, check=True)
    return json.loads(proc.stdout, object_pairs_hook=pairs)

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--expected-manifest-sha256', required=True)
    p.add_argument('--integrity-only', action='store_true')
    args=p.parse_args(); root=Path(__file__).resolve().parent
    files,dirs=authenticate(root,args.expected_manifest_sha256)
    if args.integrity_only:
        print(json.dumps({'status':'PASS_INTEGRITY_ONLY','files':files,'directories':dirs},sort_keys=True)); return
    for version in ['author_v1','author_v2']:
        require(run(root/version/'verify_manifest.py')['status']=='PASS', 'author manifest failure')
        actual=run(root/version/'verify.py')
        require(actual==read_json(root/version/'verification_results.json'), 'author results differ')
        require(actual['total_assertions']==21193, 'author count')
    audit=run(root/'independent_audit/verify_audit.py')
    require(audit['status']=='PASS' and audit['author_assertions']==21193 and audit['independent_assertions']==20371, 'audit count')
    acceptance=run(root/'delta_acceptance/verify_acceptance.py')
    require(acceptance['status']=='PASS', 'acceptance integrity')
    arc=lambda key:root/'archives'/('JACOBIAN_COCYCLE_5300056_'+ARCHIVES[key][0]+'.zip')
    delta=run(root/'delta_acceptance/verify_delta.py','--original',arc('author_v1'),'--revised',arc('author_v2'),'--prior-audit',arc('independent_audit'))
    require(delta==read_json(root/'delta_acceptance/DELTA_RESULTS.json'), 'full delta replay differs')
    require(delta['exact_required_replacements']==3 and len(delta['unchanged_original_members'])==7, 'delta scope')
    print(json.dumps({'status':'PASS_PORTABLE_PUBLICATION','problem_id':5300056,
      'disposition':'unsolved','substantive_approaches_used':5,'original_solution_credit':0,
      'publication_files':files,'publication_directories':dirs,'frozen_archives':4,
      'author_assertions_per_run':21193,'independent_assertions':20371,
      'bounded_delta':'V2_BOUNDED_DELTA_ACCEPTED','required_replacements':3,
      'unchanged_original_members':7,'code_and_results_unchanged':True,
      'omitted_source_provenance':'NOT_RUN_MISSING_OPTIONAL_SOURCE_INPUTS',
      'analytic_theorems_certified':False,'human_peer_review':False},indent=2,sort_keys=True))

if __name__=='__main__':
    try: main()
    except (OSError, ValueError, KeyError, TypeError, zipfile.BadZipFile, subprocess.CalledProcessError) as exc:
        raise SystemExit('FAIL: '+str(exc))
