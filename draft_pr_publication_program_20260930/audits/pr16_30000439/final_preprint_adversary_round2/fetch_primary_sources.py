"""Fresh round-two read-only primary-source retrieval; payloads stay ignored."""
from pathlib import Path
import concurrent.futures, datetime, hashlib, json, subprocess, urllib.request
ROOT=Path(__file__).resolve().parent
CACHE=ROOT/'tmp'/'sources'; CACHE.mkdir(parents=True,exist_ok=True)
SOURCES={
'owr2006':'https://ems.press/content/serial-article-files/46044',
'brehm_sarkaria1992':'https://archive.mpim-bonn.mpg.de/id/eprint/1946/1/preprint_1992_52.pdf',
'newman_v3':'https://arxiv.org/pdf/2212.09576v3',
'lee_nevo_v1':'https://arxiv.org/pdf/2307.14195v1',
'lee_nevo_v3':'https://arxiv.org/pdf/2307.14195v3',
'goodman_pollack1986':'https://link.springer.com/content/pdf/10.1007/BF02187696.pdf',
'frieze_karonski2026':'https://www.math.cmu.edu/~af1p/BOOK.pdf',
'lee_nevo_published':'https://link.springer.com/content/pdf/10.1007/s00454-026-00856-4.pdf',
'brehm_schild1995':'https://www.math.ucdavis.edu/~deloera/MISC/LA-BIBLIO/trunk/BrehmUlli/Brehm4.pdf',
}
def fetch(item):
 key,url=item; r={'key':key,'requested_url':url,'accessed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()}
 try:
  with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0'}),timeout=45) as response:
   raw=response.read(); r.update(resolved_url=response.url,content_type=response.headers.get('Content-Type'))
  assert raw.startswith(b'%PDF-'), 'non-PDF response'
  path=CACHE/(key+'.pdf');path.write_bytes(raw)
  result=subprocess.run(['pdftotext','-layout',str(path),str(CACHE/(key+'.txt'))],capture_output=True,text=True)
  r.update(status='success',sha256=hashlib.sha256(raw).hexdigest(),bytes=len(raw),payload=str(path.relative_to(ROOT)),pdftotext_returncode=result.returncode)
 except Exception as error:r.update(status='failed',error=repr(error))
 return r
with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:records=list(pool.map(fetch,SOURCES.items()))
(ROOT/'FRESH_SOURCE_LEDGER.json').write_text(json.dumps(records,indent=2)+'\n')
print(json.dumps(records,indent=2))
