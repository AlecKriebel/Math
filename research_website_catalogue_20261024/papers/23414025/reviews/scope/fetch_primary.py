from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from urllib.request import urlopen,Request
from datetime import datetime,timezone
import json,hashlib
from pypdf import PdfReader
B=Path('/Users/alec/Documents/Math/research_website_catalogue_20261024/papers')
entries=[('23414025','baues','https://arxiv.org/pdf/0809.0824v1'),('23414025','burde-perfect','https://homepage.univie.ac.at/dietrich.burde/papers/burde_78_perfect.pdf'),('23414025','burde-unimodular','https://homepage.univie.ac.at/Dietrich.Burde/papers/burde_44_postlie_der.pdf'),('23414025','owr2023','https://ems.press/content/serial-article-files/48175'),('23390181','owr2026','https://ems.press/content/serial-article-files/53603'),('23390181','esi2024','https://www.esi.ac.at/static/assets/extras/reports/ESI_Report_2024.43f879fc9471.pdf'),('23390181','free-products','https://arxiv.org/pdf/2502.08630v2'),('23390181','ashcroft','https://ems.press/content/serial-article-files/30259'),('23390181','drutu-mackay','https://people.maths.ox.ac.uk/drutu/lp-random.pdf'),('23390181','kotowski','https://arxiv.org/pdf/1106.2242v2'),('23390181','tropp','https://arxiv.org/pdf/1004.4389v7'),('23390181','oppenheim','https://arxiv.org/pdf/2609.21255v1')]
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
 for result in ex.map(f,entries): print(json.dumps(result))
