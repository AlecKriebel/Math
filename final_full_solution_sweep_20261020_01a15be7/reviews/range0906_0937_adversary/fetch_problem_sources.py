from pathlib import Path
import urllib.request,concurrent.futures,json,hashlib,datetime,subprocess
W=Path(__file__).resolve().parent;P=W/'private/problem_sources';P.mkdir(exist_ok=True)
urls={'owr906':'https://ems.press/content/serial-article-files/52249','mvw_v1':'https://arxiv.org/pdf/2503.08553v1','owr908':'https://ems.press/content/serial-article-files/51350','owr909':'https://ems.press/content/serial-article-files/46242?nt=1','borodzik2014':'https://ir.library.osaka-u.ac.jp/repo/ouka/all/50809/ojm51_03_573.pdf','owr919':'https://ems.press/content/serial-article-files/46504'}
def fetch(kv):
 name,url=kv;req=urllib.request.Request(url,headers={'User-Agent':'Independent-bounded-research-review/1.0'})
 try:
  with urllib.request.urlopen(req,timeout=45) as f:b=f.read();status=f.status;final=f.url
  if not b.startswith(b'%PDF-'):raise ValueError('not PDF')
  p=P/(name+'.pdf');p.write_bytes(b);subprocess.run(['pdftotext','-layout',str(p),str(P/(name+'.txt'))],check=True)
  return {'name':name,'url':url,'final_url':final,'status':status,'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest(),'at':datetime.datetime.now(datetime.timezone.utc).isoformat()}
 except Exception as e:return {'name':name,'url':url,'error':str(e)}
with concurrent.futures.ThreadPoolExecutor(max_workers=6) as e:r=list(e.map(fetch,urls.items()))
(W/'PROBLEM_SOURCE_FETCH.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r,indent=2))
