#!/usr/bin/env python3
"""Strict offline publication-package integrity check; no network or writes."""
import hashlib
import json
from pathlib import Path
import sys

HERE=Path(__file__).resolve().parent
EXPECTED_NAMES=set(['FREEZE_MANIFEST.json', 'README.md', 'SHA256SUMS', 'audit/AUDIT.md', 'audit/AUDITED_INPUTS.json', 'audit/AUDIT_MANIFEST.json', 'audit/AUDIT_MANIFEST.sha256', 'audit/AUDIT_RESULT.json', 'audit/CORRECTIONS.json', 'audit/INDEPENDENT_CHECK_RESULTS.json', 'audit/README.md', 'audit/REPLAY_RESULTS.json', 'audit/SOURCE_CHECKS.json', 'audit/independent_checks.py', 'audit/run_audit.py', 'audit/source_map.corrected.md', 'audit/source_map.patch', 'audit/verify_audit_manifest.py', 'packet/README.md', 'packet/analysis.md', 'packet/controls.json', 'packet/research_log.md', 'packet/result.json', 'packet/source_map.md', 'packet/verification_metadata.json', 'packet/verify.py', 'verify_package.py'])
EXPECTED_DIRS={'packet','audit'}

def require(ok,message):
    if not ok:
        raise SystemExit('FAIL: '+message)

def unique_object(pairs):
    obj={}
    for key,value in pairs:
        require(key not in obj,'duplicate JSON key')
        obj[key]=value
    return obj

raw=(HERE/'PUBLICATION_MANIFEST.json').read_bytes()
manifest=json.loads(raw,object_pairs_hook=unique_object)
require(manifest['problem_id']==30004996,'wrong problem')
rows=manifest['files']
require(type(rows) is list and len(rows)==len(EXPECTED_NAMES),'wrong inventory length')
seen=set()
for row in rows:
    name=row['path']
    require(type(name) is str and name in EXPECTED_NAMES and name not in seen,'unsafe, unexpected or duplicate path')
    seen.add(name)
    require(type(row['bytes']) is int and row['bytes']>=0,'invalid byte count')
    path=HERE/name
    require(path.is_file() and not path.is_symlink(),'not a plain file: '+name)
    data=path.read_bytes()
    require(len(data)==row['bytes'],'byte-count mismatch: '+name)
    require(hashlib.sha256(data).hexdigest()==row['sha256'],'hash mismatch: '+name)
require(seen==EXPECTED_NAMES,'manifest inventory mismatch')
actual_files=set()
actual_dirs=set()
for path in HERE.rglob('*'):
    require(not path.is_symlink(),'symlink rejected')
    name=path.relative_to(HERE).as_posix()
    if path.is_file():
        actual_files.add(name)
    elif path.is_dir():
        actual_dirs.add(name)
    else:
        raise SystemExit('FAIL: nonregular entry')
require(actual_files==EXPECTED_NAMES|{'PUBLICATION_MANIFEST.json'},'extra or missing file')
require(actual_dirs==EXPECTED_DIRS,'extra or missing directory')
print(json.dumps({'all_passed':True,'problem_id':30004996,'manifest_payloads':len(rows),'total_files':len(actual_files),'publication_manifest_sha256':hashlib.sha256(raw).hexdigest()},indent=2,sort_keys=True))
