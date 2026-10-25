from pathlib import Path
from urllib.request import Request,urlopen
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime,timezone
import hashlib,json,subprocess
P=Path(__file__).resolve().parent;C=P/'cache/primary-sources';C.mkdir(parents=True,exist_ok=True)
urls={
 'bkr-published':'https://www.cambridge.org/core/services/aop-cambridge-core/content/view/7C4BAF1C7EBA17DE741C36DB40691412/S2050509426102217a.pdf/on-odd-powers-of-nonnegative-polynomials-that-are-not-sums-of-squares.pdf',
 'owr2023-14':'https://ems.press/content/serial-article-files/47007',
 'bcj1979':'https://gdz.sub.uni-goettingen.de/download/pdf/PPN235181684_0243/LOG_0040.pdf',
 'rounding2013':'https://eccc.weizmann.ac.il/report/2013/184/download/',
 'powermean-v1':'https://arxiv.org/pdf/2303.11823v1',
 'symmetric-v4':'https://arxiv.org/pdf/1205.3102v4',
 'stubborn-v1':'https://arxiv.org/pdf/2602.01191v1'}
def get(x):
 n,u=x;o={'name':n+'.pdf','url':u,'retrieved_utc':datetime.now(timezone.utc).isoformat()}
 try:
  with urlopen(Request(u,headers={'User-Agent':'Independent mathematical source review'}),timeout=40) as r:b=r.read();o['resolved_url']=r.url
  assert b.startswith(b'%PDF-');(C/(n+'.pdf')).write_bytes(b);o.update(status='acquired',bytes=len(b),sha256=hashlib.sha256(b).hexdigest());subprocess.run(['pdftotext','-layout',str(C/(n+'.pdf')),str(C/(n+'.txt'))],check=True,capture_output=True)
 except Exception as e:o.update(status='unavailable',error=str(e))
 return o
with ThreadPoolExecutor(max_workers=7) as e:rows=list(e.map(get,urls.items()))
(C/'receipt.json').write_text(json.dumps(rows,indent=2)+'\n');print(json.dumps(rows,indent=2))
