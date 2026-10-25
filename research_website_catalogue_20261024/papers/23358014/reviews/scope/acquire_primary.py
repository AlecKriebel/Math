from pathlib import Path
from datetime import datetime,timezone
from concurrent.futures import ThreadPoolExecutor
import urllib.request,json,hashlib,subprocess
R=Path('/Users/alec/Documents/Math/research_website_catalogue_20261024/papers/23358014/reviews/scope');C=R/'cache/primary-sources'
items=[('km-v1.pdf','https://arxiv.org/pdf/1907.02744v1','arXiv 1907.02744v1,5 July2019'),('owr-2021-09.pdf','https://publications.mfo.de/bitstream/handle/mfo/3850/OWR_2021_09.pdf','Published Oberwolfach Report9/2021'),('ct-2015.pdf','https://www.mathematik.de/images/DMV/Jahresberichte/Jahresberichte_Archiv/2015.117Heft1.pdf','Published complete issue117(1),2015'),('cw-v1.pdf','https://arxiv.org/pdf/1707.07579v1','arXiv1707.07579v1,24July2017'),('bw-v1.pdf','https://arxiv.org/pdf/2311.14538v1','arXiv2311.14538v1,2023'),('ww-v1.pdf','https://arxiv.org/pdf/2111.10238v1','arXiv2111.10238v1,19November2021'),('hsw-2012.pdf','https://math.nyu.edu/~stadler/papers/HerzogStadlerWachsmuth12.pdf','PublishedSIAMJControlOptim50(2012)943–963'),('chw-2017.pdf','https://numdam.org/item/10.1051/cocv/2015048.pdf','PublishedESAIMCOCV23(2017)263–295')]
def one(t):
 name,url,ver=t;r={'name':name,'url':url,'version':ver,'retrieved_utc':datetime.now(timezone.utc).isoformat()}
 try:
  with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'IndependentResearchInventory/1.0'}),timeout=25) as f:b=f.read();r['resolved_url']=f.geturl()
  assert b.startswith(b'%PDF');p=C/name;p.write_bytes(b)
  subprocess.run(['pdftotext','-layout',str(p),str(p.with_suffix('.txt'))],check=True,capture_output=True)
  r.update({'status':'acquired','bytes':len(b),'sha256':hashlib.sha256(b).hexdigest(),'pdfinfo':subprocess.check_output(['pdfinfo',str(p)],text=True)})
 except Exception as e:r.update({'status':'unavailable','error':str(e)})
 return r
with ThreadPoolExecutor(max_workers=8) as ex:rows=list(ex.map(one,items))
(R/'primary-source-receipts.json').write_text(json.dumps(rows,indent=2)+'\n')
for r in rows:print(r['name'],r['status'],r.get('sha256',r.get('error')))
