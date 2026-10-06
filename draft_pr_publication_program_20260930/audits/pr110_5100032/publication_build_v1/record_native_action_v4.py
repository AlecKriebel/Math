#!/usr/bin/env python3
"""Actual bounded outer action custody; the reviewed phase source defines the mutation."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,os,selectors,signal,stat,subprocess,sys,time
A=Path(__file__).resolve().parents[1];D=A/'native_execution_programs_v1';C=A.parents[2]
def now():return datetime.now(timezone.utc).isoformat()
def canonical(v):return (json.dumps(v,sort_keys=True,ensure_ascii=False,indent=2,allow_nan=False)+'\n').encode()
def hp(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def need(v,m):
 if not v:raise RuntimeError(m)
def clean():
 e={'PATH':'/usr/bin:/bin','LC_ALL':'C','LANG':'C','TZ':'UTC'}
 if sys.platform=='darwin':e['__CF_USER_TEXT_ENCODING']='0x'+format(os.getuid(),'X')+':0x0:0x0'
 return e
def main():
 label=sys.argv[1];action=sys.argv[2];config=Path(sys.argv[3]);need(label.replace('_','').isalnum() and config.is_relative_to(A) and action in ('export','acceptance_commit','ready','merge','status'),'Dedicated actual action launch')
 cfg=json.loads(config.read_bytes());packet=json.loads((A/cfg['packet_pin']['path']).read_bytes());packetraw=(A/cfg['packet_pin']['path']).read_bytes();need(cfg['action']==action and cfg['clearance'] is True and cfg['outer_launcher_pin']=={'path':str(Path(__file__).resolve().relative_to(A)),**hp(Path(__file__).read_bytes())},'Exact action and reviewed outer source')
 need(hp(packetraw)=={k:cfg['packet_pin'][k] for k in ('bytes','sha256')},'Exact packet before choosing the interpreter')
 source=A/'native_post_assess_carryforward_v3_20261006/native_acceptance_actions_v4.py';need(cfg['program_pin']['path']==str(source.relative_to(A)) and hp(source.read_bytes())=={k:cfg['program_pin'][k] for k in ('bytes','sha256')},'Exact phase source before launch')
 env=clean();cf=env.get('__CF_USER_TEXT_ENCODING','');python=packet['runtime']['binaries']['python']['resolved_absolute_path'];need(hp(Path(python).read_bytes())=={k:packet['runtime']['binaries']['python'][k] for k in ('bytes','sha256')},'Current physical interpreter bytes before launch')
 argv=['/usr/bin/env','-i']+[k+'='+v for k,v in env.items()]+[python,'-E','-S','-B','-P',str(A/'native_post_assess_carryforward_v3_20261006/native_acceptance_actions_v4.py'),action,str(config)]
 outdir=A/'actual_operations'/label;outdir.mkdir(mode=0o700,parents=True,exist_ok=False);(outdir/'ancestry').mkdir(mode=0o700)
 workspace=A/'actual_acceptance_actions_20261006'/cfg['operation_label'];need(not workspace.exists(),'Fresh action custody directory only')
 start=now();begin=time.monotonic();p=None;sel=None;launch=None;spawn_critical=False;pending_signal=None;cleaning=False;probe_bytes=0
 caps={'stdout':1048576,'stderr':65536};count={s:0 for s in caps};hashes={s:hashlib.sha256() for s in caps};buf={s:bytearray() for s in caps};groups=set();discoveries=[];cleanup=[];reason=None;term=None
 def terminated(sig,frame):
  nonlocal pending_signal
  if spawn_critical or cleaning:pending_signal=sig;return
  raise SystemExit('Actual outer termination signal '+signal.Signals(sig).name)
 signal.signal(signal.SIGTERM,terminated);signal.signal(signal.SIGINT,terminated)
 def exists(group):
  try:os.killpg(group,0);return True
  except ProcessLookupError:return False
  except PermissionError:cleanup.append({'PGID':group,'action':'probe','error':'EPERM_absence_unconfirmed'});return True
 def send(group,sig):
  try:os.killpg(group,sig)
  except ProcessLookupError:pass
  except PermissionError:cleanup.append({'PGID':group,'action':signal.Signals(sig).name,'error':'EPERM'})
 def discover():
  nonlocal spawn_critical,probe_bytes
  need(len(discoveries)<160 and probe_bytes<=16*1024*1024,'Bounded ancestry probe count/aggregate')
  journal=workspace/'PROCESS_LAUNCHES.json'
  if journal.exists():
   need(not journal.is_symlink() and journal.stat().st_size<=128*1024,'Bounded real launch journal')
   j=json.loads(journal.read_bytes());need(j['actual_operator_PID']==p.pid,'Actual action operator/journal PID')
   for row in j['launches']:
    need(type(row['PID']) is int and row['PID']>0 and isinstance(row['argv'],list) and row['cwd']==str(A.parents[2]),'Actual recorded phase child')
    groups.add(row['PID'])
  # Best-effort actual ancestry observations supplement the launch journal.
  # Kernel SIGKILL before registration can reparent an unobserved child;
  # polling does not prove complete containment of that exceptional case.
  t=now();q=None;qs=None;why=None;drained=False;qargv=['/bin/ps','-axo','pid=,ppid=,pgid='];qc={'stdout':1048576,'stderr':65536};qb={k:bytearray() for k in qc};qn={k:0 for k in qc};qh={k:hashlib.sha256() for k in qc};qbegin=time.monotonic()
  try:
   spawn_critical=True
   try:
    q=subprocess.Popen(qargv,cwd=C,stdout=subprocess.PIPE,stderr=subprocess.PIPE,env=env,start_new_session=True);groups.add(q.pid)
   finally:spawn_critical=False
   if pending_signal is not None:raise SystemExit('Deferred outer signal during ancestry spawn')
   qs=selectors.DefaultSelector()
   for name,f in [('stdout',q.stdout),('stderr',q.stderr)]:os.set_blocking(f.fileno(),False);qs.register(f,selectors.EVENT_READ,name)
   while qs.get_map() or q.poll() is None:
    if time.monotonic()-qbegin>2:
     why='deadline_KILL_and_reap';send(q.pid,signal.SIGKILL)
    if time.monotonic()-qbegin>2.5:break
    for key,_ in qs.select(.02):
     b=os.read(key.fileobj.fileno(),65536);name=key.data
     if not b:qs.unregister(key.fileobj);key.fileobj.close();continue
     qn[name]+=len(b);qh[name].update(b);qb[name].extend(b[:max(0,qc[name]-len(qb[name]))])
     if qn[name]>qc[name]:why=name+'_cap_KILL_and_reap';send(q.pid,signal.SIGKILL)
   drained=not bool(qs.get_map())
  except BaseException:
   why='outer_exception';raise
  finally:
   if qs is not None:qs.close()
   if q is not None:
    if q.poll() is None:send(q.pid,signal.SIGKILL)
    try:q.wait(timeout=1)
    except subprocess.TimeoutExpired:why='unreaped_intervention_required'
    for f in (q.stdout,q.stderr):
     if not f.closed:f.close()
    index=len(discoveries);row={'actual_PID':q.pid,'argv':qargv,'cwd':str(C),'environment_sha256':hashlib.sha256(canonical(env)).hexdigest(),'UTC_start':t,'UTC_end':now(),'reaped':q.returncode is not None,'exit_code':q.returncode,'termination_reason':why,'streams_fully_drained':drained,'ps_executable_pin':hp(Path('/bin/ps').read_bytes())}
    for name in qc:
     body=bytes(qb[name]);rel='ancestry/'+str(index)+'.'+name+'.bin';need(probe_bytes+len(body)<=16*1024*1024,'Outer ancestry aggregate capacity');(outdir/rel).write_bytes(body);probe_bytes+=len(body)
     row[name]={'path':rel,**hp(body),'observed_bytes':qn[name],'observed_sha256':qh[name].hexdigest(),'full_raw_body':drained and qn[name]==len(body)}
    discoveries.append(row);receipt=canonical(row);need(probe_bytes+len(receipt)<=16*1024*1024,'Outer ancestry receipt capacity');(outdir/'ancestry'/(str(index)+'.execution.json')).write_bytes(receipt);probe_bytes+=len(receipt)
  need(q is not None and q.returncode==0 and why is None and drained and not qb['stderr'],'Actual bounded successful ancestry probe')
  rows=[tuple(map(int,l.split())) for l in bytes(qb['stdout']).splitlines() if l.strip()];known={p.pid};changed=True
  while changed:
   changed=False
   for pid,ppid,pgid in rows:
    if ppid in known and pid not in known:known.add(pid);groups.add(pgid);changed=True
  discoveries[-1]['descendant_PIDs']=sorted(known-{p.pid})
 def stop(why):
  nonlocal reason,term
  if reason is None:
   reason=why;term=time.monotonic()
   for g in groups:send(g,signal.SIGTERM)
 pending=None;lastdiscover=0
 try:
  spawn_critical=True
  try:
   p=subprocess.Popen(argv,cwd=C,env=env,stdout=subprocess.PIPE,stderr=subprocess.PIPE,start_new_session=True);groups.add(p.pid)
  finally:spawn_critical=False
  if pending_signal is not None:raise SystemExit('Deferred actual outer termination signal '+signal.Signals(pending_signal).name)
  launch={'actual_operator_PID':os.getpid(),'child_PID':p.pid,'argv':argv,'cwd':str(C),'environment_sha256':hashlib.sha256(canonical(env)).hexdigest(),'UTC_start':start}
  (outdir/'LAUNCH.json').write_bytes(canonical(launch))
  sel=selectors.DefaultSelector()
  for kind,f in [('stdout',p.stdout),('stderr',p.stderr)]:os.set_blocking(f.fileno(),False);sel.register(f,selectors.EVENT_READ,kind)
  while sel.get_map() or p.poll() is None:
   elapsed=time.monotonic()-begin
   if elapsed>=300:stop('whole_launch_deadline')
   if elapsed-lastdiscover>=2 and p.poll() is None:discover();lastdiscover=elapsed
   if term is not None and time.monotonic()-term>=2:
    for g in groups:send(g,signal.SIGKILL)
   if elapsed>=305:stop('drain_deadline');break
   for key,_ in sel.select(.1):
    b=os.read(key.fileobj.fileno(),65536);kind=key.data
    if not b:sel.unregister(key.fileobj);key.fileobj.close();continue
    count[kind]+=len(b);hashes[kind].update(b);buf[kind].extend(b[:max(0,caps[kind]-len(buf[kind]))])
    if count[kind]>caps[kind]:stop(kind+'_cap')
 except BaseException as error:pending=error;stop('outer_exception:'+type(error).__name__)
 finally:
  cleaning=True
  drained=sel is not None and not bool(sel.get_map())
  if sel is not None:sel.close()
  if p is None:
   (outdir/'FAILURE_BEFORE_SPAWN.json').write_bytes(canonical({'actual_operator_PID':os.getpid(),'UTC':now(),'argv':argv,'error':str(pending)[:300],'actual_child_spawned':False}))
   raise RuntimeError('No child spawned; actual pre-spawn failure retained')
  groups.add(p.pid)
  if launch is None:launch={'actual_operator_PID':os.getpid(),'child_PID':p.pid,'argv':argv,'cwd':str(C),'environment_sha256':hashlib.sha256(canonical(env)).hexdigest(),'UTC_start':start}
  # One final journal read covers descendants which completed between polls.
  try:discover()
  except BaseException as error:cleanup.append({'action':'final_discovery','error':str(error)[:300]})
  try:p.wait(timeout=1)
  except subprocess.TimeoutExpired:stop('operator_cleanup')
  active=[g for g in groups if exists(g)]
  if active:
   stop('surviving_group_cleanup')
   for g in active:send(g,signal.SIGTERM)
   end=time.monotonic()+2
   while any(exists(g) for g in active) and time.monotonic()<end:time.sleep(.02)
   for g in active:
    if exists(g):send(g,signal.SIGKILL)
  try:p.wait(timeout=3)
  except subprocess.TimeoutExpired:cleanup.append({'action':'direct_reap','error':'deadline_unreaped'})
  for f in (p.stdout,p.stderr):
   if not f.closed:f.close()
  absent=all(not exists(g) for g in groups)
 streams={}
 for kind in caps:
  body=bytes(buf[kind]);(outdir/(kind+'.bin')).write_bytes(body)
  streams[kind]={'path':kind+'.bin',**hp(body),'observed_bytes':count[kind],'observed_sha256':hashes[kind].hexdigest(),'body_custody':'full_actual_raw_CLI_stream' if drained and count[kind]==len(body) else 'explicit_truncated_prefix'}
 receipt={**launch,'schema':'pr110-actual-bounded-native-action-launch/v1','action':action,'UTC_end':now(),'exit_code':p.returncode,'reaped':p.returncode is not None,'whole_launch_deadline_seconds':300,'termination_reason':reason,'pending_actual_signal':pending_signal,'streams_fully_drained':drained,'recorded_PGIDs':sorted(groups),'all_recorded_groups_absence_confirmed':absent,'cleanup_errors':cleanup,'actual_ancestry_probes':discoveries,'ancestry_count_cap':160,'ancestry_file_count_cap':480,'ancestry_aggregate_cap':16*1024*1024,'ancestry_retained_total_bytes':probe_bytes,'ps_executable_pin':hp(Path('/bin/ps').read_bytes()),'outer_source_pin':hp(Path(__file__).read_bytes()),'kernel_SIGKILL_before_child_registration_complete_containment_claimed':False,'process_absence_scope':'Actual observed and recorded groups only; interrupted runs cannot be accepted or exported.','packet_sha256':hashlib.sha256(packetraw).hexdigest(),'config_pin':hp(config.read_bytes()),'actual_action_custody_path':str(workspace),'elapsed_monotonic_seconds':time.monotonic()-begin,**streams}
 (outdir/'execution.json').write_bytes(canonical(receipt));print(json.dumps({'label':label,'child_PID':p.pid,'exit_code':p.returncode,'action_custody':str(workspace),'all_groups_absent':absent,'termination_reason':reason}))
 need(pending is None and p.returncode==0 and reason is None and drained and absent and not cleanup,'Actual native outer launch failed; honest receipt retained')
if __name__=='__main__':main()
