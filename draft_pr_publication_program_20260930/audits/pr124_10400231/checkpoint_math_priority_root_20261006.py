"""One actual scoped PR124 math/priority checkpoint, only after a fresh writer handoff."""
from pathlib import Path
import datetime,hashlib,json,os,subprocess
A=Path(__file__).resolve().parent;P=A.parent.parent;C=P.parent
R=Path('/Users/alec/Documents/Math')
G='/opt/homebrew/Cellar/git/2.38.2/bin/git'
D=A/'actual_math_priority_root_checkpoint_20261006'
events=[]
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def sha(b):return hashlib.sha256(b).hexdigest()
def req(ok,msg):
 if not ok:raise RuntimeError(msg)
def dump(p,x):p.write_text(json.dumps(x,indent=2,sort_keys=True)+'\n')
def run(args,cwd=C):
 ch=subprocess.Popen([G,*args],cwd=cwd,stdout=subprocess.PIPE,stderr=subprocess.PIPE);out,err=ch.communicate()
 events.append({'argv':[G,*args],'cwd':str(cwd),'actual_child_PID':ch.pid,'UTC':now(),'exit_code':ch.returncode,'stdout_bytes':len(out),'stdout_sha256':sha(out),'stderr_bytes':len(err),'stderr_sha256':sha(err),'small_stdout':out.decode('utf8','replace') if len(out)<1000 else None,'stderr':err.decode('utf8','replace')})
 dump(D/'PROCESS_JOURNAL.json',{'actual_operator_PID':os.getpid(),'events':events})
 req(ch.returncode==0,'Actual Git step failed; inspect before any retry')
 return out
def pin(path):
 req(path.is_relative_to(C) and path.is_file() and not path.is_symlink(),'Regular owned path')
 req(not {'private_sources','__pycache__','private_backend'}.intersection(path.parts),'Private path rejected')
 req(path.suffix.lower() not in {'.pdf','.png','.html','.sqlite3','.zip'},'Private/binary body rejected')
 b=path.read_bytes();return {'path':str(path.relative_to(C)),'bytes':len(b),'sha256':sha(b)}
req(not D.exists(),'Prior actual checkpoint exists; inspect rather than repeat')
window=json.loads((A/'MATH_PRIORITY_WRITER_HANDOFF_20261006.json').read_text())
req(window['explicit_release_received'] and window['purpose']=='PR124 root-only math/priority audit checkpoint','Fresh specific handoff required')
BASE=window['remote_main'];req(len(BASE)==40,'Observed actual main')
grant_body=Path(window['grant_path']).read_bytes();req(sha(grant_body)==window['grant_sha256'],'Actual specific grant body')
grant=json.loads(grant_body)
def live_window():
 req(grant['granted'] and datetime.datetime.now(datetime.timezone.utc)<datetime.datetime.fromisoformat(grant['expires_UTC']),'Fresh writer window expired')
live_window()
req(grant['remote_main_expected_before']==BASE and grant['owner_thread_id']=='01a0f08c-564b-7a51-bc3c-09cc9990d0fd','Actual grant owner/base')
D.mkdir()
req(run(['branch','--show-current']).strip()==b'main','Remain main')
req(run(['rev-parse','HEAD']).decode().strip()==BASE,'Local main drift')
req(run(['ls-remote','origin','refs/heads/main']).decode().split()[0]==BASE,'Remote main drift')
req(not run(['diff','--cached','--name-only']),'Foreign index contents')
req(not run(['diff','--name-only','--diff-filter=ACMRTUXB']),'Foreign materialized tracked contents')
primary_names=run(['diff','--name-only','--diff-filter=ACMRTUXB','-z','--','draft_pr_descending_audit_20261002'],R).decode().split('\0')
primary_pins={x:{'bytes':(R/x).stat().st_size,'sha256':sha((R/x).read_bytes())} for x in primary_names if x}
primary_index=run(['diff','--cached','--raw','-z'],R)
primary_head=run(['rev-parse','HEAD'],R).decode().strip()
req(primary_head==grant['ROOT_primary_local_HEAD_observed_tool'] and not primary_index,'Primary checkout/index grant invariants')
for x in grant['held_ROOT_descending_bodies']:
 b=Path(x['path']).read_bytes();req(len(b)==x['bytes'] and sha(b)==x['sha256'],'Granted held root body changed before checkpoint')
plan=json.loads((A/'MATH_PRIORITY_CHECKPOINT_PLAN_20261006.json').read_text())
req(sha((A/'MATH_PRIORITY_CHECKPOINT_PLAN_20261006.json').read_bytes())==grant['concrete_plan']['sha256'],'Reviewed concrete plan')
req(plan['owned_new_public_member_count']==226 and len(plan['owned_new_public_members'])==226,'Concrete prepared scope')
selected={}
for x in plan['owned_new_public_members']:
 p=C/x['path'];actual=pin(p);req(actual==x,'Prepared owned body changed '+x['path']);selected[x['path']]=actual
priority=json.loads((A/'ROOT_PRIORITY_GATE_20261006.json').read_text())
req(priority['counterexample_valid'] and not priority['publication_clearance'] and not priority['ordered_cursor_may_advance'],'Bounded withheld priority gate')
auth=json.loads((A/'ROOT_PRIORITY_FAMILY_AUTHENTICATION_20261006.json').read_text())
req(auth['priority_public_member_count']==27 and auth['root_source_PDF_count']==11 and not auth['priority_clearance'],'Actual root priority authentication')
for group in [auth['original17_unchanged'],auth['mathematical47_members_unchanged']]+[x['members'] for x in auth['families']]:
 for x in group:
  b=(A/x['path']).read_bytes();req(len(b)==x['bytes'] and sha(b)==x['sha256'],'Authenticated body drift')
prior=json.loads((A/'actual_intake_root_checkpoint_20261006/RECEIPT.json').read_text())
req(prior['commit']=='6ca1f515a7efc798d0113821a75f7b351f0a32ce' and prior['changed_count']==87 and prior['all_changed_bodies_verified_in_index_commit_and_fetched_main'],'Actual previous checkpoint')
req(json.loads((A/'ACTUAL_INTAKE_WRITER_RELEASE_20261006.json').read_text())['writer_ownership_released'],'Previous actual release')
progress=P/'CURRENT_PROGRESS.json';old=progress.read_bytes();data=json.loads(old)
req(data['current_PR']==124 and data['fully_completed_count']==20 and len(data['published_PRs'])==11 and data['current_original_head']==priority['original_head'],'Ascending state/count drift')
stamp=now()
data.update({'UTC':stamp,'updated_UTC':stamp,'current_mathematical_clearance':True,'current_mathematical_audit_percent':100,
 'current_mathematical_remaining_findings':[],'current_mathematical_gate':'audits/pr124_10400231/MATHEMATICAL_SOURCE_GATE_20261006.json',
 'current_mathematical_root_actual_reproduction':'audits/pr124_10400231/ROOT_MATH_FAMILY_AUTHENTICATION_20261006.json',
 'current_source_authentication_complete':True,'current_source_authentication_percent':100,'current_priority_audit_percent':70,
 'current_bounded_priority_family_assignments_complete':True,'current_bounded_priority_family_assignments_percent':100,
 'current_priority_gate':'audits/pr124_10400231/ROOT_PRIORITY_GATE_20261006.json','current_priority_review':'audits/pr124_10400231/ROOT_PRIORITY_REVIEW_20261006.md',
 'current_priority_root_authentication':'audits/pr124_10400231/ROOT_PRIORITY_FAMILY_AUTHENTICATION_20261006.json',
 'current_priority_clearance':False,'current_novelty_established':False,'current_counterexample_valid':True,
 'current_old_all_prime_formal_consequence_verified':True,'current_explicit_prior_conjecture_refutation_located':False,
 'current_application_priority_unresolved':True,'current_blanket_already_solved_no_new_contribution_supported':False,
 'current_current_openness_established':False,'current_human_source_access_question_pending':True,'current_human_disposition_question_pending':False,
 'current_requested_source':'Vladimir Turaev, Torsions of3-dimensional Manifolds (2002), DOI10.1007/978-3-0348-7999-6, II.3/II.4.4/II.5, III.4.3; VIII.5 for realization scope',
 'current_book_chapters_read':False,'current_publication_preparation_percent':0,'current_publication_ready':False,
 'current_DOI':None,'current_Zenodo_published':False,'current_tracker_updated':False,'current_native_assessment_performed':False,
 'current_native_status_mutated':False,'current_new_central_proof_search_turns':0,'current_original_budget':'2/5',
 'current_PR_workflow_percent':35,'current_workflow_estimate_percent':35,'current_this_goal_turn_classification':'progress',
 'current_remaining_required_steps':'Obtain and audit material full-book statements, resolve application priority/current openness; only if cleared prepare paper and repeat fresh package reviews before Zenodo/tracker/merge. No blanket already_solved disposition established.',
 'current_math_priority_checkpoint_actual_receipt_pending_at_snapshot':True,
 'current_math_priority_checkpoint_actual_receipt':'audits/pr124_10400231/actual_math_priority_root_checkpoint_20261006/RECEIPT.json',
 'last_completed_late_release_audit_checkpoint_pending':False,'last_completed_late_release_audit_checkpoint_commit':prior['commit'],
 'last_completed_late_release_audit_checkpoint_note':'Actual six late PR117 final/release receipts committed in6ca intake checkpoint; its87 body and release receipts join this subsequent checkpoint. No self-commit claim.',
 'last_actual_intake_checkpoint_commit':prior['commit'],'last_actual_intake_checkpoint_release':'audits/pr124_10400231/ACTUAL_INTAKE_WRITER_RELEASE_20261006.json',
 'advance_to_next_PR_authorized_now':False,'next_numeric_intake_cursor':125,'next_eligible_PR_after_current_completion':None,
 'next_step':'Await/inspect Turaev2002 full chapters and resolve material priority/application source gap for PR124.',
 'remaining_current_step':'PR124 valid negative result, old formal antecedent verified, application priority unresolved.',
 'main_writer_owner_at_snapshot':'This chat exclusive root-only math/priority checkpoint; actual release follows verified remote body readback.',
 'persistent_goal_status':'active','persistent_goal_complete':False})
dump(progress,data)
line='\n'+stamp+': PR124 math/sourcePASS100% after three sealed families, actual root58 replays/47 public members, original17/2-of-5 preserved. Four bounded priority/contribution families sealed and root-authenticated27 members/11 primary PDFs; old all-prime formal consequence verified, explicit earlier conjecture application unlocated, current openness/application novelty unresolved. Turaev2002 book II/III material fulltext unavailable; human source-access question pending. No blanket already_solved or new-discovery clearance. Decisive priority70%, workflow35%, publication0%; program20/99=20.20%,11published; goalactive/incomplete. No PR/native/Zenodo/Sheet/paper action, no ordered advance, new central proof turns0. Actual previous6ca intake/release receipts included; shared primary/index and descending bodies preserved.\n'
for path in [P/'CURRENT_PROGRESS.md',P/'RESEARCH_LOG.md',A/'RESEARCH_LOG.md']:
 with path.open('a') as f:f.write(line)
extra=[progress,P/'CURRENT_PROGRESS.md',P/'RESEARCH_LOG.md',A/'RESEARCH_LOG.md',Path(__file__).resolve(),A/'MATH_PRIORITY_CHECKPOINT_PLAN_20261006.json',A/'MATH_PRIORITY_WRITER_HANDOFF_20261006.json',A/'MATH_PRIORITY_WRITER_REQUEST_API_RESPONSE_20261006.json']
for path in extra:selected[str(path.relative_to(C))]=pin(path)
selection=A/'MATH_PRIORITY_CHECKPOINT_SELECTION_20261006.json'
dump(selection,{'schema':'pr124-root-math-priority-exact-selection/v1','UTC':now(),'actual_precommit_operator_PID':os.getpid(),'base':BASE,'members':[selected[x] for x in sorted(selected)],'source_PDF_text_images_selected':False,'native_PR_services_actions':False,'all_families_stable_sealed':True,'self_hash_omitted':True})
selected[str(selection.relative_to(C))]=pin(selection)
run(['add','--',*sorted(selected)])
staged=set(run(['diff','--cached','--name-only','-z']).decode().split('\0'))-{''}
req(staged and staged<=set(selected),'Staged scope mismatch')
req(not run(['diff','--cached','--diff-filter=D','--name-only']),'Deletion staged')
for path in sorted(staged):
 b=run(['show',':'+path]);req(len(b)==selected[path]['bytes'] and sha(b)==selected[path]['sha256'],'Index body mismatch')
live_window()
run(['commit','-m','Audit PR124 mathematics and preserve unresolved application priority'])
commit=run(['rev-parse','HEAD']).decode().strip()
req(run(['rev-parse','HEAD^']).decode().strip()==BASE,'Unexpected parent')
changed=set(run(['diff-tree','--no-commit-id','--name-only','-r','-z',commit]).decode().split('\0'))-{''}
req(changed==staged,'Committed scope mismatch')
for path in sorted(staged):
 b=run(['show',commit+':'+path]);req(len(b)==selected[path]['bytes'] and sha(b)==selected[path]['sha256'],'Commit body mismatch')
live_window()
run(['push','origin','HEAD:refs/heads/main'])
req(run(['ls-remote','origin','refs/heads/main']).decode().split()[0]==commit,'Remote ref mismatch')
run(['fetch','--no-tags','--no-write-fetch-head','origin','refs/heads/main'])
req(run(['rev-parse','origin/main']).decode().strip()==commit,'Fetched main mismatch')
for path in sorted(staged):
 b=run(['show','origin/main:'+path]);req(len(b)==selected[path]['bytes'] and sha(b)==selected[path]['sha256'],'Fetched full-body mismatch')
req(not run(['diff','--cached','--name-only']),'Index remains staged')
req(not run(['diff','--name-only','--diff-filter=ACMRTUXB']),'Materialized tracked edit remains')
req(run(['diff','--cached','--raw','-z'],R)==primary_index,'Primary index changed')
req(run(['rev-parse','HEAD'],R).decode().strip()==primary_head,'Primary checkout HEAD changed')
for path,x in primary_pins.items():
 b=(R/path).read_bytes();req(len(b)==x['bytes'] and sha(b)==x['sha256'],'Held descending body changed')
for x in grant['held_ROOT_descending_bodies']:
 b=Path(x['path']).read_bytes();req(len(b)==x['bytes'] and sha(b)==x['sha256'],'Granted eight held bodies changed')
receipt={'schema':'pr124-actual-root-math-priority-checkpoint/v1','UTC':now(),'actual_operator_PID':os.getpid(),'base':BASE,'commit':commit,'selected_count':len(selected),'changed_count':len(staged),'changed_members':[selected[x] for x in sorted(staged)],'nonforce_push_passed':True,'all_changed_bodies_verified_in_index_commit_fetched_main':True,'shared_index_and_materialized_tracked_clean':True,'primary_index_unchanged':True,'primary_HEAD_unchanged':primary_head,'granted_eight_held_bodies_unchanged':True,'held_primary_descending_bodies_unchanged':primary_pins,'mathematical_source_PASS':True,'priority_clearance':False,'application_priority_unresolved':True,'book_source_access_question_pending':True,'program_completed':20,'published':11,'current_PR':124,'workflow_completion_estimate_percent':35,'persistent_goal_active':True,'persistent_goal_complete':False,'native_PR_Zenodo_Sheet_actions':False,'writer_release_pending':True,'previous_progress_sha256':sha(old),'this_receipt_not_part_of_its_own_commit':True}
dump(D/'RECEIPT.json',receipt)
print(json.dumps({k:v for k,v in receipt.items() if k not in ['changed_members','held_primary_descending_bodies_unchanged']},sort_keys=True))
