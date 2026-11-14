"""Read-only final custody and exact execution-receipt verifier; no network.
The mathematical proof and primary reading extents are in the sealed reports.
"""
from pathlib import Path
import json,hashlib,zipfile,subprocess,os,argparse
E=Path(__file__).resolve().parent;R=E.parents[1];S=R/'sources';G=R.parents[2]
ap=argparse.ArgumentParser();ap.add_argument('--current-local-git',action='store_true');args=ap.parse_args()
def sha(b):return hashlib.sha256(b).hexdigest()
def check(p,r):
 b=p.read_bytes();assert len(b)==r['bytes'] and sha(b)==r['sha256'],str(p);return b
fm=json.loads((E/'FINAL_MANIFEST.json').read_text());fs=json.loads((E/'FINAL_SEAL.json').read_text());assert sha((E/'FINAL_MANIFEST.json').read_bytes())==fs['manifest_sha256']
actual={str(p.relative_to(E)) for p in E.rglob('*') if p.is_file() and not any(x in ['cache','tmp'] for x in p.relative_to(E).parts)}
assert actual=={r['path'] for r in fm['files']}|{'FINAL_MANIFEST.json','FINAL_SEAL.json'}
for r in fm['files']:check(E/r['path'],r)
cache=json.loads((E/'CACHE_MANIFEST.json').read_text())
for r in cache['files']:check(E/r['path'],r)
early=json.loads((E/'EARLY_SEAL.json').read_text());assert sha((E/'EARLY_MANIFEST.json').read_bytes())==early['manifest_sha256']
for r in json.loads((E/'EARLY_MANIFEST.json').read_text())['files']:check(E/r['path'],r)
sm=json.loads((S/'SOURCE_FINAL_MANIFEST.json').read_text());ss=json.loads((S/'SOURCE_FINAL_SEAL.json').read_text());check(S/'SOURCE_FINAL_MANIFEST.json',ss['manifest'])
for r in sm['files']:check(S/r['path'],r)
assert {str(p.relative_to(S)) for p in S.rglob('*') if p.is_file()}=={r['path'] for r in sm['files']}|{'SOURCE_FINAL_MANIFEST.json','SOURCE_FINAL_SEAL.json'}
ready=json.loads((S/'SOURCE_READY.json').read_text());rs=json.loads((S/'SOURCE_READY_SEAL.json').read_text());assert sha((S/'SOURCE_READY_MANIFEST.json').read_bytes())==rs['manifest_sha256']
for r in json.loads((S/'SOURCE_READY_MANIFEST.json').read_text())['files']:check(S/r['path'],r)
api=json.loads((S/'record.raw.json').read_text());latest=json.loads((S/'latest.raw.json').read_text());versions=json.loads((S/'versions.raw.json').read_text())
assert api['id']==23383952 and api['metadata']['version']=='1.0.0'
assert latest['id']==api['id'] and latest['metadata']==api['metadata'] and latest['files']==api['files']
assert versions['hits']['total']==1 and versions['hits']['hits'][0]['id']==api['id']
assert [a['original_api_file_object'] for a in ready['all_assets_in_original_order']]==api['files']
for a in ready['all_assets_in_original_order']:
 b=check(Path(a['path']),a);assert hashlib.md5(b).hexdigest()==a['md5'] and a['original_api_file_object']['checksum']=='md5:'+a['md5']
receipts=json.loads((S/'api-receipts.json').read_text());assert len(receipts)==5 and all(r['HTTP_status']==200 and r['fresh_ordinary_HTTPS'] for r in receipts)
for r in receipts:check(Path(r['body']['path']),r['body'])
archive=json.loads((S/'archive-members.json').read_text());members=archive['members'];assert len(members)==142 and len(archive['archive_containers'])==4
for c in archive['archive_containers']:
 if '::' not in c['container']:p=S/c['container']
 else:
  parent,name=c['container'].rsplit('::',1);p=Path(next(r['extracted_path'] for r in members if r['container']==parent and r['original_member_name']==name))
 assert sha(p.read_bytes())==c['sha256']
 with zipfile.ZipFile(p) as z:
  group=[r for r in members if r['container']==c['container']];assert len(z.infolist())==len(group)
  for r in group:
   b=z.read(r['original_member_name']);assert len(b)==r['bytes'] and sha(b)==r['sha256'];assert check(Path(r['extracted_path']),r)==b
pdf=S/'weighted-yamabe-heat-trace-note.pdf';embedded=S/'published-source/note.pdf';assert pdf.read_bytes()==embedded.read_bytes()
aj=json.loads((E/'AJ2008_INPLACE_CUSTODY.json').read_text());check(Path(aj['original_path']),aj)
base=json.loads((E/'PRESERVATION_BEFORE.json').read_text());count=0
for r in base['files']:
 p=Path(r['path'])
 if p.is_relative_to(G/'.git') and not args.current_local_git:continue
 check(p,r);count+=1
if args.current_local_git:
 for ref,value in base['resolved_Git_refs'].items():assert subprocess.run(['git','rev-parse',ref],cwd=G,env={**os.environ,'GIT_OPTIONAL_LOCKS':'0'},capture_output=True,check=True).stdout.decode().strip()==value
execution=json.loads((E/'EXECUTION_RECEIPTS.json').read_text());assert len(execution['runs'])==8
for r in execution['runs']:
 assert r['returncode']==r['expected_returncode']
 for k in ['stdout','stderr']:check(Path(r[k]['path']),r[k])
assert sha((S/'published-source/trace_audit_01/check_trace_bounds.py').read_bytes())==execution['supplied_source_sha256']
v=json.loads((E/'verdict.json').read_text());assert v['status']=='FINITE_WEIGHTED_YAMABE_COUNTEREXAMPLE_SURVIVES_INDEPENDENT_SOURCE_SCOPE_REVIEW' and not v['publication_authority'] and v['follow_up'] is None
assert json.loads((E/'PRESERVATION_AFTER.json').read_text())['changed_originals']==[]
from fractions import Fraction as F
calc=json.loads((E/'execution/supplied-trace.stdout.txt').read_text());own=json.loads((E/'execution/independent-rational.stdout.txt').read_text())
limits=[629002,631338,636143,639464,641172,641202,639541]
values=[F(calc['small_time_bound_exact'])]+[F(r['bound_exact']) for r in calc['middle_intervals']]
assert all(q<F(c,10**6) for q,c in zip(values,limits))
assert all(F(q)<F(c,10**6) for q,c in zip(own['seven_exact_upper_bounds'],limits))
assert F(calc['cylinder_lower_exact'])==F(own['lower_exact'])==F(1106714561,1700054750)
assert F(calc['cylinder_lower_minus_13_over_20'])==F(3357947,3400109500)
print(json.dumps({'status':'PASS','owned_payload_files':len(fm['files']),'cache_and_render_bindings':len(cache['files']),'source_final_bindings':len(sm['files']),'original_ZIP_members':len(members),'execution_runs':8,'prior_originals_rehashed':count,'current_local_Git_required':args.current_local_git,'network_or_writes':False}))
