"""Own completed ZIP custody dedup; exact original ZIP reconstruction before retirement."""
from pathlib import Path
import zipfile,json,hashlib,io,gzip,stat,os,sys
def need(v,m):
 if not v:raise RuntimeError(m)
need(sys.flags.optimize==0 and __debug__,"Custody cleanup supports optimize0 only")
ROOT=Path(__file__).resolve().parent;PRIVATE=ROOT/'private';STORE=PRIVATE/'chunks08.zip'
def sha(b):return hashlib.sha256(b).hexdigest()
def zi_dict(i):return {k:getattr(i,k) for k in ['filename','date_time','compress_type','comment','extra','create_system','create_version','extract_version','reserved','flag_bits','volume','internal_attr','external_attr']}
def zi(d):
 d=dict(d);d['date_time']=tuple(d['date_time']);d['comment']=bytes.fromhex(d['comment']);d['extra']=bytes.fromhex(d['extra']);i=zipfile.ZipInfo(d.pop('filename'),d.pop('date_time'))
 for k,v in d.items():setattr(i,k,v)
 return i
def compact():
 present=set()
 if STORE.exists():
  with zipfile.ZipFile(STORE) as z:present=set(z.namelist())
 for path in sorted(PRIVATE.glob('case_archives*/*.zip')):
  if (path.with_suffix('.custody.json.gz')).exists():continue
  raw=path.read_bytes();s=path.stat();entries=[]
  with zipfile.ZipFile(io.BytesIO(raw)) as z,zipfile.ZipFile(STORE,'a',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as dest:
   for info in z.infolist():
    body=z.read(info.filename);keys=[]
    for offset in range(0,len(body),16384):
     part=body[offset:offset+16384];key=sha(part);keys.append(key)
     if key not in present:dest.writestr(key,part);present.add(key)
    d=zi_dict(info);d['date_time']=list(d['date_time']);d['comment']=d['comment'].hex();d['extra']=d['extra'].hex()
    entries.append({'zipinfo':d,'bytes':len(body),'sha256':sha(body),'chunks':keys})
   comment=z.comment.hex()
  index={'original_file':path.name,'original_bytes':len(raw),'original_sha256':sha(raw),'mode':stat.S_IMODE(s.st_mode),'mtime_ns':s.st_mtime_ns,'comment':comment,'entries':entries,'chunk_store':'../chunks08.zip','compression_level':9}
  # Reconstruct exact container, including order and all ZIP metadata, from new custody.
  out=io.BytesIO()
  with zipfile.ZipFile(STORE) as src,zipfile.ZipFile(out,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as dest:
   dest.comment=bytes.fromhex(index['comment'])
   for e in entries:
    body=b''.join(src.read(k) for k in e['chunks']);need(sha(body)==e['sha256'] and len(body)==e['bytes'],'Exact chunk readback failed');dest.writestr(zi(e['zipinfo']),body,compresslevel=9)
  if out.getvalue()!=raw:raise RuntimeError('Exact ZIP reconstruction mismatch')
  receipt=path.with_suffix('.custody.json.gz');receipt.write_bytes(gzip.compress((json.dumps(index,sort_keys=True,indent=2)+'\n').encode(),mtime=0))
  need(json.loads(gzip.decompress(receipt.read_bytes()))==index,'Receipt readback failed')
  need(path.read_bytes()==raw and path.stat().st_mtime_ns==index['mtime_ns'],'Original archive changed')
  path.unlink();print('Exact compacted',path.name,flush=True)
if __name__=='__main__':compact()
