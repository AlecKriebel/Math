from pathlib import Path
import urllib.request,urllib.error,hashlib,json,datetime,concurrent.futures
E=Path('/Users/alec/Documents/Math/research_website_catalogue_20261024/papers/23124601/reviews/scope');C=E/'cache/primary';C.mkdir(parents=True,exist_ok=True)
requests=[('mcgbook.pdf','https://www.math.uchicago.edu/~farb/papers/mcgbook.pdf'),('baykur-monden-vhm2017.pdf','https://msp.org/agt/2017/17-3/agt-v17-n3-p06-s.pdf'),('gonzalez-meneses2011.pdf','https://www.numdam.org/article/AMBP_2011__18_1_15_0.pdf'),('sato2008.pdf','https://www.ms.u-tokyo.ac.jp/journal/pdf/jms150403.pdf'),('elrifai-morton-author.pdf','https://www.liverpool.ac.uk/~su14/papers/elrifaimorton.pdf'),('matsumoto-landing.html','https://archive.mpim-bonn.mpg.de/id/eprint/3423/')]
def fetch(item):
 name,u=item;t=datetime.datetime.now(datetime.timezone.utc).isoformat();out={'requested_url':u,'started_utc':t,'method':'GET','path':str(C/name)}
 try:
  with urllib.request.urlopen(u,timeout=25) as r:
   b=r.read(32*1024*1024+1);assert len(b)<=32*1024*1024
   (C/name).write_bytes(b);out.update({'completed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':r.status,'reason':r.reason,'final_url':r.url,'headers_in_original_order':list(r.headers.raw_items()),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest(),'actual_PDF_magic':b.startswith(b'%PDF-')})
 except urllib.error.HTTPError as x:
  b=x.read();(C/name).write_bytes(b);out.update({'completed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':x.code,'error':repr(x),'headers_in_original_order':list(x.headers.raw_items()),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest(),'actual_PDF_magic':b.startswith(b'%PDF-')})
 except Exception as x:out.update({'completed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'error':repr(x)})
 return out
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:rows=list(pool.map(fetch,requests))
(E/'primary-fetch-receipts.json').write_text(json.dumps(rows,indent=2)+'\n')
for x in rows:print(json.dumps({k:v for k,v in x.items() if k!='headers_in_original_order'}),flush=True)
