"""Losslessly archive completed own journals; preserve all scientific/native files."""
from pathlib import Path
import gzip,hashlib,json,os,time
from datetime import datetime,timezone
P=Path('/Users/alec/Documents/Math/research_website_catalogue_20261024')
R=P/'verification/mink-riesz-k3-runtime-sol-20261117'
OPS=P/'verification/mink-riesz-k3-root-execution-20261117'
pub=json.loads((OPS/'PUBLISH.stdout.bin').read_bytes())
assert pub['status']=='SCOPED15_COMMIT_AND_PUSH_VERIFIED_SNAPSHOT'
assert pub['commit']=='4cc09d6bbbad61aa11077c5002cf84a1e93b1344'
paths=sorted(R.glob('*/'+'*'+'/journal.jsonl'))
assert len(paths)==2 and all((f.parent/'SUCCESS.json').is_file() for f in paths)
rows=[]
for f in paths:
 assert f.is_file() and not f.is_symlink()
 before=f.stat();h=hashlib.sha256();size=0
 with f.open('rb') as inp:
  for b in iter(lambda:inp.read(1048576),b''):h.update(b);size+=len(b)
 original=h.hexdigest();out=f.with_suffix(f.suffix+'.gz')
 assert not out.exists()
 with out.open('xb') as target:
  with gzip.GzipFile(fileobj=target,mode='wb',filename='',mtime=0,compresslevel=6) as z:
   with f.open('rb') as inp:
    for b in iter(lambda:inp.read(1048576),b''):z.write(b)
  target.flush();os.fsync(target.fileno())
 restored=hashlib.sha256();n=0
 with gzip.open(out,'rb') as z:
  for b in iter(lambda:z.read(1048576),b''):restored.update(b);n+=len(b)
 assert n==size and restored.hexdigest()==original
 after=f.stat();assert (before.st_ino,before.st_size,before.st_mtime_ns)==(after.st_ino,after.st_size,after.st_mtime_ns)
 out.chmod(before.st_mode & 0o777)
 row={'original_path':str(f),'raw_bytes':size,'raw_SHA256':original,'gzip_path':str(out),'gzip_bytes':out.stat().st_size,'gzip_SHA256':hashlib.sha256(out.read_bytes()).hexdigest(),'full_decompression_identity_verified':True,'original_mode':oct(before.st_mode & 0o777)}
 f.unlink();rows.append(row)
result={'UTC':datetime.now(timezone.utc).isoformat(),'decision':'Root environmental disposition: lossless compression of two completed own private journals only; all helper modes are stale and will not be rerun. No scientific source, frozen packet, native index, payload or user document removed. Exact raw streams recoverable from verified gzip.', 'journals':rows,'bytes_saved':sum(x['raw_bytes']-x['gzip_bytes'] for x in rows),'other_files_modified':False}
with (P/'verification/root-three-page-journal-storage-disposition-20261117.json').open('x') as f:json.dump(result,f,indent=2);f.write('\n')
print(json.dumps(result))
