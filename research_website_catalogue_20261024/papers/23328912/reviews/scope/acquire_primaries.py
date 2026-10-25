from pathlib import Path
from urllib.request import Request, urlopen
from concurrent.futures import ThreadPoolExecutor
import hashlib, json, datetime, subprocess

ROOT=Path(__file__).resolve().parent
OUT=ROOT/'cache/primary-sources'
OUT.mkdir(parents=True,exist_ok=True)
ITEMS=[
 ('aim-workshop-report.pdf','https://aimath.org/pastworkshops/freebycyclicrep.pdf','AIM workshop summary, October2023'),
 ('completion-v1.pdf','https://arxiv.org/pdf/2011.05374v1','Ben-Zvi–Kropholler–Lyman author v1, November2020'),
 ('dgo-v5.pdf','https://arxiv.org/pdf/1111.7048v5','Dahmani–Guirardel–Osin author v5'),
 ('hagen-wise-v3.pdf','https://arxiv.org/pdf/1605.07879v3','Hagen–Wise author v3,2025'),
 ('leary-v3.pdf','https://arxiv.org/pdf/1009.1540v3','Leary accepted author v3,15October2012'),
 ('minasyan-osin-v6.pdf','https://arxiv.org/pdf/1310.6289v6','Corrected author v6,20December2017'),
 ('sisto-v1.pdf','https://arxiv.org/pdf/1310.7753v1','Sisto author v1,2013')
]

def fetch(t):
 name,url,version=t
 try:
  with urlopen(Request(url,headers={'User-Agent':'ResearchScope/1.0'}),timeout=60) as r:
   b=r.read();resolved=r.url
  assert b.startswith(b'%PDF'),b[:100]
  p=OUT/name;p.write_bytes(b)
  subprocess.run(['pdftotext','-layout',str(p),str(p.with_suffix('.txt'))],check=True)
  inf=subprocess.check_output(['pdfinfo',str(p)],text=True)
  pages=int(next(l for l in inf.splitlines() if l.startswith('Pages:')).split(':')[1])
  return {'name':name,'url':url,'resolved_url':resolved,'version':version,'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest(),'pages':pages,'retrieved_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'acquired'}
 except Exception as e:
  return {'name':name,'url':url,'version':version,'status':'failed','error':str(e),'retrieved_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()}
with ThreadPoolExecutor(max_workers=4) as p: out=list(p.map(fetch,ITEMS))
(ROOT/'primary-source-receipts.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
