from pathlib import Path
from datetime import datetime,timezone
from urllib.request import Request,urlopen
from concurrent.futures import ThreadPoolExecutor,as_completed
import json,hashlib,subprocess
D=Path(__file__).resolve().parent/'cache/primary-sources';D.mkdir(parents=True,exist_ok=True)
items=[('englander-v4.pdf','https://www.biorxiv.org/content/10.1101/2025.04.18.649493v4.full.pdf'),('huber-published.pdf','https://link.springer.com/content/pdf/10.1007/s11538-025-01510-5.pdf'),('holtgrefe-published.pdf','https://link.springer.com/content/pdf/10.1007/s12064-025-00453-8.pdf'),('currie-v1.pdf','https://arxiv.org/pdf/2606.26673v1'),('brits-v2.pdf','https://arxiv.org/pdf/2607.12919v2'),('ardiyansyah-v1.pdf','https://arxiv.org/pdf/2104.12479v1'),('sullivant-v2.pdf','https://arxiv.org/pdf/2507.23056v2'),('coste-notes.pdf','https://perso.univ-rennes1.fr/michel.coste/polyens/SAG.pdf')]
def fetch(item):
 name,url=item;r={'name':name,'url':url,'retrieved_utc':datetime.now(timezone.utc).isoformat()}
 try:
  with urlopen(Request(url,headers={'User-Agent':'Mozilla/5.0 Research source verification'}),timeout=35) as f:b=f.read(40*1024*1024);r['resolved_url']=f.url
  assert b.startswith(b'%PDF'),b[:100]
  (D/name).write_bytes(b);r.update(status='acquired',bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
  subprocess.run(['pdftotext','-layout',str(D/name),str(D/Path(name).with_suffix('.txt'))],check=True,capture_output=True)
 except Exception as e:r.update(status='unavailable',error=type(e).__name__+': '+str(e))
 return r
rows=[]
with ThreadPoolExecutor(max_workers=8) as pool:
 for f in as_completed([pool.submit(fetch,i) for i in items]):r=f.result();rows.append(r);print(r,flush=True)
(D/'receipt.json').write_text(json.dumps(rows,indent=2)+'\n')
