#!/usr/bin/env python3
"""Verify a fixed payload against an externally supplied, independently frozen manifest."""
import argparse
import hashlib
import json
from pathlib import Path
import stat
import subprocess
import sys

PAYLOAD = {'README.md','PROOF.md','APPROACH_LOG.md','SOURCE_METADATA.json',
           'RESULTS.json','certificate.py','verify_bundle.py'}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def unique_object(pairs):
    out = {}
    for key, value in pairs:
        require(key not in out, 'Duplicate JSON key')
        out[key] = value
    return out


def verify(root, manifest_path):
    require(root.is_dir() and not root.is_symlink(), 'Root is not an ordinary directory')
    require(stat.S_ISREG(manifest_path.lstat().st_mode), 'Manifest is not a regular file')
    require(manifest_path.resolve().parent != root.resolve(), 'Manifest must be external')
    entries = list(root.iterdir())
    require({p.name for p in entries} == PAYLOAD, 'Strict inventory mismatch')
    for p in entries:
        require(stat.S_ISREG(p.lstat().st_mode), 'Nonregular payload: '+p.name)
    raw = manifest_path.read_bytes()
    manifest = json.loads(raw, object_pairs_hook=unique_object)
    require(set(manifest) == {'schema','problem_id','files'}, 'Manifest keys')
    require(manifest['schema'] == 'external-authored-payload-v1', 'Manifest schema')
    require(type(manifest['problem_id']) is int and manifest['problem_id'] == 30001702,
            'Manifest problem ID')
    records = manifest['files']
    require(isinstance(records,list) and len(records) == len(PAYLOAD), 'Manifest count')
    require(all(isinstance(r,dict) and set(r)=={'path','bytes','sha256'} for r in records),
            'Manifest records')
    require({r['path'] for r in records} == PAYLOAD, 'Manifest inventory')
    for record in records:
        require(type(record['bytes']) is int and record['bytes'] >= 0, 'Byte-count type')
        digest = record['sha256']
        require(isinstance(digest,str) and len(digest)==64 and
                all(c in '0123456789abcdef' for c in digest), 'Hash syntax')
        data = (root/record['path']).read_bytes()
        require(len(data)==record['bytes'], 'Byte count mismatch: '+record['path'])
        require(hashlib.sha256(data).hexdigest()==digest, 'Hash mismatch: '+record['path'])
    command = [sys.executable,'-I','-B']+(['-O'] if sys.flags.optimize else [])
    command.append(str(root/'certificate.py'))
    result = subprocess.run(command,cwd=str(root.parent),capture_output=True,text=True)
    require(result.returncode==0, 'Certificate failed: '+result.stderr)
    require(result.stderr=='', 'Certificate stderr')
    require(result.stdout==(root/'RESULTS.json').read_text(), 'Exact-output replay mismatch')
    report = json.loads(result.stdout)
    require(report['status']=='PARTIAL_UNRESOLVED' and
            report['universal_factorial_bound_proved'] is False, 'Claim scope mismatch')
    require(report['identity_checks']==5250 and report['product_gap_checks']==400,
            'Check count mismatch')
    return {'verified':True,'payload_files':len(PAYLOAD),'optimized':bool(sys.flags.optimize),
            'manifest_sha256':hashlib.sha256(raw).hexdigest(),
            'status':'PARTIAL_UNRESOLVED'}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root',type=Path,default=Path(__file__).absolute().parent)
    parser.add_argument('--manifest',type=Path,required=True)
    args = parser.parse_args()
    print(json.dumps(verify(args.root.absolute(),args.manifest.absolute()),indent=2,sort_keys=True))
