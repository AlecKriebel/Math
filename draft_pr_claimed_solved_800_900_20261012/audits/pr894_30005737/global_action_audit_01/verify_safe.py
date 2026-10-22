from pathlib import Path
import hashlib,json
out=Path(__file__).resolve().parent
m=json.loads((out/'SAFE_MANIFEST.json').read_text())
assert m['pr']==894 and m['problem_id']=='30005737'
expected=set()
for e in m['files']:
 rel=e['path'];p=Path(rel)
 assert not p.is_absolute() and '..' not in p.parts and 'private_tmp' not in p.parts
 assert rel!='SAFE_MANIFEST.json' and rel not in expected
 expected.add(rel)
 q=out/p
 assert q.is_file() and not q.is_symlink()
 b=q.read_bytes()
 assert len(b)==e['bytes'] and hashlib.sha256(b).hexdigest()==e['sha256'],rel
 forbidden=[chr(47)+'Users'+chr(47),chr(47)+'private'+chr(47),'file'+':'+chr(47)+chr(47)]
 text=b.decode('utf-8')
 for s in forbidden:assert s not in text,(rel,'absolute private path')
actual={p.relative_to(out).as_posix() for p in out.rglob('*') if p.is_file() and 'private_tmp' not in p.relative_to(out).parts and p.name!='SAFE_MANIFEST.json'}
assert actual==expected,{'missing':sorted(actual-expected),'extra':sorted(expected-actual)}
print('PASS all '+str(len(expected))+' public-safe files match bytes and SHA256; manifest excludes itself and private_tmp; no absolute private paths')
