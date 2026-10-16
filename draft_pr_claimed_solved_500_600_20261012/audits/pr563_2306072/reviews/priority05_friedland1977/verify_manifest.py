from pathlib import Path
import hashlib,json
B=Path(__file__).resolve().parent
m=json.loads((B/'MANIFEST.json').read_text());checks=[]
for n,ex in m['files'].items():
 p=B/n;d=p.read_bytes();ok=len(d)==ex['bytes'] and hashlib.sha256(d).hexdigest()==ex['sha256'];assert ok,n;checks.append({'file':n,'passed':ok})
assert {p.name for p in B.iterdir() if p.is_file()}-{'MANIFEST.json','MANIFEST_CHECKS.json'}==set(m['files'])
s=json.loads((B/'SOURCE.json').read_text());p=Path(s['pdf']['path']);assert p.stat().st_size==s['pdf']['bytes'] and hashlib.sha256(p.read_bytes()).hexdigest()==s['pdf']['sha256']
r={'status':'PASS','count':len(checks),'checks':checks,'original_source_sha256_recheck':True};(B/'MANIFEST_CHECKS.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r,indent=2))
