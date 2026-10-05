"""Losslessly compress completed own private PR370/372 captures only."""
from pathlib import Path
from datetime import datetime,timezone
import gzip,hashlib,json,os,subprocess
P=Path(__file__).resolve().parent;R=P.parent;folders=[P/'audits/pr370_30004811/clean_final_adversary/final_live/private',P/'audits/pr372_9700034/clean_final_adversary/private_live',P/'audits/pr372_9700034/clean_final_adversary/private_api']
j=P/'ROOT_COMPLETED_PRIVATE_GZIP_20261003_1738.jsonl';rows=[]
tracked=set(subprocess.check_output(['git','ls-files','-z','--',*[str(x.relative_to(R)) for x in folders]],cwd=R).split(b'\0'))
sha=lambda b:hashlib.sha256(b).hexdigest()
for d in folders:
 for p in sorted(d.rglob('*')):
  if not p.is_file() or p.is_symlink() or p.suffix=='.gz' or p.stat().st_size<1000000:continue
  assert str(p.relative_to(R)).encode() not in tracked
  b=p.read_bytes();z=p.with_name(p.name+'.storage.gz')
  assert not z.exists();compressed=gzip.compress(b,mtime=0)
  if len(compressed)>=len(b):continue
  z.write_bytes(compressed);assert gzip.decompress(z.read_bytes())==b
  row={'utc':datetime.now(timezone.utc).isoformat(),'original_path':str(p.relative_to(P)),'original_bytes':len(b),'original_sha256':sha(b),'gzip_path':str(z.relative_to(P)),'gzip_bytes':len(compressed),'gzip_sha256':sha(compressed),'restore':'gzip.decompress preserves exact original bytes before executing any historical checker requiring raw private paths','state':'PREPARED_VERIFIED'}
  with j.open('a') as f:f.write(json.dumps(row,sort_keys=True)+'\n');f.flush();os.fsync(f.fileno())
  p.unlink();row['state']='COMPLETE_EXACT_BYTES_PRESERVED'
  with j.open('a') as f:f.write(json.dumps(row,sort_keys=True)+'\n');f.flush();os.fsync(f.fileno())
  rows.append(row)
summary={'utc':datetime.now(timezone.utc).isoformat(),'scope':'Only completed own PR370/372 private captures; no active audit, public artifact, source, global index, or foreign data altered','files':len(rows),'uncompressed_bytes':sum(x['original_bytes'] for x in rows),'compressed_bytes':sum(x['gzip_bytes'] for x in rows),'all_full_private_streams_preserved':True,'journal':str(j.relative_to(P))}
(P/'ROOT_COMPLETED_PRIVATE_GZIP_20261003_1738.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps(summary))

