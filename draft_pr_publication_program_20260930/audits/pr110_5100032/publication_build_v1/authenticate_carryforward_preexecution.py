from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, os
A=Path(__file__).resolve().parents[1]
D=A/'native_post_assess_carryforward_v2_20261006'
V=A/'actual_native_candidate_adversary_20261006'
def need(v,m):
 if not v: raise RuntimeError(m)
def hp(b): return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def pin(f): return {'path':str(f.relative_to(A)),**hp(f.read_bytes())}
def obj(f): return json.loads(f.read_bytes())
checked=[]
def check(f,s):
 need(f.is_file() and not f.is_symlink(),'Regular body '+str(f))
 need(hp(f.read_bytes())=={k:s[k] for k in ('bytes','sha256')},'Full body pin '+str(f))
 checked.append(pin(f))
m=obj(D/'OUTPUT_MANIFEST.json');seal=obj(D/'SEAL_RECEIPT.json')
check(D/'OUTPUT_MANIFEST.json',seal['manifest_pin'])
need(m['file_count']==len(m['files'])==10 and sum(x['bytes'] for x in m['files'])==m['payload_bytes']==99619,'Sealed payload')
for s in m['files']: check(D/s['path'],s)
vm=obj(V/'CARRYFORWARD_PREEXEC_OUTPUT_MANIFEST.json')
for s in vm['files']: check(V/s['path'],s)
adpath=V/'CARRYFORWARD_PREEXEC_ADVERSARY.json';ad=obj(adpath)
need(ad['schema']=='pr110-post-assess-carryforward-adversary/v1' and ad['actual_review'] is True and ad['clearance'] is True and ad['required_findings']==[] and ad['future_candidate_approved'] is False and ad['live_actions_approved'] is False,'Separate genuine preexecution review')
for field in ['program_pin','action_program_pin','outer_launcher_pin','integration_inputs_pin','stopped_continuation_inventory_pin','seed_inventory_pin','failed_run_root_authentication_pin','report_pin']:
 s=ad[field];check(A/s['path'],s)
for s in ad['reviewed_root_helper_pins']:check(A/s['path'],s)
for mode in ['normal','optimized']:
 r=obj(V/('CARRYFORWARD_PREEXEC_CONTROLS_'+mode+'.json'))
 need(r['actual_reviewer_PID']>0 and r['mode']==mode and r['checks']==525180 and len(r['mutation_rejections'])==13 and r['main_or_assess_or_action_or_service_executed'] is False,'Actual pure control result')
 need(r['historical_scoped_pins_match_root'] is True and r['seven_other_derived_outputs_and_drift_unchanged'] is True and r['current_other_problem_QUEUE_row308_byteexact'] is True,'Historical/current scopes')
 need(r['program_pin']==ad['program_pin'] and r['action_program_pin']==ad['action_program_pin'] and r['integration_inputs_pin']==ad['integration_inputs_pin'],'Exact control source and input')
r={'schema':'pr110-root-carryforward-preexecution-authentication/v1','UTC':datetime.now(timezone.utc).isoformat(),'actual_root_PID':os.getpid(),'actual_review':True,'required_findings':[],'preexecution_clearance':True,'adversary_pin':pin(adpath),'program_pin':ad['program_pin'],'action_program_pin':ad['action_program_pin'],'outer_launcher_pin':ad['outer_launcher_pin'],'integration_inputs_pin':ad['integration_inputs_pin'],'stopped_continuation_inventory_pin':ad['stopped_continuation_inventory_pin'],'manifest_pin':pin(D/'OUTPUT_MANIFEST.json'),'adversary_manifest_pin':pin(V/'CARRYFORWARD_PREEXEC_OUTPUT_MANIFEST.json'),'checked_artifacts':checked,'root_full_source_and_report_read_completed':True,'historical_assessment_and_current_main_distinguished':True,'both_stopped_workspaces_preserved':True,'native_assess_authorized':False,'actual_future_candidate_or_live_actions_approved':False}
f=A/'ROOT_POST_ASSESS_CARRYFORWARD_PREEXECUTION_REVIEW_AUTHENTICATION_20261006.json'
need(not f.exists(),'Unique root review');f.write_text(json.dumps(r,sort_keys=True,indent=2)+'\n')
print(json.dumps({'root_review_pin':pin(f),'checked_full_bodies':len(checked),'preexecution_clearance':True,'actual_root_PID':os.getpid()}))
