"""Metadata-only completion after one authenticated successful push and stale API stop.
Never fetch, push, write a Git index, or create a Git commit. Failed original
publication remains failed; only the previously unattempted metadata step runs.
"""
from pathlib import Path
from datetime import datetime,timezone,timedelta
import base64,copy,fcntl,gzip,hashlib,json,os,signal,stat,subprocess,sys
R=Path('/Users/alec/Documents/Math');P=R/'draft_pr_descending_audit_20261002';W=Path(__file__).resolve().parent;A=W.parent
ORIGINAL_W=A/'branch_correction_preparation_v03'
D=A/'priority_correction_final_v04';S=P/'SHARED_GIT_WINDOW_STATUS.json';PLAN=W/'PLAN.json';CLEAR=W/'ROOT_BRANCH_CORRECTION_CLEARANCE.json'
ENDPOINT='https://github.com/AlecKriebel/Math.git';OLD='125d90fa3f5a4f90b813fec7a7c0f1918914d885';BASE='83f42b8d239702e55c976b033c6dd919232c6526'
BRANCH='math/30004365-gentle-invariants-wip';Q='unsolved_math_prioritization/QUEUE.md';T='problems/30004365_gentle_derived_invariant';LEASE='descending_301_stale_api_metadata_completion_v01_lease'
sha=lambda b:hashlib.sha256(b).hexdigest();utc=lambda:datetime.now(timezone.utc).isoformat();load=lambda p:json.loads(Path(p).read_bytes())
def need(x,m):
 if not x:raise RuntimeError(m+'; preserve actual attempt and reconcile read-only, no automatic mutation retry')
def pin(p):
 p=Path(p);need(p.is_file() and not p.is_symlink(),'literal file');b=p.read_bytes();return dict(path=str(p),bytes=len(b),sha256=sha(b),mode=stat.S_IMODE(p.stat().st_mode))
def match(x):need(pin(x['path'])==x,'whole immutable input');return Path(x['path']).read_bytes()
def names(b):return {x.decode() for x in b.split(b'\0') if x}
def blob(b):return hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
def main():
 need(not sys.flags.optimize and sys.argv[1:]==['finish_metadata'],'explicit unoptimized metadata-only phase');phase='metadata_completion'
 lock=(W/'OPERATOR.lock').open('a+b');fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
 source=pin(Path(__file__));planpin=pin(PLAN);plan=load(PLAN);clear=load(CLEAR);control=load(S);lease=control[LEASE]
 need(source['mode']==planpin['mode']==pin(CLEAR)['mode']==0o444 and clear['status']=='ROOT_CLEARS_EXACT_PR301_STALE_API_METADATA_COMPLETION' and clear['source']==source and clear['plan']==planpin and clear['unresolved_issues']==[],'genuine exact ROOT operator gate')
 need(lease['active'] and lease['source']==source and lease['plan']==planpin and lease['clearance']==pin(CLEAR) and lease['endpoint']==ENDPOINT and lease['starting_main']==BASE and lease['expected_original_PR_head']==OLD and lease['branch']==BRANCH,'sole fresh branch-specific lease')
 need(not control['shared_git_writes_paused'] and not control['ascending_pr85_publication_integration_window_granted'] and all(not v['active'] for k,v in control.items() if isinstance(v,dict) and 'active' in v and k!=LEASE),'no competing active lease')
 need(plan['starting_main']==BASE and plan['original_head']==OLD and plan['endpoint']==ENDPOINT and plan['branch']==BRANCH and plan['target_prefix']==T and plan['QUEUE']==Q and plan['target_count']==43 and plan['author_budget']=='1/5','exact task domain')
 def inputs():
  need(pin(Path(__file__))==source and pin(PLAN)==planpin and load(CLEAR)==clear,'complete source/plan/gate stable')
  for x in plan['bound_inputs']:match(x)
  for x in plan['packet_files']:match(x['input'])
 inputs();need(len(plan['packet_files'])==45 and len({x['relative'] for x in plan['packet_files']})==45,'exact prepared package')
 accepted=load(plan['final_package_acceptance']['path']);need(accepted['status']=='ROOT_ACCEPTS_EXACT_PR301_FINAL_CREDITED_CORRECTION_V04' and accepted['unresolved_issues']==[],'exact final package content acceptance')
 need(plan['no_merge_close_paper_DOI_tracker_release'] and clear['no_merge_close_paper_DOI_tracker_release'],'correction-only authority')
 cap=W/('actual_'+phase);need(not cap.exists(),'no prior or uncertain phase');cap.mkdir()
 for p in [Path(__file__),PLAN,CLEAR,S,*[Path(x['path']) for x in plan['bound_inputs']],*[Path(x['input']['path']) for x in plan['packet_files']]]:
  q=cap/(str(len(list(cap.iterdir())))+'_'+p.name+'.source.gz');q.write_bytes(gzip.compress(p.read_bytes(),mtime=0))
 (cap/'ATTEMPT.json').write_text(json.dumps(dict(UTC=utc(),actual_ROOT_PID=os.getpid(),phase=phase,source=source,plan=planpin,automatic_retry=False,outcome='STARTED_UNCERTAIN_UNTIL_NATIVE_READBACK'),indent=2)+'\n')
 count=0;before=None;idx=W/'actual_prepare/private_index'
 def run(argv,*,stdin=None,private=False,write=False,ok=(0,)):
  nonlocal count
  count+=1;d=cap/str(count);d.mkdir();req=dict(argv=argv,cwd=str(R),UTC=utc(),operator=source,actual_recorder_PID=os.getpid(),stdin_bytes=len(stdin) if stdin is not None else 0,stdin_sha256=sha(stdin) if stdin is not None else None,private_index=str(idx) if private else None,mutation=write,automatic_retry=False)
  (d/'request.json').write_text(json.dumps(req,indent=2)+'\n')
  if stdin is not None:(d/'stdin.gz').write_bytes(gzip.compress(stdin,mtime=0))
  if write:
   need(argv[:4]==['/opt/homebrew/bin/gh','pr','edit','301'],'only metadata edit is a permitted native mutation');authorize()
  env=dict(os.environ,GIT_OPTIONAL_LOCKS='0',GIT_NO_LAZY_FETCH='1');env.pop('GIT_INDEX_FILE',None)
  if private:env['GIT_INDEX_FILE']=str(idx)
  proc=None;out=b'';err=b'';failure=None;cleanup_errors=[];stream_collection_complete=False
  try:
   proc=subprocess.Popen(argv,cwd=R,stdin=subprocess.PIPE if stdin is not None else subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE,start_new_session=True,env=env)
   try:
    (d/'started.json').write_text(json.dumps(dict(actual_PID=proc.pid,start_UTC=utc()),indent=2)+'\n')
    out,err=proc.communicate(stdin,timeout=55);stream_collection_complete=True
   except BaseException as original_error:
    # Preserve partial bytes if cleanup itself fails. Successful communicate
    # returns the entire accumulated streams, replacing these partial bytes.
    if isinstance(original_error,subprocess.TimeoutExpired):
     if original_error.output is not None:out=original_error.output
     if original_error.stderr is not None:err=original_error.stderr
    try:os.killpg(proc.pid,signal.SIGKILL)
    except ProcessLookupError:pass
    except BaseException as cleanup:cleanup_errors.append(dict(step='killpg',type=type(cleanup).__name__,message=str(cleanup)))
    # Reaping and stream collection are attempted even if group signaling races
    # with child exit or fails. None of these cleanup outcomes relabels failure.
    try:out,err=proc.communicate(timeout=5);stream_collection_complete=True
    except BaseException as cleanup:
     cleanup_errors.append(dict(step='communicate',type=type(cleanup).__name__,message=str(cleanup)))
     if isinstance(cleanup,subprocess.TimeoutExpired):
      if cleanup.output is not None:out=cleanup.output
      if cleanup.stderr is not None:err=cleanup.stderr
     try:proc.kill()
     except ProcessLookupError:pass
     except BaseException as fallback:cleanup_errors.append(dict(step='fallback_kill',type=type(fallback).__name__,message=str(fallback)))
     try:out,err=proc.communicate(timeout=5);stream_collection_complete=True
     except BaseException as fallback:
      cleanup_errors.append(dict(step='fallback_communicate',type=type(fallback).__name__,message=str(fallback)))
      if isinstance(fallback,subprocess.TimeoutExpired):
       if fallback.output is not None:out=fallback.output
       if fallback.stderr is not None:err=fallback.stderr
    raise original_error
  except BaseException as e:failure=dict(type=type(e).__name__,message=str(e))
  streams={}
  for n,b in [('stdout',out),('stderr',err)]:
   z=d/(n+'.gz');z.write_bytes(gzip.compress(b,mtime=0));streams[n]=dict(stored=pin(z),logical_bytes=len(b),logical_sha256=sha(b))
  (d/'execution.json').write_text(json.dumps(dict(**req,actual_PID=proc.pid if proc else None,end_UTC=utc(),exit_code=proc.returncode if proc else None,parent_reaped=proc is not None and proc.poll() is not None,failure=failure,cleanup_errors=cleanup_errors,stream_collection_complete=stream_collection_complete,streams=streams),indent=2)+'\n')
  need(failure is None and proc is not None and proc.returncode in ok,'actual native command completed with permitted status');return out
 def git(*a,**kw):
  need(not kw.get('write',False),'no native Git mutation during metadata completion');return run(['/usr/bin/git','--no-optional-locks',*a],**kw)
 def gh(*a,write=False):return run(['/opt/homebrew/bin/gh',*a],write=write)
 def live():return json.loads(gh('pr','view','301','--repo','AlecKriebel/Math','--json','number,state,isDraft,headRefName,headRefOid,baseRefName,title,body,url'))
 def state():
  need(git('branch','--show-current')==b'main\n' and git('rev-parse','HEAD').decode().strip()==BASE,'shared main unchanged')
  p=Path(git('rev-parse','--git-path','index').decode().strip());p=p if p.is_absolute() else R/p
  dirty=names(git('diff','--name-only','-z','HEAD'))
  return dict(index=pin(p),stage=git('ls-files','--stage','-z').hex(),flags=git('ls-files','-v','-z').hex(),dirty={x:pin(R/x) for x in sorted(dirty)},binary_diff=git('diff','--binary','HEAD','--',*sorted(dirty)).hex() if dirty else '')
 def stable():need(state()==before,'complete shared index/flags/dirty full bodies/modes/diff preserved')
 def stable_before_write():
  # Full index/flags/diff streams are captured at phase boundaries. A byte-exact
  # unchanged physical index also preserves every logical entry and flag.
  need(git('branch','--show-current')==b'main\n' and git('rev-parse','HEAD').decode().strip()==BASE,'same main before write')
  need(pin(before['index']['path'])==before['index'],'entire physical shared index bytes/mode before write')
  dirty=names(git('diff','--name-only','-z','HEAD'));need(dirty==set(before['dirty']) and {x:pin(R/x) for x in dirty}==before['dirty'],'all current foreign dirty full bodies/modes before write')
 def authorize():
  inputs();need(load(S)==control and pin(CLEAR)==lease['clearance'],'exact sole control and ROOT gate')
  need(datetime.now(timezone.utc)+timedelta(seconds=75)<datetime.fromisoformat(lease['expires_UTC']),'lease deadline buffer')
  if before is not None:stable_before_write()
  need(load(S)==control,'final whole control before mutation')
 before=state();need(not git('diff','--cached','--raw','-z') and not any((R/'.git'/n).exists() for n in ['index.lock','MERGE_HEAD','CHERRY_PICK_HEAD','REVERT_HEAD']),'unbusy empty shared index')
 need(git('ls-remote',ENDPOINT,'refs/heads/main').split()[0].decode()==BASE,'fresh explicit remote main')
 need(not git('config','--get-regexp','^url[.]',ok=(0,1)),'no endpoint URL rewrite')
 packet={x['relative']:match(x['input']) for x in plan['packet_files']};target={T+'/'+k.removeprefix('target/'):b for k,b in packet.items() if k.startswith('target/')};need(len(target)==43 and all(not Path(k).is_absolute() and '..' not in Path(k).parts for k in packet),'literal target domain')
 need(set(packet)=={str(p.relative_to(D)) for p in D.rglob('*') if p.is_file()} and all(x['input']['path']==str(D/x['relative']) for x in plan['packet_files']),'whole exact current packet paths')
 held=load(A/'checkpoint_039_preparation/KNOWN_HELD_BASELINE.json')['files'];need(len(held)==41253,'known-held complete domain')
 def held_stable():
  for x in held:
   if x['path']!=str(S):match(x)
 held_stable();reconciliation=load(plan['stale_API_reconciliation']['path']);need(reconciliation['status']=='ROOT_AUTHENTICATES_ACTUAL_PR301_ONE_PUSH_SUCCEEDED_STALE_API_STOP_METADATA_NOT_ATTEMPTED' and reconciliation['metadata_attempt_count']==0,'authentic prior single push and metadata not attempted')
 observed=live();need(observed['number']==301 and observed['state']=='OPEN' and observed['isDraft'] and observed['headRefName']==BRANCH and observed['baseRefName']=='main' and observed['headRefOid']==plan['corrected_head'],'exact corrected draft before metadata completion')
 need(observed['title']==reconciliation['last_actual_stale_PR']['title'] and observed['body']==reconciliation['last_actual_stale_PR']['body'],'original unedited metadata; stop for any unexpected current change')
 intent=load(ORIGINAL_W/'PREPARED_INTENT.json');pub=load(ORIGINAL_W/'ROOT_EXACT_PREPARED_COMMIT_ACCEPTANCE.json');need(pub['status']=='ROOT_ACCEPTS_EXACT_PREPARED_PR301_CORRECTION_COMMIT' and pub['intent']==pin(ORIGINAL_W/'PREPARED_INTENT.json') and pub['head']==intent['head'] and pub['unresolved_issues']==[],'genuine exact prepared-commit acceptance')
 head=intent['head'];need(intent['operator']==pin(ORIGINAL_W/'integrate_correction.py') and intent['plan']==pin(ORIGINAL_W/'PLAN.json') and intent['parents']==[OLD,BASE] and intent['branch']==BRANCH and intent['endpoint']==ENDPOINT,'exact accepted prepared intent')
 expected={x['relative']:match(x['input']) for x in intent['files']};need(set(expected)==set(target)|{Q} and all(expected[k]==b for k,b in target.items()),'exact accepted prepared body domain')
 need(git('show','-s','--format=%P',head).decode().split()==[OLD,BASE] and git('show','-s','--format=%T',head).decode().strip()==intent['tree'] and names(git('diff','--name-only','-z',BASE,head))==set(expected),'actual prepared parent/tree/domain')
 for rel,b in expected.items():need(git('show',head+':'+rel)==b and git('ls-tree',head,'--',rel).decode().split()[:3]==['100644','blob',blob(b)],'every exact prepared native body')
 need(head==plan['corrected_head']==reconciliation['actual_corrected_head'] and intent['head']==pub['head'],'exact previously accepted and already pushed head')
 git('merge-base','--is-ancestor',OLD,head);need(git('ls-remote',ENDPOINT,'refs/heads/'+BRANCH).split()[0].decode()==head,'existing branch is already the exact corrected head; no repeated push')
 held_stable();authorize()
 need(git('ls-remote',ENDPOINT,'refs/heads/'+BRANCH).split()[0].decode()==head,'actual remote branch readback; never repeat push if later API lags')
 afterpush=live();need(afterpush['state']=='OPEN' and afterpush['isDraft'] and afterpush['headRefOid']==head and afterpush['headRefName']==BRANCH,'native PR shows exact already corrected head')
 need(afterpush['title']==observed['title'] and afterpush['body']==observed['body'],'metadata unchanged immediately before exact edit')
 title=packet['PR_TITLE.txt'].decode().rstrip('\n');body=packet['PR_BODY.md'].decode();gh('pr','edit','301','--repo','AlecKriebel/Math','--title',title,'--body-file',str(D/'PR_BODY.md'),write=True)
 final=live();need(final['number']==301 and final['state']=='OPEN' and final['isDraft'] and final['headRefOid']==head and final['headRefName']==BRANCH and final['title']==title and final['body']==body,'exact native PR metadata readback')
 for rel,b in expected.items():
  row=json.loads(gh('api','repos/AlecKriebel/Math/contents/'+rel+'?ref='+head));need(row['encoding']=='base64' and row['sha']==blob(b) and row['size']==len(b) and base64.b64decode(row['content'])==b,'every44 complete public native blob body')
 stable();held_stable();inputs();need(load(S)==control and not git('diff','--cached','--raw','-z'),'all shared state preserved after publication')
 authorize()  # Recheck full authority and deadline after all44 possibly slow GETs.
 result=dict(status='PASS_RECLASSIFIED_ALREADY_SOLVED_LEFT_OPEN_DRAFT',original_stale_API_failed_attempt_preserved=True,prior_successful_single_push=plan['stale_API_reconciliation'],metadata_completion_only=True,UTC=utc(),actual_ROOT_PID=os.getpid(),source=source,plan=planpin,head=head,parents=[OLD,BASE],original_status='claimed_solved',adjudicated_status='already_solved',author_budget='1/5',exact_remote_PR_readback=final,all44_public_body_reads_exact=True,only_own_QUEUE_cells_changed=[8,9],whole_foreign_shared_index_flags_dirty_bodies_modes_diff_preserved=True,all41253known_held_noncontrol_bodies_modes_preserved=True,merge=False,close=False,paper=False,Zenodo=False,DOI=None,tracker=False,immutable_release=False,automatic_retry=False,workflow_percent=100,overall_goal_complete=False)
 out=A/'PRIORITY_CORRECTION_DISPOSITION.json'
 with out.open('x') as f:json.dump(result,f,indent=2);f.write('\n')
 out.chmod(0o444);(cap/'EXACT_PRE_CLOSURE_CONTROL.json').write_text(json.dumps(control,indent=2)+'\n')
 closed=copy.deepcopy(control);closed.update(utc=utc(),descending_writer_window_released=True,descending_shared_git_writes_abstained=True,reason='Exact PR301 stale-API metadata completion published and read back; original single-push failure preserved; draft remains open/unmerged/unclosed. Fresh authority required for any further shared write.');closed[LEASE].update(active=False,completed=True,closed_UTC=utc(),actual_corrected_PR_head=head);authorize();need(load(S)==control,'fresh whole control immediately before lease closure');S.write_text(json.dumps(closed,indent=2)+'\n');print(json.dumps(dict(status=result['status'],head=head,disposition=pin(out)),indent=2))
if __name__=='__main__':main()
