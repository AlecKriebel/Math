"""SYNTHETIC_NON_RECEIPT. Separate exact-buffer dispatcher source audit."""
import sys,pathlib,json,types,hashlib,builtins,io,contextlib,traceback,copy
ROOT=pathlib.Path(__file__).resolve().parent
RAW=(ROOT/'authenticated_dispatcher_v2.py').read_bytes()
if len(RAW)!=5148 or hashlib.sha256(RAW).hexdigest()!='3cce6202317f138d4c37f15dabf58f70492e170113a7cfae2f4a9c4918cecb63':raise RuntimeError('dispatcher v1 pin drift')
if sys.flags.optimize:
 imports=[]
 def observe(name,*a,**kw):imports.append(name);return builtins.__import__(name,*a,**kw)
 ns={'__name__':'audit_dispatcher','__file__':str(ROOT/'authenticated_dispatcher_v2.py'),'__builtins__':dict(vars(builtins),__import__=observe)}
 try:exec(compile(RAW,ns['__file__'],'exec'),ns)
 except RuntimeError as e:result={'SYNTHETIC_NON_RECEIPT':True,'status':'PASS' if imports==['sys'] and 'without -O' in str(e) else 'FAIL','optimization_flag':1,'imports':imports,'observed_error':str(e),'expected':'reject before any dependency imports'}
 else:result={'status':'FAIL','error':'optimized dispatcher accepted'}
 (ROOT/'DISPATCHER_V2_RESULT_O1.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,sort_keys=True));raise SystemExit(0 if result['status']=='PASS' else 1)
raw=(ROOT/'independent_harness.py').read_text().split("case('actual_absent_authority'",1)[0].replace("'independent_work_O'","'dispatcher_v2_work_O'")
exec(compile(raw,str(ROOT/'independent_harness.py'),'exec'),globals())
ALIASES=('ops_common206','Root_pr206_publisher','Root_pr206_tracker')

def dispatcher(f):
 q=write(f.base/'root_runner/run_operations206.py',RAW);m=types.ModuleType('audit_dispatcher');m.__file__=str(q);exec(compile(RAW,str(q),'exec'),m.__dict__)
 f.adopt['dispatcher_pin']=c.pin(q);write(f.base/m.ADOPTION,f.adopt)
 return m

def invoke(m,f,action='preflight',adopt=None,confirm=None):
 q=f.base/m.ADOPTION;wanted=c.pin(q);args=[str(m.__file__),'--adoption',adopt or m.ADOPTION,'--adoption-bytes',str(wanted['bytes']),'--adoption-sha256',wanted['sha256'],action]
 if confirm is not None:args+=['--confirm-id',str(confirm)]
 old=sys.argv;sys.argv=args
 try:return m.main()
 finally:sys.argv=old

def clean_state():return list(sys.argv),{a:sys.modules.get(a) for a in ALIASES},{a:a in sys.modules for a in ALIASES}
def preserved(old):
 argv,modules,present=old
 check(sys.argv==argv,'dispatcher argv values restored')
 check(all((a in sys.modules)==present[a] and (not present[a] or sys.modules[a] is modules[a]) for a in ALIASES),'dispatcher alias presence/object state restored')

for flag,value in [('ignore_environment',0),('no_site',0),('dont_write_bytecode',False),('safe_path',False),('optimize',1)]:
 def probe(flag=flag,value=value):
  flags=types.SimpleNamespace(ignore_environment=1,no_site=1,safe_path=True,optimize=0);fake=types.SimpleNamespace(flags=flags,dont_write_bytecode=True)
  if flag=='dont_write_bytecode':fake.dont_write_bytecode=value
  else:setattr(flags,flag,value)
  imports=[]
  def importer(name,*a,**kw):
   imports.append(name)
   if name=='sys':return fake
   raise RuntimeError('EARLY_UNEXPECTED_IMPORT:'+name)
  ns={'__name__':'fake_flags','__file__':str(ROOT/'authenticated_dispatcher_v2.py'),'__builtins__':dict(vars(builtins),__import__=importer)}
  denied(lambda:exec(compile(RAW,ns['__file__'],'exec'),ns),'isolation '+flag);check(imports==['sys'],'bad isolation denies before dependencies')
 case('flags_'+flag,probe)

for variant in ('wrong_basename','adoption_changed','gate_changed','ready_changed','source_changed','self_changed','source_mode','source_symlink'):
 def probe(v=variant):
  f=Fixture();m=dispatcher(f);compiled=[];real=m.load_module
  def tracked(name,path,raw):compiled.append(name);return real(name,path,raw)
  m.load_module=tracked
  if v=='adoption_changed':
   # Externally provided pin becomes stale while exact fixed adoption bytes change.
   old=c.pin(f.base/m.ADOPTION);write(f.base/m.ADOPTION,f.adopt|{'changed':True});argv=[m.__file__,'--adoption',m.ADOPTION,'--adoption-bytes',str(old['bytes']),'--adoption-sha256',old['sha256'],'preflight'];oldargv=sys.argv;sys.argv=argv
   try:denied(m.main,'stale external adoption pin')
   finally:sys.argv=oldargv
  else:
   if v=='gate_changed':write(f.gp,f.gate|{'changed':True})
   elif v=='ready_changed':write(f.base/'ROOT_ACTUAL_READY_CHECKPOINT.json',f.pointer|{'changed':True})
   elif v=='source_changed':write(f.base/c.OWN/'publisher206.py',b'SYNTHETIC corrupt')
   elif v=='self_changed':write(pathlib.Path(m.__file__),b'SYNTHETIC corrupt')
   elif v=='source_mode':(f.base/c.OWN/'publisher206.py').chmod(0o644)
   elif v=='source_symlink':
    q=f.base/c.OWN/'publisher206.py';q.unlink();q.symlink_to(SOURCE/'publisher206.py')
   denied(lambda:invoke(m,f,adopt='../'+m.ADOPTION if v=='wrong_basename' else None),'dispatcher rejects '+v)
  check(not compiled,'failed exact pin/path preflight compiles no source')
 case('pins_'+variant,probe)

def preflight():
 f=Fixture(fullmap=True);m=dispatcher(f);compiled=[];real=m.load_module
 def track(name,path,raw):compiled.append(path.name);return real(name,path,raw)
 m.load_module=track;old=clean_state();s=io.StringIO()
 with contextlib.redirect_stdout(s):invoke(m,f)
 preserved(old);j=json.loads(s.getvalue());check(j['preflight'] and j['checked_sources']==5 and compiled==['ops_common206.py'],'preflight authenticates five and compiles only common');check(j['process_or_HTTP_or_Git_calls'] is False,'preflight has no operational action');check(not offline_guard.BLOCKED_EVENTS,'no prohibited transport attempted')
case('valid_preflight_buffer_only',preflight)

for action in ('stage','append'):
 def probe(action=action):
  f=Fixture();m=dispatcher(f);compiled=[];record=[];real=m.load_module
  def tracked(name,path,raw):
   compiled.append(path.name);module=real(name,path,raw)
   if path.name!='ops_common206.py':module.main=lambda:record.append(list(sys.argv))
   return module
  m.load_module=tracked;old=clean_state();invoke(m,f,action);preserved(old)
  selected='tracker206.py' if action=='append' else 'publisher206.py';check(compiled==['ops_common206.py',selected],'only common and selected module compiled');check(len(record)==1 and '--base' in record[0] and '--adoption' in record[0],'selected main exact CLI dispatch')
  check(('--kit' not in record[0]) if action=='append' else record[0][-2:]==['--kit',m.KIT],'explicit unchanged kit path for publisher')
 case('dispatch_'+action,probe)

for failure in ('common_compile','selected_compile','selected_main','invalid_confirm'):
 def probe(failure=failure):
  f=Fixture();m=dispatcher(f);real=m.load_module;compiled=[]
  def tracked(name,path,raw):
   compiled.append(path.name)
   if failure=='common_compile' and path.name=='ops_common206.py':
    # Install then fail as actual load_module does, testing finally cleanup.
    sys.modules[name]=types.ModuleType(name);raise SyntaxError('SYNTHETIC common compile failure')
   if failure=='selected_compile' and path.name=='publisher206.py':
    return real(name,path,b'def synthetic invalid')
   module=real(name,path,raw)
   if path.name!='ops_common206.py':
    def fail_main():raise RuntimeError('SYNTHETIC selected main failure')
    module.main=fail_main
   return module
  m.load_module=tracked;old=clean_state();denied(lambda:invoke(m,f,'stage',confirm=123 if failure=='invalid_confirm' else None),'dispatcher '+failure);preserved(old);check('offline_guards.py' not in compiled and 'run_offline.py' not in compiled,'never compiles author offline helpers')
 case('cleanup_'+failure,probe)


def normalized_path_probes():
 f=Fixture();m=dispatcher(f);target=write(WORK/'SYNTHETIC_outside_A.json',{'SYNTHETIC_NON_RECEIPT':True});wanted=c.pin(target)
 for path,label in [(f.base/'..'/'SYNTHETIC_outside_A.json','lexical dotdot'),(target,'absolute outside A'),(pathlib.Path('SYNTHETIC_relative.json'),'relative path')]:
  denied(lambda path=path:m.checked(path,wanted),'v2 normalized path denial '+label)
 alias=f.base/'alias.json';alias.symlink_to(target);denied(lambda:m.checked(alias,wanted),'v2 file symlink denial')
 large=write(f.base/'SYNTHETIC_large.bin',b'x'*2000001);denied(lambda:m.checked(large,c.pin(large)),'v2 input bound denial')
case('normalized_paths_and_bound',normalized_path_probes)

result={'SYNTHETIC_NON_RECEIPT':True,'status':'PASS' if all(x['status']=='PASS' for x in RESULTS) else 'FAIL','optimization_flag':0,'case_count':len(RESULTS),'check_count':sum(len(x['checks']) for x in RESULTS),'cases':RESULTS,'reviewed_dispatcher':{'bytes':5148,'sha256':hashlib.sha256(RAW).hexdigest()},'no_live_dispatch':True,'blocked_events':offline_guard.BLOCKED_EVENTS,'lexical_dotdot_observation':'v1 helper observation repaired; v2 direct helper rejects'}
(ROOT/'DISPATCHER_V2_RESULT_O0.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n');print(json.dumps({'status':result['status'],'case_count':result['case_count'],'check_count':result['check_count'],'failed_cases':[x['id'] for x in RESULTS if x['status']!='PASS']},sort_keys=True));raise SystemExit(0 if result['status']=='PASS' else 1)
