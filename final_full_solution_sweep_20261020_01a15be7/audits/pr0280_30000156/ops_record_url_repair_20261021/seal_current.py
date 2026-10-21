#!/usr/bin/env python3
"""Seal/verify local PR280 record-URL repair and preserved historical bindings."""
import argparse
import datetime as dt
import hashlib
import json
from pathlib import Path
import finalize_evidence as F
HERE=Path(__file__).resolve().parent
AUDIT=HERE.parent


def sha(data):return hashlib.sha256(data).hexdigest()
def check_inputs():
    original=json.loads((HERE/'INPUT_PRESERVATION.json').read_text())
    F.verify(F.FROZEN,original['files'])
    F.verify(F.FROZEN,json.loads((HERE/'SUPPLEMENTAL_PRESERVATION.json').read_text())['files'])
    old=AUDIT/'ops_doi_identity_repair_20261021/MANIFEST.json'
    if sha(old.read_bytes())!=F.OLD:raise RuntimeError('Historical122 manifest changed')
    F.verify(F.FROZEN,json.loads(old.read_text())['files'])
    for e in original['files']:
        if e['path'] not in F.CHANGED:F.verify(AUDIT,[e])
    F.verify(AUDIT,json.loads((HERE/'CURRENT_HELPER_BINDING.json').read_text())['files'])
    for path,expected in [('ops_repair_20261021/MANIFEST.json','96702c6f1b8981817fa4b8ae2b6201fab36f4518418274f7b584de924918c8de'),
                          ('publication_operations_preparation/MANIFEST.json','999852717308827d82c11825f1ccb727be39da786fa5a1f34a6dde229c26c6e5')]:
        if sha((AUDIT/path).read_bytes())!=expected:raise RuntimeError('Earlier historical manifest changed')
    if json.loads((AUDIT/'ROOT_PUBLICATION_CLEARANCE.json').read_text())['publication_ready'] is not False:
        raise RuntimeError('Root clearance must remain suspended')
    snapshot=json.loads((AUDIT/'SOURCE_SNAPSHOT.json').read_text())
    for e in snapshot['files']:
        b=(AUDIT/e['snapshot']).read_bytes()
        if len(b)!=e['bytes'] or sha(b)!=e['sha256']:raise RuntimeError('Original17 changed')
    state=F.REPO/'.zenodo-state'
    if any(p.is_symlink() for p in state.rglob('*')):raise RuntimeError('Unexpected state symlink')
    inventory=[F.entry(p,F.REPO) for p in sorted(p for p in state.rglob('*') if p.is_file())]
    before=json.loads((HERE/'STATE_BEFORE.json').read_text())
    if len(inventory)!=before['files'] or sha(json.dumps(inventory,sort_keys=True,separators=(',',':')).encode())!=before['inventory_sha256']:
        raise RuntimeError('Local state inventory changed')


def selection():
    check_inputs()
    excluded={HERE/'MANIFEST.json',HERE/'MANIFEST.sha256'}
    paths=[p for p in HERE.rglob('*') if p.is_file() and p not in excluded]
    if any('__pycache__' in p.parts for p in paths):raise RuntimeError('Unexpected generated cache must be reviewed')
    paths += [AUDIT/n for n in F.HELPERS]
    paths += [AUDIT/e['path'] for e in json.loads((HERE/'INPUT_PRESERVATION.json').read_text())['files'] if e['path'] not in F.HELPERS]
    review=AUDIT/'reviews/package_adversary_04'
    paths += [review/e['path'] for e in json.loads((review/'AUTHORED_FILE_MANIFEST.json').read_text())['files']]
    paths += list(review.glob('AUTHORED_FILE_MANIFEST.*'))
    paths += [AUDIT/'ops_repair_20261021/MANIFEST.json',AUDIT/'publication_operations_preparation/MANIFEST.json']
    if any(p.is_symlink() for p in paths):raise RuntimeError('Unsafe seal path')
    return sorted(set(paths))


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--verify',action='store_true');args=parser.parse_args()
    paths=selection();manifest=HERE/'MANIFEST.json';checksum=HERE/'MANIFEST.sha256'
    if args.verify:
        value=json.loads(manifest.read_text())
        if checksum.read_text().split()[0]!=sha(manifest.read_bytes()):raise RuntimeError('Manifest seal changed')
        if {p.relative_to(AUDIT).as_posix() for p in paths}!={e['path'] for e in value['files']}:raise RuntimeError('Repair inventory changed')
        F.verify(AUDIT,value['files'])
        print(json.dumps({'verified':True,'artifacts':len(value['files']),'manifest_sha256':sha(manifest.read_bytes()),
              'old122_reconstructed':True,'old44_and16_manifests_unchanged':True,'publication_ready':False,'provider_actions':0}))
        return
    if manifest.exists() or checksum.exists():raise RuntimeError('Existing seal is immutable; do not silently rewrite')
    value={'timestamp':dt.datetime.now(dt.timezone.utc).isoformat(),'pr':280,'completion_estimate_percent':100,
           'publication_ready':False,'pending':'NEW COMPLETE history-free whole-package reviewer05 and root decision',
           'scope':'Local record URL operational repair only; no provider/Git/lifecycle actions or scientific promotion',
           'previous122_manifest_sha256':F.OLD,'current_controls_per_mode':1704,'frozen_old_counterexamples_per_mode':32,
           'files':[F.entry(p,AUDIT) for p in paths]}
    manifest.write_text(json.dumps(value,indent=2)+'\n');checksum.write_text(sha(manifest.read_bytes())+'  MANIFEST.json\n')
    print(json.dumps({'artifacts':len(value['files']),'manifest_sha256':sha(manifest.read_bytes()),'publication_ready':False}))


if __name__=='__main__':main()
