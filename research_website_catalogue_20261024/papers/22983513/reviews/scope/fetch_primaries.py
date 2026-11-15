"""Bounded actual primary GETs; receipts and failures retained; no source edits."""
from pathlib import Path
from urllib.request import Request,urlopen
from urllib.error import HTTPError
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime,timezone
import hashlib,json,subprocess
HERE=Path(__file__).resolve().parent/'primary'
URLS={
 'HS1995':'https://web.ma.utexas.edu/mp_arc/e/95-431.amstex',
 'HS1997-publisher-attempt':'https://www.ams.org/journals/tran/1997-349-05/S0002-9947-97-01846-1/S0002-9947-97-01846-1.pdf',
 'LP2002':'https://www.homepages.ucl.ac.uk/~ucahlep/Papers/commutators.pdf',
 'HS2008-v1':'https://arxiv.org/pdf/0808.1133v1',
 'OWR2009':'https://publications.mfo.de/bitstream/handle/mfo/3107/OWR_2009_06.pdf',
 'Ash2002-publisher-attempt':'https://www.ias.ac.in/article/fulltext/pmsc/112/01/0003-0030',
 'Ash2002-historical-archive':'https://web.archive.org/web/20070101113227id_/http://www.ias.ac.in:80/mathsci/vol112/feb2002/Pm1970.pdf',
 'Stubbe2026-v1':'https://arxiv.org/pdf/2605.24694v1',
}
def fetch(it):
 name,url=it;p=HERE/(name+'.receipt.json')
 if p.exists():return {'name':name,'existing':True}
 r={'UTC':datetime.now(timezone.utc).isoformat(),'requested_URL':url}
 try:
  with urlopen(Request(url,headers={'User-Agent':'Mozilla/5.0'}),timeout=45) as h:body=h.read();r.update(status=h.status,final_URL=h.url,headers_ordered=list(h.headers.raw_items()))
 except HTTPError as h:body=h.read();r.update(status=h.code,final_URL=h.url,headers_ordered=list(h.headers.raw_items()))
 except Exception as e:body=b'';r['error']=repr(e)
 pdf=body.startswith(b'%PDF-');suffix='.pdf' if pdf else ('.amstex' if name=='HS1995' and b'\\document' in body else '.response')
 q=HERE/(name+suffix);q.write_bytes(body)
 r.update(path=str(q),bytes=len(body),SHA256=hashlib.sha256(body).hexdigest(),actual_PDF=pdf);p.write_text(json.dumps(r,indent=2)+'\n')
 if pdf:subprocess.run(['pdftotext','-layout',str(q),str(HERE/(name+'.txt'))],check=True)
 return {'name':name,**{k:r.get(k) for k in ('status','bytes','SHA256','actual_PDF','error')}}
if __name__=='__main__':
 with ThreadPoolExecutor(max_workers=6) as pool:
  for r in pool.map(fetch,URLS.items()):print(json.dumps(r))
