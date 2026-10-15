#!/usr/bin/env python3
"""Read-only integrity, metadata, copy-custody and optional upload binding check."""
import argparse,hashlib,json,zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def require(ok,message):
    if not ok:raise RuntimeError(message)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def safe_path(root,name):
    p=root/name
    require(not p.is_symlink() and p.resolve().is_relative_to(root.resolve()),'Unsafe member: '+name)
    return p
def verify(root=ROOT,bindings=None,archive=None,require_bindings=False):
    manifest=json.loads((root/'PACKAGE_MANIFEST.json').read_text());members=manifest['members']
    require(len({r['path'] for r in members})==len(members),'Duplicate manifest members.')
    require('PACKAGE_MANIFEST.json' not in {r['path'] for r in members},'Circular manifest hash.')
    for r in members:
        p=safe_path(root,r['path']);require(p.is_file(),'Missing member: '+r['path'])
        require(p.stat().st_size==r['bytes'] and sha(p)==r['sha256'],'Member mismatch: '+r['path'])
    metadata=json.loads((root/'metadata.json').read_text())
    require(metadata==json.loads((root/'metadata_wrapped.json').read_text())['metadata']==json.loads((root/'deposit.json').read_text())['metadata'],'Three metadata objects differ.')
    require(metadata['title']=='A localized Gaussian-witness lower bound for fractional iterated area on uniform grids','Title drift.')
    require(metadata['creators'][0]['orcid']=='0009-0001-9320-500X','ORCID drift.')
    require(metadata['license']=='cc-by-4.0' and metadata['publication_type']=='preprint','License/type drift.')
    status=json.loads((root/'STATUS.json').read_text())
    require(status['publication_ready'] is False and status['issues_resolved'] is False,'Preparation prematurely promoted.')
    require(status['fresh_whole_package_reviews_completed']==0 and status['minimum_fresh_reviews_required']==2,'Review state drift.')
    for r in json.loads((root/'INPUT_COPY_MAP.json').read_text())['copies']:
        p=safe_path(root,r['package_copy']);require(sha(p)==r['sha256'] and p.stat().st_size==r['bytes'],'Custody copy mismatch: '+r['package_copy'])
    selected=bindings if bindings is not None else root/'UPLOAD_BINDINGS.json'
    checked=False
    if selected.exists():
        b=json.loads(selected.read_text());pdf=root/b['pdf']['filename'];require(pdf.is_file() and sha(pdf)==b['pdf']['sha256'] and pdf.stat().st_size==b['pdf']['bytes'],'Upload PDF binding mismatch.')
        ap=archive if archive is not None else selected.parent/b['archive']['filename'];require(ap.is_file(),'Present bindings require a readable archive.')
        require(sha(ap)==b['archive']['sha256'] and ap.stat().st_size==b['archive']['bytes'],'Upload ZIP binding mismatch.')
        expected=sorted([r['path'] for r in members]+['PACKAGE_MANIFEST.json'])
        with zipfile.ZipFile(ap) as z:
            require(z.namelist()==expected,'Archive member/order mismatch.')
            for name in expected:require(z.read(name)==safe_path(root,name).read_bytes(),'Archive bytes mismatch: '+name)
            for i in z.infolist():
                require(i.compress_type==zipfile.ZIP_STORED and i.date_time==(2026,10,14,0,0,0) and i.external_attr==(0o100644<<16),'Archive determinism attributes differ.')
        require(b['manifest_sha256']==sha(root/'PACKAGE_MANIFEST.json'),'Manifest external binding mismatch.');checked=True
    else:require(not require_bindings,'Required bindings are absent.')
    return {'status':'PASS','manifest_members':len(members),'historical_copies':len(json.loads((root/'INPUT_COPY_MAP.json').read_text())['copies']),'metadata_objects_equal':True,'upload_bindings_checked':checked,'verification':'Read-only. Manifest excludes its own hash; archive and PDF bindings live outside the ZIP to avoid self-reference.'}
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--bindings',type=Path);p.add_argument('--archive',type=Path);p.add_argument('--require-bindings',action='store_true');a=p.parse_args()
    print(json.dumps(verify(bindings=a.bindings,archive=a.archive,require_bindings=a.require_bindings),indent=2))
