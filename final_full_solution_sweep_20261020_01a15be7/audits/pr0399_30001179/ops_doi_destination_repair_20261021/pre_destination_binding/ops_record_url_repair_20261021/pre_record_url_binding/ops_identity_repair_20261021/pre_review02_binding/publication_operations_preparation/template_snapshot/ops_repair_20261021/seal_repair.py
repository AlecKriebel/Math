#!/usr/bin/env python3
"""Seal/verify current narrow repair, preserving the historical preparation binding."""
import argparse
import datetime as dt
import hashlib
import json
from pathlib import Path
HERE=Path(__file__).resolve().parent
AUDIT=HERE.parent
OLD=AUDIT/'publication_operations_preparation/prior_review_02_full'
HISTORICAL=AUDIT/'publication_operations_preparation/MANIFEST.json'
OLD_SHA='999852717308827d82c11825f1ccb727be39da786fa5a1f34a6dde229c26c6e5'
HELPERS=['ops_binding.py','prepublication_check.py','publication_live_gates.py','repository_integration.py',
         'publication_lifecycle.py','record_publication_ledger.py','verify_published_files.py']


def sha(data):return hashlib.sha256(data).hexdigest()


def preserved():
    if sha(HISTORICAL.read_bytes())!=OLD_SHA:
        raise RuntimeError('Historical original preparation manifest changed')
    manifest=json.loads(HISTORICAL.read_text())
    if len(manifest['files'])!=16:raise RuntimeError('Historical inventory differs')
    for e in manifest['files']:
        data=(OLD/e['path']).read_bytes()
        if len(data)!=e['bytes'] or sha(data)!=e['sha256']:
            raise RuntimeError('Preserved old artifact changed: '+e['path'])
        if '/' in e['path'] and (AUDIT/e['path']).read_bytes()!=data:
            raise RuntimeError('Original historical preparation evidence changed')
    if (OLD/'publication_operations_preparation/MANIFEST.json').read_bytes()!=HISTORICAL.read_bytes():
        raise RuntimeError('Copied historical manifest differs')
    return manifest


def selection():
    old=preserved()
    paths=[AUDIT/name for name in HELPERS]
    paths+=[p for p in HERE.rglob('*') if p.is_file() and p.name not in {'MANIFEST.json','MANIFEST.sha256'} and '__pycache__' not in p.parts]
    paths+=[OLD/e['path'] for e in old['files']]
    paths+=[OLD/'publication_operations_preparation/MANIFEST.json',HISTORICAL,HISTORICAL.with_suffix('.sha256')]
    if any(p.is_symlink() for p in paths) or len(paths)!=len(set(paths)):
        raise RuntimeError('Unsafe or duplicate repair inventory')
    return sorted(paths)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--verify',action='store_true')
    args=parser.parse_args()
    path=HERE/'MANIFEST.json';checksum=HERE/'MANIFEST.sha256'
    paths=selection()
    if args.verify:
        value=json.loads(path.read_text())
        if checksum.read_text().split()[0]!=sha(path.read_bytes()):raise RuntimeError('New repair seal differs')
        if {p.relative_to(AUDIT).as_posix() for p in paths}!={e['path'] for e in value['files']}:
            raise RuntimeError('New repair inventory differs')
        for e in value['files']:
            data=(AUDIT/e['path']).read_bytes()
            if len(data)!=e['bytes'] or sha(data)!=e['sha256']:
                raise RuntimeError('Repaired bound artifact differs: '+e['path'])
        print(json.dumps({'verified':True,'artifacts':len(value['files']),'manifest_sha256':sha(path.read_bytes()),'historical16_plus_manifest_verified':True}))
        return
    value={'timestamp':dt.datetime.now(dt.timezone.utc).isoformat(),'pr':280,'completion_estimate_percent':100,
           'scope':'Narrow local operational repair only, pending new independent complete review; no publication readiness or lifecycle outcomes asserted.',
           'old_preparation_manifest_sha256':OLD_SHA,'historical_binding_status':'Preserved unchanged; verify old16 against prior_review_02_full, not repaired canonical helpers.',
           'publication_ready':False,'files':[{'path':p.relative_to(AUDIT).as_posix(),'bytes':p.stat().st_size,'sha256':sha(p.read_bytes())} for p in paths]}
    path.write_text(json.dumps(value,indent=2)+'\n');checksum.write_text(sha(path.read_bytes())+'  MANIFEST.json\n')
    print(json.dumps({'artifacts':len(value['files']),'manifest_sha256':sha(path.read_bytes())}))


if __name__=='__main__':main()
