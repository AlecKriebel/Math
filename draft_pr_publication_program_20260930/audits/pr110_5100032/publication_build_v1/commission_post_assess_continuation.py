#!/usr/bin/env python3
"""Create an exact fresh root gate only after the new source review is complete."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,os,sys
A=Path(__file__).resolve().parents[1];D=A/'native_post_assess_continuation_v1_20261006'
def need(x,m):
 if not x:raise RuntimeError(m)
def can(x):return (json.dumps(x,sort_keys=True,ensure_ascii=False,indent=2,allow_nan=False)+'\n').encode()
def hp(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def pin(f):return {'path':str(f.relative_to(A)),**hp(f.read_bytes())}
def read(f):return json.loads(f.read_bytes())
adpath=Path(sys.argv[1]);need(adpath.is_relative_to(A),'Dedicated actual independent review')
program=D/'post_assess_continuation.py';phase=D/'native_acceptance_actions_v2.py';outer=A/'publication_build_v1/record_native_continuation.py';seed=D/'SEED_INVENTORY.json';packet=A/'native_actual_input_preparation_20261006/root_fresh_native_preflight_20261006/EXECUTION_INPUTS.json';failed=A/'ROOT_FAILED_NATIVE_RUN_AUTHENTICATION_20261006.json'
ad=read(adpath);need(ad['schema']=='pr110-post-assess-continuation-adversary/v1' and ad['actual_review'] is True and ad['clearance'] is True and ad['required_findings']==[] and ad['template_only'] is False and ad.get('fixture',False) is False and ad.get('simulated',False) is False,'Completed independent narrow preexecution review')
need(ad['program_pin']==pin(program) and ad['action_program_pin']==pin(phase) and ad['outer_launcher_pin']==pin(outer) and ad['packet_sha256']==hp(packet.read_bytes())['sha256'] and ad['seed_inventory_pin']==pin(seed),'Exact independent source/packet/seed/outer review')
rootpath=A/'ROOT_POST_ASSESS_PREEXECUTION_REVIEW_AUTHENTICATION_20261006.json';root=read(rootpath)
need(root['actual_review'] is True and root['required_findings']==[] and root['preexecution_clearance'] is True and root['adversary_pin']==pin(adpath) and root['program_pin']==pin(program) and root['action_program_pin']==pin(phase) and root['outer_launcher_pin']==pin(outer),'Root review fully complete before commissioning')
facts=read(failed);need(facts['actual_assess_once_success_authenticated'] is True and facts['safe_scope_stop_authenticated'] is True and facts['narrow_correction_pure_scope_replay_passed'] is True and facts['native_export_executed'] is False,'Actual failedrun independently authenticated')
g={'schema':'pr110-post-assess-continuation-commission/v1','role':'root','UTC':datetime.now(timezone.utc).isoformat(),'actual_root_PID':os.getpid(),'actual_review':True,'clearance':True,'required_findings':[],'template_only':False,'fixture':False,'simulated':False,'successful_existing_worker_and_failure_independently_authenticated':True,'narrow_empty_clear_holds_only':True,'no_reassessment_authorized':True,'program_pin':pin(program),'action_program_pin':pin(phase),'packet_pin':pin(packet),'seed_inventory_pin':pin(seed),'failed_run_root_authentication_pin':pin(failed),'adversary_pin':pin(adpath),'outer_launcher_pin':pin(outer),'root_preexecution_review_pin':pin(rootpath),'outer_startup_cwd':str(A.parents[2]),'outer_whole_deadline_seconds':300,'kernel_SIGKILL_before_child_registration_complete_containment_claimed':False}
f=D/'ROOT_CONTINUATION_GATE.json';need(not f.exists(),'Unique actual root continuation decision');f.write_bytes(can(g));print(json.dumps({'actual_root_PID':os.getpid(),'gate':str(f),'gate_pin':pin(f),'actual_continuation_executed':False}))
