from pathlib import Path
import urllib.request,urllib.error,datetime,hashlib,json,concurrent.futures,subprocess
p=Path(__file__).resolve().parent/'primary';p.mkdir(exist_ok=True)
urls=[('Stanley1988','https://math.mit.edu/~rstan/pubs/pubfiles/77.pdf'),('Byrnes2012','https://conservancy.umn.edu/server/api/core/bitstreams/45a1bae8-402f-42a7-ad67-4caa7b55d104/content'),('OWR2018-23','https://ems.press/content/serial-article-files/46745'),('StanleyZanello2012','https://www.combinatorics.org/ojs/index.php/eljc/article/download/v19i2p13/pdf/'),('GV1806.03509v3','https://arxiv.org/pdf/1806.03509v3'),('Lewis2007','https://bpb-us-e1.wpmucdn.com/blogs.gwu.edu/dist/5/693/files/2018/04/JBLHarvardSeniorThesis-20drube.pdf'),('MillerReiner0811.1983v1','https://arxiv.org/pdf/0811.1983v1'),('Qing2008','https://web.math.utk.edu/~yqing/MasterThesis.pdf'),('Wright2019','https://math.mit.edu/research/highschool/primes/materials/2019/conf/9-1-Wright.pdf'),('Miller1202.3006v1','https://arxiv.org/pdf/1202.3006v1')]
def get(pair):
 name,url=pair;rec={'started_UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'requested_URL':url,'method':'ordinary GET','custom_headers':[],'retries':0}
 try:
  try:r=urllib.request.urlopen(url,timeout=35)
  except urllib.error.HTTPError as e:r=e
  body=r.read();pdf=body.startswith(b'%PDF-');q=p/(name+('.pdf'if pdf else'.response.body'));q.write_bytes(body)
  rec.update(status=r.status,final_URL=r.url,response_headers_in_received_order=list(r.headers.raw_items()),bytes=len(body),SHA256=hashlib.sha256(body).hexdigest(),actual_PDF=pdf,path=str(q));r.close()
  if pdf:
   info=subprocess.run(['pdfinfo',str(q)],capture_output=True,text=True,check=True).stdout;rec['pdfinfo_whole']=info
   subprocess.run(['pdftotext','-layout',str(q),str(p/(name+'.txt'))],check=True)
 except Exception as e:rec['transport_or_processing_error']=type(e).__name__+': '+str(e)
 rec['completed_UTC']=datetime.datetime.now(datetime.timezone.utc).isoformat();(p/(name+'.receipt.json')).write_text(json.dumps(rec,indent=2)+'\n');return{name:{k:v for k,v in rec.items()if k in['status','bytes','SHA256','actual_PDF','transport_or_processing_error']}}
with concurrent.futures.ThreadPoolExecutor(max_workers=5)as pool:
 for result in pool.map(get,urls):print(json.dumps(result),flush=True)
