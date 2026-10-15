#!/usr/bin/env python3
"""Retrieve primary bodies into ignored storage; publish only access fingerprints."""
from pathlib import Path
import concurrent.futures,datetime,hashlib,json,subprocess,urllib.request
HERE=Path(__file__).resolve().parent
URLS={
 'owr.pdf':'https://ems.press/content/serial-article-files/51350',
 'owr_landing.html':'https://ems.press/journals/owr/articles/14299085',
 'siebert2026.pdf':'https://arxiv.org/pdf/2609.34402v1',
 'siebert2026.html':'https://arxiv.org/html/2609.34402v1',
 'siebert2026_abs.html':'https://arxiv.org/abs/2609.34402',
 'siebert2025.pdf':'https://arxiv.org/pdf/2409.10495v2',
 'siebert2025.html':'https://arxiv.org/html/2409.10495v2',
 'siebert2025_abs.html':'https://arxiv.org/abs/2409.10495',
 'siebert2025_published.pdf':'https://link.springer.com/content/pdf/10.1007/s11005-025-01919-y.pdf',
 'siebert2025_published.html':'https://link.springer.com/article/10.1007/s11005-025-01919-y',
 'owr_doi.html':'https://doi.org/10.4171/owr/2025/7',
}
def fetch(item):
 name,url=item
 r={'url':url,'utc':datetime.datetime.now(datetime.timezone.utc).isoformat()}
 try:
  req=urllib.request.Request(url,headers={'User-Agent':'Independent mathematical source verification'})
  with urllib.request.urlopen(req,timeout=45) as response:
   data=response.read(); r.update(status=response.status,final_url=response.url,content_type=response.headers.get('Content-Type'),bytes=len(data),sha256=hashlib.sha256(data).hexdigest())
  (HERE/'private_sources'/name).write_bytes(data)
  if name.endswith('.pdf'):
   r['pdf_magic']=data.startswith(b'%PDF-')
   if r['pdf_magic']:
    text=HERE/'private_sources'/name.replace('.pdf','.txt')
    subprocess.run(['pdftotext','-layout',str(HERE/'private_sources'/name),str(text)],check=True)
    r['pdf_info']=subprocess.check_output(['pdfinfo',str(HERE/'private_sources'/name)],text=True)
 except Exception as e: r['error']=type(e).__name__+': '+str(e)
 return name,r
if __name__=='__main__':
 with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool: out=dict(pool.map(fetch,URLS.items()))
 (HERE/'SOURCE_ACCESS_RECEIPTS.json').write_text(json.dumps(out,indent=2)+'\n')
 print(json.dumps({n:{k:v for k,v in r.items() if k!='pdf_info'} for n,r in out.items()},indent=2))
