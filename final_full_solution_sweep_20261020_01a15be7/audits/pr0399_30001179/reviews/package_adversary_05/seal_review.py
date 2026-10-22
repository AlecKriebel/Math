#!/usr/bin/env python3
"""Self-excluding authored review seal. Does not grant publication permission."""
import argparse,datetime,hashlib,json,re
from pathlib import Path,PurePosixPath
O=Path(__file__).resolve().parent
sha=lambda b:hashlib.sha256(b).hexdigest()
def require(v,m):
    if not v:raise RuntimeError(m)
def entries():
    result=[]
    for p in sorted(O.rglob('*')):
        require(not p.is_symlink(),'no symlinks')
        if p.is_file() and p.name not in {'AUTHORED_FILE_MANIFEST.json','AUTHORED_FILE_MANIFEST.sha256'}:
            b=p.read_bytes();result.append({'path':p.relative_to(O).as_posix(),'bytes':len(b),'sha256':sha(b)})
    return result
def main():
    parser=argparse.ArgumentParser();parser.add_argument('--verify',action='store_true');a=parser.parse_args();manifest=O/'AUTHORED_FILE_MANIFEST.json';checksum=O/'AUTHORED_FILE_MANIFEST.sha256'
    verdict=json.loads((O/'VERDICT.json').read_bytes());require(verdict['verdict']=='QUALIFIED_CLEAN' and verdict['unresolved_material_findings']==[] and verdict['publication_ready'] is False and verdict['publication_authorized'] is False,'bounded verdict')
    if a.verify:
        b=manifest.read_bytes();v=json.loads(b);require(checksum.read_text()==sha(b)+'  AUTHORED_FILE_MANIFEST.json\n','checksum');require(v['files']==entries(),'exact self-excluding inventory');require(v['publication_ready'] is False and v['completion_estimate_percent']==100,'review scope');print(json.dumps({'verified':True,'authored_artifacts':len(v['files']),'manifest_sha256':sha(b),'publication_ready':False}));return
    require(not manifest.exists() and not checksum.exists(),'never overwrite a frozen seal')
    v={'schema':1,'timestamp_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'pr':399,'problem_id':'30001179','reviewer':'package_adversary_05','completion_estimate_percent':100,'publication_ready':False,'scope':'Complete new independent adversarial review; self-excluding byte seal, not scientific signature or publication permission.','files':entries()};b=(json.dumps(v,indent=2)+'\n').encode()
    with manifest.open('xb') as f:f.write(b)
    with checksum.open('x') as f:f.write(sha(b)+'  AUTHORED_FILE_MANIFEST.json\n')
    print(json.dumps({'authored_artifacts':len(v['files']),'manifest_sha256':sha(b),'publication_ready':False}))
if __name__=='__main__':main()
