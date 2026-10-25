from pathlib import Path
from urllib.request import urlopen, Request
from datetime import datetime,timezone
from concurrent.futures import ThreadPoolExecutor
from pypdf import PdfReader
import json,hashlib
B=Path('/Users/alec/Documents/Math/research_website_catalogue_20261024/papers')
entries=[
 ('23353160','fawzi','https://arxiv.org/pdf/1905.02575v1'),
 ('23353160','sanyal','https://ems.press/content/serial-article-files/46561'),
 ('23353160','harvey-lawson','https://archive.ymsc.tsinghua.edu.cn/pacm_download/117/6313-11511_2006_Article_BF02392726.pdf'),
 ('23353160','vrana-levay','https://arxiv.org/pdf/0902.2269v2'),
 ('23353160','grabowski-kus-marmo','https://arxiv.org/pdf/1111.4812v2'),
 ('23353160','orbitopes','https://arxiv.org/pdf/0911.5436'),
 ('23353160','bettiol-kummer-mendes','https://arxiv.org/pdf/1908.03713v2'),
 ('23353160','rostalski','https://www.birs.ca/workshops/2010/10w5007/files/rostalski.pdf'),
 ('23147866','bruss2004','https://arxiv.org/pdf/quant-ph/0407037v3'),
 ('23147866','bruss2005','https://ems.press/content/serial-article-files/45978'),
 ('23147866','bruss2006','https://arxiv.org/pdf/quant-ph/0507146v1'),
 ('23147866','pradhan-agrawal-pati','https://arxiv.org/pdf/0705.1917v1'),
 ('23147866','winter','https://arxiv.org/pdf/quant-ph/9807019v3'),
 ('23147866','huang-zhang-hou','https://arxiv.org/pdf/quant-ph/9911120v5'),
 ('23147866','das2015','https://arxiv.org/pdf/1412.6247v1'),
 ('23147866','muhuri2024','https://arxiv.org/pdf/2211.13057v2')]
def fetch(t):
 ident,name,url=t;p=B/ident/'reviews/scope/primary-sources';p.mkdir(exist_ok=True);(p/'.gitignore').write_text('*.pdf\n*.txt\n')
 r=dict(name=name,url=url,retrieved_utc=datetime.now(timezone.utc).isoformat())
 try:
  with urlopen(Request(url,headers={'User-Agent':'Research catalogue primary source review'}),timeout=35) as res:b=res.read()
  assert b.startswith(b'%PDF');(p/(name+'.pdf')).write_bytes(b);reader=PdfReader(p/(name+'.pdf'))
  (p/(name+'.txt')).write_text('\n\n'.join(f'===== PDF PAGE {i+1} =====\n'+(pg.extract_text() or '') for i,pg in enumerate(reader.pages)))
  r.update(status='ok',bytes=len(b),sha256=hashlib.sha256(b).hexdigest(),pages=len(reader.pages))
 except Exception as e:r.update(status='failed',error=str(e))
 (p/(name+'.receipt.json')).write_text(json.dumps(r,indent=2)+'\n');return r
with ThreadPoolExecutor(max_workers=5) as ex:
 for r in ex.map(fetch,entries):print(json.dumps(r),flush=True)
