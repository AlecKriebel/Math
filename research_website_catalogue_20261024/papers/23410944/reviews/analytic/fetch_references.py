from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime,timezone
import subprocess,hashlib,json
from pypdf import PdfReader
r=Path(__file__).resolve().parent;c=r/'.reference-cache';c.mkdir(exist_ok=True)
refs=[('kl','https://arxiv.org/pdf/2205.08172v2'),('k26','https://arxiv.org/pdf/2609.28602v1'),('owr','https://ems.press/content/serial-article-files/47475')]
def get(item):
 n,u=item;p=c/(n+'.pdf')
 try:
  done=subprocess.run(['curl','-L','--max-time','45','--fail','--silent','--show-error',u,'-o',str(p)],capture_output=True,text=True)
  if done.returncode:raise ValueError(done.stderr)
  data=p.read_bytes()
  if data[:4]!=b'%PDF':raise ValueError('Not PDF')
  rd=PdfReader(p)
  subprocess.run(['pdftotext','-layout',str(p),str(p.with_suffix('.txt'))],check=True)
  return {'name':n,'url':u,'sha256':hashlib.sha256(data).hexdigest(),'bytes':len(data),'pages':len(rd.pages),'status':'downloaded','timestamp_utc':datetime.now(timezone.utc).isoformat()}
 except Exception as e:return {'name':n,'url':u,'status':'failed','error':str(e)}
if __name__=='__main__':
 rows=list(ThreadPoolExecutor(max_workers=4).map(get,refs));(r/'reference_acquisition.json').write_text(json.dumps(rows,indent=2)+'\n');print(json.dumps(rows,indent=2))
