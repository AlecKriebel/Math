#!/usr/bin/env python3
"""Fetch primary audit sources privately; never mutates frozen artifacts or Git."""
from pathlib import Path
from urllib.request import urlopen, Request
from datetime import datetime, timezone
from concurrent.futures import ThreadPoolExecutor
import hashlib, json, subprocess
BASE=Path(__file__).resolve().parent
SOURCES={
 'owr2014':'https://ems.press/content/serial-article-files/46543',
 'van_enter1310v2':'https://arxiv.org/pdf/1310.0267v2',
 'baake_grimm0810v2':'https://arxiv.org/pdf/0810.5750v2',
 'baake_lenz_van_enter1307v2':'https://arxiv.org/pdf/1307.7518v2',
 'entropy1205v1':'https://arxiv.org/pdf/1205.0392v1',
 'kinematic2011':'https://sfb701.math.uni-bielefeld.de/preprints/sfb11047.pdf',
}
def fetch(item):
 name,url=item
 p=BASE/'private_sources'/f'{name}.pdf'
 try:
  with urlopen(Request(url,headers={'User-Agent':'IndependentResearchAudit/1.0'}),timeout=45) as r:
   data=r.read(); final_url=r.url; status=r.status
  if not data.startswith(b'%PDF'): raise ValueError('response not PDF')
  p.write_bytes(data)
  subprocess.run(['pdftotext','-layout',str(p),str(p.with_suffix('.txt'))],check=True)
  info=subprocess.check_output(['pdfinfo',str(p)],text=True)
  p.with_suffix('.pdfinfo.txt').write_text(info)
  return {'name':name,'url':url,'final_url':final_url,'http_status':status,'sha256':hashlib.sha256(data).hexdigest(),'bytes':len(data),'retrieved_at_utc':datetime.now(timezone.utc).isoformat(),'pdfinfo':info,'private_path':str(p.relative_to(BASE))}
 except Exception as e: return {'name':name,'url':url,'retrieved_at_utc':datetime.now(timezone.utc).isoformat(),'error':str(e)}
if __name__=='__main__':
 with ThreadPoolExecutor(max_workers=6) as ex: receipts=list(ex.map(fetch,SOURCES.items()))
 (BASE/'PRIMARY_SOURCE_RECEIPTS.json').write_text(json.dumps(receipts,indent=2)+'\n')
 print(json.dumps([{k:v for k,v in x.items() if k!='pdfinfo'} for x in receipts],indent=2))
