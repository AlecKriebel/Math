from pathlib import Path
from urllib.request import Request, urlopen
from concurrent.futures import ThreadPoolExecutor
import hashlib, json, datetime, subprocess

ROOT=Path(__file__).resolve().parent
OUT=ROOT/'cache/primary-sources'
OUT.mkdir(parents=True,exist_ok=True)
ITEMS=[
 ('problems-v2.pdf','https://arxiv.org/pdf/1804.03737v2','Author v2, 14 January 2020'),
 ('problems-v1.pdf','https://arxiv.org/pdf/1804.03737v1','Author v1, 10 April 2018'),
 ('bkm-v2.pdf','https://arxiv.org/pdf/1903.04603v2','Author v2, 11 December 2019'),
 ('bkm3-v1.pdf','https://arxiv.org/pdf/2007.09506v1','Author v1, July 2020'),
 ('bkm3-online-first.pdf','https://ems.press/content/serial-article-files/37551','Publisher online-first PDF, DOI 10.4171/RMI/1416'),
 ('bkm4-v1.pdf','https://arxiv.org/pdf/2304.10626v1','Author v1, 20 April 2023'),
 ('bkm3-published.pdf','https://ems.press/content/serial-article-files/40231?nt=1','Publisher issue PDF, Rev Mat Iberoam40 (2024),155–188')
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
