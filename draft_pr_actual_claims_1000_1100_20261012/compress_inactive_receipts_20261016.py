"""Transparent compression of immutable inactive logical files; no bytes retired."""
from pathlib import Path
import os,stat,json,hashlib,subprocess,datetime
B=Path(__file__).resolve().parent
ledger=B/'INACTIVE_RECEIPT_SOURCE_TRANSPARENT_COMPRESSION_SECOND_20261016.json'
def identity(p):return hashlib.sha256(p.read_bytes()).hexdigest()
groups={}
for p in B.rglob('*'):
 if p.is_file() and not p.is_symlink():
  s=p.stat();groups.setdefault((s.st_dev,s.st_ino),[]).append(p)
attempts=json.loads(ledger.read_text())['entries'] if ledger.exists() else []
for aliases in sorted(groups.values(),key=lambda a:(a[0].suffix.lower()=='.html',a[0].stat().st_blocks),reverse=True):
 p=aliases[0];s=p.stat();names=[str(q.relative_to(B)) for q in aliases]
 if s.st_blocks*512<131072 or s.st_size<131072 or len(aliases)!=s.st_nlink:continue
 if any('pr1071_' in n or 'pr1080_' in n or 'preprint_v1_0/' in n or '/publication/' in n or '/submitted/' in n or '/intake/' in n for n in names):continue
 if p.suffix.lower() not in ('.json','.jsonl','.txt','.html'):continue
 if any('/reviews/' not in n and '/finalization/' not in n and '/repairs/' not in n and not n.startswith('DISPOSABLE_') for n in names):continue
 before={'paths':names,'bytes':s.st_size,'sha256':identity(p),'mode':stat.S_IMODE(s.st_mode),'mtime_ns':s.st_mtime_ns,'nlink':s.st_nlink,'allocated_bytes':s.st_blocks*512}
 temp=B/('.compression_second_'+str(s.st_ino))
 try:
  result=subprocess.run(['/usr/bin/ditto','--hfsCompression',str(p),str(temp)],capture_output=True,text=True)
  if result.returncode:raise RuntimeError(result.stderr)
  ns=temp.stat()
  if identity(temp)!=before['sha256'] or ns.st_size!=s.st_size or stat.S_IMODE(ns.st_mode)!=before['mode'] or ns.st_mtime_ns!=s.st_mtime_ns:raise RuntimeError('temporary identity mismatch')
  if ns.st_blocks>=s.st_blocks:
   temp.unlink();continue
  row={'before':before,'after_allocated_bytes':ns.st_blocks*512,'logical_identity_verified':True}
  for q in aliases:
   fresh=q.with_name(q.name+'.transparent_compression_second');os.link(temp,fresh);os.replace(fresh,q)
  temp.unlink()
  for q in aliases:
   t=q.stat()
   if identity(q)!=before['sha256'] or t.st_size!=before['bytes'] or stat.S_IMODE(t.st_mode)!=before['mode'] or t.st_mtime_ns!=before['mtime_ns'] or t.st_nlink!=before['nlink']:raise RuntimeError('post identity mismatch')
  attempts.append(row)
  ledger.write_text(json.dumps({'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'scope':'Only inactive immutable own local receipts or retained source text/HTML. All bytes/modes/mtimes/own hardlink aliases retained. No canonical proof/code/publication assets or active1071/1080 touched.','entries':attempts,'estimated_allocated_reduction':sum(x['before']['allocated_bytes']-x['after_allocated_bytes'] for x in attempts)},indent=2)+'\n')
 except Exception as e:
  if temp.exists():temp.unlink()
  print(json.dumps({'stopped_at':names,'error':str(e),'completed_groups':len(attempts)}));raise
print(json.dumps({'status':'PASS','compressed_inode_groups':len(attempts),'estimated_allocated_reduction':sum(x['before']['allocated_bytes']-x['after_allocated_bytes'] for x in attempts)}))
