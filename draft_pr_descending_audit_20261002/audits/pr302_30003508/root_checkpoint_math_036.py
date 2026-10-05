"""One literal PR302 mathematical checkpoint on main, with guarded release.

No PR, native QUEUE, DOI, tracker, or preprint action is authorized here.
"""
from pathlib import Path
from datetime import datetime,timezone,timedelta
import ast,copy,fcntl,gzip,hashlib,json,os,signal,stat,subprocess,sys,types
if sys.flags.optimize:raise RuntimeError('Unoptimized execution required')
A=Path(__file__).resolve().parent;P=A.parent.parent;R=P.parent
W=A/'math_checkpoint_036_preparation';PLAN=W/'CONTENT_PLAN.json';S=P/'SHARED_GIT_WINDOW_STATUS.json'
utc=lambda:datetime.now(timezone.utc).isoformat();sha=lambda b:hashlib.sha256(b).hexdigest()
load=lambda p:json.loads(Path(p).read_bytes())
def pin(p):
 p=Path(p);b=p.read_bytes();return dict(path=str(p),bytes=len(b),sha256=sha(b),mode=oct(stat.S_IMODE(p.stat().st_mode)))
def require(v,msg):
 if not v:raise RuntimeError(msg+'; do not retry any mutation without fresh read-only reconciliation')
def names(b):return {x.decode() for x in b.split(b'\0') if x}
def main():
 lock=(W/'ACTUAL_WRITER.lock').open('a+b');fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
 plan=load(PLAN);source=pin(__file__);planpin=pin(PLAN);control=load(S)
 lease=control['descending_302_math_checkpoint_lease']
 require(not control['shared_git_writes_paused'] and not control['descending_writer_window_released'],'Current scope inactive')
 require(lease['source']==source and lease['plan']==planpin and lease['scope']=='PR302 exact mathematical checkpoint only' and lease['allowed_paths']==plan['allowed_paths'],'Literal scope binding differs')
 require(not control.get('ascending_pr85_math_checkpoint_window_granted') and control.get('ascending_pr85_math_checkpoint_complete_and_released'),'Peer release missing')
 base=current=plan['starting_main'];require(base=='2e0162fbb5773d0c1b41bfaa9f461bc474338902','Starting main differs')
 owned=set(plan['allowed_paths']);targets=plan['targets'];require(len(owned)==len(targets)+1 and str(PLAN.relative_to(R)) in owned,'Duplicate/literal plan scope')
 expected={e['target']:(R/e['input']['path']).read_bytes() for e in targets};expected[str(PLAN.relative_to(R))]=PLAN.read_bytes()
 actual=A/'math_checkpoint_036_actual_private';require(not actual.exists(),'A previous checkpoint attempt exists');actual.mkdir()
 (actual/'ATTEMPT.json').write_text(json.dumps(dict(UTC=utc(),operator=source,plan=planpin,token=lease['token'],automatic_retry=False),indent=2)+'\n')
 # Use the exact previously adversarially reviewed complete native recorder.
 framework=P/'audits/pr305_5100034/root_during_peer_pause_20261005/native_integration_preparation/integrate_pr305.py'
 require(pin(framework)['sha256']=='0ea02436c0ac1e0070169df466c34ba141c43291e16515b3fd1cce2135071897','Native recorder source differs')
 tree=ast.parse(framework.read_bytes());fn=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='main');node=next(n for n in fn.body if isinstance(n,ast.FunctionDef) and n.name=='run')
 factory=ast.parse('def factory(actual):\n count=0\n return run\n').body[0];factory.body.insert(1,copy.deepcopy(node));module=ast.fix_missing_locations(ast.Module(body=[factory],type_ignores=[]))
 env=dict(Path=Path,datetime=datetime,timezone=timezone,timedelta=timedelta,hashlib=hashlib,json=json,stat=stat,os=os,sys=sys,subprocess=subprocess,gzip=gzip,signal=signal,R=R,g=types.SimpleNamespace(pin=pin),sha=sha,utc=utc,require=require,__file__=str(Path(__file__).resolve()))
 exec(compile(module,str(framework)+'::unchanged_run_AST','exec'),env);run=env['factory'](actual)
 def git(*args):return run(['/usr/bin/git','--no-optional-locks',*args])
 require(git('branch','--show-current')==b'main\n' and git('rev-parse','HEAD').decode().strip()==base,'Initial main drift')
 require(not git('diff','--cached','--raw','-z') and not (R/'.git/MERGE_HEAD').exists(),'Initial index or merge busy')
 require(git('ls-remote',lease['endpoint'],'refs/heads/main').split()[0].decode()==base,'Remote baseline drift')
 index=git('ls-files','--stage','-z');flags=git('ls-files','-v','-z');dirty=names(git('diff','--name-only','-z','HEAD'))-owned
 foreign={p:pin(R/p) for p in dirty};diff=git('diff','--binary','HEAD','--',*sorted(dirty)) if dirty else b''
 def exclude(b):return b'\0'.join(x for x in b.split(b'\0') if x and (x.split(b'\t',1)[-1].decode() if b'\t' in x else x[2:].decode()) not in owned)
 prior=P/'audits/pr305_5100034/root_during_peer_pause_20261005/peer_pr85_math_checkpoint_window/KNOWN_HELD_INVENTORY.json'
 require(pin(prior)['sha256']=='a8f8ad508fa75f13a0e94a45d948a6b1b311d5a69ef76368219f41ee4f628de8','Previous known-path inventory drift')
 private_prefixes=[str((P/'audits/pr305_5100034/root_during_peer_pause_20261005').relative_to(R))+'/',
  'draft_pr_publication_program_20260930/audits/pr85_30001203/priority_direct_target_20261005/',
  'draft_pr_publication_program_20260930/audits/pr85_30001203/priority_covering_mechanism_20261005/',
  'draft_pr_publication_program_20260930/audits/pr85_30001203/original_source_authentication/process_evidence/']
 held={e['path']:pin(R/e['path']) for e in load(prior)['files'] if e['path'] not in owned and e['path']!=str(S.relative_to(R)) and not any(e['path'].startswith(x) for x in private_prefixes)}
 (actual/'KNOWN_HELD_AT_ACTUAL_START.json').write_text(json.dumps(dict(UTC=utc(),files=held,file_count=len(held),explicit_private_exclusions=private_prefixes),indent=2)+'\n')
 def stable():
  require(git('branch','--show-current')==b'main\n' and git('rev-parse','HEAD').decode().strip()==current,'Current main drift')
  require(names(git('diff','--name-only','-z','HEAD'))-owned==dirty and {p:pin(R/p) for p in dirty}==foreign,'Foreign dirty scope/body/mode drift')
  require((git('diff','--binary','HEAD','--',*sorted(dirty)) if dirty else b'')==diff,'Foreign whole diff drift')
  require(exclude(git('ls-files','--stage','-z'))==exclude(index) and exclude(git('ls-files','-v','-z'))==exclude(flags),'Whole foreign index/flags drift')
 def inputs():
  require(pin(__file__)==source and pin(PLAN)==planpin,'Checkpoint source/plan drift')
  for e in targets:
   q=pin(R/e['input']['path']);require((q['bytes'],q['sha256'],q['mode'])==(e['input']['bytes'],e['input']['sha256'],e['input']['mode']),'Selected input drift')
 def authorize():
  inputs();stable();require(load(S)==control,'Shared control epoch drift')
  require(datetime.now(timezone.utc)+timedelta(seconds=75)<=datetime.fromisoformat(lease['expires_UTC']),'Checkpoint deadline insufficient')
 env['authorize']=authorize
 inputs()
 for e in targets:
  if e['input']['path']==e['target']:continue
  p=R/e['target'];old=e['original_target'];require((not p.exists()) if old is None else pin(p)==old,'Prepared target baseline drift')
 for e in targets:
  if e['input']['path']==e['target']:continue
  authorize();p=R/e['target'];p.write_bytes(expected[e['target']]);p.chmod(int(e['input']['mode'],8))
 authorize();git('add','--',*sorted(owned));staged=names(git('diff','--cached','--name-only','-z'));require(staged<=owned,'Staged foreign path')
 entries={}
 for line in git('ls-files','--stage','-z').split(b'\0'):
  if line:
   meta,p=line.split(b'\t',1);entries[p.decode()]=meta.decode().split()
 for rel,b in expected.items():
  require(git('show',':'+rel)==b and entries[rel]==['100644',hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest(),'0'],'Whole staged body/mode/blob differs')
 authorize();git('commit','-m','Verify PR302 smooth fixed-lag tensor consistency before priority audit');current=git('rev-parse','HEAD').decode().strip()
 require(git('show','-s','--format=%P',current).decode().split()==[base] and names(git('diff','--name-only','-z',base,current))==staged,'Actual commit parent/scope differs')
 for rel,b in expected.items():
  require(git('show',current+':'+rel)==b and (R/rel).read_bytes()==b,'Committed/current full body differs')
  require(git('ls-tree',current,'--',rel).decode().split()[:3]==['100644','blob',hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()],'Committed mode/blob differs')
  mode=0o644 if rel==str(PLAN.relative_to(R)) else int(next(e['input']['mode'] for e in targets if e['target']==rel),8)
  require(stat.S_IMODE((R/rel).stat().st_mode)==mode,'Current filesystem mode differs')
 authorize();require({p:pin(R/p) for p in held}==held,'Known held body/mode changed')
 git('merge-base','--is-ancestor',base,current);require(git('ls-remote',lease['endpoint'],'refs/heads/main').split()[0].decode()==base,'Remote moved before guarded descendant push')
 git('push','--force-with-lease=refs/heads/main:'+base,lease['endpoint'],current+':refs/heads/main')
 require(git('ls-remote',lease['endpoint'],'refs/heads/main').split()[0].decode()==current,'Final remote differs');stable();inputs();require(not git('diff','--cached','--raw','-z'),'Final index busy')
 require({p:pin(R/p) for p in held}==held and load(S)==control,'Held body/mode or shared control drift')
 receipt=dict(status='PASS_PR302_EXACT_MATHEMATICAL_CHECKPOINT036_PUSHED',UTC=utc(),parent=base,commit=current,plan=planpin,source=source,allowlist_paths=len(owned),changed_paths=len(staged),whole_selected_live_staged_committed_bodies_modes_blobs_verified=True,whole_foreign_logical_index_flags_dirty_bodies_modes_diff_preserved=True,known_held_file_count=len(held),known_held_all_complete_bodies_modes_preserved=True,explicit_expected_old_descendant_push_verified=True,main_equals_remote=True,index_empty=True,mathematics_percent=100,priority_percent=0,workflow_percent=30,completed_by_descending=27,published_by_descending=8,priority_and_publication_unaccepted=True,no_PR_native_QUEUE_DOI_tracker_action=True,token=lease['token'],actual_native_capture_directory=str(actual),postcommit_receipt_intentionally_outside_own_commit=True)
 out=P/'checkpoint_302_mathematical_036_receipt.json';require(not out.exists(),'Postcommit receipt exists');out.write_text(json.dumps(receipt,indent=2)+'\n')
 # This exact scope ends after successful full readback, never during uncertainty.
 (actual/'CLOSED_SHARED_CONTROL_EPOCH.json').write_text(json.dumps(control,indent=2)+'\n')
 closed=copy.deepcopy(control);closed.update(utc=utc(),shared_git_writes_paused=True,descending_writer_window_released=True,descending_shared_git_writes_abstained=True,reason='PR302 exact mathematics checkpoint036 completed and scope released; priority continues privately; fresh literal scope required for any further shared write',local_main_at_pause=current,remote_main_at_pause=current)
 closed['descending_302_math_checkpoint_lease'].update(active=False,completed=True,closed_UTC=utc(),actual_checkpoint=current)
 S.write_text(json.dumps(closed,indent=2)+'\n')
 print(json.dumps(receipt,indent=2))
if __name__=='__main__':main()
