import datetime,gzip,hashlib,json,os
from pathlib import Path
P=Path('/Users/alec/Documents/Math/draft_pr_descending_audit_20261002')
S=P/'audits/pr374_30005116/clean_final_adversary/private'
journal=P/'ROOT_COMPLETED_PRIVATE_GZIP_20261003.jsonl'
assert S.is_dir()
files=sorted((p for p in S.rglob('*') if p.is_file() and p.suffix in ('.stdout','.stderr') and p.stat().st_size>1000000),key=lambda p:-p.stat().st_size)
done=[]
def sha(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(1048576),b''):h.update(b)
 return h.hexdigest()
def log(o):
 with journal.open('a') as f:f.write(json.dumps(o,sort_keys=True)+'\n');f.flush();os.fsync(f.fileno())
for p in files:
 dst=p.with_name(p.name+'.storage_gzip_20261003.gz')
 assert not dst.exists()
 stat=p.stat();rawsha=sha(p)
 with p.open('rb') as fi,dst.open('xb') as fo:
  with gzip.GzipFile(fileobj=fo,mode='wb',mtime=0) as gz:
   for b in iter(lambda:fi.read(1048576),b''):gz.write(b)
  fo.flush();os.fsync(fo.fileno())
 h=hashlib.sha256();n=0
 with gzip.open(dst,'rb') as f:
  for b in iter(lambda:f.read(1048576),b''):h.update(b);n+=len(b)
 assert n==stat.st_size and h.hexdigest()==rawsha and sha(p)==rawsha
 row={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'source_path':str(p.relative_to(P)),'compressed_path':str(dst.relative_to(P)),'source_bytes':n,'source_sha256':rawsha,'compressed_bytes':dst.stat().st_size,'compressed_sha256':sha(dst),'state':'PREPARED_VERIFIED_LOSSLESS','restore':'gzip -dc compressed_path > source_path','scope':'Completed PR374 own-private full command stream; immutable public bindings untouched'}
 log(row);p.unlink();row['state']='ORIGINAL_REPLACED_WITH_VERIFIED_LOSSLESS_GZIP';log(row);done.append(row)
print(json.dumps({'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'streams':len(done),'source_bytes':sum(r['source_bytes'] for r in done),'gzip_bytes':sum(r['compressed_bytes'] for r in done),'journal':str(journal),'public_bindings_changed':0}))
