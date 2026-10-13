"""Read-only concrete scope for a fresh coordinated main writer window."""
from pathlib import Path
import datetime,hashlib,json,os,subprocess,sys
A=Path(__file__).resolve().parent;P=A.parent.parent;C=P.parent
GIT='/opt/homebrew/Cellar/git/2.38.2/bin/git'; BASE=sys.argv[1]
def req(v,s):
 if not v:raise RuntimeError(s)
def sha(b):return hashlib.sha256(b).hexdigest()
def load(p):return json.loads(p.read_text())
def git(*args):return subprocess.check_output([GIT,*args],cwd=C)
def pin(p):
 req(p.is_file() and not p.is_symlink(),'Regular public body')
 req(not {'private_sources','private_renders','private_backend','__pycache__'}.intersection(p.parts),'Private body')
 req(p.suffix.lower() not in {'.pdf','.png','.html','.sqlite','.sqlite3','.zip'},'Private source binary')
 b=p.read_bytes();return {'path':str(p.relative_to(C)),'bytes':len(b),'sha256':sha(b)}
path=A/'PUBLISHED_OBSTRUCTION_CHECKPOINT_PLAN_AFTER_PEER_20261006.json';req(not path.exists(),'Freeze plan once')
ready=load(A/'ROOT_NATIVE_PUBLISHED_OBSTRUCTION_PROTOCOL_READY_20261006.json');req(ready['fresh_protocol_PASS'],'Fresh sealed native protocol review')
prep=load(A/'native_published_obstruction_preparation_20261006/CORRECTED_PREPARED_RECEIPT_V2.json')
transport_path=A/'POST_PEER_MAIN_TRANSPORT_AUTHENTICATION_20261006.json';transport=load(transport_path)
req(prep['base_commit']==transport['prepared_base'] and BASE==transport['actual_new_main'] and prep['new_native_commands_in_v2']==0,'Actual unchanged transported baseline')
transport_protocol=load(A/'ROOT_POST_PEER_TRANSPORT_PROTOCOL_READY_20261006.json');req(transport_protocol['PASS'] and transport_protocol['transport_authentication_sha256']==sha(transport_path.read_bytes()),'Fresh transport protocol PASS')
req(git('rev-parse','HEAD').decode().strip()==transport['current_local_main_before_fresh_writer_window'] and git('branch','--show-current').strip()==b'main','Local main baseline')
req(git('ls-remote','origin','refs/heads/main').decode().split()[0]==BASE,'Remote main baseline')
req(not git('diff','--cached','--name-only') and not git('diff','--name-only','--diff-filter=ACMRTUXB'),'Shared tracked/index untouched')
tracked=[P/'CURRENT_PROGRESS.json',P/'CURRENT_PROGRESS.md',P/'RESEARCH_LOG.md',A/'RESEARCH_LOG.md']
oldpins=[]
for p in tracked:
 b=git('show',BASE+':'+str(p.relative_to(C)));req(p.read_bytes()==b,'Tracked program preimage');oldpins.append(pin(p))
names=git('ls-files','--others','--exclude-standard','-z','--',str(A.relative_to(C))).decode().split('\0')
members=[pin(C/n) for n in names if n]
native_existing=[x['path'] for x in prep['proposed_native_pins'] if any(z['path']==x['path'] for z in prep['source_inputs'])]
newnative=[x['path'] for x in prep['proposed_native_pins'] if x['path'] not in native_existing]
req(len(native_existing)==9 and len(newnative)==6,'Exact native export scope')
future=['PUBLISHED_OBSTRUCTION_CHECKPOINT_PLAN_AFTER_PEER_20261006.json','PUBLISHED_OBSTRUCTION_WRITER_HANDOFF_20261006.json','PUBLISHED_OBSTRUCTION_WRITER_REQUEST_API_RESPONSE_20261006.json','PUBLISHED_OBSTRUCTION_CHECKPOINT_SELECTION_20261006.json','ROOT_CLOSURE_COMPLETION_20261006.json','COMPLETION_METADATA_SELECTION_20261006.json','actual_native_published_obstruction_checkpoint_20261006/RECEIPT.json','actual_native_published_obstruction_checkpoint_20261006/PROCESS_JOURNAL.json','actual_completion_metadata_20261006/RECEIPT.json','actual_completion_metadata_20261006/PROCESS_JOURNAL.json','actual_final_completion_readback_20261006/RECEIPT.json','actual_final_completion_readback_20261006/PROCESS_JOURNAL.json','FINAL_COMPLETION_RELEASE_API_RESPONSE_20261006.json','FINAL_COMPLETION_OWNER_RELEASE_20261006.json']
record={'schema':'pr124-concrete-published-obstruction-native-completion-plan/v1','UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'actual_preparer_PID':os.getpid(),'observed_main':BASE,'current_local_main_before_guarded_fast_forward':transport['current_local_main_before_fresh_writer_window'],'transport_authentication_sha256':sha(transport_path.read_bytes()),'guarded_local_main_fast_forward_to_actual_remote_planned':True,'purpose':'PR124 scoped published-obstruction native correction and completion','owned_new_public_members':sorted(members,key=lambda x:x['path']),'owned_new_public_member_count':len(members),'allowed_existing_tracked_updates':[str(p.relative_to(C)) for p in tracked]+native_existing,'existing_program_preimages':oldpins,'new_native_attempt_paths':newnative,'native_postimages':prep['proposed_native_pins'],'future_operational_members':future,'native_status':'already_solved','native_correction_scope':'Old published theorems imply original full family/general obstruction; express earlier named-conjecture refutation not established','original_budget':'2/5','new_central_proof_search_turns':0,'two_main_nonforce_checkpoints_planned':True,'program_count_before':20,'program_count_after_verified_native_completion':21,'published_count_unchanged':11,'PR_actual_closed_without_merge':True,'closing_comment':'https://github.com/AlecKriebel/Math/pull/124#issuecomment-6025266251','new_PR_comment_close_merge_actions':False,'paper_Zenodo_DOI_tracker_actions':False,'private_primary_source_bytes_excluded':True,'source_access_previous_hold_superseded':True,'fresh_explicit_writer_handoff_required':True,'primary_checkout_index_and_held_descending_bodies_must_remain_unchanged':True,'actual_full_remote_body_readbacks_then_explicit_writer_release_required':True,'main_index_native_updates_performed':False,'persistent_goal_status':'active'}
path.write_text(json.dumps(record,indent=2,sort_keys=True)+'\n')
print(json.dumps({'plan':str(path),'bytes':path.stat().st_size,'sha256':sha(path.read_bytes()),'owned_members':len(members),'existing_tracked_updates':len(record['allowed_existing_tracked_updates']),'new_native_paths':len(newnative),'observed_main':BASE},sort_keys=True))
