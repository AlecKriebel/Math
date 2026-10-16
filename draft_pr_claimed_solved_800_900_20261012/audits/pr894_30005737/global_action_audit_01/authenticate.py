from pathlib import Path
import hashlib,json
base=Path(__file__).resolve().parent.parent
manifest_bytes=(base/'SOURCE_MANIFEST.json').read_bytes()
expected='1d677ef16697e1e294f9f86800c10fe3189270cf2d9771a75d7c4e64954c0d1c'
assert hashlib.sha256(manifest_bytes).hexdigest()==expected
m=json.loads(manifest_bytes)
assert m['pr']==894 and m['problem_id']=='30005737'
assert m['original_head']=='401f86e018e8cc5075e37a29bae9350eb9f89c36'
assert len(m['files'])==18
for e in m['files']:
 b=(base/'source'/e['path']).read_bytes()
 sha=hashlib.sha256(b).hexdigest()
 blob=hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
 assert len(b)==e['bytes'] and sha==e['sha256'] and blob==e['git_blob'],e['path']
 print('PASS source/'+e['path']+' bytes='+str(len(b))+' sha256='+sha+' git_blob='+blob)
actual={p.relative_to(base/'source').as_posix() for p in (base/'source').rglob('*') if p.is_file()}
assert actual=={e['path'] for e in m['files']}
b=(base/'private_native/canonical_pair.json').read_bytes()
assert len(b)==3524 and hashlib.sha256(b).hexdigest()=='b27d5dbb0f92c0ab330bf44891ec4467f7d8c593cef610196cbd82d4cc6d5298'
n=json.loads(b)
assert len(n)==2 and n[0]['id']==30005737
print('PASS complete native canonical pair bytes=3524 sha256='+hashlib.sha256(b).hexdigest())
print('PASS authenticated all 18 original files, exact external manifest, and complete native statement/background')
