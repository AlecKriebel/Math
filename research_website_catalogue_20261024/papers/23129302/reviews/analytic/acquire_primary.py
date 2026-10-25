#!/usr/bin/env python3
from pathlib import Path
import concurrent.futures,datetime,hashlib,json,subprocess,urllib.request
O=Path(__file__).resolve().parent
C=O/'primary';C.mkdir(exist_ok=True)
sources=[('bkz-v1','https://arxiv.org/pdf/0812.4040v1'),('bkz-author','https://mat.univie.ac.at/~zweimueller/MyPub/bkz.pdf'),('owr-ems','https://ems.press/content/serial-article-files/46250')]
def fetch(item):
 name,url=item;r={'name':name,'url':url,'started_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()}
 try:
  with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'Independent mathematical source reader'}),timeout=25) as response:
   data=response.read(8_000_000);r.update({'status':response.status,'final_url':response.url,'headers':dict(response.headers)})
  assert data.startswith(b'%PDF')
  f=C/(name+'.pdf');f.write_bytes(data);r.update({'raw_path':str(f.relative_to(O)),'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()})
  text=C/(name+'.txt');x=subprocess.run(['pdftotext','-layout',str(f),str(text)],capture_output=True,text=True,timeout=25)
  r.update({'extract_returncode':x.returncode,'text_path':str(text.relative_to(O)),'text_sha256':hashlib.sha256(text.read_bytes()).hexdigest()})
  info=subprocess.run(['pdfinfo',str(f)],capture_output=True,text=True,timeout=10);r['pdfinfo']=info.stdout
 except Exception as error:r['error']=str(error)
 r['finished_utc']=datetime.datetime.now(datetime.timezone.utc).isoformat();return r
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:rows=list(pool.map(fetch,sources))
(O/'primary-acquisition.json').write_text(json.dumps({'record_id':'23129302','sources':rows},indent=2)+'\n')
print(json.dumps([{k:v for k,v in r.items() if k in ['name','status','bytes','sha256','error']} for r in rows]))
