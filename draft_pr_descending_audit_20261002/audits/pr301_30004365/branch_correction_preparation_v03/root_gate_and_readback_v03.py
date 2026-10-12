"""ROOT grant and independent exact native readbacks for PR301 correction.
Grant is conditional on a separately earned frozen operational acceptance.
Prepare/publication are executed only by the separately reviewed operator.
"""
from pathlib import Path
from datetime import datetime,timezone,timedelta
import base64,copy,gzip,hashlib,json,os,signal,stat,subprocess,sys
W=Path(__file__).resolve().parent;A=W.parent;R=Path('/Users/alec/Documents/Math');P=R/'draft_pr_descending_audit_20261002';S=P/'SHARED_GIT_WINDOW_STATUS.json';D=A/'priority_correction_final_v04'
BASE='83f42b8d239702e55c976b033c6dd919232c6526';OLD='125d90fa3f5a4f90b813fec7a7c0f1918914d885';ENDPOINT='https://github.com/AlecKriebel/Math.git';BRANCH='math/30004365-gentle-invariants-wip';T='problems/30004365_gentle_derived_invariant';Q='unsolved_math_prioritization/QUEUE.md';LEASE='descending_301_existing_branch_correction_v01_lease'
sha=lambda b:hashlib.sha256(b).hexdigest();utc=lambda:datetime.now(timezone.utc).isoformat();load=lambda p:json.loads(Path(p).read_bytes())
def need(x,m):
 if not x:raise RuntimeError(m+'; preserve this actual attempt, reconcile read-only')
def pin(p):
 p=Path(p);need(p.is_file() and not p.is_symlink(),'literal input');b=p.read_bytes();return dict(path=str(p),bytes=len(b),sha256=sha(b),mode=stat.S_IMODE(p.stat().st_mode))
def body(x,p=None):
 p=Path(p or x['path']);b=p.read_bytes();need(len(b)==x['bytes'] and sha(b)==x['sha256'],'whole body '+str(p));return b
def blob(b):return hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
def logical(b):return dict(bytes=len(b),sha256=sha(b))
def write_new(p,x):
 with p.open('x') as f:json.dump(x,f,indent=2);f.write('\n')
 p.chmod(0o444)
def main():
 need(not sys.flags.optimize and sys.argv[1:] in [['grant'],['accept_prepare'],['accept_publish']],'explicit unoptimized ROOT phase');phase=sys.argv[1]
 need(not any(k in os.environ for k in ['GIT_DIR','GIT_WORK_TREE','GIT_INDEX_FILE','GIT_OBJECT_DIRECTORY','GIT_ALTERNATE_OBJECT_DIRECTORIES','GIT_COMMON_DIR']),'no ambient Git repository/index/object redirection')
 source=pin(W/'integrate_correction.py');launcher=pin(W/'launch_exact_correction.py');planpin=pin(W/'PLAN.json');plan=load(W/'PLAN.json')
 need(source['sha256']=='0742327802ca322928657d840d39c1480eebdfec301c0bce5d8e0847dfa28ab2' and launcher['sha256']=='324d0a43af8cd763ecd3d072cf20960ccfed87a23a2947533960a54fd3899dab' and planpin['sha256']=='071128d4a9191c5299db8d10a8f6c4109aa83dea48aed21eedfc2706f2806de3','exact reviewed v03')
 need(source['mode']==launcher['mode']==planpin['mode']==0o444,'frozen operator package')
 gate=load(W/'ROOT_OPERATIONAL_REVIEW_ACCEPTANCE.json');need(gate['status']=='ROOT_ACCEPTS_EXACT_PR301_BRANCH_CORRECTION_OPERATOR_V03' and gate['source']==source and gate['launcher']==launcher and gate['plan']==planpin and gate['unresolved_issues']==[] and pin(W/'ROOT_OPERATIONAL_REVIEW_ACCEPTANCE.json')['mode']==0o444,'genuine earned exact operational acceptance')
 def inputs():
  need(pin(W/'integrate_correction.py')==source and pin(W/'launch_exact_correction.py')==launcher and pin(W/'PLAN.json')==planpin,'whole reviewed operator stable')
  for x in plan['bound_inputs']:need(pin(x['path'])==x,'whole fixed role')
  for x in plan['packet_files']:need(pin(x['input']['path'])==x['input'],'whole prepared packet role')
  need(load(plan['final_package_acceptance']['path'])['status']=='ROOT_ACCEPTS_EXACT_PR301_FINAL_CREDITED_CORRECTION_V04','final exact content accepted')
 inputs();cap=W/('root_'+phase+'_native');cap.mkdir(exist_ok=False);count=0
 (cap/'ROOT_source_prelaunch.py.gz').write_bytes(gzip.compress(Path(__file__).read_bytes(),mtime=0))
 def run(argv,ok=(0,)):
  nonlocal count
  count+=1;c=cap/str(count);c.mkdir();q=dict(argv=argv,cwd=str(R),UTC=utc(),actual_recorder_PID=os.getpid(),ROOT_source=pin(__file__),read_only=True)
  write_new(c/'request.json',q);proc=None;out=b'';err=b'';failure=None;cleanup=[];complete=False
  try:
   proc=subprocess.Popen(argv,cwd=R,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE,start_new_session=True,env=dict(os.environ,GIT_OPTIONAL_LOCKS='0',GIT_NO_LAZY_FETCH='1'))
   try:
    write_new(c/'started.json',dict(UTC=utc(),actual_PID=proc.pid,request=pin(c/'request.json')))
    out,err=proc.communicate(timeout=55);complete=True
   except BaseException as original:
    try:os.killpg(proc.pid,signal.SIGKILL)
    except ProcessLookupError:pass
    except BaseException as ex:cleanup.append(str(ex))
    try:out,err=proc.communicate(timeout=5);complete=True
    except BaseException as ex:
     cleanup.append(str(ex))
     if isinstance(ex,subprocess.TimeoutExpired):out=ex.output or out;err=ex.stderr or err
     try:proc.kill()
     except ProcessLookupError:pass
     except BaseException as ex:cleanup.append('fallback_kill: '+str(ex))
     try:out,err=proc.communicate(timeout=5);complete=True
     except BaseException as ex:
      cleanup.append('fallback_communicate: '+str(ex))
      if isinstance(ex,subprocess.TimeoutExpired):out=ex.output or out;err=ex.stderr or err
    raise original
  except BaseException as ex:failure=dict(type=type(ex).__name__,message=str(ex))
  streams={}
  for n,b in [('stdout',out),('stderr',err)]:
   z=c/(n+'.gz');z.write_bytes(gzip.compress(b,mtime=0));z.chmod(0o444);streams[n]=dict(**logical(b),stored=pin(z))
  write_new(c/'execution.json',dict(**q,end_UTC=utc(),actual_PID=proc.pid if proc else None,exit_code=proc.returncode if proc else None,parent_reaped=proc is not None and proc.poll() is not None,failure=failure,cleanup_errors=cleanup,stream_collection_complete=complete,streams=streams))
  need(failure is None and proc.returncode in ok and complete,'actual ROOT native read completed');return out
 def git(*args,ok=(0,)):return run(['/usr/bin/git','--no-optional-locks',*args],ok)
 def gh(*args):return run(['/opt/homebrew/bin/gh',*args])
 def live():return json.loads(gh('pr','view','301','--repo','AlecKriebel/Math','--json','number,state,isDraft,headRefName,headRefOid,baseRefName,title,body,url'))
 def names(b):return {x.decode() for x in b.split(b'\0') if x}
 def state():
  need(git('branch','--show-current')==b'main\n' and git('rev-parse','HEAD').decode().strip()==BASE,'main exact current checkpoint')
  p=Path(git('rev-parse','--git-path','index').decode().strip());p=p if p.is_absolute() else R/p
  dirty=names(git('diff','--name-only','-z','HEAD'))-{str(S.relative_to(R))}
  return dict(index=pin(p),full_stage=logical(git('ls-files','--stage','-z')),full_flags=logical(git('ls-files','-v','-z')),dirty={x:pin(R/x) for x in sorted(dirty)},full_foreign_binary_diff=logical(git('diff','--binary','HEAD','--',*sorted(dirty))) if dirty else logical(b''))
 def fresh_common():
  inputs();need(not git('diff','--cached','--raw','-z'),'empty shared stage')
  need(not any((R/'.git'/n).exists() for n in ['index.lock','MERGE_HEAD','CHERRY_PICK_HEAD','REVERT_HEAD']),'unbusy shared checkout')
  need(git('ls-remote',ENDPOINT,'refs/heads/main').split()[0].decode()==BASE,'explicit remote main exact')
  need(not git('config','--get-regexp','^url[.]',ok=(0,1)),'no endpoint rewrites')
 def held():
  xs=load(A/'checkpoint_039_preparation/KNOWN_HELD_BASELINE.json')['files'];need(len(xs)==41253,'entire held domain')
  for x in xs:
   if x['path']!=str(S):need(pin(x['path'])==x,'all held full body/mode')
 fresh_common();current=state();held();control=load(S)
 if phase=='grant':
  need(not control['shared_git_writes_paused'] and not control['ascending_pr85_publication_integration_window_granted'] and control['descending_writer_window_released'] and all(not x['active'] for x in control.values() if isinstance(x,dict) and 'active' in x),'fresh released sole writer window')
  pr=live();need(pr['number']==301 and pr['state']=='OPEN' and pr['isDraft'] and pr['headRefOid']==OLD and pr['headRefName']==BRANCH and pr['baseRefName']=='main','original live draft')
  need(git('ls-remote',ENDPOINT,'refs/heads/'+BRANCH).split()[0].decode()==OLD,'original branch unchanged')
  need(load(S)==control and state()==current,'all state stable immediately before grant')
  write_new(W/'ROOT_GRANT_FOREIGN_STATE.json',dict(UTC=utc(),state=current,control_mode=pin(S)['mode'],original_control=control,actual_ROOT_source=pin(__file__),native_capture_directory=str(cap)))
  clear=dict(status='ROOT_CLEARS_EXACT_PR301_EXISTING_DRAFT_CORRECTION',UTC=utc(),actual_ROOT_PID=os.getpid(),ROOT_source=pin(__file__),source=source,launcher=launcher,plan=planpin,operational_review=pin(W/'ROOT_OPERATIONAL_REVIEW_ACCEPTANCE.json'),final_content_acceptance=plan['final_package_acceptance'],fresh_foreign_state=pin(W/'ROOT_GRANT_FOREIGN_STATE.json'),unresolved_issues=[],no_merge_close_paper_DOI_tracker_release=True,scope='Private index and exact original-history descendant commit; separately accepted prepared commit; one expected-old existing-branch push and exact title/body update; native full readback; no shared main/index/foreign body mutation')
  write_new(W/'ROOT_BRANCH_CORRECTION_CLEARANCE.json',clear)
  granted=copy.deepcopy(control);granted.update(utc=utc(),descending_writer_window_released=False,descending_shared_git_writes_abstained=False,reason='Fresh exact PR301 existing draft correction v03 lease; original author history retained, no paper/merge/close/DOI/tracker.')
  granted[LEASE]=dict(active=True,source=source,launcher=launcher,plan=planpin,clearance=pin(W/'ROOT_BRANCH_CORRECTION_CLEARANCE.json'),endpoint=ENDPOINT,starting_main=BASE,expected_original_PR_head=OLD,branch=BRANCH,created_UTC=utc(),expires_UTC=(datetime.now(timezone.utc)+timedelta(minutes=40)).isoformat(),no_merge_close_paper_DOI_tracker_release=True)
  inputs();need(load(S)==control,'final whole control before sole grant');S.write_text(json.dumps(granted,indent=2)+'\n');write_new(W/'ROOT_GRANTED_CONTROL.json',granted)
  need(state()==current and load(S)==granted,'whole foreign state preserved by grant')
  print(json.dumps(dict(status=clear['status'],clearance=pin(W/'ROOT_BRANCH_CORRECTION_CLEARANCE.json'),lease_deadline=granted[LEASE]['expires_UTC']),indent=2));return
 baseline=load(W/'ROOT_GRANT_FOREIGN_STATE.json');need(current==baseline['state'],'full grant-baseline index/flags/body/mode/diff equality');granted=load(W/'ROOT_GRANTED_CONTROL.json')
 intent=load(W/'PREPARED_INTENT.json');head=intent['head'];tree=intent['tree'];need(intent['operator']==source and intent['plan']==planpin and intent['parents']==[OLD,BASE] and intent['branch']==BRANCH and intent['endpoint']==ENDPOINT,'exact prepared intent')
 target={T+'/'+x['relative'].removeprefix('target/'):body(x['input']) for x in plan['packet_files'] if x['relative'].startswith('target/')};expected={x['relative']:body(x['input']) for x in intent['files']}
 need(len(target)==43 and len(expected)==44 and set(expected)==set(target)|{Q} and all(expected[k]==v for k,v in target.items()),'all and only exact target/queue bodies')
 raw=git('show',BASE+':'+Q);new=expected[Q];rows=raw.splitlines(keepends=True);news=new.splitlines(keepends=True)
 own=[n for n,b in enumerate(rows) if len(b.split(b'|'))>11 and b.split(b'|')[2].strip().split(b' / ')[0]==b'30004365'];need(len(own)==1 and len(rows)==len(news),'own single queue row')
 row=own[0];before=rows[row].split(b'|');after=news[row].split(b'|');need(len(before)==len(after) and [n for n,(a,b) in enumerate(zip(before,after)) if a!=b]==[8,9] and [after[n].strip() for n in [8,9]]==[b'already_solved',b'1/5'] and all(a==b for n,(a,b) in enumerate(zip(rows,news)) if n!=row),'entire queue except own two cells exact')
 need(git('show','-s','--format=%P',head).decode().split()==[OLD,BASE] and git('show','-s','--format=%T',head).decode().strip()==tree and names(git('diff','--name-only','-z',BASE,head))==set(expected),'native parents/tree/domain')
 git('merge-base','--is-ancestor',OLD,head)
 for rel,b in expected.items():need(git('show',head+':'+rel)==b and git('ls-tree',head,'--',rel).decode().split()[:3]==['100644','blob',blob(b)],'every native complete body/mode/blob')
 def authenticate_phase(ph):
  inner=W/('actual_'+ph);outer=W/('actual_correction_'+ph+'_outer');e=load(outer/'execution.json');q=load(outer/'request.json');st=load(outer/'started.json')
  need(e['status']=='ACTUAL_BRANCH_CORRECTION_OUTER_COMPLETED' and e['exit_code']==0 and not e['failed_or_uncertain_execution_not_reclassified'] and e['failure'] is None and not e['capture_errors'] and e['actual_operator_PID']==st['actual_operator_PID']>0 and q['argv']==['/opt/homebrew/bin/python3','-E','-B',str(W/'integrate_correction.py'),ph],'actual bounded outer completed')
  for x in q['full_prelaunch_inputs']:
   z=body(x['stored']);b=gzip.decompress(z);need(logical(b)==dict(bytes=x['input']['bytes'],sha256=x['input']['sha256']),'complete exact prelaunch source/plan/gate bodies')
  for n,x in e['streams'].items():
   b=body(x['raw']);need(logical(b)==dict(bytes=x['logical_bytes'],sha256=x['logical_sha256']) and gzip.decompress(body(x['stored']))==b,'complete outer raw/compressed native streams')
  captures=[];mutations=[];public=[]
  dirs=sorted([p for p in inner.iterdir() if p.is_dir() and p.name.isdigit()],key=lambda p:int(p.name));need({int(p.name) for p in dirs}==set(range(1,len(dirs)+1)),'entire native capture domain')
  for c in dirs:
   rq=load(c/'request.json');ex=load(c/'execution.json');start=load(c/'started.json')
   need(all(ex[k]==v for k,v in rq.items()) and rq['operator']==source and rq['actual_recorder_PID']==e['actual_operator_PID'] and ex['actual_PID']==start['actual_PID']>0 and ex['failure'] is None and ex['parent_reaped'] and ex['stream_collection_complete'] and not ex['cleanup_errors'],'actual exact operator/source/native capture custody')
   output={}
   for n,x in ex['streams'].items():
    b=gzip.decompress(body(x['stored']));need(logical(b)==dict(bytes=x['logical_bytes'],sha256=x['logical_sha256']),'full inner native stream');output[n]=b
   if rq['stdin_sha256'] is not None:need(logical(gzip.decompress((c/'stdin.gz').read_bytes()))==dict(bytes=rq['stdin_bytes'],sha256=rq['stdin_sha256']),'entire native input')
   permitted=ex['exit_code']==0 or (ex['exit_code']==1 and rq['argv']==['/usr/bin/git','--no-optional-locks','config','--get-regexp','^url[.]']) or (ph=='prepare' and ex['exit_code']==128 and rq['argv']==['/usr/bin/git','--no-optional-locks','cat-file','-e',OLD+'^{commit}'])
   need(permitted,'only declared actual native exits')
   captures.append(dict(execution=pin(c/'execution.json'),actual_PID=ex['actual_PID'],exit_code=ex['exit_code']))
   if rq['mutation']:mutations.append(rq['argv'])
   if rq['argv'][:2]==['/opt/homebrew/bin/gh','api'] and '/contents/' in rq['argv'][2]:public.append((rq['argv'][2],json.loads(output['stdout'])))
  return dict(outer_execution=pin(outer/'execution.json'),actual_operator_PID=e['actual_operator_PID'],native_capture_count=len(captures),native_captures=captures,mutations=mutations),public
 prepare,_=authenticate_phase('prepare')
 allowed={'read-tree','hash-object','update-index','write-tree','commit-tree'}
 for argv in prepare['mutations']:
  need(argv[:2]==['/usr/bin/git','--no-optional-locks'] and (argv[2] in allowed or argv[2:8]==['-c','gc.auto=0','-c','maintenance.auto=false','fetch','--no-tags']),'private prepare writes only reviewed Git object/index mechanism')
 original=load(A/'snapshot_manifest.json');need(len(original['files'])==18 and original['head']==OLD,'original intake')
 for x in original['files']:
  b=body(x['snapshot']);need(git('show',OLD+':'+x['path'])==b,'every original native body')
  if x['path'].startswith(T+'/'):
   rel=x['path'][len(T)+1:];need(expected[T+'/history/original_submission/'+rel]==b,'all original history exact')
   if rel not in {'README.md','DISPOSITION.md','PUBLIC_SCOPE.json','PUBLIC_MANIFEST.json'}:need(expected[x['path']]==b,'all13 unchanged old paths')
 if phase=='accept_prepare':
  need(load(S)==granted and state()==current,'private prepare preserves full shared state/control')
  pr=live();need(pr['state']=='OPEN' and pr['isDraft'] and pr['headRefOid']==OLD and git('ls-remote',ENDPOINT,'refs/heads/'+BRANCH).split()[0].decode()==OLD,'no public prepare mutation')
  held();inputs();record=dict(status='ROOT_ACCEPTS_EXACT_PREPARED_PR301_CORRECTION_COMMIT',UTC=utc(),actual_ROOT_PID=os.getpid(),ROOT_source=pin(__file__),intent=pin(W/'PREPARED_INTENT.json'),head=head,tree=tree,parents=[OLD,BASE],files=intent['files'],whole_QUEUE_except_own_two_cells_preserved=True,all18_original_native_bodies_exact=True,all17_original_history_preserved=True,all13_old_paths_unchanged=True,actual_prepare=prepare,whole_shared_foreign_state_preserved=True,unresolved_issues=[],no_merge_close_paper_DOI_tracker_release=True,workflow_percent=85)
  write_new(W/'ROOT_EXACT_PREPARED_COMMIT_ACCEPTANCE.json',record);print(json.dumps(dict(status=record['status'],acceptance=pin(W/'ROOT_EXACT_PREPARED_COMMIT_ACCEPTANCE.json'),head=head),indent=2));return
 publication,public=authenticate_phase('publish');need(publication['mutations']==[['/usr/bin/git','--no-optional-locks','push','--force-with-lease=refs/heads/'+BRANCH+':'+OLD,ENDPOINT,head+':refs/heads/'+BRANCH],['/opt/homebrew/bin/gh','pr','edit','301','--repo','AlecKriebel/Math','--title',(D/'PR_TITLE.txt').read_text().rstrip('\n'),'--body-file',str(D/'PR_BODY.md')]],'one actual exact branch push and metadata edit')
 need(len(public)==44 and {x[0] for x in public}=={'repos/AlecKriebel/Math/contents/'+rel+'?ref='+head for rel in expected},'all44 public native body reads')
 for query,rowdata in public:
  rel=query.split('/contents/',1)[1].split('?ref=',1)[0];b=expected[rel];need(rowdata['encoding']=='base64' and rowdata['sha']==blob(b) and rowdata['size']==len(b) and base64.b64decode(rowdata['content'])==b,'every authenticated public body exact')
 disposition=load(A/'PRIORITY_CORRECTION_DISPOSITION.json');need(disposition['head']==head and disposition['status']=='PASS_RECLASSIFIED_ALREADY_SOLVED_LEFT_OPEN_DRAFT','actual disposition')
 final=live();need(final['number']==301 and final['state']=='OPEN' and final['isDraft'] and final['headRefOid']==head and final['headRefName']==BRANCH and final['baseRefName']=='main' and final['title']==(D/'PR_TITLE.txt').read_text().rstrip('\n') and final['body']==(D/'PR_BODY.md').read_text(),'fresh exact native public metadata')
 need(git('ls-remote',ENDPOINT,'refs/heads/'+BRANCH).split()[0].decode()==head,'fresh actual corrected remote branch')
 closed=load(S);pre=load(W/'actual_publish/EXACT_PRE_CLOSURE_CONTROL.json');need(pre==granted,'exact preclosure control provenance')
 expected_control=copy.deepcopy(granted)
 for key in ['utc','descending_writer_window_released','descending_shared_git_writes_abstained','reason']:expected_control[key]=closed[key]
 for key in ['active','completed','closed_UTC','actual_corrected_PR_head']:expected_control[LEASE][key]=closed[LEASE][key]
 need(closed==expected_control and closed['descending_writer_window_released'] and closed['descending_shared_git_writes_abstained'] and not closed[LEASE]['active'] and closed[LEASE]['completed'] and closed[LEASE]['actual_corrected_PR_head']==head and pin(S)['mode']==baseline['control_mode'],'only reviewed own lease closure; every foreign control field exact')
 need(state()==current and not git('diff','--cached','--raw','-z'),'full shared index/flags/bodies/modes/diff preserved after public correction');held();inputs();fresh_common()
 record=dict(status='ROOT_ACCEPTS_ACTUAL_PR301_CREDITED_CORRECTION_PUBLICATION',UTC=utc(),actual_ROOT_PID=os.getpid(),ROOT_source=pin(__file__),head=head,tree=tree,parents=[OLD,BASE],intent=pin(W/'PREPARED_INTENT.json'),prepared_commit_acceptance=pin(W/'ROOT_EXACT_PREPARED_COMMIT_ACCEPTANCE.json'),disposition=pin(A/'PRIORITY_CORRECTION_DISPOSITION.json'),actual_prepare=prepare,actual_publication=publication,fresh_native_PR=final,all44_complete_public_native_blobs_authenticated=True,whole_shared_foreign_state_preserved=True,all41253_known_held_noncontrol_paths_preserved=True,exact_own_control_closure=pin(S),original_status='claimed_solved',adjudicated_status='already_solved',author_budget='1/5',OPEN=True,DRAFT=True,merged=False,closed=False,paper=False,DOI=None,tracker=False,immutable_release=False,unresolved_issues=[],workflow_percent=100,overall_goal_complete=False)
 write_new(A/'ROOT_ACTUAL_PR301_CORRECTION_ACCEPTANCE.json',record);print(json.dumps(dict(status=record['status'],acceptance=pin(A/'ROOT_ACTUAL_PR301_CORRECTION_ACCEPTANCE.json'),head=head),indent=2))
if __name__=='__main__':main()
