"""Acquire bounded official mathematical source bodies, never raw headers."""
from pathlib import Path
import datetime,hashlib,json,subprocess,urllib.request
A=Path(__file__).resolve().parent
D=A/'root_primary';D.mkdir(exist_ok=True);private=D/'private';private.mkdir(exist_ok=True)
sources=[('owr57_2017','https://ems.press/content/serial-article-files/46721'),('ahlberg_deijfen_janson_v1','https://arxiv.org/pdf/1711.02902v1')]
out=[]
for name,url in sources:
 request=urllib.request.Request(url,headers={'User-Agent':'Math-PR173-Primary-Source-Read/1.0'})
 try:
  with urllib.request.urlopen(request,timeout=45) as response:
   b=response.read(5000001);status=response.status;final=response.url
  if not b.startswith(b'%PDF') or len(b)>5000000:raise RuntimeError('Not a bounded PDF')
  p=private/(name+'.pdf');p.write_bytes(b);p.chmod(0o444)
  subprocess.run(['/opt/homebrew/bin/pdftotext','-layout',str(p),str(private/(name+'.txt'))],check=True)
  (private/(name+'.txt')).chmod(0o444)
  out.append({'name':name,'url':url,'final_url':final,'http_status':status,'PDF_bytes':len(b),'PDF_sha256':hashlib.sha256(b).hexdigest(),'raw_headers_retained':False})
 except Exception as e:out.append({'name':name,'url':url,'access_error_type':type(e).__name__,'source_body_read':False,'raw_headers_retained':False})
(D/'ACQUISITION.json').write_text(json.dumps({'UTC':datetime.datetime.now(datetime.UTC).isoformat(),'sources':out,'scope':'Primary model/original problem validation; no historical novelty clearance'},indent=2)+'\n')
print(json.dumps(out))
