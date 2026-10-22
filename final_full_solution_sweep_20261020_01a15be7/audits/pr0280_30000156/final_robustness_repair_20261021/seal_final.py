#!/usr/bin/env python3
"""Final v1.1 repair seal: current binding plus immutable reconstructed history."""
import argparse
import datetime as dt
import json
from pathlib import Path
import build_final_evidence as C
HERE=Path(__file__).resolve().parent;AUDIT=HERE.parent


def selection():
    C.verify_preserved()
    for e in C.load(HERE/'CURRENT_HELPER_BINDING.json')['files']:C.ck(C.matches(AUDIT/e['path'],e),'Current helper changed')
    release=C.load(C.PUB/'RELEASE_FILES.json')
    for e in release['files']:C.ck(C.matches(C.PUB/e['path'],e),'Current payload changed')
    review=AUDIT/'reviews/package_adversary_05';review_entries=C.load(review/'AUTHORED_FILE_MANIFEST.json')['files']
    C.ck(len(review_entries)==33,'Review05 inventory changed')
    for e in review_entries:C.ck(C.matches(review/e['path'],e),'Review05 artifact changed')
    excluded={HERE/'MANIFEST.json',HERE/'MANIFEST.sha256'}
    paths=[p for p in HERE.rglob('*') if p.is_file() and p not in excluded]
    C.ck(not any('__pycache__' in p.parts or p.is_symlink() for p in paths),'Unexpected cache or symlink')
    paths += [AUDIT/n for n in C.HELPERS]
    paths += [C.PUB/'RELEASE_FILES.json']+[C.PUB/e['path'] for e in release['files']]
    paths += [p for p in (AUDIT/'preprint/package_source').rglob('*') if p.is_file()]
    paths += [p for p in C.HISTORY.rglob('*') if p.is_file()]
    paths += [AUDIT/'preprint/main.tex']+[p for p in (AUDIT/'preprint/output').rglob('*') if p.is_file()]
    paths += [AUDIT/'publication_support'/n for n in ['build_package.py','verify.py','check_math.py','expected_checks.json','REPLAY_RECEIPT.json',
              'check_all_odd_primes.py','expected_all_odd_checks.json','ALL_ODD_REPLAY_RECEIPT.json','ROBUSTNESS_SCOPE.md',
              'PACKAGE_README.md','SOURCE_REFERENCES.json','PRIORITY_SCOPE.md']]
    paths += [AUDIT/'SOURCE_SNAPSHOT.json']+[AUDIT/e['snapshot'] for e in C.load(AUDIT/'SOURCE_SNAPSHOT.json')['files']]
    paths += [AUDIT/n for n in ['ROOT_PREPUBLICATION_LEAD_RECONCILIATION.json','ROOT_PUBLICATION_CLEARANCE.json',
              'ROOT_SCOPE_RELEASE_LEAD_REBINDING.json','publication_clearance_history/lead01_pre_scope_extension.json',
              'ROOT_RECORD_URL_FINDING.json','ROOT_ACTUAL_LEDGER_ROUTE_COMPATIBILITY.json',
              'ops_record_url_repair_20261021/MANIFEST.json','ops_record_url_repair_20261021/MANIFEST.sha256',
              'ops_bibliographic_context_repair_20261021/PROPOSAL_MANIFEST.json','ops_bibliographic_context_repair_20261021/PROPOSAL_MANIFEST.sha256']]
    paths += [review/e['path'] for e in review_entries]+[review/'AUTHORED_FILE_MANIFEST.json',review/'AUTHORED_FILE_MANIFEST.sha256']
    C.ck(not any(p.is_symlink() for p in paths),'Unsafe final selection')
    return sorted(set(paths))


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--verify',action='store_true');args=parser.parse_args()
    paths=selection();manifest=HERE/'MANIFEST.json';checksum=HERE/'MANIFEST.sha256'
    if args.verify:
        value=C.load(manifest);C.ck(checksum.read_text().split()[0]==C.sha(manifest.read_bytes()),'Final seal checksum differs')
        C.ck({p.relative_to(AUDIT).as_posix() for p in paths}=={e['path'] for e in value['files']},'Final artifact inventory differs')
        for e in value['files']:C.ck(C.matches(AUDIT/e['path'],e),'Final sealed artifact changed: '+e['path'])
        print(json.dumps({'verified':True,'artifacts':len(value['files']),'manifest_sha256':C.sha(manifest.read_bytes()),
              'historical390_and451_reconstructed':True,'release_sha256':C.RELEASE,'root_lead_sha256':C.LEAD,'publication_ready':False}))
        return
    C.ck(not manifest.exists() and not checksum.exists(),'Existing final seal is immutable; never overwrite')
    value={'schema':1,'timestamp':dt.datetime.now(dt.timezone.utc).isoformat(),'pr':280,'version':'1.1',
           'completion_estimate_percent':100,'publication_ready':False,'pending':'NEW COMPLETE history-free whole-package reviewer06 and root reproduction/decision',
           'release_manifest_sha256':C.RELEASE,'root_lead_sha256':C.LEAD,'operations_per_mode':3134,
           'class3_checks_per_replay':147619,'all_odd_checks_per_replay':46298,'scope':'Complete local canonical mathematical-scope/package/operations repair; no live provider/Git/lifecycle outcome',
           'files':[C.entry(p) for p in paths]}
    manifest.write_text(json.dumps(value,indent=2)+'\n');checksum.write_text(C.sha(manifest.read_bytes())+'  MANIFEST.json\n')
    print(json.dumps({'artifacts':len(value['files']),'manifest_sha256':C.sha(manifest.read_bytes()),'publication_ready':False}))


if __name__=='__main__':main()
