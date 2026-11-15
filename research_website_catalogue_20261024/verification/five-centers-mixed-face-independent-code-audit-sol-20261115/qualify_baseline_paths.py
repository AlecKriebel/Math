#!/usr/bin/env python3
"""Resolve a source-only planning locator from the newly authorized actual baseline."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json
A=Path(__file__).resolve().parent
if (A/'BASELINE_SEAL.json').exists():raise RuntimeError('baseline immutable')
def load(p):return json.loads(p.read_bytes())
def sha(b):return hashlib.sha256(b).hexdigest()
def pin(p):
 b=p.read_bytes();return {'path':str(p),'bytes':len(b),'SHA256':sha(b)}
def put(n,x):
 p=A/n;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
now=datetime.now(timezone.utc).isoformat()
old=load(A/'EXPECTED_OUTPUT_PATHS.json');actual=load(A/'FRESH_WEBSITE_BASELINE.json')
paths={e['public_relative_path'] for e in actual['public_files']}
if 'research/sitemap.xml' not in paths or 'sitemap.xml' in paths:raise ValueError('unexpected actual sitemap namespace')
for e in old['paths']:
 if e['kind']=='aggregate_exact_existing_locations_preserved_plus_two_new_locations':
  if e['website_relative_path']!='sitemap.xml':raise ValueError('unexpected initial planning locator')
  e['website_relative_path']='research/sitemap.xml'
old['actual_website_baseline_inspected']=True
old['qualification']='Only previously unmeasured aggregate sitemap locator resolved from actual authorized baseline; initial sealed proposal is unchanged.'
put('ACTUAL_EXPECTED_OUTPUT_PATHS.json',old)
g=load(A/'FRESH_GIT_OBSERVATIONS.json');put('private/baseline-diagnostics/first-protection-scope.json',g)
raw=Path(g['raw_index_records']['path']).read_bytes();excluded={('public/'+e['website_relative_path']).encode() for e in old['paths']}
records=raw.split(b'\0');records=records[:-1] if records[-1]==b'' else records
kept=[e for e in records if e.split(b'\t',1)[1] not in excluded];b=b'\0'.join(kept)+b'\0'
q=A/'private/baseline-blobs'/sha(b)
if not q.exists():q.write_bytes(b)
g['excluded_future11_gitpaths']=sorted(x.decode() for x in excluded);g['fresh_protected_index_record_count']=len(kept);g['fresh_protected_raw_records']=pin(q);g['scope_qualification']='Actual sitemap is research/sitemap.xml; raw index observation reused exactly, no new Git action.'
put('FRESH_GIT_OBSERVATIONS.json',g)
# A phase log was inadvertently appended to the sealed initial log. Retain the diagnostic and restore exact original bytes.
log=A/'RESEARCH_LOG.md';current=log.read_bytes();entry=next(e for e in load(A/'INITIAL_MANIFEST.json')['files'] if e['path']==str(log))
if sha(current)!=entry['SHA256']:
 original=b''.join(current.splitlines(keepends=True)[:-1])
 if len(original)!=entry['bytes'] or sha(original)!=entry['SHA256']:raise ValueError('cannot recover exact initial log')
 q=A/'private/baseline-diagnostics/initial-log-with-accidental-append.txt';q.write_bytes(current);log.write_bytes(original)
 logfix={'temporary_initial_log_append_occurred':True,'whole_diagnostic':pin(q),'original_exact_bytes_and_SHA_restored':pin(log)}
else:logfix={'temporary_initial_log_append_occurred':False}
put('BASELINE_PATH_QUALIFICATION.json',{'UTC':now,'initial_proposal':pin(A/'EXPECTED_OUTPUT_PATHS.json'),'actual_contract':pin(A/'ACTUAL_EXPECTED_OUTPUT_PATHS.json'),'original_initial_artifacts_remain_exact_at_phase_close':True,'initial_aggregate_locator':'sitemap.xml','actual_authorized_aggregate_locator':'research/sitemap.xml','basis':'Independent fresh actual614 public namespace and preceding authorized installation exact gitpaths','source_main_or_scientific_content_change':False,'protected_records_corrected_from_same_exact_fresh_raw_observation':len(kept),'initial_log_diagnostic':logfix})
(A/'BASELINE_RESEARCH_LOG.md').write_text('# Authorized baseline checkpoint log\n\n- '+now+' — 40% overall audit: Fresh actual46773fd3… master baseline614public/92typed+visibleindex/93sitemap captured before writer exposure. Source-only aggregate locator resolved to actual research/sitemap.xml; initial expectation payloads unchanged. Fresh58552 protected records derived from58554 current raw index entries excluding only two currently present authorized aggregate entries. Temporary initial-log append restored to its exact sealed bytes; phase log is separate. Original17 core files plus authorized405b checkpoint qualification intact. Await writer FINAL.\n')
print(json.dumps({'status':'ACTUAL_AGGREGATE_SCOPE_QUALIFIED','protected_records':len(kept),'initial_log_exact':pin(log)['SHA256']==entry['SHA256']}))
