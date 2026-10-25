from pathlib import Path
import subprocess,hashlib,json,datetime
r=Path(__file__).resolve().parent;p=r/'primary-sources';p.mkdir(exist_ok=True)
items=[('chsss-published.pdf','https://www.combinatorics.org/ojs/index.php/eljc/article/download/v29i2p47/pdf/'),('chsss-author.pdf','https://web.math.princeton.edu/~pds/papers/chain/paper.pdf'),('owr2019-1.pdf','https://ems.press/content/serial-article-files/46780?nt=1')]
rows=[]
for name,url in items:
 q=p/name
 proc=subprocess.run(['curl','--location','--fail','--silent','--show-error','--max-time','45','--output',str(q),url],capture_output=True,text=True)
 if proc.returncode or not q.read_bytes().startswith(b'%PDF-'):
  rows.append({'name':name,'url':url,'status':'unavailable','stderr':proc.stderr});continue
 subprocess.run(['pdftotext','-layout',str(q),str(q.with_suffix('.txt'))],check=True)
 rows.append({'name':name,'url':url,'status':'saved','bytes':q.stat().st_size,'sha256':hashlib.sha256(q.read_bytes()).hexdigest(),'retrieved_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()})
(r/'primary-source-receipts.json').write_text(json.dumps(rows,indent=2)+'\n');print(json.dumps(rows,indent=2))
