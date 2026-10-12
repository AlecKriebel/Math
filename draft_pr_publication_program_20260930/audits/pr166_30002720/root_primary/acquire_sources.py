from pathlib import Path
from datetime import datetime,timezone
import urllib.request,json,hashlib,subprocess
A=Path(__file__).resolve().parents[1];D=A/'root_primary/private';D.mkdir(parents=True,exist_ok=True);rows=[]
for name,url in [('owr','https://ems.press/content/serial-article-files/46539'),('analysis2014','https://arxiv.org/pdf/1404.3672v1'),('process_v2','https://arxiv.org/pdf/1605.02352v2'),('author_journal','https://www.math.uni-frankfurt.de/~neiningr/radix_journal.pdf')]:
 row={'name':name,'requested_URL':url,'UTC':datetime.now(timezone.utc).isoformat()}
 try:
  req=urllib.request.Request(url,headers={'User-Agent':'Independent mathematical source verification'})
  with urllib.request.urlopen(req,timeout=35) as r:
   b=r.read(16000001);row.update({'status':r.status,'resolved_URL':r.url,'headers':dict(r.headers)})
  if len(b)>16000000:raise RuntimeError('Source oversized')
  row.update({'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest(),'PDF_header':b.startswith(b'%PDF-')})
  p=D/(name+('.pdf' if row['PDF_header'] else '.response'));p.write_bytes(b);row['local_path']=str(p)
  if row['PDF_header']:
   cp=subprocess.run(['/opt/homebrew/bin/pdftotext','-layout',str(p),str(D/(name+'.txt'))],capture_output=True,text=True,timeout=20)
   row['text_extraction_exit_code']=cp.returncode
 except Exception as e:row['error']=type(e).__name__+': '+str(e)
 rows.append(row);print(json.dumps({k:v for k,v in row.items() if k!='headers'}),flush=True)
out=A/'root_primary/SOURCE_ACQUISITIONS.json';out.write_text(json.dumps({'UTC':datetime.now(timezone.utc).isoformat(),'sources':rows,'third_party_full_bodies_private':True,'priority_started':False},indent=2)+'\n')

