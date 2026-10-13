"""Read-only primary web provenance, bodies held in memory and never archived."""
from pathlib import Path
import datetime,hashlib,json,os,sys,urllib.request
F=Path(__file__).resolve().parent
urls=[
'https://ems.press/journals/owr/articles/14299288',
'https://arxiv.org/abs/2302.09792',
'https://arxiv.org/abs/2302.09801',
'https://link.springer.com/article/10.1007/s42543-023-00079-z',
'https://arxiv.org/abs/0810.4996',
'https://arxiv.org/html/0810.4996v3',
'https://link.springer.com/article/10.1007/s00454-010-9242-7',
'https://arxiv.org/abs/1410.6703',
'https://arxiv.org/abs/1112.1012',
'https://arxiv.org/abs/2412.14748',
'https://arxiv.org/abs/2602.19563',
'https://arxiv.org/abs/2509.02963',
'https://arxiv.org/abs/2607.17966',
'https://math.berkeley.edu/~bernd/articles.html']
results=[]
for url in urls:
 start=datetime.datetime.now(datetime.timezone.utc).isoformat()
 try:
  with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'Math independent priority audit'}),timeout=20) as r:
   b=r.read(); h=dict(r.headers); final=r.url; status=r.status
  item={'url':url,'started_utc':start,'finished_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'http_status':status,'final_url':final,'body_bytes':len(b),'body_sha256':hashlib.sha256(b).hexdigest(),'headers_selected':{k:v for k,v in h.items() if k.lower() in ['content-type','content-length','last-modified','etag']},'body_retained':False}
 except Exception as e:
  item={'url':url,'started_utc':start,'finished_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'error_type':type(e).__name__,'error':str(e),'body_retained':False}
 results.append(item);print(json.dumps(item),flush=True)
result={'schema':'pr55-priority-primary-body-metadata/v1','actual_pid':os.getpid(),'argv':sys.argv,'bodies_retained':False,'root_authority':False,'purpose':'Fresh reproducible retrieval metadata; intellectual content was personally read using web tools. Body hash does not prove theorem truth or exhaustivity.','results':results}
(F/'PRIMARY_RETRIEVAL_METADATA.json').write_text(json.dumps(result,indent=2)+'\n')
