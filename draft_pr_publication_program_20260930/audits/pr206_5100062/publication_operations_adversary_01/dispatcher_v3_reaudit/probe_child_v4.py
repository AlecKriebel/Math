"""SYNTHETIC_NON_RECEIPT. Exact dispatcher buffers with bounded owned fake contexts."""
import sys
sys.dont_write_bytecode=True
from pathlib import Path
import argparse,builtins,contextlib,hashlib,io,json,os,stat,traceback,types
ROOT=Path(__file__).resolve().parent
probe=sys.argv[1];version=sys.argv[2];runid=sys.argv[3]
SOURCE=ROOT/('reviewed_dispatcher_'+version+'.py');RAW=SOURCE.read_bytes()
PINS={'v2':(5148,'3cce6202317f138d4c37f15dabf58f70492e170113a7cfae2f4a9c4918cecb63'),'v3':(5631,'94faca0bac216ebbca4e641bfa848bacddaae61f71544b44371361e60f2a3604'),'v4':(5737,'f927ec97eceeb73aaef7f6eec030b3697596930021efd946c04cccc07f2ecd2e')}
if (len(RAW),hashlib.sha256(RAW).hexdigest())!=PINS[version]:raise RuntimeError('reviewed source drift')
BASE=ROOT/'fixtures'/runid;BASE.mkdir(parents=True)
BLOCKED=[]
def own(path):
 if isinstance(path,int):return True
 return Path(os.fsdecode(path)).resolve().is_relative_to(ROOT)
def audit(event,args):
 if event.startswith(('socket.','subprocess.','http.client.','urllib.')) or event in ('os.system','os.fork','os.posix_spawn'):
  BLOCKED.append(event);raise RuntimeError('PROHIBITED_TRANSPORT')
 if event=='open':
  path,mode,flags=args;write=(isinstance(mode,str) and any(c in mode for c in 'wax+')) or (isinstance(flags,int) and bool(flags&(os.O_CREAT|os.O_TRUNC|os.O_WRONLY|os.O_RDWR|os.O_APPEND)))
  if write and not own(path):raise RuntimeError('WRITE_OUTSIDE_OWNED_SUBFOLDER')
 if event in ('os.mkdir','os.remove','os.rmdir','os.mkfifo','os.chmod') and not own(args[0]):raise RuntimeError('MUTATION_OUTSIDE_OWNED_SUBFOLDER')
sys.addaudithook(audit)
def pin(raw):return {'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()}
def write(path,obj):
 path.parent.mkdir(parents=True,exist_ok=True)
 if path.exists() and not path.is_symlink():path.chmod(0o600)
 path.write_bytes(obj if type(obj)is bytes else (json.dumps(obj,sort_keys=True)+'\n').encode());path.chmod(0o444);return path
meta={'SYNTHETIC_NON_RECEIPT':True,'probe':probe,'version':version,'reviewed_source_pin':pin(RAW),'checks':[],'compiled':[],'blocked_events':BLOCKED,'runtime':{'argv_at_start':list(sys.argv),'flags':repr(sys.flags),'executable':sys.executable,'version':sys.version}}
def check(ok,msg):
 if type(ok)is not bool or not ok:raise RuntimeError('HARNESS_CHECK:'+msg)
 meta['checks'].append(msg)
def rejected(fn,msg):
 try:fn()
 except BaseException as e:meta.setdefault('expected_rejections',[]).append({'probe':msg,'type':type(e).__name__,'body':str(e)});check(True,msg);return
 raise RuntimeError('FALSE_ACCEPT:'+msg)
exitcode=0
try:
 if probe.startswith('flag_'):
  imports=[]
  if probe=='flag_real_optimized':
   def importer(name,*a,**kw):imports.append(name);return builtins.__import__(name,*a,**kw)
  else:
   flags=types.SimpleNamespace(ignore_environment=1,no_site=1,safe_path=True,optimize=0);fake=types.SimpleNamespace(flags=flags,dont_write_bytecode=True)
   name=probe.removeprefix('flag_')
   if name=='dont_write_bytecode':fake.dont_write_bytecode=False
   else:setattr(flags,name,1 if name=='optimize' else 0)
   def importer(name,*a,**kw):
    imports.append(name)
    if name=='sys':return fake
    raise RuntimeError('HARNESS_UNEXPECTED_IMPORT:'+name)
  ns={'__name__':'audit_flags','__file__':str(SOURCE),'__builtins__':dict(vars(builtins),__import__=importer)}
  rejected(lambda:exec(compile(RAW,str(SOURCE),'exec'),ns),'early invalid flags reject');check(imports==['sys'],'early flag failure imports sys alone');meta['imports']=imports
 else:
  selfpath=write(BASE/'runner/dispatcher.py',RAW)
  d=types.ModuleType('owned_dispatcher');d.__file__=str(selfpath);exec(compile(RAW,str(selfpath),'exec'),d.__dict__)
  for name in d.PINS:write(BASE/d.OWN/name,(ROOT/'owned_final07_sources'/name).read_bytes())
  gate=write(BASE/'ROOT_PUBLICATION_GATE_01.json',{'SYNTHETIC_NON_RECEIPT':True,'kind':'fake_gate'});ready=write(BASE/'ROOT_ACTUAL_READY_CHECKPOINT.json',{'SYNTHETIC_NON_RECEIPT':True,'kind':'fake_ready'})
  adoption={'SYNTHETIC_NON_RECEIPT':True,'schema':'pr206-root-publication-operations-adoption-v1','evidence_scope':'ACTUAL_ROOT_RECEIPT','accepted_preparation_only':True,'PR':206,'original_head':'488e8f575a6c9bcc0bd097d2852c9a7fa19bf8a7','sources':{d.OWN+'/'+n:{'bytes':w[0],'sha256':w[1]} for n,w in d.PINS.items()},'dispatcher_pin':pin(RAW),'approved_publication_gate_pin':pin(gate.read_bytes()),'approved_actual_ready_pointer_pin':pin(ready.read_bytes())}
  ap=write(BASE/d.ADOPTION,adoption);ap_pin=pin(ap.read_bytes())
  aliases=('ops_common206','Root_pr206_publisher','Root_pr206_tracker');absent=probe.endswith('_absent')
  for a in aliases:
   if absent:sys.modules.pop(a,None)
   else:sys.modules[a]=types.ModuleType('PREEXISTING_'+a)
  prior={a:(a in sys.modules,sys.modules.get(a)) for a in aliases}
  oldargv=['SYNTHETIC_owned_dispatch','--adoption',d.ADOPTION,'--adoption-bytes',str(ap_pin['bytes']),'--adoption-sha256',ap_pin['sha256'],'preflight']
  action='append' if 'tracker' in probe else 'stage' if 'publisher' in probe or probe.startswith('cleanup_selected') else 'preflight'
  
  if probe.startswith('route_publisher_'):action=probe.removeprefix('route_publisher_').removesuffix('_confirm')
  if probe=='route_tracker_recover':action='recover'
  oldargv[-1]=action;sys.argv=list(oldargv)
  if probe.endswith('_confirm'):sys.argv+=['--confirm-id','123']
  real_load=d.load_module
  MARKER='SYNTHETIC_RAW_EXCEPTION_BODY_91'
  def chained(kind=RuntimeError):
   try:raise ValueError(MARKER+'_CAUSE')
   except ValueError as inner:raise kind(MARKER+'_OUTER') from inner
  def load(name,path,raw):
   meta['compiled'].append({'name':name,'file':path.name,'pin':pin(raw)})
   if probe.startswith('cleanup_common_compile') and path.name=='ops_common206.py':sys.modules[name]=types.ModuleType(name);chained(SyntaxError)
   if probe.startswith('cleanup_selected_compile') and path.name=='publisher206.py':sys.modules[name]=types.ModuleType(name);chained(SyntaxError)
   module=real_load(name,path,raw)
   if path.name=='ops_common206.py':
    module.load_context=lambda base:({'SYNTHETIC_NON_RECEIPT':True})
    module.context_pin=lambda context:{'SYNTHETIC_NON_RECEIPT':True,'stub_context':True}
    if probe=='error_preflight':module.load_context=lambda base:chained(RuntimeError)
   else:
    def fake_main():
     meta['selected_argv']=list(sys.argv)
     if probe.startswith('error_'):chained(OSError if 'tracker' in probe else RuntimeError)
     if probe.startswith('cleanup_selected_main'):chained(ValueError)
     if probe.startswith('systemexit_'):
      suffix=probe.split('_',1)[1];raise SystemExit(None if suffix=='none' else 0 if suffix=='zero' else True if suffix=='bool' else MARKER)
     if probe=='baseexception_tracker':raise KeyboardInterrupt(MARKER)
     print(json.dumps({'SYNTHETIC_NON_RECEIPT':True,'selected_stub':path.name},sort_keys=True))
    module.main=fake_main
   return module
  d.load_module=load
  if probe.startswith('safe_'):
   target=BASE/'special';raw=b'SYNTHETIC_NON_RECEIPT regular input\n';write(target,raw);wanted=pin(raw);mode=probe.removeprefix('safe_')
   if mode=='fifo':target.unlink();os.mkfifo(target,0o444)
   elif mode=='directory':target.unlink();target.mkdir()
   elif mode=='symlink':target.unlink();target.symlink_to(gate)
   elif mode=='mode':target.chmod(0o644)
   elif mode=='oversize':write(target,b'x'*2000001);wanted=pin(target.read_bytes())
   real_lstat=Path.lstat
   if mode in ('socket_kind','char_kind'):
    def simulated_lstat(self):
     if self==target:return types.SimpleNamespace(st_mode=(stat.S_IFSOCK if mode=='socket_kind' else stat.S_IFCHR)|0o444,st_size=0)
     return real_lstat(self)
    Path.lstat=simulated_lstat
   real_open=d.os.open;opened=[]
   def opened_fn(path,flags,*a,**kw):
    if Path(path)==target:
     opened.append(flags)
     check(bool(flags&os.O_NONBLOCK) if version!='v2' else True,'open carries O_NONBLOCK when required');check(bool(flags&os.O_NOFOLLOW),'open carries O_NOFOLLOW')
     if mode.startswith('race_'):
      target.unlink()
      if mode=='race_fifo':os.mkfifo(target,0o444)
      elif mode=='race_directory':target.mkdir()
      elif mode=='race_symlink':target.symlink_to(gate)
      elif mode=='race_oversize':write(target,b'x'*2000001)
    return real_open(path,flags,*a,**kw)
   d.os.open=opened_fn
   try:
    if mode=='regular':check(d.checked(target,wanted)==raw,'normal bounded regular file accepted')
    else:rejected(lambda:d.checked(target,wanted),'special or replaced input rejects')
   finally:d.os.open=real_open;Path.lstat=real_lstat
   if mode in ('fifo','directory','symlink','mode','oversize','socket_kind','char_kind'):check(not opened,'static disallowed input rejected before open')
   if mode.startswith('race_'):check(len(opened)==1,'race exercised exact real open once')
   meta['open_flags']=opened
  else:
   should_fail=probe.startswith(('auth_','cleanup_','error_')) or probe in ('systemexit_bool','systemexit_text','baseexception_tracker','parser_bad_int','parser_unknown','parser_bad_confirm','parser_choice','parser_missing')
   if probe=='auth_basename':sys.argv[2]='../'+d.ADOPTION
   elif probe=='auth_adoption':write(ap,adoption|{'changed':True})
   elif probe=='auth_gate':write(gate,{'SYNTHETIC_NON_RECEIPT':True,'changed':True})
   elif probe=='auth_ready':write(ready,{'SYNTHETIC_NON_RECEIPT':True,'changed':True})
   elif probe=='auth_self':write(selfpath,b'SYNTHETIC changed self')
   elif probe=='auth_source':write(BASE/d.OWN/'publisher206.py',b'SYNTHETIC changed source')
   elif probe=='auth_source_mode':(BASE/d.OWN/'publisher206.py').chmod(0o644)
   elif probe=='auth_source_symlink':
    q=BASE/d.OWN/'publisher206.py';q.unlink();q.symlink_to(ROOT/'owned_final07_sources/publisher206.py')
   elif probe=='auth_source_set':
    adoption['sources'].pop(d.OWN+'/offline_guards.py');write(ap,adoption);updated=pin(ap.read_bytes());sys.argv[4]=str(updated['bytes']);sys.argv[6]=updated['sha256']
   elif probe=='cleanup_invalid_confirm_publisher':sys.argv+=['--confirm-id','123']
   elif probe=='help':sys.argv=['SYNTHETIC_owned_dispatch','--help']
   elif probe=='parser_bad_int':sys.argv[4]=MARKER
   elif probe=='parser_unknown':sys.argv+=['--SYNTHETIC_UNKNOWN_'+MARKER]
   elif probe=='parser_bad_confirm':sys.argv+=['--confirm-id',MARKER]
   elif probe=='parser_choice':sys.argv[-1]=MARKER
   elif probe=='parser_missing':sys.argv=['SYNTHETIC_owned_dispatch']
   if probe.startswith('systemexit_'):sys.argv[-1]='stage'
   beforeargv=list(sys.argv)
   try:
    if version=='v2':d.main()
    else:d.entry()
   except SystemExit as e:exitcode=e.code if type(e.code)is int else 1;meta['entry_systemexit']={'code':e.code,'type':type(e).__name__}
   meta['post_argv']=list(sys.argv);check(sys.argv==beforeargv,'argv restored after dispatcher path')
   check(all((a in sys.modules)==was and (not was or sys.modules[a] is old) for a,(was,old) in prior.items()),'all alias presence and identity restored')
   if probe.startswith('auth_'):check(not meta['compiled'],'auth failure compiles nothing')
   elif probe=='preflight':check([x['file'] for x in meta['compiled']]==['ops_common206.py'],'preflight compiles common only')
   elif probe.startswith('route_'):
    name='tracker206.py' if 'tracker' in probe else 'publisher206.py';check([x['file'] for x in meta['compiled']]==['ops_common206.py',name],'route compiles common and selected only')
    argv=meta['selected_argv'];check(('--kit' not in argv) if 'tracker' in probe else argv[argv.index('--kit')+1]==d.KIT,'fixed kit string routed without kit execution');check(argv[1]==action,'exact selected action routed')
   check(not any(x['file'] in ('offline_guards.py','run_offline.py') for x in meta['compiled']),'no authored offline module compiled')
   if should_fail:check(exitcode==1,'failed entry exits1')
   elif probe in ('help','systemexit_none','systemexit_zero','preflight','route_publisher','route_tracker'):check(exitcode==0,'clean entry/help/SystemExit0 exits0')
 check(not BLOCKED,'no prohibited action attempted');meta['status']='PASS'
except BaseException as error:
 meta.update(status='HARNESS_OR_SOURCE_FAILURE',error_type=type(error).__name__,error=str(error),traceback=traceback.format_exc());exitcode=99
finally:
 (BASE/'probe_result.json').write_text(json.dumps(meta,sort_keys=True,indent=2,default=str)+'\n')
raise SystemExit(exitcode)
