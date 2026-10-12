"""Read-only verification of effective assertions, receipts and immutable V1."""
from pathlib import Path
import json,hashlib,os,datetime
B=Path(__file__).resolve().parent;V1=B.parent
def check(p,e):
 d=p.read_bytes();assert len(d)==e['bytes'] and hashlib.sha256(d).hexdigest()==e['sha256'],p
counts={}
for name,pathkey in [('PUBLIC_MANIFEST.json','relative_path'),('PRIVATE_CUSTODY_MANIFEST.json','private_relative_path')]:
 m=json.loads((V1/name).read_text())
 for e in m['files']:check(V1/e[pathkey],e)
 counts['V1_'+name]=len(m['files'])
binding=json.loads((B/'V1_IMMUTABLE_BINDINGS.json').read_text())
for k in ['V1_public_manifest','V1_private_custody_manifest','V1_report','V1_verdict']:check(V1/binding[k]['relative_path'],binding[k])
for line in (B/'CLI_LEDGER.jsonl').read_text().splitlines():
 c=json.loads(line)
 for stream in ['stdout','stderr']:check(B/'_private'/(c['label']+'.'+stream),{'bytes':c[stream+'_bytes'],'sha256':c[stream+'_sha256']})
for p in B.glob('*.json'):json.loads(p.read_text())
sources=json.loads((B/'SOURCES_AND_READ_SCOPE.json').read_text())
pins=0
for s in sources['sources']:
 for key in ['private_source_body_pin','private_full_extract_pin','private_relevant_extract_pin','V2_relevant_extract_pin']:
  if key in s:check(B/s[key]['relative_path'],s[key]);pins+=1
v=json.loads((B/'VERDICT.json').read_text());assert v['effective_version']=='corrected_v2' and v['priority_established_percent']==0 and v['new_central_proof_search_approaches']==0
r=next(s for s in json.loads((B/'NOVELTY_MATRIX.json').read_text())['rows'] if s['source']=='S3')
assert 'Zero flow charges can retain fixed-cost Steiner support' in r['exact_gap']
report=(B/'REPORT.md').read_text()
assert 'Steiner-type hardness retains the flow term' not in report
assert 'Removing that term changes the problem to minimum arborescence' not in report
assert 'fixed-cost Steiner support problem' in report and 'conditional statement for the independent pricing problem' in report
z=json.loads((B/'TILK_ZERO_FLOW_RESULTS.json').read_text());assert z['optional_zero_demand_case']['fixed_cost']==1 and z['all_positive_demand_case']['fixed_cost']==6
for key in ['candidate_proof','original_source_pdf','gate']:
 e=json.loads((B/'INPUT_BINDINGS.json').read_text())[key];check(B/e['path'],e)
print(json.dumps({'UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'operator_PID':os.getpid(),'V1_immutable_verified':True,'V1_file_counts':counts,'existing_source_pins_checked':pins,'effective_assertion_replacement_verified':True,'zero_flow_boundary_check_verified':True,'all_V2_JSON_valid':True}))
