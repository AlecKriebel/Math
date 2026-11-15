"""Bounded ordinary GETs of exact cited primaries, retaining failures/headers."""
from pathlib import Path
from urllib.request import Request,urlopen
from urllib.error import HTTPError
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime,timezone
import hashlib,json,subprocess
P=Path(__file__).resolve().parent/'primary'
URLS={'OWR2006':'https://ems.press/content/serial-article-files/46037','Kohl2006-GWDG':'https://webdoc.sub.gwdg.de/ebook/dissts/Freiberg/Kohl2006.pdf','Kohl-URN-attempt':'https://nbn-resolving.org/urn:nbn:de:bsz:105-5454783','FS2001':'https://kam.mff.cuni.cz/kamserie/clanky/2001/s530.pdf','KSTV-publisher-attempt':'https://doi.org/10.1016/j.tcs.2005.09.032'}
def get(it):
 name,url=it;receipt=P/(name+'.receipt.json')
 if receipt.exists():return {'name':name,'existing_preserved':True}
 r={'UTC':datetime.now(timezone.utc).isoformat(),'requested_URL':url}
 try:
  with urlopen(Request(url,headers={'User-Agent':'Mozilla/5.0'}),timeout=45) as h:body=h.read();r.update(status=h.status,final_URL=h.url,headers_ordered=list(h.headers.raw_items()))
 except HTTPError as h:body=h.read();r.update(status=h.code,final_URL=h.url,headers_ordered=list(h.headers.raw_items()))
 except Exception as e:body=b'';r.update(status=None,error=repr(e),headers_ordered=[])
 pdf=body.startswith(b'%PDF-');p=P/(name+('.pdf' if pdf else '.response'));p.write_bytes(body)
 r.update(path=str(p),bytes=len(body),SHA256=hashlib.sha256(body).hexdigest(),actual_PDF=pdf);receipt.write_text(json.dumps(r,indent=2)+'\n')
 if pdf:subprocess.run(['pdftotext','-layout',str(p),str(P/(name+'.txt'))],check=True)
 return {'name':name,**{k:r.get(k) for k in ('status','bytes','SHA256','actual_PDF','error')}}
if __name__=='__main__':
 P.mkdir(exist_ok=True)
 with ThreadPoolExecutor(max_workers=5) as ex:
  for r in ex.map(get,URLS.items()):print(json.dumps(r))
