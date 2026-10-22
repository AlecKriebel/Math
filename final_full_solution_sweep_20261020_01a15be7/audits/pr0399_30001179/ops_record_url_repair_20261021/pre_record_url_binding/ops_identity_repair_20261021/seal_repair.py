#!/usr/bin/env python3
"""Seal current PR399 repair while preserving and reconstructing old42/26 lineage."""
import argparse,datetime,hashlib,json
from pathlib import Path
HERE=Path(__file__).resolve().parent
AUDIT=HERE.parent
OLD=HERE/'pre_review02_binding'
HELPERS=['ops_binding.py','prepublication_check.py','publication_live_gates.py','repository_integration.py','publication_lifecycle.py','record_publication_ledger.py','verify_published_files.py']
OLD_SHA='ad5c2339d915d8fe33f4ffbdab2d528d9258a394e70a66437d2b615ab70a3e9d'
LEAD_SHA='af763826f5e22bb64887496eada7e4aaa9c944faf45db3a0c93386b9833fbe39'

def sha(data):return hashlib.sha256(data).hexdigest()

def check_entry(root,e):
    path=root/e['path'];data=path.read_bytes()
    if path.is_symlink() or len(data)!=e['bytes'] or sha(data)!=e['sha256']:raise RuntimeError('Bound artifact differs: '+e['path'])

def preserved():
    path=AUDIT/'publication_operations_preparation/MANIFEST.json';copy=OLD/'publication_operations_preparation/MANIFEST.json'
    if sha(path.read_bytes())!=OLD_SHA or copy.read_bytes()!=path.read_bytes():raise RuntimeError('Historical seal changed')
    if (OLD/'publication_operations_preparation/MANIFEST.sha256').read_bytes()!=(AUDIT/'publication_operations_preparation/MANIFEST.sha256').read_bytes():raise RuntimeError('Historical checksum changed')
    value=json.loads(copy.read_text())
    if len(value['files'])!=42 or len(value['immutable_inputs'])!=26:raise RuntimeError('Historical42/26 inventory changed')
    for e in value['files']+value['immutable_inputs']:
        check_entry(OLD,e)
        if e['path'] not in HELPERS:check_entry(AUDIT,e)
    for root in [AUDIT,OLD]:
        if sha((root/'ROOT_PREPUBLICATION_LEAD_RECONCILIATION.json').read_bytes())!=LEAD_SHA:raise RuntimeError('Root lead reconciliation changed')
    return value

def selection():
    preserved();all_paths=list(HERE.rglob('*'))
    if any(p.is_symlink() for p in all_paths):raise RuntimeError('Symlink in repair inventory')
    excluded={HERE/'MANIFEST.json',HERE/'MANIFEST.sha256'}
    paths=[AUDIT/n for n in HELPERS]+[p for p in all_paths if p.is_file() and p not in excluded and '__pycache__' not in p.parts]
    if len(paths)!=len(set(paths)):raise RuntimeError('Duplicate repair path')
    return sorted(paths)

def entry(p):
    data=p.read_bytes();return {'path':p.relative_to(AUDIT).as_posix(),'bytes':len(data),'sha256':sha(data)}

def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--verify',action='store_true');args=parser.parse_args()
    path=HERE/'MANIFEST.json';checksum=HERE/'MANIFEST.sha256';paths=selection()
    if args.verify:
        data=path.read_bytes();value=json.loads(data)
        if checksum.read_text()!=sha(data)+'  MANIFEST.json\n':raise RuntimeError('Repair checksum differs')
        if {e['path'] for e in value['files']}!={p.relative_to(AUDIT).as_posix() for p in paths}:raise RuntimeError('Repair inventory differs')
        for e in value['files']:check_entry(AUDIT,e)
        print(json.dumps({'verified':True,'artifacts':len(value['files']),'manifest_sha256':sha(data),'historical42_plus26_reconstructed':True,'publication_ready':False}));return
    if path.exists() or checksum.exists():raise RuntimeError('Preserve this checkpoint before any intentional new seal')
    value={'schema':1,'timestamp_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'pr':399,'problem_id':'30001179','completion_estimate_percent':100,'publication_ready':False,
        'scope':'Local repair and offline evidence only, pending NEW complete independent package03 and affirmative root clearance; no publication authorization or live outcome.',
        'historical_preparation_manifest_sha256':OLD_SHA,'historical42_plus26_reconstructed':True,'root_lead_reconciliation_sha256':LEAD_SHA,
        'review02_repair_required_seal_sha256':'87ccb1871311c3090953d304faed6e19819d1c40fd5be1ef21713380ba3cb3a1','current_controls_per_mode':530,'files':[entry(p) for p in paths]}
    data=(json.dumps(value,indent=2)+'\n').encode();path.write_bytes(data);checksum.write_text(sha(data)+'  MANIFEST.json\n')
    print(json.dumps({'artifacts':len(value['files']),'manifest_sha256':sha(data)}))
if __name__=='__main__':main()
