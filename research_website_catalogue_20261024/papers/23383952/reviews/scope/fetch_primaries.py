"""Only after EARLY_SEAL: actual primary bodies in preignored cache.
Independent ordinary HTTPS requests; no author-code execution or source edits.
"""
from pathlib import Path
from datetime import datetime,timezone
import json,hashlib,urllib.request,urllib.error,concurrent.futures,subprocess
from pypdf import PdfReader
E=Path(__file__).resolve().parent;assert (E/'EARLY_SEAL.json').is_file();C=E/'cache/primary';C.mkdir(parents=True,exist_ok=True)
tasks=[('owr2009-06.pdf','https://ems.press/content/serial-article-files/46205'),('ammann-jammes-2008.pdf','https://ammann.app.uni-regensburg.de/preprints/supdir/supdir.pdf'),('ammann-jammes-v1.pdf','https://arxiv.org/pdf/0708.0529v1'),('morpurgo-final-response','https://projecteuclid.org/journals/duke-mathematical-journal/volume-114/issue-3/Sharp-inequalities-for-functional-integrals-and-traces-of-conformally-invariant/10.1215/S0012-7094-02-11433-1.pdf'),('morpurgo-author-page.html','https://www.researchgate.net/publication/38337286_Sharp_inequalities_for_functional_integrals_and_traces_of_conformally_invariant_operators')]
def now():return datetime.now(timezone.utc).isoformat()
def get(task):
 name,url=task;p=C/name;assert not p.exists();start=now()
 try:
  req=urllib.request.Request(url,headers={'User-Agent':'IndependentResearchPrimaryCustody/1.0'})
  try:r=urllib.request.urlopen(req,timeout=45)
  except urllib.error.HTTPError as err:r=err
  with r:b=r.read(12*1024*1024+1);status=r.status;headers=list(r.headers.items());final=r.url
  assert len(b)<=12*1024*1024;p.write_bytes(b)
  rec={'requested_url':url,'started_utc':start,'completed_utc':now(),'HTTP_status':status,'final_url':final,'response_headers':headers,'path':str(p),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest(),'PDF_magic':b.startswith(b'%PDF-')}
  if rec['PDF_magic']:
   rec['pages']=len(PdfReader(p).pages);out=subprocess.run(['/opt/homebrew/bin/pdftotext','-layout',str(p),'-'],capture_output=True,check=True,timeout=40).stdout;txt=p.with_suffix('.full-text.txt');txt.write_bytes(out);rec['text_extract']={'path':str(txt),'bytes':len(out),'sha256':hashlib.sha256(out).hexdigest()}
  return rec
 except Exception as err:return {'requested_url':url,'started_utc':start,'completed_utc':now(),'error_type':type(err).__name__,'error':str(err),'no_actual_PDF_asserted':True}
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:receipts=list(pool.map(get,tasks))
out=E/'primary-fetch-receipts.json';assert not out.exists();out.write_text(json.dumps({'utc':now(),'acquired_after_own_early_seal':True,'requests_in_listed_order':receipts},indent=2,ensure_ascii=False)+'\n')
print(json.dumps(receipts,indent=2,ensure_ascii=False))
