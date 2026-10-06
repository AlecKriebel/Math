"""Authenticate completed independent review artifacts without changing them."""
from pathlib import Path
import json,hashlib,datetime,os
A=Path(__file__).resolve().parent
families=['geometry_source_adversary_20261006','period_identity_adversary_20261006','independent_reproduction_20261006']
records=[]
def require(ok,message):
    if not ok:raise RuntimeError(message)
for name in families:
    folder=A/name;manifest=folder/'MANIFEST.json';data=json.loads(manifest.read_text())
    require((folder/'REPORT.md').is_file() and (folder/'VERDICT.json').is_file(),'family incomplete: '+name)
    pins=data['inputs']+data['outputs']
    for row in pins:
        p=Path(row['path']);p=(p if p.is_absolute() else folder/p).resolve()
        require(p.is_relative_to(A) and p.is_file() and not p.is_symlink(),'input/output scope')
        body=p.read_bytes()
        require(len(body)==row['bytes'] and hashlib.sha256(body).hexdigest()==row['sha256'],'pin mismatch '+str(p))
    records.append({'family':name,'manifest_sha256':hashlib.sha256(manifest.read_bytes()).hexdigest(),
                    'verified_pins':len(pins),'verdict':json.loads((folder/'VERDICT.json').read_text()),
                    'report_sha256':hashlib.sha256((folder/'REPORT.md').read_bytes()).hexdigest()})
result={'UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'actual_reader_PID':os.getpid(),
 'status':'ALL_THREE_REVIEW_MANIFESTS_AUTHENTICATED','records':records,
 'mathematical_adjudication_separate':True,'priority_clearance':False,'publication_clearance':False,
 'original_budget':'1/5','new_central_proof_search_turns':0}
(A/'ROOT_MATH_FAMILY_AUTHENTICATION_20261006.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
print(json.dumps({k:v for k,v in result.items() if k!='records'}))
