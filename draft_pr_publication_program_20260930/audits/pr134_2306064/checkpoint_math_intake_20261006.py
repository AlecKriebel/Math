"""PR134 v3: import-safe candidate, no automatic grant request or messaging.
Invocation: checkpoint GRANT_FILE TRUSTED_GRANT_SHA EVIDENCE_FILE TRUSTED_EVIDENCE_SHA.
Both expected hashes must come from the authenticated peer message/readback;
locally hashing a self-styled grant does not establish peer authorization.
"""
from pathlib import Path, PurePosixPath
import datetime, hashlib, json, os, signal, stat, subprocess, sys, threading, time
R=Path('/Users/alec/Documents/Math')
C=R/'draft_pr_publication_program_20260930/audits/pr85_30001203/isolated_main_integration_20261005/checkout'
P=C/'draft_pr_publication_program_20260930';A=P/'audits/pr134_2306064'
G=Path('/opt/homebrew/Cellar/git/2.38.2/bin/git');GH=Path('/opt/homebrew/Cellar/gh/2.85.0/bin/gh')
ORIGIN='https://github.com/AlecKriebel/Math.git'
PEER='01a0ff30-7e80-7053-abb4-4a9c45f2fd62';OWNER='01a0f08c-564b-7a51-bc3c-09cc9990d0fd';SCOPE='PR134_math_intake_main_archive_only'
REVIEW=A/'checkpoint_protocol_v3_adversary_20261006';REPAIR=A/'checkpoint_protocol_v3_repair_20261006'
AUTHORITY=A/'private_checkpoint_authority_v3_20261006';HANDOFF=A/'MAIN_ARCHIVE_HANDOFF_20261006.json'
PLAN=A/'MATH_INTAKE_CHECKPOINT_PLAN_20261006.json';REQUEST=A/'MAIN_ARCHIVE_GRANT_REQUEST_20261006.json'
PROGRAM_PATHS=[str((P/n).relative_to(C)) for n in ('CURRENT_PROGRESS.json','CURRENT_PROGRESS.md','RESEARCH_LOG.md')]
FUTURE_PATHS=[str(f.relative_to(C)) for f in (PLAN,REQUEST,HANDOFF,REVIEW/'AUDIT.md',REVIEW/'RESULT.json',REVIEW/'FINAL_MANIFEST.json',REPAIR/'REPORT.md',REPAIR/'RESULT.json',REPAIR/'FINAL_MANIFEST.json')]
SAFE_CONFIG={'core.repositoryformatversion':'0','core.filemode':'true','core.bare':'false','core.logallrefupdates':'true','core.ignorecase':'true','core.precomposeunicode':'true','remote.origin.url':ORIGIN,'remote.origin.fetch':'+refs/heads/*:refs/remotes/origin/*','branch.main.remote':'origin','branch.main.merge':'refs/heads/main'}
WRITES={'hash-object','update-index','write-tree','commit-tree','update-ref','push','fetch'}
READS={'rev-parse','symbolic-ref','config','ls-tree','diff','ls-remote','cat-file','check-ignore','ls-files'}
BOUNDS={'main_commits':1,'main_compare_and_swap_ref_updates':1,'nonforce_main_pushes':1,'own_actual_index_installs':1,'program_existing_tracked_updates':3,'new_central_proof_search_turns':0}

def ck(v,m):
 if not v:raise RuntimeError(m)
def now():return datetime.datetime.now(datetime.timezone.utc)
def sha(b):return hashlib.sha256(b).hexdigest()
def oid(b):return hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
def encoded(v):return (json.dumps(v,indent=2,sort_keys=True)+'\n').encode()
def relative(s):
 ck(isinstance(s,str) and s and not any(c in s for c in ('\0','\n','\r')),'relative path text')
 p=PurePosixPath(s);ck(not p.is_absolute() and '..' not in p.parts and '.' not in p.parts and str(p)==s,'canonical relative path');return s
def safe(path):
 p=Path(path);ck(p.is_absolute() and '..' not in p.parts and str(p)==str(p.absolute()),'canonical absolute custody')
 for q in reversed([p,*p.parents]):
  if q.exists() or q.is_symlink():ck(not stat.S_ISLNK(q.lstat().st_mode),'symlink component '+str(q))
 return p
def read_regular(path):
 p=safe(path);fd=os.open(p,os.O_RDONLY|os.O_NOFOLLOW)
 try:
  s=os.fstat(fd);ck(stat.S_ISREG(s.st_mode) and s.st_nlink==1,'regular single-link body '+str(p));parts=[]
  while True:
   b=os.read(fd,1024*1024)
   if not b:break
   parts.append(b)
  t=os.fstat(fd);ck((s.st_dev,s.st_ino,s.st_size,s.st_mtime_ns,s.st_ctime_ns)==(t.st_dev,t.st_ino,t.st_size,t.st_mtime_ns,t.st_ctime_ns),'body changed during read')
  u=p.lstat();ck((u.st_dev,u.st_ino)==(t.st_dev,t.st_ino),'body replaced during read')
  b=b''.join(parts);ck(len(b)==t.st_size,'complete body');return b,{'bytes':len(b),'sha256':sha(b),'mode':t.st_mode&0o7777}
 finally:os.close(fd)
def regular_mode(mode):
 ck(mode in (0o644,0o755),'approved regular mode');return '100755' if mode==0o755 else '100644'
def pin(b,mode):return {'bytes':len(b),'sha256':sha(b),'mode':mode,'git_mode':regular_mode(mode)}
def instant(s):
 t=datetime.datetime.fromisoformat(s.replace('Z','+00:00'));ck(t.tzinfo is not None and t.utcoffset()==datetime.timedelta(0),'aware UTC');return t
def interval(g,at=None):
 at=now() if at is None else at;start,end=instant(g['granted_at_utc']),instant(g['expires_at_utc'])
 ck(datetime.timedelta(0)<end-start<=datetime.timedelta(minutes=15),'bounded15minute grant');ck(start<=at<end,'grant not begun or expired');return (end-at).total_seconds()
def member_map(members):
 ck(isinstance(members,list),'full member list');out={}
 for x in members:
  s=relative(x['path']);ck(s not in out and set(x)=={'path','bytes','sha256','mode','git_mode'},'unique complete regular member')
  ck(isinstance(x['bytes'],int) and x['bytes']>=0 and len(x['sha256'])==64 and x['git_mode']==regular_mode(x['mode']),'member pin format')
  out[s]={k:x[k] for k in ('bytes','sha256','mode','git_mode')}
 return out
def deterministic_handoff(plan_pin,request_pin,grant_pin,evidence_pin,p,g,e):
 return {'schema':'pr134-directional-main-archive-handoff/v3','UTC':g['granted_at_utc'],'scope':SCOPE,'source_thread_id':PEER,'owner_thread_id':OWNER,'trusted_peer_message_id':e['message_id'],'authentication_basis':'out_of_band_authenticated_peer_message_and_readback_hashes','concrete_plan':plan_pin,'root_request':request_pin,'actual_peer_grant':grant_pin,'trusted_peer_evidence':evidence_pin,'base_main':p['base_main'],'operator_sha256':p['operator_sha256'],'primary_HEAD':p['primary_HEAD'],'protected_primary_pins':p['protected_primary_pins'],'own_full_index_preimage':p['own_full_index_preimage'],'bounded_mutations':p['bounded_mutations'],'counts':p['counts'],'granted_at_utc':g['granted_at_utc'],'expires_at_utc':g['expires_at_utc'],'grant_bound_future_members':g['future_protocol_members'],'execution_performed':False,'actual_writer_release_required_after_verified_execution':True,'directional_custody':'Grant seals plan/request/review/repair. Handoff is deterministically derived from grant/evidence; no checksum cycle.'}

class ChildDeadline:
 """Kill-only watchdog; main thread alone communicates, terminates and reaps.
 Cooperative process model: a controlled child starts its own process group.
 A delayed Popen cannot expose its PID until return; bind immediately kills an
 already expired child. No hard real-time OS/filesystem scheduling claim.
 """
 def __init__(self,deadline,clock=time.monotonic,kill_group=None):
  self.deadline=deadline;self.clock=clock;self.kill_group=kill_group or (lambda pid:os.killpg(pid,signal.SIGKILL))
  self.cancel=threading.Event();self.lock=threading.Lock();self.pid=None;self.expired=False;self.kill_attempted=False;self.signal_result=None;self.signal_error=None;self.joined=False
  self.armed_at=clock();self.thread=threading.Thread(target=self.watch,name='pr134-child-absolute-deadline',daemon=False);self.thread.start()
 def remaining(self):return self.deadline-self.clock()
 def watch(self):
  if not self.cancel.wait(max(0.0,self.remaining())):self.expire()
 def expire(self):
  with self.lock:
   self.expired=True
   if self.pid is None or self.kill_attempted:return
   self.kill_attempted=True;pid=self.pid
  try:self.kill_group(pid);result='SIGKILL_sent';error=None
  except ProcessLookupError:result='group_already_empty';error=None
  except BaseException as exc:result='signal_failed';error=type(exc).__name__+': '+str(exc)
  with self.lock:self.signal_result=result;self.signal_error=error
 def bind(self,pid):
  with self.lock:
   ck(self.pid is None and isinstance(pid,int) and pid>0,'single actual child process-group bind');self.pid=pid;expired=self.expired or self.remaining()<=0
  if expired:self.expire()
 def close(self):
  self.cancel.set();self.thread.join(timeout=2.0);self.joined=not self.thread.is_alive();ck(self.joined,'watchdog shutdown not verified')
 def snapshot(self):
  with self.lock:return {'clock':'absolute_time.monotonic','armed_before_Popen_and_running_journal':True,'armed_at_monotonic':self.armed_at,'deadline_monotonic':self.deadline,'child_process_group':self.pid,'expired':self.expired,'kill_attempted':self.kill_attempted,'signal_result':self.signal_result,'signal_error':self.signal_error,'watchdog_thread_ident':self.thread.ident,'watchdog_joined':self.joined}

class Operator:
 def __init__(self,grant_file,grant_sha,evidence_file,evidence_sha):
  ck(Path(__file__).absolute()==A/'checkpoint_math_intake_20261006.py','exact operator custody')
  ck(safe(grant_file)==AUTHORITY/'FRESH_PEER_GRANT.json' and safe(evidence_file)==AUTHORITY/'TRUSTED_PEER_MESSAGE_READBACK.json','exact private authority paths')
  ck(len(grant_sha)==len(evidence_sha)==64,'out-of-band authenticated hashes')
  self.cache={};op,self.op_pin=self.load(A/'checkpoint_math_intake_20261006.py');pb,self.plan_pin=self.load(PLAN);self.p=json.loads(pb)
  ck(self.p['schema']=='pr134-concrete-math-intake-main-archive-plan/v3' and self.p['operator_sha256']==sha(op),'exact v3 operator/plan')
  qb,self.request_pin=self.load(REQUEST);self.q=json.loads(qb)
  gb,self.grant_pin=self.load(grant_file);eb,self.evidence_pin=self.load(evidence_file)
  ck(sha(gb)==grant_sha and sha(eb)==evidence_sha,'trusted external grant/evidence pins');self.g,self.e=json.loads(gb),json.loads(eb)
  self.expected_head=self.p['base_main'];self.expected_index=self.p['own_full_index_preimage'];self.locks=[];self.live=None;self.events=[]
  self.state={'main_ref_updates':0,'nonforce_push_attempts':0,'actual_index_installs':0,'program_install_paths':[],'no_blind_retry':True}
  self.authority()
  self.D=safe(A/'actual_math_intake_checkpoint_v3_20261006');ck(not self.D.exists(),'already attempted; inspect actual journal, never blind retry');self.D.mkdir(mode=0o700);(self.D/'.gitignore').write_bytes(b'*\n');self.journal()
 def load(self,path):
  path=safe(path);b,p=read_regular(path)
  if path in self.cache:ck(self.cache[path]==(b,p),'changed cached authority')
  self.cache[path]=(b,p);return b,p
 def authority(self):
  p,g,e,q=self.p,self.g,self.e,self.q
  ck(g['schema']=='pr134-authenticated-main-archive-peer-grant/v3' and g['source_thread_id']==PEER and g['owner_thread_id']==OWNER and g['scope']==SCOPE,'fresh peer grant identity')
  ck(g['concrete_plan_sha256']==self.plan_pin['sha256'] and g['operator_sha256']==self.op_pin['sha256'] and g['root_request_sha256']==self.request_pin['sha256'] and g['base_main']==p['base_main'],'full grant plan/operator/request/base')
  for k in ('new_public_members','program_updates','protected_primary_pins','own_full_index_preimage','own_config_preimage','primary_HEAD','counts','bounded_mutations'):ck(g[k]==p[k],'grant full binding '+k)
  ck(e['schema']=='pr134-trusted-peer-grant-message-readback/v1' and e['source_thread_id']==PEER and e['owner_thread_id']==OWNER and e['scope']==SCOPE and isinstance(e['message_id'],str) and e['message_id'],'actual trusted message identity')
  ck(e['grant_sha256']==self.grant_pin['sha256'] and e['concrete_plan_sha256']==self.plan_pin['sha256'] and e['operator_sha256']==self.op_pin['sha256'] and e['root_request_sha256']==self.request_pin['sha256'] and json.loads(e['peer_message_full_text'])==g,'complete actual grant message and authority pins')
  ck(instant(g['granted_at_utc'])<=instant(e['message_created_at_utc'])<=now(),'actual message timestamp')
  ck(q['schema']=='pr134-concrete-main-math-intake-archive-grant-request/v3' and q['scope']==SCOPE and q['owner_thread_id']==OWNER and q['peer_thread_id']==PEER and q['concrete_plan_sha256']==self.plan_pin['sha256'] and q['operator_sha256']==self.op_pin['sha256'] and q['base_main']==p['base_main'],'root request authority')
  for k in ('allowed_existing_tracked_updates','new_public_members','future_protocol_paths','counts','bounded_mutations','protected_primary_pins','own_full_index_preimage','own_config_preimage','primary_HEAD'):ck(q[k]==p[k],'request full binding '+k)
  ck(q['will_execute_only_after_exact_protocol_PASS_and_fresh_authenticated_grant'] and q['will_explicitly_release_after_actual_full_receipts'],'request PASS/fresh grant/release gates')
  ck(interval(g)>=120 and (now()-instant(g['granted_at_utc'])).total_seconds()<=120,'fresh grant and completion margin')
  self.new=member_map(p['new_public_members']);future=[relative(s) for s in p['future_protocol_paths']];old=[relative(s) for s in p['allowed_existing_tracked_updates']]
  ck(len(future)==len(set(future)) and set(future)==set(FUTURE_PATHS),'compiled exact future scope');ck(len(old)==len(set(old)) and set(old)==set(PROGRAM_PATHS),'compiled exact3existing scope')
  ck(len(p['new_public_paths'])==len(set(p['new_public_paths'])) and set(p['new_public_paths'])==set(self.new),'new paths/full pins bijection')
  ck(not(set(self.new)&set(future) or set(self.new)&set(old) or set(future)&set(old)),'scope disjointness')
  ck(len(p['program_updates'])==3 and {x['path'] for x in p['program_updates']}==set(old),'complete3programupdates')
  ck(len(p['protected_originals'])==len({x['path'] for x in p['protected_originals']})==17 and len(p['protected_primary_pins'])==len({x['path'] for x in p['protected_primary_pins']})==9,'complete17original9primary')
  self.future=member_map(g['future_protocol_members']);ck(set(self.future)==set(future)-{str(HANDOFF.relative_to(C))},'grant seals all non-handoff future bodies')
  counts={'new_public':len(self.new),'future_protocol':len(future),'existing_updates':3,'total_selected':len(self.new)+len(future)+3,'protected_originals':17,'protected_primary':9}
  ck(p['counts']==counts and p['bounded_mutations']==BOUNDS,'computed counts and compiled bounds')
  frozen=json.loads(self.load(A/'checkpoint_v1_rejected_20261006/MATH_INTAKE_CHECKPOINT_PLAN_20261006.json')[0])
  archive={str(f.relative_to(C)) for f in (A/'checkpoint_v1_rejected_20261006').rglob('*') if f.is_file()}
  exact={str((A/'checkpoint_v1_rejected_20261006'/s).relative_to(C)) for s in ('checkpoint_math_intake_20261006.py','MATH_INTAKE_CHECKPOINT_PLAN_20261006.json','MAIN_ARCHIVE_GRANT_REQUEST_20261006.json','ARCHIVE_MANIFEST.json','math_intake_checkpoint_protocol_adversary_20261006/AUDIT.md','math_intake_checkpoint_protocol_adversary_20261006/RESULT.json','math_intake_checkpoint_protocol_adversary_20261006/FINAL_MANIFEST.json')}
  oldreview={str((A/'math_intake_checkpoint_protocol_adversary_20261006'/s).relative_to(C)) for s in ('AUDIT.md','RESULT.json','FINAL_MANIFEST.json')}
  v2archive={str(f.relative_to(C)) for f in (A/'checkpoint_v2_rejected_20261006').rglob('*') if f.is_file()}
  v2exact={str((A/'checkpoint_v2_rejected_20261006'/s).relative_to(C)) for s in ('checkpoint_math_intake_20261006.py','MATH_INTAKE_CHECKPOINT_PLAN_20261006.json','MAIN_ARCHIVE_GRANT_REQUEST_20261006.json','ARCHIVE_MANIFEST.json','checkpoint_protocol_repair_20261006/REPORT.md','checkpoint_protocol_repair_20261006/RESULT.json','checkpoint_protocol_repair_20261006/FINAL_MANIFEST.json','checkpoint_protocol_v2_adversary_20261006/AUDIT.md','checkpoint_protocol_v2_adversary_20261006/RESULT.json','checkpoint_protocol_v2_adversary_20261006/FINAL_MANIFEST.json')}
  ck(archive==exact and v2archive==v2exact and set(self.new)==set(frozen['new_public_paths'])|exact|oldreview|v2exact,'exact original inventory plus v1archive7/review3/v2archive10; priority/new root outputs excluded')
  for k in ('base_main','primary_HEAD','protected_primary_pins','original_PR134_head','protected_originals','own_full_index_preimage'):ck(p[k]==frozen[k],'frozen primary/base/original authority '+k)
  self.selected={};self.bodies={}
  for path,expected in {**self.new,**self.future}.items():
   b,actual=self.load(C/path);ck(pin(b,actual['mode'])==expected,'full public body/mode '+path);ck(not b.startswith((b'%PDF',b'\x89PNG',b'\xff\xd8\xff')) and b'\0' not in b,'source/render bytes excluded');b.decode('utf8');self.selected[path]=expected;self.bodies[path]=b
  hb,hp=self.load(HANDOFF);ck(hb==encoded(deterministic_handoff(self.plan_pin,self.request_pin,self.grant_pin,self.evidence_pin,p,g,e)),'exact directional handoff derived from actual grant/evidence')
  h=str(HANDOFF.relative_to(C));self.selected[h]=pin(hb,hp['mode']);self.bodies[h]=hb;self.program=[]
  for x in p['program_updates']:
   ck(safe(x['prepared_path'])==A/'private_checkpoint_postimages_20261006'/Path(x['path']).name,'prepared own custody')
   before,bp=self.load(C/x['path']);after,ap=self.load(x['prepared_path']);ck(bp==x['preimage'] and ap==x['postimage'] and bp['mode']==ap['mode'],'cached full program pre/post/mode')
   self.program.append((x,before,after));self.selected[x['path']]=pin(after,ap['mode']);self.bodies[x['path']]=after
  ck(len(self.selected)==counts['total_selected'] and len({s.casefold() for s in self.selected})==len(self.selected),'exact selected count and no physical case aliases')
  self.protocol(REVIEW,'AUDIT.md','pr134-checkpoint-v3-operational-adversarial-result/v1',True);self.protocol(REPAIR,'REPORT.md','pr134-checkpoint-v3-repair-candidate/v1',False)
 def protocol(self,folder,report,schema,clearance):
  result=json.loads(self.load(folder/'RESULT.json')[0]);mf=json.loads(self.load(folder/'FINAL_MANIFEST.json')[0])
  ck(result['schema']==schema and result['scope']==SCOPE and result['operator_sha256']==self.op_pin['sha256'] and result['plan_sha256']==self.plan_pin['sha256'],'exact protocol result')
  if clearance:ck(result['verdict']=='PASS' and result['mandatory_corrections']==[] and result['no_mutating_operator_execution'] is True and result['no_git_index_main_native_service_writer'] is True and isinstance(result['actual_reviewer_PID'],int) and result['actual_reviewer_PID']>0,'fresh independent PASS only')
  else:ck(result['verdict']=='CANDIDATE_READY_FOR_INDEPENDENT_REVIEW' and result['no_execution'] is True,'repair candidate only, no execution clearance')
  ck(mf['scope']==SCOPE and mf['operator_sha256']==self.op_pin['sha256'] and mf['plan_sha256']==self.plan_pin['sha256'] and mf['self_excluded']=='FINAL_MANIFEST.json' and mf['self_checksum_claim'] is False,'self-excluded directional manifest')
  public=set();seen=set()
  for x in mf['files']:
   s=relative(x['path']);ck(s not in seen and s!='FINAL_MANIFEST.json','unique canonical manifest members');seen.add(s)
   if s.startswith('private_controls/'):ck(x.get('ignored_private_control') is True,'private control explicitly ignored')
   else:public.add(s);ck(not x.get('ignored_private_control'),'public protocol member')
   b,_=self.load(folder/s);ck(len(b)==x['bytes'] and sha(b)==x['sha256'],'full manifest body')
  ck(public=={report,'RESULT.json'},'exact complete public report/result membership')
 def journal(self):
  (self.D/'PROCESS_JOURNAL.json').write_bytes(encoded({'schema':'pr134-main-archive-v3-process-journal/v1','actual_operator_PID':os.getpid(),'UTC':now().isoformat(),'events':self.events,'actual_state':self.state}))
 def env(self,index=None):
  env={k:v for k,v in os.environ.items() if not k.startswith(('GIT_','DYLD_','LD_')) and (not k.startswith('GH_') or k=='GH_TOKEN') and k not in {'GITHUB_API_URL','GITHUB_GRAPHQL_URL','SSH_ASKPASS'}}
  env.update({'GIT_OPTIONAL_LOCKS':'0','GIT_CONFIG_NOSYSTEM':'1','GIT_CONFIG_SYSTEM':'/dev/null','GIT_CONFIG_GLOBAL':'/dev/null','GIT_TERMINAL_PROMPT':'0','GIT_AUTHOR_NAME':'Alec Kriebel','GIT_AUTHOR_EMAIL':'me@aleckriebel.com','GIT_COMMITTER_NAME':'Alec Kriebel','GIT_COMMITTER_EMAIL':'me@aleckriebel.com','GH_HOST':'github.com','GH_CONFIG_DIR':'/Users/alec/.config/gh','LC_ALL':'C'})
  if index is not None:
   ck(safe(index)==self.D/'OWNED_PRIVATE_INDEX','owned alternate index only');env['GIT_INDEX_FILE']=str(index)
  return env
 @staticmethod
 def group_empty(pid):
  try:os.killpg(pid,0);return False
  except ProcessLookupError:return True
 @staticmethod
 def stop(child):
  for sig,seconds in ((signal.SIGTERM,2),(signal.SIGKILL,3)):
   try:os.killpg(child.pid,sig)
   except ProcessLookupError:pass
   try:
    child.communicate(timeout=seconds)
    if Operator.group_empty(child.pid):return
   except subprocess.TimeoutExpired:pass
  ck(child.poll() is not None and Operator.group_empty(child.pid),'termination outcome uncertain')
 def run(self,exe,args,cwd=C,data=None,index=None,writer=False):
  ck(exe in (G,GH) and cwd in (C,R),'compiled executable/cwd')
  if writer:self.writer_guard()
  event={'UTC_started':now().isoformat(),'argv':[str(exe),*args],'cwd':str(cwd),'writer':writer,'deadline_seconds':None,'input_bytes':len(data) if data is not None else 0,'input_sha256':sha(data) if data is not None else None,'child_PID':None,'status':'launching'}
  self.events.append(event);self.journal();child=None;watchdog=None
  try:
   # Persisting the launching record may block. Recheck every writer invariant
   # afterwards; do not carry its earlier expiry or relative timeout forward.
   if writer:self.writer_guard()
   launch_env=self.env(index)
   remaining=interval(self.g);budget=min(60.0,remaining-2.0)
   ck(budget>0 and(not writer or remaining>=65),'fresh post-journal launch margin')
   absolute_deadline=time.monotonic()+budget
   watchdog=ChildDeadline(absolute_deadline)
   # The watchdog is independently armed before Popen or running journaling.
   ck(interval(self.g)>2 and(not writer or interval(self.g)>=65) and watchdog.remaining()>0 and not watchdog.expired,'immediate spawn authority/deadline')
   event.update(UTC_launch_admitted=now().isoformat(),deadline_seconds=budget,child_absolute_deadline_monotonic=absolute_deadline)
   child=subprocess.Popen(event['argv'],cwd=cwd,env=launch_env,stdin=subprocess.PIPE if data is not None else subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE,start_new_session=True)
   self.live=child;watchdog.bind(child.pid)
   event.update(child_PID=child.pid,process_group=child.pid,status='running',absolute_deadline_guard=watchdog.snapshot())
   ck(not watchdog.expired and watchdog.remaining()>0,'spawn returned after absolute deadline; child stopped')
   self.journal()
   # The watchdog stays active while this journal blocks. Only the remaining
   # absolute budget is available to communicate; no new60second wait begins.
   wait=watchdog.remaining();ck(wait>0 and not watchdog.expired,'running journal exhausted child deadline')
   try:out,err=child.communicate(input=data,timeout=wait)
   except BaseException:self.stop(child);event['status']='failed_or_timed_out_reaped';raise
   empty=self.group_empty(child.pid)
   if not empty:self.stop(child)
   ck(not watchdog.expired and watchdog.remaining()>0,'child absolute deadline exhausted')
   event.update(UTC_finished=now().isoformat(),exit_code=child.returncode,stdout_bytes=len(out),stdout_sha256=sha(out),stderr_bytes=len(err),stderr_sha256=sha(err),process_group_empty=self.group_empty(child.pid),child_reaped=child.poll() is not None,status='completed')
   ck(empty and event['process_group_empty'] and child.returncode==0,'failed child or descendants; no retry');interval(self.g);return out
  finally:
   try:
    if child is not None:
     if child.poll() is None or not self.group_empty(child.pid):self.stop(child)
     event.update(exit_code=child.returncode,child_reaped=child.poll() is not None,process_group_empty=self.group_empty(child.pid))
     ck(event['child_reaped'] and event['process_group_empty'],'child cleanup remains uncertain')
    self.live=None
   finally:
    if watchdog is not None:
     watchdog.close();event['absolute_deadline_guard']=watchdog.snapshot()
    event['UTC_last_recorded']=now().isoformat();self.journal()
 def git(self,*args,cwd=C,data=None,index=None):
  command=args[0];ck(command in READS|WRITES,'uncompiled Git operation');writer=command in WRITES;ck(not writer or cwd==C,'no primary Git writer')
  if command=='hash-object':ck(args==('hash-object','-w','--no-filters','--stdin-paths'),'exact unfiltered cached blob writer')
  if command=='update-index':ck(args==('update-index','-z','--index-info') and index==self.D/'OWNED_PRIVATE_INDEX','owned private index writer only')
  if command=='write-tree':ck(args==('write-tree',) and index==self.D/'OWNED_PRIVATE_INDEX','owned private tree writer only')
  if command=='commit-tree':ck(args==('commit-tree',self.tree,'-p',self.p['base_main']),'exact immutable sole-parent commit writer')
  if command=='update-ref':ck(args==('update-ref','--no-deref','refs/heads/main',self.commit,self.p['base_main']) and self.state['main_ref_updates']==0,'single CAS main update')
  if command=='fetch':ck(args==('fetch','--no-tags','--no-write-fetch-head','--no-recurse-submodules',ORIGIN,'refs/heads/main:refs/remotes/origin/main'),'exact own fetched-main ref writer')
  if command=='push':
   ck(args==('push','--no-verify','--porcelain',ORIGIN,self.commit+':refs/heads/main') and self.state['nonforce_push_attempts']==0,'single immutable nonforce Math push');self.state['nonforce_push_attempts']+=1
  prefix=['-c','core.hooksPath=/dev/null','-c','commit.gpgsign=false','-c','protocol.file.allow=never','-c','protocol.ext.allow=never','-c','protocol.ssh.allow=never','-c','credential.helper=','-c','credential.helper=!'+str(GH)+' auth git-credential','-c','user.name=Alec Kriebel','-c','user.email=me@aleckriebel.com']
  return self.run(G,[*prefix,*args],cwd=cwd,data=data,index=index,writer=writer)
 def cache_guard(self):
  for f,(b,expected) in self.cache.items():
   if f in [C/x['path'] for x,_,_ in self.program] and str(f.relative_to(C)) in self.state['program_install_paths']:continue
   current,p=read_regular(f);ck(current==b and p==expected,'cached authority changed '+str(f))
 def materialized_guard(self):
  for path,expected in self.selected.items():
   b,p=read_regular(C/path)
   if path in PROGRAM_PATHS and path not in self.state['program_install_paths']:
    x=next(x for x,_,_ in self.program if x['path']==path);ck(p==x['preimage'],'program preimage until installed')
   else:ck(pin(b,p['mode'])==expected,'full materialized selected bytes/modes')
 def guard(self):
  interval(self.g);ck(self.git('rev-parse','HEAD',cwd=R).decode().strip()==self.p['primary_HEAD'],'primary HEAD')
  for x in self.p['protected_primary_pins']:ck(read_regular(x['path'])[1]=={k:x[k] for k in ('bytes','sha256','mode')},'primary9 full physical invariants')
  ck(self.git('symbolic-ref','-q','HEAD').decode().strip()=='refs/heads/main' and self.git('rev-parse','refs/heads/main').decode().strip()==self.expected_head,'own exact main/phase HEAD')
  ck(read_regular(C/'.git/index')[1]==self.expected_index and read_regular(C/'.git/config')[1]==self.p['own_config_preimage'],'own phase full index/config')
  self.cache_guard();self.materialized_guard()
  for path,fd,identity in self.locks:
   s=path.lstat();t=os.fstat(fd);ck((s.st_dev,s.st_ino)==identity and (t.st_dev,t.st_ino)==identity and stat.S_ISREG(s.st_mode),'own lock custody')
  interval(self.g)
 def writer_guard(self):
  ck(len(self.locks)==2,'exclusive actual index/config locks required');self.guard();ck(interval(self.g)>=65,'authorized completion margin after expensive guard')
 def tree_map(self,ref):
  out={}
  for record in self.git('ls-tree','-r','-z',ref).split(b'\0'):
   if record:
    left,path=record.split(b'\t',1);mode,kind,blob=left.decode().split();s=path.decode('utf8');ck(s not in out,'duplicate tree member');out[s]=(mode,kind,blob)
  return out
 def verify_tree(self,ref,expected):
  actual=self.tree_map(ref);ck(actual==expected,'complete tree/base preservation/exact modes');paths=sorted(self.selected);blobs=[actual[s][2] for s in paths]
  raw=self.git('cat-file','--batch',data=('\n'.join(blobs)+'\n').encode());at=0;receipt=[]
  for s,blob in zip(paths,blobs):
   end=raw.index(b'\n',at);h=raw[at:end].decode().split();ck(len(h)==3 and h[0]==blob and h[1]=='blob','full regular blob frame');size=int(h[2]);b=raw[end+1:end+1+size];ck(len(b)==size and raw[end+1+size:end+2+size]==b'\n','complete blob');at=end+2+size;x=self.selected[s]
   ck(size==x['bytes'] and sha(b)==x['sha256'] and actual[s][0]==x['git_mode'],'full selected blob/mode');receipt.append({'path':s,**x,'Git_blob':blob})
  ck(at==len(raw),'no unparsed output');return receipt
 def remote(self):
  lines=self.git('ls-remote',ORIGIN,'refs/heads/main').decode().splitlines();ck(len(lines)==1 and lines[0].split()[1]=='refs/heads/main','exact Math main remote');return lines[0].split()[0]
 def target(self):
  pr=json.loads(self.run(GH,['api','--hostname','github.com','--method','GET','repos/AlecKriebel/Math/pulls/134']))
  ck(pr['number']==134 and pr['html_url']=='https://github.com/AlecKriebel/Math/pull/134' and pr['head']['sha']==self.p['original_PR134_head'] and pr['state']=='open' and pr['draft'] and not pr['merged'],'same original open draft134')
 def semantics(self):
  p=self.p
  for x in p['protected_originals']:
   b,_=self.load(A/'original_head_authentication_20261006/original_attempt'/relative(x['path']));ck(len(b)==x['bytes'] and sha(b)==x['sha256'] and oid(b)==x['Git_blob'],'original17 full bytes/blobs')
  auth=json.loads(self.cache[A/'original_head_authentication_20261006/ORIGINAL_AUTHENTICATION.json'][0]);ready=json.loads(self.cache[A/'original_head_authentication_20261006/original_attempt/readiness.json'][0])
  ck(auth['original_files']==p['protected_originals'] and auth['original_budget']=='1/5' and auth['original_literal_status']=='claimed_solved' and auth['original_head']==p['original_PR134_head'] and ready['substantive_approaches']==1 and not ready['novelty_established'] and not ready['human_peer_review'],'original immutable1/5 ledger')
  gate=json.loads(self.cache[A/'MATHEMATICS_SOURCE_GATE_20261006.json'][0]);ck(gate['verdict']=='PASS_EXACT_MATHEMATICS_AND_SOURCE_AFTER_EXERCISED_METHOD_CONTROL_REPAIR' and gate['original_head']==p['original_PR134_head'] and gate['original_effort']=='1/5' and gate['original_readiness_substantive_approaches']==1 and gate['original_17_full_bodies_and_Git_blobs_unchanged'] and gate['completion_math_source_percent']==100 and gate['priority_gate']=='now may begin; no novelty clearance' and not gate['service_mutations'],'sealed science-only gate')
  old=A.parent/'pr126_11000147';meta=json.loads(self.cache[old/'actual_completion_metadata_20261006/RECEIPT.json'][0]);back=json.loads(self.cache[old/'actual_final_completion_readback_20261006/RECEIPT.json'][0]);rel=json.loads(self.cache[old/'FINAL_COMPLETION_OWNER_RELEASE_20261006.json'][0]);resp=json.loads(self.cache[old/'FINAL_COMPLETION_RELEASE_API_RESPONSE_20261006.json'][0])
  ck(meta['commit']==p['base_main'] and meta['actual_full_changed_bodies_verified'] and meta['actual_nonforce_push_passed'] and back['metadata_checkpoint_commit']==p['base_main'] and back['remote_main']==p['base_main'] and back['latest_combined_body_count']==261 and back['all_latest_native_and_metadata_changed_bodies_verified'] and rel['writer_ownership_released'] and rel['actual_release_API_accepted'] and not rel['writer_release_pending'] and not resp['isError'] and json.loads(resp['content'][0]['text'])['threadId']==PEER,'old126 actual metadata/readback/release')
  root=P/'ordered_intake_20261006/after_PR126';intake=json.loads(self.cache[root/'INTAKE_AFTER_PR126.json'][0]);rows=intake['ascending_status_only_rows']
  ck([x['PR'] for x in rows]==list(range(127,135)) and all(not x['eligible'] and x['literal_status']!='claimed_solved' and not x['math_review_or_service_action_if_ineligible'] for x in rows[:-1]),'127–133 status-only skips')
  ck(rows[-1]['eligible'] and rows[-1]['literal_status']=='claimed_solved' and rows[-1]['effort']=='1/5' and rows[-1]['head']==p['original_PR134_head'] and intake['next_eligible_PR']==134 and intake['previous_PR126_completed_and_writer_released'] and intake['Git_mutations']==intake['service_writes']==0,'134-only intake')
  for x in rows:
   b=self.cache[root/f'PR{x["PR"]}_AUTHENTICATED_HEAD_QUEUE.md'][0];ck(len(b)==x['queue_bytes'] and sha(b)==x['queue_sha256'] and oid(b)==x['queue_Git_blob'] and x['row'].encode() in b,'full immutable queue snapshot')
  prog=json.loads(next(after for x,_,after in self.program if x['path']==PROGRAM_PATHS[0]));ck(prog['current_PR']==134 and prog['current_original_head']==p['original_PR134_head'] and prog['current_original_budget']=='1/5' and prog['current_new_central_proof_search_turns']==0 and prog['current_mathematical_audit_percent']==prog['current_source_authentication_percent']==100 and not prog['current_priority_clearance'] and not prog['current_novelty_established'] and not prog['current_publication_ready'] and not prog['current_tracker_updated'] and not prog['current_Zenodo_published'],'prepared exact science/priority boundary')
  ck(prog['fully_completed_count']==len(prog['fully_completed_eligible_PRs'])==p['program_completed']==22 and len(prog['published_PRs'])==p['published']==11 and prog['dated_eligible_total']==99 and prog['persistent_goal_status']=='active' and not prog['persistent_goal_complete'] and prog['last_completed_PR']==126 and prog['last_completed_metadata_checkpoint_commit']==p['base_main'],'actual22/11 and incomplete goal')
 def preflight(self):
  ck(self.git('rev-parse','--show-toplevel').decode().strip()==str(C) and self.git('rev-parse','--absolute-git-dir').decode().strip()==str(C/'.git') and self.git('rev-parse','--show-object-format').strip()==b'sha1','own repository identity')
  config={}
  for r in self.git('config','--local','--includes','--list','--null').split(b'\0'):
   if r:
    k,v=r.decode().split('\n',1);ck(k not in config,'duplicate config');config[k]=v
  ck(config==SAFE_CONFIG and self.p['own_config_values']==SAFE_CONFIG,'exact safe local config; no includes/url rewrites/hooks/filters')
  ck(set(self.p['executable_pins'])=={str(G),str(GH)},'compiled executables')
  for path,expected in self.p['executable_pins'].items():ck(self.load(path)[1]==expected,'executable full pin')
  self.guard();ck(not self.git('diff','--no-ext-diff','--no-textconv','--cached','--name-only') and not self.git('diff','--no-ext-diff','--no-textconv','--name-only','--diff-filter=ACMRTUXB'),'initial own index/nondeletion materialized baseline');ck(self.remote()==self.p['base_main'],'exact remote base');self.base=self.tree_map(self.p['base_main'])
  new=set(self.new)|set(self.p['future_protocol_paths']);ck(not new&set(self.base) and set(PROGRAM_PATHS)<=set(self.base),'all new/future collision checks')
  base_fold={s.casefold() for s in self.base};ancestor_fold={str(q).casefold() for s in self.base for q in PurePosixPath(s).parents if str(q)!='.'}
  for s in new:ck(s.casefold() not in base_fold|ancestor_fold and not any(str(q).casefold() in base_fold for q in PurePosixPath(s).parents),'file/directory/case tree collision')
  for x,b,_ in self.program:ck(self.base[x['path']]==(regular_mode(x['preimage']['mode']),'blob',oid(b)),'full exact-base program body/mode')
  self.semantics();ignored=[str(f.relative_to(C)) for f in self.cache if '/private_controls/' in str(f) or f.parent==AUTHORITY or f.parent==A/'private_checkpoint_postimages_20261006']
  ignored += [str(f.relative_to(C)) for root in (A/'private_primary_sources_20261006',A/'analytic_zero_boundary_adversary_20261006/private_sources') for f in root.rglob('*') if f.is_file() and f.name!='.gitignore']
  ck(set(self.git('check-ignore','--',*sorted(set(ignored))).decode().splitlines())==set(ignored) and not set(ignored)&set(self.selected),'private controls/authority/postimages/sources ignored and excluded');self.target()
 def acquire(self):
  self.guard()
  for name in ('index.lock','config.lock'):
   path=safe(C/'.git'/name);fd=os.open(path,os.O_WRONLY|os.O_CREAT|os.O_EXCL|os.O_NOFOLLOW,0o600);s=os.fstat(fd);self.locks.append((path,fd,(s.st_dev,s.st_ino)))
  self.writer_guard()
 def install_program(self):
  for x,before,after in self.program:
   self.writer_guard();path=safe(C/x['path']);fd=os.open(path,os.O_RDWR|os.O_NOFOLLOW)
   try:
    s=os.fstat(fd);ck(stat.S_ISREG(s.st_mode) and s.st_nlink==1 and s.st_mode&0o7777==x['preimage']['mode'],'owned program descriptor');parts=[]
    while True:
     b=os.read(fd,1024*1024)
     if not b:break
     parts.append(b)
    ck(b''.join(parts)==before and (path.lstat().st_dev,path.lstat().st_ino)==(s.st_dev,s.st_ino),'exact cached preimage at writer boundary');ck(interval(self.g)>=65,'immediate program writer deadline');os.lseek(fd,0,os.SEEK_SET);os.ftruncate(fd,0);view=memoryview(after)
    while view:view=view[os.write(fd,view):]
    os.fsync(fd)
   finally:os.close(fd)
   self.state['program_install_paths'].append(x['path']);self.journal();self.materialized_guard();interval(self.g)
 def execute(self):
  self.preflight();self.acquire();self.install_program();ib,_=read_regular(C/'.git/index');self.private_index=self.D/'OWNED_PRIVATE_INDEX';self.private_index.write_bytes(ib)
  ck(self.git('write-tree',index=self.private_index).decode().strip()==self.git('rev-parse',self.p['base_main']+'^{tree}').decode().strip(),'full private index baseline tree');inputs=[]
  for n,path in enumerate(sorted(self.selected)):
   f=self.D/f'BLOB_INPUT_{n:04d}';f.write_bytes(self.bodies[path]);self.load(f);inputs.append(str(f))
  blobs=self.git('hash-object','-w','--no-filters','--stdin-paths',data=('\n'.join(inputs)+'\n').encode()).decode().splitlines();ck(blobs==[oid(self.bodies[s]) for s in sorted(self.selected)],'complete unfiltered cached blob identities');rows=[];self.expected_tree=dict(self.base)
  for s,blob in zip(sorted(self.selected),blobs):
   mode=self.selected[s]['git_mode'];rows.append((mode+' '+blob+'\t'+s).encode()+b'\0');self.expected_tree[s]=(mode,'blob',blob)
  self.git('update-index','-z','--index-info',data=b''.join(rows),index=self.private_index);self.tree=self.git('write-tree',index=self.private_index).decode().strip();self.staged=self.verify_tree(self.tree,self.expected_tree)
  ck({s for s in self.expected_tree if self.expected_tree.get(s)!=self.base.get(s)}==set(self.selected),'exact staged scope/no deletions');stage_index,stage_pin=read_regular(self.private_index);self.guard();ck(self.remote()==self.p['base_main'],'remote before immutable main commit')
  self.commit=self.git('commit-tree',self.tree,'-p',self.p['base_main'],data=b'Audit PR134 mathematics and preserve completed PR126 readbacks\n').decode().strip();headers=self.git('cat-file','-p',self.commit).split(b'\n\n',1)[0].decode().splitlines()
  ck([h for h in headers if h.startswith('tree ')]==['tree '+self.tree] and [h for h in headers if h.startswith('parent ')]==['parent '+self.p['base_main']],'immutable exact-tree single-parent commit');self.committed=self.verify_tree(self.commit,self.expected_tree);ck(read_regular(self.private_index)==(stage_index,stage_pin),'full private index unchanged before CAS')
  self.git('update-ref','--no-deref','refs/heads/main',self.commit,self.p['base_main']);self.state['main_ref_updates']=1;self.expected_head=self.commit;self.journal();self.writer_guard()
  install=self.D/'ACTUAL_INDEX_INSTALL';install.write_bytes(stage_index);os.chmod(install,self.p['own_full_index_preimage']['mode']);post={'bytes':len(stage_index),'sha256':sha(stage_index),'mode':self.p['own_full_index_preimage']['mode']};ck(read_regular(install)[1]==post,'complete own index install');self.writer_guard();os.replace(install,C/'.git/index');self.expected_index=post;self.state['actual_index_installs']=1;self.journal();self.guard()
  ck(not self.git('diff','--no-ext-diff','--no-textconv','--cached','--name-only') and not self.git('diff','--no-ext-diff','--no-textconv','--name-only','--diff-filter=ACMRTUXB'),'actual own index and nondeletion materialized state match commit');self.verify_tree(self.commit,self.expected_tree);ck(self.remote()==self.p['base_main'],'remote before immutable nonforce push');self.target()
  self.git('push','--no-verify','--porcelain',ORIGIN,self.commit+':refs/heads/main');ck(self.remote()==self.commit,'actual pushed Math main readback');self.git('fetch','--no-tags','--no-write-fetch-head','--no-recurse-submodules',ORIGIN,'refs/heads/main:refs/remotes/origin/main');ck(self.git('rev-parse','refs/remotes/origin/main').decode().strip()==self.commit,'actual fetched main');self.fetched=self.verify_tree('refs/remotes/origin/main',self.expected_tree);self.guard();self.target()
  ck(self.state['main_ref_updates']==self.state['nonforce_push_attempts']==self.state['actual_index_installs']==1 and self.live is None,'actual bounded operations/reaped children');self.state['full_execution_verified']=True;self.journal()
  v={'schema':'pr134-actual-math-intake-main-checkpoint/v3','UTC':now().isoformat(),'actual_operator_PID':os.getpid(),'scope':SCOPE,'sole_parent':self.p['base_main'],'commit':self.commit,'tree':self.tree,'actual_nonforce_push_and_remote_fetched_readback':True,'full_selected_member_count':len(self.selected),'full_staged_members':self.staged,'full_committed_members':self.committed,'full_fetched_members':self.fetched,'full_materialized_members':[{'path':s,**self.selected[s]} for s in sorted(self.selected)],'staging_method':'owned private index under exclusive actual index/config locks; immutable tree/commit; CAS main; atomic actual index install','own_final_full_index_pin':read_regular(C/'.git/index')[1],'primary_HEAD_and_nine_physical_pins_unchanged':True,'same_original_open_draft_PR134_verified':True,'original1of5_unchanged':True,'new_central_proof_search_turns':0,'program_completed':22,'published':11,'math_source':100,'priority_in_progress_no_clearance':True,'paper_Zenodo_tracker_merge_close_comment_native_author_actions':False,'all_controlled_children_reaped_and_groups_empty':True,'actual_writer_release_still_required':True,'plan':self.plan_pin,'operator':self.op_pin,'grant':self.grant_pin,'trusted_peer_evidence':self.evidence_pin,'no_self_commit_claim':True,'actual_state':dict(self.state)}
  (self.D/'RECEIPT.json').write_bytes(encoded(v));return {'UTC':v['UTC'],'actual_operator_PID':os.getpid(),'commit':self.commit,'full_selected_member_count':len(self.selected),'actual_writer_release_still_required':True}
 def close(self):
  if self.live is not None:self.stop(self.live);self.live=None
  for path,fd,identity in reversed(self.locks):
   try:
    s=path.lstat();ck((s.st_dev,s.st_ino)==identity,'refuse foreign/replaced lock removal');path.unlink()
   finally:os.close(fd)
  self.locks=[]
  if hasattr(self,'D'):self.state['own_exclusive_locks_released']=True;self.journal()

def main(argv):
 ck(len(argv)==6 and argv[1]=='checkpoint','checkpoint plus exact private grant/evidence paths and out-of-band authenticated hashes');op=None
 try:
  op=Operator(Path(argv[2]),argv[3],Path(argv[4]),argv[5]);result=op.execute();op.close();print(json.dumps(result,sort_keys=True))
 except BaseException as exc:
  if op is not None:
   op.state['failure']={'type':type(exc).__name__,'message':str(exc),'UTC':now().isoformat(),'actual_outcome_requires_inspection_and_fresh_authority_before_retry':True}
   try:op.journal()
   finally:op.close()
  raise
if __name__=='__main__':main(sys.argv)
