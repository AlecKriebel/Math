from pathlib import Path
from datetime import datetime,timezone
from urllib.request import Request,urlopen
from concurrent.futures import ThreadPoolExecutor,as_completed
import hashlib,json,tarfile
R=Path(__file__).resolve().parent
D=R.parents[1]/'sources/related-record-22064121'
rec=json.loads((D/'record.json').read_text())
(D/'.gitignore').write_text('*.pdf\n*.tar.gz\n*.part\npublished-source/\n')
def fetch(item):
 name=item['key'];assert Path(name).name==name
 url=item['links']['self']; errors=[]
 for attempt in range(3):
  try:
   tmp=D/(name+'.part');s=hashlib.sha256();m=hashlib.md5();n=0
   started=datetime.now(timezone.utc).isoformat()
   with urlopen(Request(url,headers={'User-Agent':'Independent research source verification'}),timeout=45) as response,tmp.open('wb') as out:
    while True:
     b=response.read(1024*1024)
     if not b:break
     n+=len(b); assert n<=item['size'];out.write(b);s.update(b);m.update(b)
   assert n==item['size'] and 'md5:'+m.hexdigest()==item['checksum']
   tmp.replace(D/name)
   return {'name':name,'url':url,'retrieved_utc':started,'bytes':n,'md5':m.hexdigest(),'sha256':s.hexdigest(),'zenodo_checksum':item['checksum'],'integrity':'PASS','attempts':attempt+1,'prior_errors':errors}
  except Exception as e:errors.append(type(e).__name__+': '+str(e))
 raise RuntimeError(name+': '+repr(errors))
rows=[]
with ThreadPoolExecutor(max_workers=4) as pool:
 for fut in as_completed([pool.submit(fetch,x) for x in rec['files']]):
  row=fut.result();rows.append(row);print('Received',row['name'],row['bytes'],flush=True)
rows.sort(key=lambda x:x['name'])
r={'record_id':'22064121','selected_paper_record':'22089373','completed_utc':datetime.now(timezone.utc).isoformat(),'completion_percent':100,'record_sha256':hashlib.sha256((D/'record.json').read_bytes()).hexdigest(),'complete':len(rows)==len(rec['files']),'files':rows,'historical_log_summary_bodies_read':False}
(D/'receipt.json').write_text(json.dumps(r,indent=2)+'\n')
archive=D/'stc_jc_sharp_boundary_atlas_certificates_v1.1.7.tar.gz'
assert hashlib.sha256(archive.read_bytes()).hexdigest()=='ffcce5398c8be387d6d808620fc939490f31ac41fb48592e22608cf0e7b05db4'
with tarfile.open(archive,'r:gz') as t:
 members=t.getmembers(); total=sum(x.size for x in members if x.isfile())
 for x in members:
  assert not Path(x.name).is_absolute() and '..' not in Path(x.name).parts
  assert x.isfile() or x.isdir(),x.name
 inv={'generated_utc':datetime.now(timezone.utc).isoformat(),'completion_percent':100,'archive_sha256':'ffcce5398c8be387d6d808620fc939490f31ac41fb48592e22608cf0e7b05db4','members':len(members),'regular_files':sum(x.isfile() for x in members),'expanded_bytes':total,'all_regular_or_directory':True,'names':[x.name for x in members]}
 (D/'archive-inventory.json').write_text(json.dumps(inv,indent=2)+'\n')
 print(json.dumps({k:v for k,v in inv.items() if k!='names'},indent=2),flush=True)
