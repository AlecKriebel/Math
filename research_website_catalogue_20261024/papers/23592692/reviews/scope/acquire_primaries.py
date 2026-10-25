from pathlib import Path
from urllib.request import Request, urlopen
from concurrent.futures import ThreadPoolExecutor
import hashlib, json, datetime, subprocess

ROOT=Path(__file__).resolve().parent
OUT=ROOT/'cache/primary-sources'
OUT.mkdir(parents=True,exist_ok=True)
ITEMS=[
 ('owr-2023-12.pdf','https://ems.press/content/serial-article-files/47008','Published Oberwolfach Reports 12/2023'),
 ('warm-2016-published.pdf','https://pure.tue.nl/ws/portalfiles/portal/46706436/hofsstro2016.pdf','Published Annals of Applied Probability 26 (2016), 2494–2539'),
 ('hk-2017-author.pdf','https://researchers.ms.unimelb.edu.au/~mholmes1@unimelb/Reinforced-graphs_final.pdf','Author manuscript, title page dated March 2017'),
 ('hhk-2023-published.pdf','https://pure.au.dk/ws/portalfiles/portal/418609000/Hirsch_2023_Nonlinearity_36_3013.pdf','Published Nonlinearity 36 (2023), 3013–3042, institutional cover sheet')
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
