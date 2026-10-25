#!/usr/bin/env python3
"""Acquire only the explicitly selected public primary URLs; no downloaded code runs."""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import datetime, hashlib, json, urllib.request

E = Path(__file__).resolve().parent
C = E / 'primary-cache'
URLS = {
 'gualtieri-tube': 'https://www.math.toronto.edu/mgualt/courses/17-1300/docs/17-1300-notes-11.pdf',
 'whitney1936-osu': 'https://people.math.osu.edu/davis.12/courses/6701/whitney36.pdf',
 'marugame-v1': 'https://arxiv.org/pdf/2103.10102v1',
 'amari1997-riken': 'https://bsi-ni.brain.riken.jp/database/file/166/169.pdf',
 'matumoto-doi': 'https://doi.org/10.32917/hmj/1206128255',
 'lauritzen-IMS-doi': 'https://doi.org/10.1214/lnms/1215467061',
 'lauritzen-bibliography': 'https://web.math.ku.dk/~lauritzen/publications.html',
}

def fetch(item):
 name,url=item
 r={'name':name,'url':url,'started_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()}
 try:
  req=urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0'})
  with urllib.request.urlopen(req,timeout=25) as res:
   b=res.read(20000000)
   r.update(status=res.status,final_url=res.url,content_type=res.headers.get('Content-Type'))
  suffix='.pdf' if b.startswith(b'%PDF') else '.html'
  p=C/(name+suffix)
  p.write_bytes(b)
  r.update(path=str(p),bytes=len(b),sha256=hashlib.sha256(b).hexdigest(),pdf_magic=b.startswith(b'%PDF'))
 except Exception as exc:
  r['error']=str(exc)
 r['finished_utc']=datetime.datetime.now(datetime.timezone.utc).isoformat()
 return r

if __name__=='__main__':
 C.mkdir(exist_ok=True)
 with ThreadPoolExecutor(max_workers=4) as ex: rows=list(ex.map(fetch,URLS.items()))
 out={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'scope':'One bounded request per selected known primary URL; raw bodies only in wholly ignored primary-cache. Failed DOI bodies are not treated as read.','requests':rows}
 (E/'primary-acquisition-receipt.json').write_text(json.dumps(out,indent=2)+'\n')
 print(json.dumps(out,indent=2))
