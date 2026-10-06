"""Actual scoped root-only PR124 intake checkpoint after fresh writer handoff."""
from pathlib import Path
import datetime,hashlib,json,os,subprocess
A=Path(__file__).resolve().parent;P=A.parent.parent;C=P.parent
R=Path('/Users/alec/Documents/Math')
G='/opt/homebrew/Cellar/git/2.38.2/bin/git'
BASE='4c0cf917d52223aa101881bdeab20e26534c65c5'
D=A/'actual_intake_root_checkpoint_20261006'
events=[]
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def sha(x):return hashlib.sha256(x).hexdigest()
def require(b,s):
 if not b:raise RuntimeError(s)
def dump(p,x):p.write_text(json.dumps(x,indent=2,sort_keys=True)+'\n')
def run(args,cwd=C):
 ch=subprocess.Popen([G,*args],cwd=cwd,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
 out,err=ch.communicate()
 events.append({'argv':[G,*args],'cwd':str(cwd),'PID':ch.pid,'UTC':now(),'exit_code':ch.returncode,'stdout_bytes':len(out),'stdout_sha256':sha(out),'stderr_bytes':len(err),'stderr_sha256':sha(err),'small_stdout':out.decode('utf8','replace') if len(out)<1000 else None,'stderr':err.decode('utf8','replace')})
 dump(D/'PROCESS_JOURNAL.json',{'actual_operator_PID':os.getpid(),'events':events})
 require(ch.returncode==0,'Actual Git step failed; inspect journal before retry')
 return out
def pin(path):
 require(path.is_relative_to(C) and path.is_file() and not path.is_symlink(),'Regular owned file')
 require(not {'private_sources','private_backend','runs','__pycache__'}.intersection(path.parts),'Private selection')
 body=path.read_bytes()
 return {'path':str(path.relative_to(C)),'bytes':len(body),'sha256':sha(body)}
require(not D.exists(),'Prior actual checkpoint exists; inspect instead of retrying')
D.mkdir()
window=json.loads((A/'ACTUAL_WRITER_HANDOFF_20261006.json').read_text())
require(window['explicit_release_received'] and window['remote_main']==BASE,'Fresh observed handoff')
require(run(['branch','--show-current']).strip()==b'main','Main branch required')
require(run(['rev-parse','HEAD']).decode().strip()==BASE,'Local main changed')
require(run(['ls-remote','origin','refs/heads/main']).decode().split()[0]==BASE,'Remote main changed')
require(not run(['diff','--cached','--name-only']),'Foreign index contents')
require(not run(['diff','--name-only','--diff-filter=ACMRTUXB']),'Foreign materialized tracked contents')
primary_paths=run(['diff','--name-only','--diff-filter=ACMRTUXB','-z','--','draft_pr_descending_audit_20261002'],R).decode().split('\0')
primary_pins={path:{'bytes':(R/path).stat().st_size,'sha256':sha((R/path).read_bytes())} for path in primary_paths if path}
primary_index=run(['diff','--cached','--raw','-z'],R)
auth=json.loads((A/'original_head_authentication_20261006/ORIGINAL_AUTHENTICATION.json').read_text())
require(auth['original_head']=='d110ad761291aa6ac1d66d2a49e8b8212c18bed6' and auth['original_budget']=='2/5' and auth['original_file_count']==17,'Authenticated original124')
for member in auth['original_files']:
 path=A/'original_head_authentication_20261006/original_attempt'/member['path']
 require(len(path.read_bytes())==member['bytes'] and sha(path.read_bytes())==member['sha256'],'Original body changed')
release=json.loads((P/'audits/pr117_30001234/FINAL_COMPLETION_OWNER_RELEASE_20261006.json').read_text())
require(release['same_head_closed_without_merge'] and release['all_latest_native_and_metadata_changed_bodies_verified'] and release['writer_ownership_released'] and release['metadata_checkpoint_commit']==BASE,'Actual prior completion/release')
intake=json.loads((P/'ordered_intake_20261006/after_PR117/INTAKE_AFTER_PR117.json').read_text())
require(intake['next_selected']['PR']==124 and intake['next_selected']['literal_status']=='claimed_solved','Next literal selected124')
progress=P/'CURRENT_PROGRESS.json';old=progress.read_bytes();data=json.loads(old)
require(data['current_PR']==117 and data['fully_completed_count']==20 and len(data['published_PRs'])==11,'Prior cursor/count')
snapshot=A/'PR117_COMMITTED_PROGRESS_AT_PR124_INTAKE_20261006.json'
require(not snapshot.exists(),'Prior snapshot exists');snapshot.write_bytes(old)
for key in list(data):
 if key.startswith('current_'):del data[key]
stamp=now()
data.update({'UTC':stamp,'updated_UTC':stamp,'current_PR':124,'current_problem_id':10400231,'current_code':'AMR-103-0231',
 'current_original_head':auth['original_head'],'current_original_literal_status':'claimed_solved','current_original_budget':'2/5',
 'current_source_authentication_complete':True,'current_source_authentication_percent':100,'current_sourcepair_record':'audits/pr124_10400231/original_head_authentication_20261006/SOURCEPAIR_AUTHENTICATION.json',
 'current_mathematical_clearance':False,'current_mathematical_audit_percent':75,'current_mathematical_remaining_findings':['Independent mathematical/source families must seal and pass root authentication/reproduction before clearance'],
 'current_original_assert_guard_weakness_repaired_in_separate_diagnostic_copies':True,'current_repaired_diagnostics':'audits/pr124_10400231/repaired_diagnostics_v1',
 'current_new_central_proof_search_turns':0,'current_priority_audit_percent':0,'current_priority_clearance':False,'current_novelty_established':False,
 'current_publication_preparation_percent':0,'current_publication_ready':False,'current_DOI':None,'current_Zenodo_published':False,'current_tracker_updated':False,
 'current_native_assessment_performed':False,'current_native_status_mutated':False,'current_PR_workflow_percent':15,'current_workflow_estimate_percent':15,
 'current_human_disposition_question_pending':False,'current_human_source_access_question_pending':False,'current_this_goal_turn_classification':'progress',
 'current_remaining_required_steps':'Complete independent math/source gate; only then bounded deep priority, appropriate disposition, publication package and fresh review loop if novelty supports a full original resolution.',
 'last_completed_metadata_checkpoint_commit':release['metadata_checkpoint_commit'],'last_completed_final_completion_readback':'audits/pr117_30001234/FINAL_COMPLETION_OWNER_RELEASE_20261006.json',
 'last_completed_record':'audits/pr117_30001234/FINAL_COMPLETION_OWNER_RELEASE_20261006.json','last_completed_actual_final_gate':'audits/pr117_30001234/actual_final_completion_readback_20261006/RECEIPT.json',
 'last_completed_audit_checkpoint_push_pending':False,'last_completed_late_release_audit_checkpoint_pending':True,
 'last_completed_late_release_audit_checkpoint_note':'Actual117 final/release receipts selected for this checkpoint; actual new commit/readback joins its separate receipt, no self-commit claim.',
 'latest_ordered_intake_record':'ordered_intake_20261006/after_PR117/INTAKE_AFTER_PR117.json',
 'completion_metadata_checkpoint_pending_at_snapshot':False,'advance_to_next_PR_authorized_now':False,
 'next_numeric_intake_cursor':125,'next_eligible_PR_after_current_completion':None,
 'next_step':'Authenticate sealed independent math/source reviews for124, then deep bounded priority if mathPASS.',
 'remaining_current_step':'PR124 integral topology, order and source audit.',
 'main_writer_owner_at_snapshot':'This chat: exclusive root-only intake checkpoint; actual release follows remote body readback.',
 'skipped_since_last_completion':[{k:row[k] for k in ['PR','literal_status','effort']} for row in intake['ascending_status_only_rows'] if not row['eligible']],
 'persistent_goal_status':'active','persistent_goal_complete':False})
dump(progress,data)
line='\n'+stamp+': PR117 actually complete/released at4c0cf917;20/99=20.20%,11published. PR118–123literalunsolved skipped by status only. PR124/10400231 incomingclaimed_solved2/5 head d110ad761291aa6ac1d66d2a49e8b8212c18bed6 selected;17 original bodies/full nonempty prior authenticated,8967author/13154independent normal outputs reproduced, guard-only diagnostic repair additive. Primary full-page target/order conventions read, no scope mismatch found. Independent math/source families active, clearance pending. Math/source75%, workflow15%, priority0%, publication0%; new central proof turns0; no PR/native/Zenodo/tracker mutation. Goal active/incomplete.\n'
for path in [P/'RESEARCH_LOG.md',P/'CURRENT_PROGRESS.md',A/'RESEARCH_LOG.md']:
 with path.open('a') as f:f.write(line)
selected={progress,P/'RESEARCH_LOG.md',P/'CURRENT_PROGRESS.md',snapshot,Path(__file__).resolve()}
selected.update(x for x in A.iterdir() if x.is_file() and not x.is_symlink() and x.suffix in {'.py','.md','.json'})
for folder in ['original_head_authentication_20261006','actual_original_object_acquisition_20261006','root_reproduction_20261006','repaired_diagnostics_v1','root_primary_sources_20261006']:
 for path in (A/folder).rglob('*'):
  if not path.is_file():continue
  relative=path.relative_to(A/folder)
  if {'private_sources','runs','author_normal','author_optimized','independent_normal','independent_optimized','__pycache__'}.intersection(relative.parts):continue
  selected.add(path)
selected.update(x for x in (P/'ordered_intake_20261006/after_PR117').rglob('*') if x.is_file())
previous=P/'audits/pr117_30001234'
for rel in ['FINAL_COMPLETION_OWNER_RELEASE_20261006.json','ACTUAL_FINAL_RELEASE_API_RESPONSE_20261006.json','actual_completion_metadata_20261006/RECEIPT.json','actual_completion_metadata_20261006/PROCESS_JOURNAL.json','actual_final_completion_readback_20261006/RECEIPT.json','actual_final_completion_readback_20261006/PROCESS_JOURNAL.json']:
 selected.add(previous/rel)
pins={str(x.relative_to(C)):pin(x) for x in selected}
selection=A/'INTAKE_ROOT_CHECKPOINT_SELECTION_20261006.json'
dump(selection,{'UTC':now(),'base':BASE,'schema':'pr124-root-only-intake-selection/v1','members':[pins[x] for x in sorted(pins)],'active_family_files_selected':False,'private_PDFs_text_renders_selected':False,'native_PR_service_mutations':False,'self_hash_omitted':True})
pins[str(selection.relative_to(C))]=pin(selection)
run(['add','--',*sorted(pins)])
staged=set(run(['diff','--cached','--name-only','-z']).decode().split('\0'))-{''}
require(staged and staged<=set(pins),'Staged scope mismatch')
require(not run(['diff','--cached','--diff-filter=D','--name-only']),'Deletion staged')
for path in sorted(staged):
 body=run(['show',':'+path]);require(len(body)==pins[path]['bytes'] and sha(body)==pins[path]['sha256'],'Index body mismatch')
run(['commit','-m','Authenticate PR124 counterexample intake and preserve completed PR117 receipts'])
commit=run(['rev-parse','HEAD']).decode().strip()
require(run(['rev-parse','HEAD^']).decode().strip()==BASE,'Unexpected parent')
changed=set(run(['diff-tree','--no-commit-id','--name-only','-r','-z',commit]).decode().split('\0'))-{''}
require(changed==staged,'Committed scope mismatch')
for path in sorted(staged):
 body=run(['show',commit+':'+path]);require(len(body)==pins[path]['bytes'] and sha(body)==pins[path]['sha256'],'Committed body mismatch')
run(['push','origin','HEAD:refs/heads/main'])
require(run(['ls-remote','origin','refs/heads/main']).decode().split()[0]==commit,'Actual remote readback mismatch')
run(['fetch','--no-tags','--no-write-fetch-head','origin','refs/heads/main'])
require(run(['rev-parse','origin/main']).decode().strip()==commit,'Fetched ref mismatch')
for path in sorted(staged):
 body=run(['show','origin/main:'+path]);require(len(body)==pins[path]['bytes'] and sha(body)==pins[path]['sha256'],'Fetched body mismatch')
require(not run(['diff','--cached','--name-only']),'Index not empty')
require(not run(['diff','--name-only','--diff-filter=ACMRTUXB']),'Foreign materialized tracked edits after checkpoint')
require(run(['diff','--cached','--raw','-z'],R)==primary_index,'Primary index changed')
for path,pinned in primary_pins.items():
 body=(R/path).read_bytes();require(len(body)==pinned['bytes'] and sha(body)==pinned['sha256'],'Held primary descending body changed')
receipt={'schema':'pr124-root-only-intake-checkpoint-actual/v1','UTC':now(),'actual_operator_PID':os.getpid(),'base':BASE,'commit':commit,
 'selected_count':len(pins),'changed_count':len(staged),'changed_members':[pins[x] for x in sorted(staged)],'nonforce_push_passed':True,
 'all_changed_bodies_verified_in_index_commit_and_fetched_main':True,'index_and_materialized_tracked_changes_empty':True,
 'primary_index_unchanged':True,'held_primary_descending_bodies_unchanged':primary_pins,'active_family_files_selected':False,
 'native_PR_Zenodo_Sheet_mutations':False,'program_completed':20,'published':11,'current_PR':124,'math_source_estimate_percent':75,
 'workflow_estimate_percent':15,'persistent_goal_status':'active','goal_complete':False,'writer_release_pending':True}
dump(D/'RECEIPT.json',receipt)
print(json.dumps({k:v for k,v in receipt.items() if k not in ['changed_members','held_primary_descending_bodies_unchanged']},sort_keys=True))

