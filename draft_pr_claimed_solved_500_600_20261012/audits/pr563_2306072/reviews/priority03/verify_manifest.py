from pathlib import Path
import hashlib,json
B=Path(__file__).resolve().parent
m=json.loads((B/'MANIFEST.json').read_text()); checks=[]
for n,expected in m['files'].items():
 p=B/n; data=p.read_bytes(); ok=len(data)==expected['bytes'] and hashlib.sha256(data).hexdigest()==expected['sha256']; checks.append({'file':n,'passed':ok}); assert ok,n
assert {p.name for p in B.iterdir() if p.is_file()}-{ 'MANIFEST.json','MANIFEST_CHECKS.json'}==set(m['files'])
result={'status':'PASS','count':len(checks),'checks':checks}; (B/'MANIFEST_CHECKS.json').write_text(json.dumps(result,indent=2)+'\n'); print(json.dumps(result,indent=2))
