from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import subprocess,hashlib,json,datetime
r=Path(__file__).resolve().parent;p=r/'primary-sources';p.mkdir(exist_ok=True)
items=[('owr44-2008.pdf','https://ems.press/content/serial-article-files/46191'),('simon-ntu-gmt.pdf','https://math.stanford.edu/~lms/ntu-gmt-text.pdf'),('demouth-goaoc-topve-archive.pdf','https://web.archive.org/web/20110401122240id_/http://www.loria.fr/~goaoc/papers/TopVE.pdf')]
def get(item):
 name,url=item;q=p/name
 cmd=['curl','--location','--fail','--silent','--show-error','--max-time','55','--output',str(q),url]
 proc=subprocess.run(cmd,capture_output=True,text=True)
 if proc.returncode:return {'name':name,'url':url,'status':'unavailable','error':proc.stderr}
 data=q.read_bytes()
 if not data.startswith(b'%PDF-'):return {'name':name,'url':url,'status':'not_pdf','bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()}
 subprocess.run(['pdftotext','-layout',str(q),str(q.with_suffix('.txt'))],check=True)
 return {'name':name,'url':url,'status':'saved','bytes':len(data),'sha256':hashlib.sha256(data).hexdigest(),'retrieved_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()}
with ThreadPoolExecutor(max_workers=3) as pool:rows=list(pool.map(get,items))
(r/'primary-source-receipts.json').write_text(json.dumps(rows,indent=2)+'\n');print(json.dumps(rows,indent=2))
