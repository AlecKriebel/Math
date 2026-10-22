#!/usr/bin/env python3
"""Fresh primary-source byte identities; retain no third-party PDF/text bodies."""
from pathlib import Path
from datetime import datetime,timezone
from concurrent.futures import ThreadPoolExecutor
from hashlib import sha256
from urllib.request import Request,urlopen
from pypdf import PdfReader
from io import BytesIO
import json,re
ROOT=Path(__file__).resolve().parent
requests=[
 ('OWR full report','https://ems.press/content/serial-article-files/46677?nt=1','10b9fc68562190e98239377547967474944026cab1eef1aa10f31cbeb0c3363c'),
 ('NT arxiv PDF','https://arxiv.org/pdf/1412.1857','2a2605de55aa34fb89a28283e9ea36cfa02b42ba5aa378928ceed3a9cbd49915'),
 ('Hildebrand PDF','https://arxiv.org/pdf/1305.4814','f4562fe72265016838254e309f35038d42cc1cf72202c62448079e7d3d73a36a'),
 ('Roy-Xiao PDF','https://optimization-online.org/wp-content/uploads/2018/01/6441.pdf',None),
 ('DTV arxiv v2 PDF','https://arxiv.org/pdf/2509.10263v2','df11c946ad11073881ad5274a08edc3f25f4f1cbb153a5c36388d24ea717ad76'),
 ('DTV author PDF','https://www.math.uwaterloo.ca/~ltuncel/publications/2509.10263.pdf','df11c946ad11073881ad5274a08edc3f25f4f1cbb153a5c36388d24ea717ad76'),
 ('DTV v2 HTML','https://arxiv.org/html/2509.10263v2',None),
 ('DTV version record','https://arxiv.org/abs/2509.10263',None)]
def run(item):
 name,url,pin=item
 try:
  with urlopen(Request(url,headers={'User-Agent':'Mozilla/5.0'}),timeout=30) as r:body=r.read();final=r.url;status=r.status
  result={'source':name,'url':url,'final_url':final,'http_status':status,'bytes':len(body),'sha256':sha256(body).hexdigest(),'retrieved_at_utc':datetime.now(timezone.utc).isoformat()}
  if pin:result['matches_pinned_identity']=result['sha256']==pin
  if body.startswith(b'%PDF-'):
   doc=PdfReader(BytesIO(body));texts=[page.extract_text() or ''for page in doc.pages];text='\n'.join(texts)
   result['pages']=len(texts);result['negative_curvature_phrase_occurrences']=len(re.findall('negative\\s+curvature',text,re.I));result['relevant_page_numbers']={}
   for phrase in ['Open Problems','Theorem 3.2','Theorem 2.','Does every','June 16, 2026']:
    hits=[i+1 for i,t in enumerate(texts)if phrase in t]
    if hits:result['relevant_page_numbers'][phrase]=hits
   if name=='OWR full report':result['original_existential_question_at_printed799']=bool(re.search('Does there exist an algebraic convex cone',texts[28]));result['algebraic_defined_by_homogeneous_inequalities']=bool(re.search('homogeneous multivariate polynomial inequalities',texts[28]))
   if name.startswith('DTV'):result['internal_revision_date']='June 16, 2026' if 'June 16, 2026' in texts[0] else 'not matched';result['universal_question_present']=bool(re.search('Does every convex cone admit',text))
   if name=='Roy-Xiao PDF':result['theorem2_nonnegative_power_cone_page3']='nonnegative power cone' in texts[2] and 'Theorem 2' in texts[2]
  else:
   text=body.decode('utf-8')
   if name=='DTV v2 HTML':result['internal_revision_date']='August 24, 2026' if 'August 24, 2026' in text else 'not matched'
   if name=='DTV version record':result['v2_June12_2026_record']=bool(re.search(r'12 Jun 2026',text))
  return result
 except Exception as e:return {'source':name,'url':url,'error':str(e),'retrieved_at_utc':datetime.now(timezone.utc).isoformat()}
with ThreadPoolExecutor(max_workers=4) as pool:results=list(pool.map(run,requests))
ledger=(ROOT/'tmp/unpacked/audits/priority_01/SEARCH_LEDGER.md').read_text()
queries=ledger.split('```text\n',1)[1].split('```',1)[0].splitlines()
result={'checked_at_utc':datetime.now(timezone.utc).isoformat(),'fresh_primary_source_results':results,'archived_independent_query_count':len(queries),'archived_query_ledger_sha256':sha256(ledger.encode()).hexdigest(),'scope':'Fresh identity/definition/attribution checks, not a repetition of all 65 searches or worldwide priority certification. All primary bodies parsed only in memory and discarded.','coverage_limits_verified_in_archive':['Hildebrand 2017 habilitation HTTP404 uninspected lead','Hildebrand 2026 version-of-record subscription full text not inspected','OpenReview direct HTTP403 / verification redirect','Guler1997 and Hildebrand2014 primary abstract/record only'],'failed_fresh_attempts_before_this_script':['DOI resolver via web.open returned inaccessible; publisher full-report PDF and author contribution succeeded','Initial guessed MFO handle identified an unrelated 2018 report and was discarded.']}
(ROOT/'source_scope_results.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
