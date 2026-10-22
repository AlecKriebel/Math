"""Read-only custody for narrowly selected EulerSolve mathematical-model leads."""
from pathlib import Path
from urllib.request import Request,urlopen
from urllib.parse import urljoin
from datetime import datetime,timezone
import json,re,hashlib,subprocess
BASE=Path('/Users/alec/Documents/Math/final_full_solution_sweep_20261020_01a15be7')
OUT=BASE/'audits/pr0280_30000156/reviews/reconciliation_priority_20261021/corpus_adversary'
PRIVATE=BASE/'private/pr0280_priority_reconciliation/corpus_adversary'
SLUGS=['aim-analysis-0055','amr-126-0025','amr-152-0049','aim-dynamical-systems-0042','amr-042-0001']
receipts=[]
def get(url,dest):
 t=datetime.now(timezone.utc).isoformat()
 try:
  with urlopen(Request(url,headers={'User-Agent':'Independent mathematical source reconciliation/1.0'}),timeout=45) as r: b=r.read();s=r.status;f=r.url
  dest.write_bytes(b)
  rec={'started_utc':t,'completed_utc':datetime.now(timezone.utc).isoformat(),'url':url,'final_url':f,'http_status':s,'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest(),'private_path':str(dest)}
  receipts.append(rec);return b
 except Exception as e:
  receipts.append({'started_utc':t,'completed_utc':datetime.now(timezone.utc).isoformat(),'url':url,'error':str(e)});return b''
for slug in SLUGS:
 url=f'https://eulersolve.org/papers/{slug}/';s=get(url,PRIVATE/f'{slug}.html').decode(errors='replace')
 links=re.findall(r'href="([^"]+)"',s)
 pdfs=[urljoin(url,u) for u in links if 'paper.pdf' in u]
 if pdfs:
  b=get(pdfs[0],PRIVATE/f'{slug}.pdf')
  if b.startswith(b'%PDF'):
   p=subprocess.run(['pdftotext','-layout',str(PRIVATE/f'{slug}.pdf'),str(PRIVATE/f'{slug}.txt')],capture_output=True,text=True)
   receipts[-1]['pdftotext_exit']=p.returncode
(OUT/'CANDIDATE_SOURCE_RECEIPTS.json').write_text(json.dumps(receipts,indent=2))
print(json.dumps(receipts,indent=2))
