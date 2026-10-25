"""Read-only primary body retrieval; no submitted checker or historic report execution."""
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import datetime,hashlib,json,subprocess,urllib.request
O=Path(__file__).resolve().parent;D=O/'cache/primary-sources';D.mkdir(parents=True,exist_ok=True)
sources=[
 ('owr-2025-02','https://publications.mfo.de/bitstream/handle/mfo/4296/OWR_2025_02.pdf','Published OWR2/2025'),
 ('cjmst-v13','https://math.berkeley.edu/~marks/papers/polycyclic_v13.pdf','Author manuscript filename polycyclic_v13; exact body date recorded after reading'),
 ('iyer-shinko-v1','https://arxiv.org/pdf/2409.03078v1','arXiv2409.03078v1'),
 ('agw-author','https://www.math.tau.ac.il/~glasner/papers/fat.pdf','Author-hosted manuscript; do not presume publisher-final identity'),
 ('doucha-v3','https://arxiv.org/pdf/2211.08145v3','arXiv2211.08145v3'),
 ('dmt-v1','https://arxiv.org/pdf/2507.05474v1','arXiv2507.05474v1'),
 ('dmt-v2','https://arxiv.org/pdf/2507.05474v2','arXiv2507.05474v2'),
]
def get(item):
 name,url,version=item
 try:
  req=urllib.request.Request(url,headers={'User-Agent':'ResearchScope/1.0 public primary theorem review'})
  with urllib.request.urlopen(req,timeout=45) as r:data=r.read();resolved=r.geturl()
  assert data.lstrip().startswith(b'%PDF-')
  p=D/(name+'.pdf');p.write_bytes(data)
  subprocess.run(['pdftotext','-layout',str(p),str(D/(name+'.txt'))],check=True)
  info=subprocess.run(['pdfinfo',str(p)],capture_output=True,text=True,check=True).stdout
  return {'name':name+'.pdf','url':url,'resolved_url':resolved,'version':version,'status':'acquired','bytes':len(data),'sha256':hashlib.sha256(data).hexdigest(),'retrieved_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'pdfinfo':info}
 except Exception as e:return {'name':name+'.pdf','url':url,'version':version,'status':'unavailable','error':repr(e),'attempted_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()}
with ThreadPoolExecutor(max_workers=7) as pool:results=list(pool.map(get,sources))
(O/'primary-source-receipts.json').write_text(json.dumps(results,ensure_ascii=False,indent=2)+'\n')
print(json.dumps([{k:x[k] for k in ('name','status','sha256','error') if k in x} for x in results],indent=2))
