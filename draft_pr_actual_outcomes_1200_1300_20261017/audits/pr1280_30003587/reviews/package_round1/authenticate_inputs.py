import json,hashlib,datetime,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent; A=HERE.parent.parent
f=HERE/'INPUT_FREEZE.json'; expected='0cd3f59375daf5f054f4bc7557f228a9347ac7cfb4eb2a7b4a962d5d04c413cd'
def require(v,m):
 if not v: raise RuntimeError(m)
require(hashlib.sha256(f.read_bytes()).hexdigest()==expected,'freeze mismatch')
d=json.loads(f.read_text()); checks=[]
for group in ['files','external_readonly_inputs']:
 for e in d[group]:
  p=Path(e['path']);p=p if p.is_absolute() else A/p
  b=p.read_bytes(); require(len(b)==e['bytes'] and hashlib.sha256(b).hexdigest()==e['sha256'],str(p)); checks.append({'path':e['path'],'group':group,'verified':True})
result={'at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'input_freeze_sha256':expected,'file_count':len(d['files']),'external_count':len(d['external_readonly_inputs']),'checks':checks}
(HERE/sys.argv[1]).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k!='checks'}))
