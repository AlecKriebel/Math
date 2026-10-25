from pathlib import Path
import concurrent.futures,datetime,urllib.request,hashlib,json,subprocess
base=Path(__file__).resolve().parent;out=base/'.reference-cache';out.mkdir(exist_ok=True)
urls={'boros-craciun-yu.pdf':'https://pollyyu.web.illinois.edu/manuscripts/2020-WR%20systems%20with%20infinitely%20many%20steady%20states.pdf','feliu-henriksson-pascual-escudero.pdf':'https://arxiv.org/pdf/2412.17798'}
def fetch(item):
 name,url=item;r={'name':name,'url':url}
 try:
  with urllib.request.urlopen(url,timeout=45) as response:b=response.read();r['resolved_url']=response.geturl()
  assert b.startswith(b'%PDF');p=out/name;p.write_bytes(b)
  subprocess.run(['pdftotext','-layout',str(p),str(p.with_suffix('.txt'))],check=True)
  info=subprocess.check_output(['pdfinfo',str(p)],text=True)
  r.update(status='saved',path=str(p),sha256=hashlib.sha256(b).hexdigest(),bytes=len(b),pages=int(next(x.split(':')[1].strip() for x in info.splitlines() if x.startswith('Pages:'))),retrieved_utc=datetime.datetime.now(datetime.timezone.utc).isoformat())
 except Exception as e:r.update(status='error',error=repr(e))
 return r
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as ex:a=list(ex.map(fetch,urls.items()))
(base/'primary_source_receipts.json').write_text(json.dumps(a,indent=2)+'\n');print(json.dumps(a,indent=2))
