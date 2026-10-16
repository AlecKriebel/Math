from pathlib import Path, PurePosixPath
import hashlib,json,zipfile,datetime,stat
B=Path('/Users/alec/Documents/Math/draft_pr_descending_audit_20261002/audits/pr209_5100015/preprint')
O=B.parent/'whole_package_adversary_01'
def sha(b):return hashlib.sha256(b).hexdigest()
def rec(p):
 b=p.read_bytes();return {'path':str(p.relative_to(B)),'bytes':len(b),'sha256':sha(b),'is_symlink':p.is_symlink()}
s=json.loads((B/'SOURCE_MANIFEST.json').read_text()); files=[]
for f in s['files']:
 r=rec(B/f['path']);r['declared_match']=r['bytes']==f['bytes'] and r['sha256']==f['sha256'];files.append(r)
core=[rec(B/p) for p in ['SOURCE_MANIFEST.json','PACKAGE_MANIFEST.json','manuscript.tex','manuscript.pdf','metadata.json','deposit.json','k303b-source-verification.zip']]
with zipfile.ZipFile(B/'k303b-source-verification.zip') as z:
 entries=[]
 for i in z.infolist():
  d=z.read(i);p=PurePosixPath(i.filename);entries.append({'path':i.filename,'bytes':len(d),'sha256':sha(d),'crc':i.CRC,'safe':not p.is_absolute() and '..' not in p.parts and not stat.S_ISLNK(i.external_attr>>16),'matches_disk':not i.is_dir() and (B/i.filename).exists() and d==(B/i.filename).read_bytes()})
 data={'frozen_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'candidate':str(B),'core':core,'source_manifest_actual_entries':files,'zip_entries':entries,'zip_duplicate_names':len(entries)!=len({i['path'] for i in entries}),'zip_membership_equals_source_plus_manifest':{i['path'] for i in entries}=={i['path'] for i in files}|{'SOURCE_MANIFEST.json'},'source_matches':all(r['declared_match'] for r in files),'zip_matches':all(r['matches_disk'] for r in entries),'zip_safe':all(r['safe'] for r in entries)}
(O/'FROZEN_BYTES.json').write_text(json.dumps(data,indent=2)+'\n')
print(json.dumps({k:v for k,v in data.items() if k not in ['source_manifest_actual_entries','zip_entries']},indent=2))
