from pathlib import Path
import json,hashlib,sys
root=Path(__file__).resolve().parent
manifest=Path(sys.argv[1]) if len(sys.argv)>1 else root/'FAMILY_MANIFEST.json'
m=json.loads(manifest.read_text());expected=m['files'];listed=[x['path'] for x in expected]
actual={str(p.relative_to(root)) for p in root.rglob('*') if p.is_file() and 'ignoredtmp' not in p.relative_to(root).parts and p.name!='FAMILY_MANIFEST.json'}
assert m['excluded']==['FAMILY_MANIFEST.json','ignoredtmp/**'],'strict exclusions'
assert len(listed)==len(set(listed)),'duplicate manifest paths'
assert set(listed)==actual,'complete authored path coverage'
for x in expected:
 p=root/x['path'];assert p.is_file() and not p.is_symlink(),'file safety'
 b=p.read_bytes();assert len(b)==x['bytes'],'exact bytes '+x['path']
 assert hashlib.sha256(b).hexdigest()==x['sha256'],'exact SHA256 '+x['path']
print(json.dumps({'status':'PASS','file_count':len(listed),'bytes':sum(x['bytes'] for x in expected),'strict_self_exclusion':True,'only_other_exclusion':'ignoredtmp/**','manifest_sha256':hashlib.sha256(manifest.read_bytes()).hexdigest()},indent=2))
