"""Read-only bounded primary priority acquisition."""
from pathlib import Path
import urllib.request,hashlib,json,datetime,subprocess
A=Path(__file__).resolve().parent;D=A/'root_priority_primary';D.mkdir(exist_ok=True);P=D/'private';P.mkdir(exist_ok=True)
S=[('admp1109_2575','https://arxiv.org/pdf/1109.2575'),('adj_author_sj325','https://www2.math.uu.se/~svantejs/papers/sj325.pdf')]
rows=[]
for name,url in S:
 pdf=P/(name+'.pdf');txt=P/(name+'.txt')
 if pdf.exists():raise RuntimeError('Already acquired; reconcile rather than overwrite')
 try:
  req=urllib.request.Request(url,headers={'User-Agent':'Math-Independent-Priority-Read/1.0'})
  with urllib.request.urlopen(req,timeout=45) as r:b=r.read(10000001);status=r.status;final=r.url
  if len(b)>10000000 or not b.startswith(b'%PDF'):raise RuntimeError('Not a bounded PDF')
  pdf.write_bytes(b);pdf.chmod(0o444)
  subprocess.run(['/opt/homebrew/bin/pdftotext','-layout',str(pdf),str(txt)],check=True);txt.chmod(0o444)
  rows.append({'name':name,'url':url,'final_url':final,'http_status':status,'PDF_bytes':len(b),'PDF_sha256':hashlib.sha256(b).hexdigest(),'raw_headers_retained':False})
 except Exception as e:rows.append({'name':name,'url':url,'access_error_type':type(e).__name__,'raw_headers_retained':False})
o=D/'ACQUISITION.json';o.write_text(json.dumps({'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'sources':rows},indent=2)+'\n');o.chmod(0o444)
print(json.dumps(rows))

