from pathlib import Path
import ast,datetime,hashlib,json,runpy
R=Path(__file__).resolve().parent;A=R.parents[1];T=A.parents[1];P=A/'publication';D=R/'deployed'
def binding(p):b=p.read_bytes();return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def require(value,message):
 if not value:raise RuntimeError(message)
receipt=json.loads((R/'ACTUAL_DEPLOYMENT_RECEIPT.json').read_text());checks=[]
for entry in receipt['files']:
 p=Path(entry['path']);require(binding(p)=={k:entry[k] for k in ['bytes','sha256']},'Actual deployment drift '+str(p))
 relative=p.relative_to(T);mirror=D/relative;require(mirror.read_bytes()==p.read_bytes(),'Mirror/actual bytes differ '+str(p))
 require(not any(isinstance(n,ast.Assert) for n in ast.walk(ast.parse(p.read_text()))),'Assertion validation '+str(p));checks.append({'path':str(p),**binding(p),'mirror_exact':True})
v=runpy.run_path(str(P/'verification/verify.py'));s=json.loads((A/'SUBMITTED_SNAPSHOT.json').read_text());v['authenticate_snapshot'](A/'submitted',s);current_status='pending';correction=None
if (A/'CURRENT_EDITION_CORRECTION.json').exists():
 record=json.loads((A/'CURRENT_EDITION_CORRECTION.json').read_text());ctx={'edition_mode':'documented_correction','source_bindings':{'submitted_snapshot_sha256':binding(A/'SUBMITTED_SNAPSHOT.json')['sha256'],'current_edition_correction_sha256':binding(A/'CURRENT_EDITION_CORRECTION.json')['sha256'],'current_edition':record['current_files']}};v['authenticate_source_bindings'](A,A,ctx);current_status='documented_correction_authenticated_at_observation';correction={'receipt':binding(A/'CURRENT_EDITION_CORRECTION.json'),'changed_files':[entry['path'] for entry in record['changes']],'current_files':record['current_files']}
else:
 v['authenticate_current'](A/'current_edition',{'edition_mode':'preserve_submitted'},A/'submitted');current_status='still_original_at_observation'
c=runpy.run_path(str(T/'publication_coordinators/pr1280.py'));kit=c['load_exact_kit']();require(getattr(kit,'pr1280_exact_verifier',False),'Strict wrapper not installed')
blocked=None
if not (P/'FINAL_REVIEW_GATE.json').exists():
 try:c['authenticate_release']()
 except FileNotFoundError as error:require(Path(error.filename)==P/'FINAL_REVIEW_GATE.json','Unexpected missing release input');blocked='Missing actual final review gate prevents any deposit-kit call'
 else:raise RuntimeError('Missing gate did not block')
print(json.dumps({'at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'pr':1280,'problem_id':30003587,'checked_files':checks,'deployed_helpers':len(checks),'exact_original_files':9,'original_bytes':sum(e['bytes'] for e in s['files']),'actual_current_edition_status':current_status,'actual_current_correction_observation':correction,'current_edition_observation_policy':'Current edition may evolve through a new explicit root correction receipt before the final review freeze. This records actual bytes/time, not permanent current-edition immutability. Runtime helpers reauthenticate the then-current context and correction.','no_assert_statements':True,'pinned_kit_sha256':binding(T.parent/'zenodo_deposit_tool/zenodo.py')['sha256'],'strict_wrapper_loaded_without_network':True,'pending_publication_guard':blocked,'scope':'Read-only actual deployed hashes/AST/mirror comparison, original packet authentication and strict-wrapper import. No package, source, context, metadata, approval, remote operation or publication result is fabricated.'},indent=2))
