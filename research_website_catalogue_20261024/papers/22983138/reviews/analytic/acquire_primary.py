#!/usr/bin/env python3
from pathlib import Path
import concurrent.futures,datetime,hashlib,json,subprocess,urllib.request
O=Path(__file__).resolve().parent;C=O/'primary-cache';C.mkdir(exist_ok=True)
sources=[
 ('fps-published','https://www.cambridge.org/core/services/aop-cambridge-core/content/view/DE65A193C3EE743DF0EA834A8405026E/S0008439500021561a.pdf/simplices_in_the_euclidean_ball.pdf'),
 ('fps-author','https://perso.math.u-pem.fr/fradelizi.matthieu/pdf/FPS_Simplex-submission.pdf'),
 ('owr-ems','https://ems.press/content/serial-article-files/46255')]
def fetch(item):
 name,url=item;row={'name':name,'url':url,'started_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()}
 try:
  with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'Independent mathematical source reader'}),timeout=25) as response:data=response.read(5000000);row.update({'status':response.status,'final_url':response.url,'headers':dict(response.headers)})
  assert data.startswith(b'%PDF')
  pdf=C/(name+'.pdf');pdf.write_bytes(data);text=C/(name+'.txt')
  row.update({'raw_path':str(pdf.relative_to(O)),'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()})
  sub=subprocess.run(['pdftotext','-layout',str(pdf),str(text)],capture_output=True,text=True,timeout=20)
  row.update({'extract_returncode':sub.returncode,'text_path':str(text.relative_to(O)),'text_sha256':hashlib.sha256(text.read_bytes()).hexdigest()})
  info=subprocess.run(['pdfinfo',str(pdf)],capture_output=True,text=True,timeout=10);row['pdfinfo']=info.stdout
 except Exception as error:row['error']=str(error)
 row['finished_utc']=datetime.datetime.now(datetime.timezone.utc).isoformat();return row
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:rows=list(pool.map(fetch,sources))
(O/'primary-acquisition.json').write_text(json.dumps({'record_id':'22983138','sources':rows},indent=2)+'\n')
print(json.dumps([{k:v for k,v in row.items() if k in ['name','status','bytes','sha256','error']} for row in rows]))
