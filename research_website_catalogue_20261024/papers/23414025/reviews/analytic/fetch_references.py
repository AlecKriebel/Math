from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime,timezone
import subprocess,hashlib,json
from pypdf import PdfReader
r=Path(__file__).resolve().parent;c=r/'.reference-cache';c.mkdir(exist_ok=True)
refs=[('etingof','https://ocw.mit.edu/courses/18-755-lie-groups-and-lie-algebras-ii-spring-2024/mit18_755_s24_lec_full.pdf'),('hatcher','https://pi.math.cornell.edu/~hatcher/AT/AT.pdf'),('bdm','https://homepage.univie.ac.at/dietrich.burde/papers/burde_78_perfect.pdf'),('owr','https://ems.press/content/serial-article-files/48175'),('baues','https://arxiv.org/pdf/0809.0824v1'),('bd','https://homepage.univie.ac.at/dietrich.burde/papers/burde_44_postlie_der.pdf'),('bdv','https://arxiv.org/pdf/1109.0251')]
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
