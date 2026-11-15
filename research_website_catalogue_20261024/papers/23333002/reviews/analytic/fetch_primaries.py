"""Bounded ordinary primary GETs after the independent initial seal."""
from pathlib import Path
from datetime import datetime, timezone
from urllib.request import urlopen
from urllib.error import HTTPError
from concurrent.futures import ThreadPoolExecutor
import json
import hashlib

P=Path(__file__).resolve().parent/'primary'
URLS={
 'OWR2007-14':'https://ems.press/content/serial-article-files/46100?nt=1',
 'Reznick2000':'https://reznick.web.illinois.edu/Paper34.pdf',
 'Schweighofer0511617':'https://arxiv.org/pdf/math/0511617',
 'Laurent2010update':'https://homepages.cwi.nl/~monique/files/moment-ima-update-new.pdf',
 'GCV2010':'https://perso.lip6.fr/Mohab.Safey/Articles/gcv_sos.pdf',
}


def fetch(pair):
 name,url=pair
 receipt={'started_UTC':datetime.now(timezone.utc).isoformat(),'requested_URL':url,'method':'ordinary GET','custom_headers':[],'retries':0}
 try:r=urlopen(url,timeout=40)
 except HTTPError as error:r=error
 with r:
  body=r.read();receipt.update(status=r.status,final_URL=r.geturl(),response_headers_in_received_order=list(r.headers.items()))
 actual=body.startswith(b'%PDF-');path=P/(name+('.pdf'if actual else'.response'))
 if path.exists()or(P/(name+'.receipt.json')).exists():raise FileExistsError(path)
 path.write_bytes(body)
 receipt.update(completed_UTC=datetime.now(timezone.utc).isoformat(),path=str(path),bytes=len(body),SHA256=hashlib.sha256(body).hexdigest(),actual_PDF=actual)
 (P/(name+'.receipt.json')).write_text(json.dumps(receipt,indent=2)+'\n')
 return{k:receipt[k]for k in ['status','path','bytes','SHA256','actual_PDF']}


if __name__=='__main__':
 P.mkdir(exist_ok=False)
 with ThreadPoolExecutor(max_workers=5)as pool:
  for receipt in pool.map(fetch,URLS.items()):print(json.dumps(receipt),flush=True)
