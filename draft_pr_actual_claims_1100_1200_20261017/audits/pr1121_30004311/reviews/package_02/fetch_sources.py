#!/usr/bin/env python3
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from datetime import datetime,timezone
import urllib.request,hashlib,json,subprocess
BASE=Path(__file__).resolve().parent
PRIVATE=BASE/'sources/private'
SOURCES=[('owr','https://ems.press/content/serial-article-files/46831'),('1705.08493v1','https://arxiv.org/pdf/1705.08493v1'),('2001.08905v1','https://arxiv.org/pdf/2001.08905v1'),('1511.08477v3','https://arxiv.org/pdf/1511.08477v3'),('1610.00477v1','https://arxiv.org/pdf/1610.00477v1'),('1807.06408v1','https://arxiv.org/pdf/1807.06408v1'),('2401.12904v2','https://arxiv.org/pdf/2401.12904v2'),('2608.01884v2','https://arxiv.org/pdf/2608.01884v2'),('2609.20401v1','https://arxiv.org/pdf/2609.20401v1'),('2609.24640v1','https://arxiv.org/pdf/2609.24640v1')]
def fetch(row):
 name,url=row
 result={'name':name,'url':url,'retrieved_utc':datetime.now(timezone.utc).isoformat()}
 try:
  with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'IndependentResearch/1.0'}),timeout=35) as response:
   raw=response.read(); result.update(status=response.status,resolved_url=response.url,bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest())
  if not raw.startswith(b'%PDF'):raise ValueError('Not a PDF')
  p=PRIVATE/(name+'.pdf');p.write_bytes(raw)
  subprocess.run(['pdftotext','-layout',str(p),str(PRIVATE/(name+'.txt'))],check=True,capture_output=True)
 except Exception as e:result['error']=str(e)
 return result
if __name__=='__main__':
 with ThreadPoolExecutor(max_workers=5) as ex:rows=list(ex.map(fetch,SOURCES))
 (BASE/'FETCH_RECEIPTS.json').write_text(json.dumps(rows,indent=2)+'\n')
 print(json.dumps(rows,indent=2))
