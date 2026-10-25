from pathlib import Path
from urllib.request import Request, urlopen
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pypdf import PdfReader
import json, hashlib
B = Path('/Users/alec/Documents/Math/research_website_catalogue_20261024/papers')
entries = [
 ('22929486','kourovka-september','https://kourovkanotebookorg.wordpress.com/wp-content/uploads/2026/09/21tkt.pdf'),
 ('22929486','kourovka-update','https://kourovkanotebookorg.wordpress.com/wp-content/uploads/2026/09/21upd.pdf'),
 ('22929486','cameron2014','https://arxiv.org/pdf/1408.0968v1'),
 ('22929486','cameron2024','https://msp.org/mt/2024/3-2/mt-v3-n2-p13-p.pdf'),
 ('23088066','brehm2006','https://ems.press/content/serial-article-files/46044'),
 ('23088066','brehm-sarkaria','https://archive.mpim-bonn.mpg.de/id/eprint/1946/1/preprint_1992_52.pdf'),
 ('23088066','newman','https://arxiv.org/pdf/2212.09576v3'),
 ('23088066','lee-nevo-v1','https://arxiv.org/pdf/2307.14195v1'),
 ('23088066','lee-nevo-v3','https://arxiv.org/pdf/2307.14195v3'),
 ('23088066','frieze-karonski','https://www.math.cmu.edu/~af1p/BOOK.pdf'),
]
def fetch(e):
 ident,name,url=e;p=B/ident/'reviews/scope/primary-sources';p.mkdir(exist_ok=True);(p/'.gitignore').write_text('*.pdf\n*.txt\n*.html\n')
 r=dict(name=name,url=url,retrieved_utc=datetime.now(timezone.utc).isoformat())
 try:
  with urlopen(Request(url,headers={'User-Agent':'Research catalogue primary source review'}),timeout=40) as response: b=response.read()
  assert b.startswith(b'%PDF');(p/(name+'.pdf')).write_bytes(b);reader=PdfReader(p/(name+'.pdf'))
  (p/(name+'.txt')).write_text('\n\n'.join(f'===== PDF PAGE {i+1} =====\n'+(pg.extract_text() or '') for i,pg in enumerate(reader.pages)))
  r.update(status='ok',bytes=len(b),sha256=hashlib.sha256(b).hexdigest(),pages=len(reader.pages))
 except Exception as err:r.update(status='failed',error=str(err))
 (p/(name+'.receipt.json')).write_text(json.dumps(r,indent=2)+'\n');return r
with ThreadPoolExecutor(max_workers=5) as ex:
 for r in ex.map(fetch,entries):print(json.dumps(r),flush=True)
