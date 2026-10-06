"""Rebind reviewed unchanged native postimages across an actual peer checkpoint."""
from pathlib import Path
import datetime,hashlib,json,os,subprocess,sys
A=Path(__file__).resolve().parent;P=A.parent.parent;C=P.parent
GIT='/opt/homebrew/Cellar/git/2.38.2/bin/git';BASE=sys.argv[1];events=[]
def req(v,s):
 if not v:raise RuntimeError(s)
def sha(b):return hashlib.sha256(b).hexdigest()
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def load(p):return json.loads(p.read_text())
def run(args):
 start=now();ch=subprocess.Popen([GIT,*args],cwd=C,stdout=subprocess.PIPE,stderr=subprocess.PIPE);out,err=ch.communicate();events.append({'argv':[GIT,*args],'PID':ch.pid,'UTC_start':start,'UTC_end':now(),'exit_code':ch.returncode,'stdout_bytes':len(out),'stdout_sha256':sha(out),'stderr_bytes':len(err),'stderr_sha256':sha(err)});req(ch.returncode==0,'Read-only transport check');return out
path=A/'POST_PEER_MAIN_TRANSPORT_AUTHENTICATION_20261006.json';req(not path.exists(),'Authenticate actual transport once')
prep_path=A/'native_published_obstruction_preparation_20261006/CORRECTED_PREPARED_RECEIPT_V2.json';prep=load(prep_path)
req(sha(prep_path.read_bytes())=='cbcc2d7ada7ccd6d08bec3a8871c42ed3bed7ed5bf5d379ce33663e2cfd747fe','Exact sealed V2')
old=prep['base_commit'];oldplan=load(A/'PUBLISHED_OBSTRUCTION_CHECKPOINT_PLAN_20261006.json')
req(BASE!=old and len(BASE)==40,'Actual distinct new checkpoint')
req(run(['ls-remote','origin','refs/heads/main']).decode().split()[0]==BASE,'Actual peer remote head')
req(run(['rev-parse','HEAD']).decode().strip()==old and run(['branch','--show-current']).strip()==b'main','Unmutated isolated main')
req(not run(['diff','--cached','--raw','-z']) and not run(['diff','--name-only','--diff-filter=ACMRTUXB']),'No staged/materialized changes')
run(['fetch','--no-tags','--no-write-fetch-head','origin','refs/heads/main'])
req(run(['rev-parse','origin/main']).decode().strip()==BASE,'Exact fetched actual head')
run(['merge-base','--is-ancestor',old,BASE])
req(run(['rev-list','--parents','-n','1',BASE]).decode().split()==[BASE,old],'Peer checkpoint exact sole parent')
verified=[]
for item in prep['source_inputs']+oldplan['existing_program_preimages']:
 b=run(['show',BASE+':'+item['path']]);req(len(b)==item['bytes'] and sha(b)==item['sha256'],'Peer changed source/program preimage '+item['path']);verified.append({'path':item['path'],'bytes':len(b),'sha256':sha(b)})
for item in prep['proposed_native_pins']:
 b=Path(item['prepared_local_path']).read_bytes();req(len(b)==item['bytes'] and sha(b)==item['sha256'],'Prepared postimage unchanged')
changed=[s for s in run(['diff-tree','--no-commit-id','--name-only','-r','-z',old,BASE]).decode().split('\0') if s]
req(all(s.startswith('draft_pr_descending_audit_20261002/') for s in changed),'Peer checkpoint unexpectedly touches other program scope')
physical=[]
for name in changed:
 dest=C/name;body=run(['show',BASE+':'+name]);req(not dest.is_symlink(),'Changed peer path symlink')
 req(not dest.exists() or (dest.is_file() and dest.read_bytes()==body),'Changed peer physical path conflicts before advancement')
 physical.append({'path':name,'new_bytes':len(body),'new_sha256':sha(body),'observed_absent':not dest.exists()})
record={'schema':'pr124-actual-post-peer-unchanged-native-source-transport/v1','UTC':now(),'actual_operator_PID':os.getpid(),'prepared_base':old,'actual_new_main':BASE,'current_local_main_before_fresh_writer_window':old,'exact_V2_prepared_receipt_sha256':sha(prep_path.read_bytes()),'all12_native_source_inputs_and4_program_preimages_unchanged':True,'verified_preimages':verified,'peer_changed_paths':changed,'peer_changed_physical_preflight':physical,'peer_changed_physical_paths_absent_or_equal_new_main':True,'peer_changes_only_descending_program':True,'fast_forward_ancestry_verified':True,'all15_reviewed_postimages_unchanged':True,'native_commands_repeated':False,'new_history_proof_events':0,'main_index_worktree_mutations':False,'remote_tracking_fetch_only':True,'fresh_concrete_grant_and_guarded_local_main_fast_forward_still_required':True,'events':events}
path.write_text(json.dumps(record,indent=2,sort_keys=True)+'\n');print(json.dumps({'UTC':record['UTC'],'PID':os.getpid(),'actual_new_main':BASE,'verified_preimages':len(verified),'peer_changed_paths':len(changed),'sha256':sha(path.read_bytes())},sort_keys=True))
