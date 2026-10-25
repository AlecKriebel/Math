from pathlib import Path
from urllib.request import Request,urlopen
from datetime import datetime,timezone
from concurrent.futures import ThreadPoolExecutor,as_completed
from pypdf import PdfReader
import hashlib,json,io
P=Path(__file__).resolve().parent/'primary-sources';P.mkdir(exist_ok=True)
sources={
 'brits-v2':'https://arxiv.org/pdf/2607.12919v2',
 'brits-v3':'https://arxiv.org/pdf/2607.12919v3',
 'ardiyansyah':'https://arxiv.org/pdf/2104.12479v1',
 'englander-v4':'https://www.biorxiv.org/content/biorxiv/early/2026/07/04/2025.04.18.649493.full.pdf',
}
def run(item):
 name,url=item
 try:
  with urlopen(Request(url,headers={'User-Agent':'Mozilla/5.0 (Research source verification)'}),timeout=40) as response:b=response.read();final=response.geturl()
  assert b.startswith(b'%PDF'),b[:40]
  r=PdfReader(io.BytesIO(b));(P/(name+'.pdf')).write_bytes(b)
  (P/(name+'.txt')).write_text('\n\n'.join(f'===== PDF PAGE {i+1} =====\n'+p.extract_text() for i,p in enumerate(r.pages)))
  v=dict(url=url,final_url=final,retrieved_utc=datetime.now(timezone.utc).isoformat(),sha256=hashlib.sha256(b).hexdigest(),bytes=len(b),pages=len(r.pages))
  (P/(name+'.receipt.json')).write_text(json.dumps(v,indent=2)+'\n');return name,v
 except Exception as e:
  v=dict(url=url,retrieved_utc=datetime.now(timezone.utc).isoformat(),error=str(e));(P/(name+'.error.json')).write_text(json.dumps(v,indent=2)+'\n');return name,v
with ThreadPoolExecutor(max_workers=4) as ex:
 for f in as_completed([ex.submit(run,x) for x in sources.items()]):print(f.result(),flush=True)
