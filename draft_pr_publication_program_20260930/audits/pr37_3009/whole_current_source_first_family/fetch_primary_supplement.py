#!/usr/bin/env python3
"""Read-only primary source acquisition; writes only this family's primary/receipts."""
from pathlib import Path
import datetime,hashlib,json,subprocess,urllib.request
B=Path(__file__).resolve().parent
urls={
 'hamilton1954':'https://www.cambridge.org/core/services/aop-cambridge-core/content/view/0C64B48E1D93B4C117C7A327B79613D7/S0008414X00024007a.pdf/a-short-proof-of-the-cartwright-littlewood-fixed-point-theorem.pdf',
 'boronski_v1':'https://arxiv.org/pdf/1510.06663v1',
 'pardon_v3':'https://arxiv.org/pdf/1112.2324v3'}
for name,url in urls.items():
 r={'at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'url':url,'scope':'Live independent primary retrieval; no individual contacted'}
 try:
  with urllib.request.urlopen(url,timeout=40)as f:b=f.read();r.update(http_status=f.status,final_url=f.url,headers=dict(f.headers))
  p=B/'primary'/f'{name}.pdf';p.write_bytes(b);r.update(bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
  cp=subprocess.run(['pdftotext','-layout',str(p),str(p.with_suffix('.txt'))],capture_output=True)
  for ch in ['stdout','stderr']:(B/'receipts'/f'{name}.extract.{ch}').write_bytes(getattr(cp,ch))
  r['extract_exit']=cp.returncode
 except Exception as e:r['failure']=repr(e)
 (B/'receipts'/f'{name}.fetch.json').write_text(json.dumps(r,indent=2)+'\n')
 print(json.dumps({'name':name,**r},ensure_ascii=False))
