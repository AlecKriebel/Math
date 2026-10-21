from pathlib import Path
import datetime,hashlib,json,subprocess,urllib.request,shutil
out=Path(__file__).resolve().parent
url='https://ocw.mit.edu/courses/18-755-lie-groups-and-lie-algebras-ii-spring-2024/mit18_755_s24_lec_full.pdf'
start=datetime.datetime.now(datetime.timezone.utc).isoformat()
req=urllib.request.Request(url,headers={'User-Agent':'IndependentMathAudit/1.0'})
with urllib.request.urlopen(req,timeout=60) as r:
 data=r.read(15000001);status=r.status;final_url=r.url;headers=dict(r.headers)
assert len(data)<=15000000
assert data.startswith(b'%PDF')
pdf=out/'private_tmp'/'etingof.pdf';pdf.write_bytes(data)
receipt={'url':url,'final_url':final_url,'http_status':status,'start_utc':start,'end_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'pdf_bytes':len(data),'pdf_sha256':hashlib.sha256(data).hexdigest(),'http_headers':{k:v for k,v in headers.items() if k.lower() in ['etag','last-modified','content-type','content-length']}}
(out/'PRIMARY_RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps(receipt,sort_keys=True))
exe=shutil.which('pdftotext')
assert exe is not None,'pdftotext unavailable'
r=subprocess.run([exe,'-layout',str(pdf),str(out/'private_tmp'/'etingof.txt')],capture_output=True)
(out/'private_tmp'/'PDF_EXTRACTION.stdout').write_bytes(r.stdout)
(out/'private_tmp'/'PDF_EXTRACTION.stderr').write_bytes(r.stderr)
print('pdftotext_returncode='+str(r.returncode)+' stdout_sha256='+hashlib.sha256(r.stdout).hexdigest()+' stderr_sha256='+hashlib.sha256(r.stderr).hexdigest())
if r.returncode: raise SystemExit(r.returncode)
b=(out/'private_tmp'/'etingof.txt').read_bytes();print('extracted_text_bytes='+str(len(b))+' sha256='+hashlib.sha256(b).hexdigest())
