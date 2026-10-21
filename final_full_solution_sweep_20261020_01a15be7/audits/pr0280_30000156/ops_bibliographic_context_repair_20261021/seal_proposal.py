#!/usr/bin/env python3
"""Seal local proposal without authorizing/installing a canonical helper change."""
import argparse
import datetime as dt
import json
from pathlib import Path
import build_checkpoint as C
HERE=Path(__file__).resolve().parent
AUDIT=HERE.parent


def selection():
    C.check_inputs()
    binding=C.load('PROPOSED_HELPER_BINDING.json')
    C.verify(AUDIT,binding['canonical_current']);C.verify(C.PROPOSED,binding['proposed'])
    excluded={HERE/'PROPOSAL_MANIFEST.json',HERE/'PROPOSAL_MANIFEST.sha256'}
    paths=[p for p in HERE.rglob('*') if p.is_file() and p not in excluded]
    C.check(not any(p.is_symlink() or '__pycache__' in p.parts for p in paths),'Unsafe/generated proposal artifact')
    paths += [AUDIT/n for n in C.HELPERS]
    paths += [AUDIT/'ops_record_url_repair_20261021/MANIFEST.json',AUDIT/'ops_record_url_repair_20261021/MANIFEST.sha256',
              AUDIT/'ROOT_ACTUAL_LEDGER_ROUTE_COMPATIBILITY.json']
    C.check((AUDIT/'ROOT_ACTUAL_LEDGER_ROUTE_COMPATIBILITY.json').read_bytes()==(HERE/'ROOT_COMPATIBILITY_INPUT.json').read_bytes(),'Compatibility root input changed')
    C.check(len(paths)==len(set(paths)),'Duplicate proposal seal path')
    return sorted(paths)


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--verify',action='store_true');args=parser.parse_args()
    paths=selection();manifest=HERE/'PROPOSAL_MANIFEST.json';checksum=HERE/'PROPOSAL_MANIFEST.sha256'
    if args.verify:
        value=json.loads(manifest.read_text())
        C.check(checksum.read_text().split()[0]==C.sha(manifest.read_bytes()),'Proposal manifest checksum changed')
        C.check({p.relative_to(AUDIT).as_posix() for p in paths}=={e['path'] for e in value['files']},'Proposal inventory changed')
        C.verify(AUDIT,value['files'])
        print(json.dumps({'verified':True,'artifacts':len(value['files']),'manifest_sha256':C.sha(manifest.read_bytes()),
              'canonical390_unchanged':True,'preserved392_verified':True,'proposal_only':True,'publication_ready':False}))
        return
    C.check(not manifest.exists() and not checksum.exists(),'Existing proposal seal is immutable')
    value={'schema':1,'timestamp':dt.datetime.now(dt.timezone.utc).isoformat(),'pr':280,'proposal_only':True,
           'publication_ready':False,'completion_estimate_percent':100,'canonical_installation_authorized':False,
           'pending':'Explicit root authorization after complete sealed review05; consistent canonical evidence and NEW complete reviewer06',
           'old390_manifest_sha256':C.OLD,'current_controls_per_mode':2971,
           'files':[{'path':p.relative_to(AUDIT).as_posix(),'bytes':p.stat().st_size,'sha256':C.sha(p.read_bytes())} for p in paths]}
    manifest.write_text(json.dumps(value,indent=2)+'\n');checksum.write_text(C.sha(manifest.read_bytes())+'  PROPOSAL_MANIFEST.json\n')
    print(json.dumps({'artifacts':len(value['files']),'manifest_sha256':C.sha(manifest.read_bytes()),'proposal_only':True,'publication_ready':False}))


if __name__=='__main__':main()
