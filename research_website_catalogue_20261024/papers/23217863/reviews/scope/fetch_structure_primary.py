"""Ordinary public primary requests; all bodies stay in preignored cache."""
from pathlib import Path
from datetime import datetime,timezone
from concurrent.futures import ThreadPoolExecutor,as_completed
import hashlib,json,urllib.request,urllib.error
r=Path(__file__).resolve().parent;c=r/'cache/primary';assert (r/'.gitignore').read_text()=='cache/\n';assert (r/'INITIAL_SEAL.json').is_file()
tasks=[('nelson209.pdf','https://users.math.msu.edu/users/banelson/teaching/209/209_notes.pdf')]

now=lambda:datetime.now(timezone.utc).isoformat()
def fetch(task):
 name,url=task;start=now();error=None
 request=urllib.request.Request(url,headers={'User-Agent':'IndependentResearchSourceCustody/1.0','Accept':'application/pdf,*/*;q=0.5'})
 try:
  with urllib.request.urlopen(request,timeout=35) as response:
   data=response.read(10*1024*1024+1);headers=dict(response.headers.items());status=response.status;final=response.url
 except urllib.error.HTTPError as e:data=e.read(2*1024*1024+1);headers=dict(e.headers.items());status=e.code;final=e.url;error=type(e).__name__
 except Exception as e:return {'name':name,'requested_url':url,'started_utc':start,'completed_utc':now(),'error_type':type(e).__name__,'error':str(e),'body_saved':False}
 pdf=data.startswith(b'%PDF-');path=c/(name if pdf else name+'.response')
 path.write_bytes(data)
 return {'name':name,'requested_url':url,'started_utc':start,'completed_utc':now(),'status':status,'final_url':final,'headers':headers,'path':str(path),'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest(),'PDF_magic':pdf,'error_type':error,'body_saved':True,'body_read_bound_bytes':10*1024*1024+1 if error is None else 2*1024*1024+1}
results=[]
with ThreadPoolExecutor(max_workers=3) as pool:
 for future in as_completed([pool.submit(fetch,x) for x in tasks]):
  item=future.result();results.append(item)
  (r/'structure-primary-fetch-receipts.json').write_text(json.dumps({'utc':now(),'cache_rule_written_before_fetch':True,'requests':results},indent=2)+'\n')
  print(json.dumps({k:v for k,v in item.items() if k not in ['headers','started_utc','completed_utc']}),flush=True)
