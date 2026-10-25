from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from urllib.request import urlopen,Request
from datetime import datetime,timezone
import json,hashlib
from pypdf import PdfReader
B=Path('/Users/alec/Documents/Math/research_website_catalogue_20261024/papers')
entries=[('23410944','krejcirik-lotoreichik','https://arxiv.org/pdf/2205.08172v2'),('23410944','krejcirik-survey','https://arxiv.org/pdf/2609.28602v1'),('23410944','owr2023','https://ems.press/content/serial-article-files/47475'),('23422055','dlz','https://arxiv.org/pdf/1104.2511v1'),('23422055','hind-tomassini','https://arxiv.org/pdf/1908.03016v3'),('23422055','tan-wang-zhang-zhu','https://arxiv.org/pdf/1112.0768v3'),('23422055','donaldson','https://arxiv.org/pdf/math/0607083v1'),('23422055','bande-kotschick','https://arxiv.org/pdf/math/0703348v2'),('23422055','owr2020','https://ems.press/content/serial-article-files/46869'),('23422055','chen-zhang-I','https://wrap.warwick.ac.uk/id/eprint/164863/1/WRAP-Kodaira-dimensions-almost-complex-manifolds-I-Zhang-2022.pdf'),('23422055','chen-zhang-II','https://wrap.warwick.ac.uk/id/eprint/163848/1/WRAP-Kodaira-dimensions-almost-complex-manifolds-II-Zhang-2022.pdf'),('23422055','dlz-original-question','https://arxiv.org/pdf/0812.3680v1')]
def f(entry):
 id,name,url=entry
 p=B/id/'reviews/scope/primary-sources';p.mkdir(exist_ok=True);(p/'.gitignore').write_text('*.pdf\n*.txt\n')
 receipt={'name':name,'url':url,'retrieved_utc':datetime.now(timezone.utc).isoformat()}
 try:
  with urlopen(Request(url,headers={'User-Agent':'Research source review'}),timeout=45) as r: data=r.read()
  assert data.startswith(b'%PDF')
  q=p/(name+'.pdf');q.write_bytes(data);rd=PdfReader(q)
  (p/(name+'.txt')).write_text('\n\n'.join(f'===== PDF PAGE {i+1} =====\n'+pg.extract_text() for i,pg in enumerate(rd.pages)))
  receipt.update(status='ok',bytes=len(data),sha256=hashlib.sha256(data).hexdigest(),pages=len(rd.pages))
 except Exception as e:receipt.update(status='failed',error=str(e))
 (p/(name+'.receipt.json')).write_text(json.dumps(receipt,indent=2)+'\n')
 return {k:v for k,v in receipt.items() if k in ['name','status','error','pages']}
with ThreadPoolExecutor(max_workers=6) as ex:
 for result in ex.map(f,entries): print(json.dumps(result),flush=True)
