#!/usr/bin/env python3
"""Independently bind cached primary identities and candid scopes; no downloads."""
from pathlib import Path
import json,hashlib
R=Path(__file__).resolve().parent; A=R.parents[1]; rows=[];failed=[]
v=json.loads((A/'reviews/priority01/SOURCE_LEDGER.json').read_bytes())
for e in v['entries']:
 if not e.get('cache_path'):
  assert 'error' in e;failed.append({'name':e['name'],'error':e['error'],'scope':e['read_scope']});continue
 f=A/'reviews/priority01'/e['cache_path'];b=f.read_bytes();assert hashlib.sha256(b).hexdigest()==e['sha256'];assert len(b)==e['bytes']
 rows.append({'family':'priority01','name':e['name'],'sha256':e['sha256'],'read_scope':e.get('read_scope'),'version':e.get('version')})
 if e.get('extracted_text'):
  t=e['extracted_text'];f=A/'reviews/priority01'/t['cache_path'];assert hashlib.sha256(f.read_bytes()).hexdigest()==t['sha256'];rows.append({'family':'priority01','name':t['cache_path'],'sha256':t['sha256'],'extracted_text_only':True})
v=json.loads((A/'reviews/priority02/SOURCE_RECEIPT.json').read_bytes())
for category in ['pdf_sources','cached_web_records']:
 for e in v[category]:
  filename=e.get('cache_pdf',e.get('cache'));f=A/'reviews/priority02'/filename;b=f.read_bytes();assert hashlib.sha256(b).hexdigest()==e['sha256'];assert 'bytes' not in e or len(b)==e['bytes']
  rows.append({'family':'priority02','name':filename,'sha256':e['sha256'],'read_scope':e.get('read_locations',e.get('read_scope')),'version':e.get('version')})
res={'status':'PASS','cached_hash_records_verified':len(rows),'priority01_source_records':25,'priority01_extracted_text_records':10,'priority02_source_records':12,'entries':rows,'failed_acquisition_records_not_treated_as_text':failed,'harness_note':'Initial inline reader assumed every entry had cache_path; it stopped on an explicitly failed download record. This corrected reader distinguishes failed records. This was a review-harness schema assumption, not a package defect.','limits':'Cache identity verifies source versions, not historical completeness or truth. Own source reads recorded separately.'}
assert len(rows)==47
(R/'SOURCE_HASH_RECHECK.json').write_text(json.dumps(res,indent=2)+'\n');print(json.dumps({k:v for k,v in res.items() if k not in ['entries','failed_acquisition_records_not_treated_as_text']},indent=2))
