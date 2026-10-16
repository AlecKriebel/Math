"""Bound public review artifacts; ignore all private raw inputs."""
import hashlib,json
from pathlib import Path
root=Path(__file__).parent.parent
files=[]
for p in sorted(root.rglob('*')):
 if not p.is_file():continue
 rel=p.relative_to(root)
 if rel.parts[0]=='raw_sources' or '__pycache__' in rel.parts or p.name=='PUBLIC_MANIFEST.json':continue
 b=p.read_bytes()
 files.append({'path':str(rel),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()})
result={'scope':'Independent thermodynamic audit; scoped PASS, original unresolved after five substantive turns','frozen_head':'9a92b6a0bd7cff3a8c11bf66ff9338264ab012d1','raw_sources_excluded':True,'files':files}
(root/'PUBLIC_MANIFEST.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
for item in files:
 b=(root/item['path']).read_bytes()
 assert len(b)==item['bytes'] and hashlib.sha256(b).hexdigest()==item['sha256']
print(f'Bound {len(files)} public files; {sum(f["bytes"] for f in files)} bytes; all bindings verified.')
