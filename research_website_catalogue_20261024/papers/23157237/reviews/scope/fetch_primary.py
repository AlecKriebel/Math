from pathlib import Path
from urllib.request import urlopen,Request
from datetime import datetime,timezone
from concurrent.futures import ThreadPoolExecutor
from pypdf import PdfReader
import hashlib,json
B=Path('/Users/alec/Documents/Math/research_website_catalogue_20261024/papers')
entries=[
('23157237','reiss','https://www.math.utah.edu/~fguevara/pubs/Guevara_2017_ISS.pdf'),
('23157237','hansen-scheinkman','https://www.nber.org/system/files/working_papers/t0141/t0141.pdf'),
('23157237','crommelin2006','https://intlpress.com/api/bgcloud-front/resource/pdf/volume/1806266279453478914-1806266279453478914-5be73e60a7578b2388be90b0817a9cc0.pdf'),
('23157237','crommelin2011','https://ir.cwi.nl/pub/18934/18934B.pdf'),
('23157237','nickl','https://arxiv.org/pdf/2210.13008v3'),
('23157237','giordano-wang','https://arxiv.org/pdf/2405.01372v3'),
('23157237','alberti','https://arxiv.org/pdf/2410.19393v2'),
('23157237','grubb','https://web.math.ku.dk/~grubb/MN16.pdf'),
('23157237','lenzen-scherzer','https://franklenzen.de/pdf/lenzen_scherzer_eccomas2004.pdf'),
('22729355','satnoianu','https://people.maths.ox.ac.uk/maini/PKM%20publications/122.pdf'),
('22729355','anma','https://www.jstage.jst.go.jp/article/kodaimath/35/2/35_215/_pdf'),
('22729355','haas-goldstein','https://harvest.aps.org/v2/journals/articles/10.1103/PhysRevLett.126.238101/fulltext'),
('22729355','diego','https://harvest.aps.org/v2/journals/articles/10.1103/PhysRevX.8.021071/fulltext'),
('22729355','conradi','https://arxiv.org/pdf/2605.16049'),
('22729355','cross-diffusion','https://arxiv.org/pdf/2409.06860'),
('22729355','crandall-rabinowitz','https://jxshix.people.wm.edu/2013-taiwan/crandall-rabinowitz-1971-JFA.pdf')]
def fetch(t):
 ident,name,url=t;p=B/ident/'reviews/scope/primary-sources';p.mkdir(exist_ok=True);(p/'.gitignore').write_text('*.pdf\n*.txt\n')
 r=dict(name=name,url=url,retrieved_utc=datetime.now(timezone.utc).isoformat())
 try:
  b=urlopen(Request(url,headers={'User-Agent':'Research catalogue primary-source review'}),timeout=30).read();assert b.startswith(b'%PDF');(p/(name+'.pdf')).write_bytes(b);rd=PdfReader(p/(name+'.pdf'))
  (p/(name+'.txt')).write_text('\n\n'.join(f'===== PDF PAGE {j+1} =====\n'+(pg.extract_text() or '') for j,pg in enumerate(rd.pages)))
  r.update(status='ok',bytes=len(b),sha256=hashlib.sha256(b).hexdigest(),pages=len(rd.pages))
 except Exception as e:r.update(status='failed',error=str(e))
 (p/(name+'.receipt.json')).write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r),flush=True)
with ThreadPoolExecutor(max_workers=5) as ex:list(ex.map(fetch,entries))
