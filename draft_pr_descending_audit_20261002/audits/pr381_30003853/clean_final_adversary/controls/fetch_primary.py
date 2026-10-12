from pathlib import Path
import urllib.request, hashlib, json, datetime, subprocess
from concurrent.futures import ThreadPoolExecutor
D=Path(__file__).resolve().parents[1]/'sources'
S=[('bgk0807.5138v1','https://arxiv.org/pdf/0807.5138v1'),('bleak_math0602038v2','https://arxiv.org/pdf/math/0602038v2'),('kassabov_matucci_math0607167v3','https://arxiv.org/pdf/math/0607167v3'),('guba_sapir_math0301225v2','https://arxiv.org/pdf/math/0301225v2'),('golan2609.14702v1','https://arxiv.org/pdf/2609.14702v1'),('farley2606.27753v2','https://arxiv.org/pdf/2606.27753v2')]
def get(item):
 n,u=item
 r={'name':n,'requested_url':u,'retrieved_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'representation':'complete PDF response bytes; not author TeX/source archive'}
 try:
  with urllib.request.urlopen(u,timeout=90) as x: b=x.read(); r.update(final_url=x.url,content_type=x.headers.get('Content-Type'))
  assert b.startswith(b'%PDF'),b[:100]
  p=D/(n+'.pdf'); p.write_bytes(b)
  subprocess.run(['pdftotext','-layout',str(p),str(p.with_suffix('.txt'))],check=True)
  r.update(bytes=len(b),sha256=hashlib.sha256(b).hexdigest(),status='downloaded_and_text_extracted')
 except Exception as e:r.update(status='failed',error=str(e))
 return r
with ThreadPoolExecutor(max_workers=6) as ex: receipts=list(ex.map(get,S))
p=D/'source_receipts.json'; p.write_text(json.dumps(receipts,indent=2)+'\n')
print(p.read_text(),end='')
