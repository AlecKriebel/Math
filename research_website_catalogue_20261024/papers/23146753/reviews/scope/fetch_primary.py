from pathlib import Path
import urllib.request,urllib.error,datetime,hashlib,json,concurrent.futures,subprocess
E=Path(__file__).resolve().parent;C=E/'cache/primary';C.mkdir(parents=True,exist_ok=True)
urls={'lauritzen-2022':'https://ems.press/content/serial-article-files/46992?nt=1','kahle-sullivant-v1':'https://arxiv.org/pdf/2411.03139v1','geiger-meek-sturmfels-published':'https://math.berkeley.edu/~bernd/AOS0092.pdf','gandolfi-lenarda-published':'https://msp.org/memocs/2016/4-3/memocs-v4-n3-p13-s.pdf'}
def one(x):
 name,url=x;start=datetime.datetime.now(datetime.timezone.utc).isoformat()
 try:
  with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'Independent-research-primary-custody/1.0'}),timeout=40) as r:b=r.read();status=r.status;headers=dict(r.headers.items());final=r.url
 except urllib.error.HTTPError as r:b=r.read();status=r.code;headers=dict(r.headers.items());final=r.url
 except Exception as ex:return {'name':name,'requested_url':url,'started_utc':start,'error':type(ex).__name__+':'+str(ex),'body_saved':False}
 ispdf=b.startswith(b'%PDF-');path=C/(name+('.pdf' if ispdf else '.response'))
 if path.exists():raise RuntimeError('preserve_previous_primary')
 path.write_bytes(b);info=None
 if ispdf:
  subprocess.run(['/opt/homebrew/bin/pdftotext',str(path),str(C/(name+'.txt'))],check=True,capture_output=True);info=subprocess.check_output(['/opt/homebrew/bin/pdfinfo',str(path)],text=True)
 return {'name':name,'requested_url':url,'started_utc':start,'completed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':status,'final_url':final,'headers':headers,'path':str(path),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest(),'actual_PDF':ispdf,'pdfinfo':info}
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:rows=list(ex.map(one,urls.items()))
(E/'primary-fetch-receipts.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n');print(json.dumps([{k:v for k,v in x.items() if k not in ['headers','pdfinfo']} for x in rows],indent=2))
