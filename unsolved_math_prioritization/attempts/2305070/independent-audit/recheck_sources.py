#!/usr/bin/env python3
"""Fresh read-only source checks; retain receipts, never redistribute corpora/PDFs."""
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path
import hashlib,json,time,urllib.request
BASE=Path(__file__).resolve().parent.parent
OUT=Path(__file__).resolve().parent
EXPECTED=json.loads((BASE/'public/SOURCE_MANIFEST.json').read_text())
SPECS=[
 ('problems',EXPECTED['upstream_dataset']['problems']),
 ('research_results',EXPECTED['upstream_dataset']['research_results']),
 ('primary_statement',dict(EXPECTED['primary_statement'],url=EXPECTED['primary_statement']['pdf_url'])),
 ('related_article',dict(EXPECTED['related_article'],url=EXPECTED['related_article']['author_pdf'])),
]
def check(spec):
 name,record=spec;t=time.monotonic();r={'name':name,'url':record['url'],'checked_at_utc':datetime.now(timezone.utc).isoformat()}
 try:
  with urllib.request.urlopen(record['url'],timeout=45) as response:
   b=response.read();r.update(http_status=response.status,final_url=response.url.split("?")[0])
  h=hashlib.sha256(b).hexdigest()
  r.update(bytes=len(b),sha256=h,bytes_match=len(b)==record['bytes'],sha256_matches=h==record['sha256'])
  if name=='problems':
   j=json.loads(b);sel=[x for x in j if x.get('id')==2305070]
   r.update(records=len(j),selected_count=len(sel),selected_matches_saved=sel==json.loads((BASE/'private/selected-problems.json').read_text()))
  if name=='research_results':
   j=json.loads(b);key='AMR-022-5070'
   r.update(selected_present=key in j,selected_matches_saved={key:j[key]}==json.loads((BASE/'private/selected-research_results.json').read_text()))
  r['passed']=r['bytes_match'] and r['sha256_matches'] and r.get('selected_matches_saved',True)
 except Exception as e:r.update(passed=False,error=type(e).__name__+': '+str(e))
 r['elapsed_seconds']=round(time.monotonic()-t,3);return r
with ThreadPoolExecutor(max_workers=3) as pool:checks=list(pool.map(check,SPECS))
result={'checked_at_utc':datetime.now(timezone.utc).isoformat(),'source_checks':checks,'passed':all(x['passed'] for x in checks),'retention':'Only hashes, sizes, URLs, and selected-record equality results retained; no raw source documents or full corpora saved.'}
(OUT/'source_recheck.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
print(json.dumps(result,indent=2,sort_keys=True))
