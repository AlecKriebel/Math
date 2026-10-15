from pathlib import Path
import urllib.request, urllib.parse, hashlib, json, datetime, subprocess, concurrent.futures
ROOT=Path(__file__).resolve().parent
SOURCES=[('published_nsf','https://par.nsf.gov/servlets/purl/10582270'),('arxiv_v3','https://arxiv.org/pdf/2205.01587v3')]
def acquire(item):
 name,url=item
 req=urllib.request.Request(url,headers={'User-Agent':'Independent mathematical source verification'})
 with urllib.request.urlopen(req,timeout=45) as response:
  final=response.geturl(); headers=list(response.headers.items()); body=response.read(); status=response.status
 if status!=200 or not body.startswith(b'%PDF-'):
  raise ValueError(f'Unexpected PDF response for {name}: HTTP {status}; {len(body)} bytes')
 if urllib.parse.urlparse(final).hostname not in {'par.nsf.gov','arxiv.org','export.arxiv.org'}:
  raise ValueError(f'Unexpected acquisition host: {final}')
 pdf=ROOT/'private'/f'{name}.pdf'; pdf.write_bytes(body)
 raw=ROOT/'private'/f'{name}_raw_headers.json'; raw.write_text(json.dumps({'requested_url':url,'effective_url':final,'status':status,'headers':headers},indent=2)+'\n')
 txt=ROOT/'private'/f'{name}_layout.txt'
 subprocess.run(['/opt/homebrew/bin/pdftotext','-layout',str(pdf),str(txt)],check=True)
 return {'name':name,'requested_url':url,'effective_url':final,'status':status,'acquired_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'pdf_sha256':hashlib.sha256(body).hexdigest(),'pdf_bytes':len(body),'extract_sha256':hashlib.sha256(txt.read_bytes()).hexdigest(),'extract_bytes':txt.stat().st_size,'body_scope':'private; not for public source-body redistribution'}
if __name__=='__main__':
 records=[]; errors=[]
 with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
  futures={pool.submit(acquire,item):item for item in SOURCES}
  for future,item in futures.items():
   try: records.append(future.result())
   except Exception as exc: errors.append({'source':item,'error_type':type(exc).__name__,'error':str(exc)})
 result={'sources':records,'errors':errors}
 (ROOT/'SOURCE_ACQUISITION_LEDGER.json').write_text(json.dumps(result,indent=2)+'\n')
 print(json.dumps(result))
 if errors: raise SystemExit(1)
