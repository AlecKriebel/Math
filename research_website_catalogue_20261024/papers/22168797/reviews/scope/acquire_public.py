from pathlib import Path,PurePosixPath
from datetime import datetime,timezone
import urllib.request,json,hashlib,concurrent.futures,zipfile,stat,os
BASE=Path(__file__).resolve().parents[2];S=BASE/'sources';R=BASE/'reviews/scope'
def stamp():return datetime.now(timezone.utc).isoformat()
def log(msg,pct):
 with (R/'research-log.md').open('a') as f:f.write(f'\n{stamp()} — {pct}%: {msg}\n')
 print(msg,flush=True)
log('Starting fresh public acquisition and independent scope review. No sibling or dedicated historical review opinions consulted.',2)
url='https://zenodo.org/api/records/22168797'
req=urllib.request.Request(url,headers={'User-Agent':'Research inventory validation/1.0'})
raw=urllib.request.urlopen(req,timeout=90).read();(S/'record.json').write_bytes(raw)
rec=json.loads(raw);files=rec['files']
(S/'metadata-receipt.json').write_text(json.dumps({'url':url,'retrieved_utc':stamp(),'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()},indent=2)+'\n')
def fetch(f):
 name=f['key'];target=S/name
 if Path(name).name!=name:raise ValueError('unsafe asset filename')
 u=f['links'].get('self') or f['links']['download']
 req=urllib.request.Request(u,headers={'User-Agent':'Research inventory validation/1.0'})
 h=hashlib.sha256();m=hashlib.md5();n=0
 with urllib.request.urlopen(req,timeout=180) as inp,target.open('wb') as out:
  final=inp.url
  while True:
   chunk=inp.read(1024*1024)
   if not chunk:break
   h.update(chunk);m.update(chunk);n+=len(chunk);out.write(chunk)
 expected=f['checksum'].split(':',1)[-1]
 if n!=f['size'] or m.hexdigest()!=expected:raise ValueError(('integrity mismatch',name,n,m.hexdigest()))
 result={'name':name,'url':u,'resolved_url':final,'retrieved_utc':stamp(),'bytes':n,'sha256':h.hexdigest(),'md5':m.hexdigest(),'zenodo_checksum':f['checksum'],'integrity':'PASS'}
 print('ACQUIRED '+name+' '+str(n)+' bytes '+h.hexdigest(),flush=True)
 return result
small=[f for f in files if f['size']<10_000_000];large=[f for f in files if f['size']>=10_000_000]
results=list(concurrent.futures.ThreadPoolExecutor(4).map(fetch,small))
(S/'partial-receipt.json').write_text(json.dumps({'record_id':'22168797','retrieved_utc':stamp(),'complete':False,'files':results},indent=2)+'\n')
log('All small public assets including both PDFs acquired and size/MD5 checked; large reproducibility archive downloading next.',10)
results+=list(concurrent.futures.ThreadPoolExecutor(2).map(fetch,large))
receipt={'record_id':'22168797','retrieved_utc':stamp(),'record_sha256':hashlib.sha256(raw).hexdigest(),'complete':True,'files':results}
(S/'receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
log('All seven public files freshly downloaded and verified by published size and MD5; SHA256 receipt finalized. Safe extraction starting.',20)
archives=[]
for f in results:
 if not f['name'].endswith('.zip'):continue
 zpath=S/f['name'];dest=S/'published-source'/zpath.stem;dest.mkdir(parents=True,exist_ok=True)
 entries=[]
 with zipfile.ZipFile(zpath) as z:
  infos=z.infolist();total=sum(i.file_size for i in infos)
  if total>3_000_000_000:raise ValueError(('unexpected expanded size',total))
  seen=set()
  for i in infos:
   rel=PurePosixPath(i.filename)
   if rel.is_absolute() or '..' in rel.parts or '\\' in i.filename or i.filename in seen:raise ValueError(('unsafe or duplicate archive path',i.filename))
   seen.add(i.filename)
   mode=(i.external_attr>>16)&0xffff
   if stat.S_ISLNK(mode):raise ValueError(('symlink entry',i.filename))
   target=dest.joinpath(*rel.parts)
   if i.is_dir():target.mkdir(parents=True,exist_ok=True);continue
   target.parent.mkdir(parents=True,exist_ok=True)
   data=z.read(i);target.write_bytes(data)
   entries.append({'path':i.filename,'bytes':len(data),'crc32':f'{i.CRC:08x}','sha256':hashlib.sha256(data).hexdigest()})
 archives.append({'archive':f['name'],'archive_sha256':f['sha256'],'expanded_bytes':total,'files':len(entries),'safe_path_checks':'PASS','crc_read':'PASS','entries':entries})
 print('EXTRACTED '+f['name']+' '+str(len(entries))+' files '+str(total)+' expanded bytes',flush=True)
(S/'extraction-integrity.json').write_text(json.dumps({'verified_utc':stamp(),'archives':archives},indent=2)+'\n')
log('Every ZIP entry safely extracted with traversal/duplicate/symlink checks and CRC read verification; per-file SHA256 inventory saved. No mathematical code executed.',25)
