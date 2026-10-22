"""Acquire a bounded published primary body without raw headers."""
from pathlib import Path
import urllib.request,hashlib,json,datetime,subprocess
A=Path(__file__).resolve().parent;D=A/'root_priority_primary';P=D/'private'
url='https://par.nsf.gov/servlets/purl/10582270';pdf=P/'ganguly_ramanan_published.pdf';txt=P/'ganguly_ramanan_published.txt'
if pdf.exists():raise RuntimeError('Reconcile existing acquisition; do not overwrite')
req=urllib.request.Request(url,headers={'User-Agent':'Independent-Math-Priority-Read/1.0'})
with urllib.request.urlopen(req,timeout=45) as r:b=r.read(10000001);status=r.status;final=r.url
if len(b)>10000000 or not b.startswith(b'%PDF'):raise RuntimeError('Not a bounded PDF')
pdf.write_bytes(b);pdf.chmod(0o444)
subprocess.run(['/opt/homebrew/bin/pdftotext','-layout',str(pdf),str(txt)],check=True);txt.chmod(0o444)
j={'utc':datetime.datetime.now(datetime.UTC).isoformat(),'url':url,'final_url':final,'http_status':status,'PDF_bytes':len(b),'PDF_sha256':hashlib.sha256(b).hexdigest(),'extract_bytes':txt.stat().st_size,'extract_sha256':hashlib.sha256(txt.read_bytes()).hexdigest(),'raw_headers_retained':False}
o=D/'GANGULY_RAMANAN_PUBLISHED_ACQUISITION.json';o.write_text(json.dumps(j,indent=2)+'\n');o.chmod(0o444);print(json.dumps(j))
