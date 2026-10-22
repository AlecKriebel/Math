#!/usr/bin/env python3
"""Seal/verify exact PR399 preparation and its immutable inputs. No provider calls."""
import argparse
import datetime as dt
import hashlib
import json
from pathlib import Path
HERE=Path(__file__).resolve().parent
AUDIT=HERE.parent
HELPERS=['ops_binding.py','prepublication_check.py','publication_live_gates.py','repository_integration.py','publication_lifecycle.py','record_publication_ledger.py','verify_published_files.py']

def sha(data):return hashlib.sha256(data).hexdigest()

def entry(path):
    data=path.read_bytes()
    return {'path':path.relative_to(AUDIT).as_posix(),'bytes':len(data),'sha256':sha(data)}

def outputs():
    excluded={HERE/'MANIFEST.json',HERE/'MANIFEST.sha256'}
    all_paths=list(HERE.rglob('*'))
    if any(p.is_symlink() for p in all_paths):raise RuntimeError('Symlink in preparation custody')
    paths=[AUDIT/n for n in HELPERS]+[p for p in all_paths if p.is_file() and p not in excluded and '__pycache__' not in p.parts]
    if len(paths)!=len(set(paths)):raise RuntimeError('Duplicate preparation path')
    return sorted(paths)

def inputs():
    paths=[AUDIT/n for n in ['SOURCE_SNAPSHOT.json','ROOT_SCIENTIFIC_REVIEW_ACCEPTANCE.json','ROOT_PRIORITY_ACCEPTANCE.json','ROOT_MANUSCRIPT_VISUAL_ASSESSMENT.json','ROOT_PUBLICATION_ARCHIVE_REPRODUCTION.json','ROOT_PACKAGE_REVIEW01_ACCEPTANCE.json']]
    snapshot=json.loads((AUDIT/'SOURCE_SNAPSHOT.json').read_text())
    paths += [AUDIT/e['snapshot'] for e in snapshot['files']]
    release=json.loads((AUDIT/'preprint/publication/RELEASE_FILES.json').read_text())
    paths += [AUDIT/'preprint/publication/RELEASE_FILES.json']
    paths += [AUDIT/'preprint/publication'/e['path'] for e in release['files']+release['preparation_auxiliary_files']]
    return sorted(paths)

def verify_entry(e):
    p=AUDIT/e['path']
    if p.is_symlink() or not p.is_file():raise RuntimeError('Unsafe/non-file sealed artifact')
    data=p.read_bytes()
    if len(data)!=e['bytes'] or sha(data)!=e['sha256']:raise RuntimeError('Bound artifact differs: '+e['path'])

def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--verify',action='store_true');args=parser.parse_args()
    manifest=HERE/'MANIFEST.json';checksum=HERE/'MANIFEST.sha256'
    if args.verify:
        data=manifest.read_bytes();value=json.loads(data)
        if checksum.read_text()!=sha(data)+'  MANIFEST.json\n':raise RuntimeError('Preparation seal differs')
        if {e['path'] for e in value['files']}!={p.relative_to(AUDIT).as_posix() for p in outputs()}:raise RuntimeError('Preparation inventory differs')
        if {e['path'] for e in value['immutable_inputs']}!={p.relative_to(AUDIT).as_posix() for p in inputs()}:raise RuntimeError('Input inventory differs')
        for e in value['files']+value['immutable_inputs']:verify_entry(e)
        print(json.dumps({'verified':True,'authored_and_captured_artifacts':len(value['files']),'immutable_inputs':len(value['immutable_inputs']),'manifest_sha256':sha(data),'publication_ready':False}));return
    if manifest.exists() or checksum.exists():raise RuntimeError('Seal already exists; preserve prior checkpoint before any intentional reseal')
    value={'schema':1,'timestamp_utc':dt.datetime.now(dt.timezone.utc).isoformat(),'pr':399,'problem_id':'30001179','completion_estimate_percent':100,
        'scope':'Offline operation preparation only, pending independent complete operational review and affirmative root clearance. No live lifecycle outcome or publication authorization.',
        'publication_ready':False,'files':[entry(p) for p in outputs()],'immutable_inputs':[entry(p) for p in inputs()]}
    data=(json.dumps(value,indent=2)+'\n').encode();manifest.write_bytes(data);checksum.write_text(sha(data)+'  MANIFEST.json\n')
    print(json.dumps({'authored_and_captured_artifacts':len(value['files']),'immutable_inputs':len(value['immutable_inputs']),'manifest_sha256':sha(data)}))
if __name__=='__main__':main()
