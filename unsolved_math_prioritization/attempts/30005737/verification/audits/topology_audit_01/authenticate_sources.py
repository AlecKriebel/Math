import json,hashlib,pathlib,sys
base=pathlib.Path(sys.argv[1]); m=base/'SOURCE_MANIFEST.json'; b=m.read_bytes()
assert hashlib.sha256(b).hexdigest()=='1d677ef16697e1e294f9f86800c10fe3189270cf2d9771a75d7c4e64954c0d1c'
d=json.loads(b); assert len(d['files'])==18
assert d['original_head']=='401f86e018e8cc5075e37a29bae9350eb9f89c36'
records=[]
for e in d['files']:
 p=base/'source'/e['path']; b=p.read_bytes(); sh=hashlib.sha256(b).hexdigest(); gh=hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
 assert len(b)==e['bytes'] and sh==e['sha256'] and gh==e['git_blob'], e['path']
 records.append({'path':e['path'],'bytes':len(b),'sha256':sh,'git_blob':gh,'pass':True})
p=base/'private_native'/'canonical_pair.json'; b=p.read_bytes()
assert len(b)==3524 and hashlib.sha256(b).hexdigest()=='b27d5dbb0f92c0ab330bf44891ec4467f7d8c593cef610196cbd82d4cc6d5298'
print(json.dumps({'manifest_sha256':hashlib.sha256(m.read_bytes()).hexdigest(),'source_files_verified':records,'canonical_pair_sha256':hashlib.sha256(b).hexdigest(),'result':'PASS'},indent=2))
