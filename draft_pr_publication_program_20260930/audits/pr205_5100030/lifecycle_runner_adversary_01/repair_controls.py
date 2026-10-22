"""Extract only runner02's capture/install/finally AST into a synthetic function.
No runner/project module import, entrypoint, backend, real fd/cache or API.
"""
from pathlib import Path
import ast,copy,hashlib,json,types
D=Path(__file__).resolve().parent
path=D.parent/'root_lifecycle_runner_02/run_lifecycle205.py';raw=path.read_bytes()
def need(ok,msg):
    if not ok:raise RuntimeError(msg)
need(len(raw)==8063 and hashlib.sha256(raw).hexdigest()=='7b2c0249e37db445f0da2eea057673cd788490f1a335c993da5bc8f64f641e05','Exact reviewed runner02')
tree=ast.parse(raw);main=next(x for x in tree.body if isinstance(x,ast.FunctionDef) and x.name=='main');outer=next(x for x in main.body if isinstance(x,ast.Try));start=next(i for i,x in enumerate(outer.body) if isinstance(x,ast.Assign) and ast.unparse(x.targets[0])=='original_init');install=next(i for i,x in enumerate(outer.body[start:],start) if isinstance(x,ast.Try));slice_body=copy.deepcopy(outer.body[start:install+1]);final=copy.deepcopy(outer.finalbody)
template=ast.parse('def exercise(adapter,c,h,mods,original_api,original_spec,aliases,present,prior,sys,importlib,after):\n cache=None\n try:\n  pass\n finally:\n  pass\n return cache\n');fn=template.body[0];block=fn.body[1];block.body=slice_body+ast.parse('after()').body;block.finalbody=final;scope={'json':json,'print':lambda *a,**k:None};exec(compile(ast.fix_missing_locations(template),'synthetic_runner02_capture_finally','exec'),scope);exercise=scope['exercise'];results=[]
def run(label,init_failure=None,partial=None,action_failure=False,divergent=False,close_failure=False,set_failure=None):
    original_api=object();spec=object();changed_spec=object();sentinel=object();events=[];instances=[]
    class Mod:
        def __init__(self,index):object.__setattr__(self,'index',index);object.__setattr__(self,'api',original_api)
        def __setattr__(self,key,value):
            if key=='api' and value is original_api:
                events.append(('restore',self.index))
                if self.index==set_failure:raise RuntimeError('synthetic setter failure')
            object.__setattr__(self,key,value)
    mods=[Mod(i) for i in range(6)]
    class Cache:
        def __init__(self,original):
            instances.append(self)
            if init_failure=='before_fd':raise RuntimeError('synthetic constructor before fd')
            self.fd=7
            if init_failure=='after_fd':raise RuntimeError('synthetic constructor after fd')
            self.stats={'synthetic':True}
        def close(self):
            events.append(('close',self.fd));self.fd=None
            if close_failure:raise RuntimeError('synthetic close failure')
    original_init=Cache.__init__
    def install(c,h):
        if partial=='preconstructor':raise RuntimeError('synthetic before constructor')
        value=Cache(original_api)
        for i,m in enumerate(mods):
            if partial==i:raise RuntimeError('synthetic partial installation')
            m.api=value
        if partial==6:raise RuntimeError('synthetic final installation check')
        return value,lambda:None
    adapter=types.SimpleNamespace(TreeCache=Cache,install_loaded=install);aliases=['one','two','three','four'];prior={'one':sentinel,'two':None,'three':None,'four':sentinel};present={'one':True,'two':False,'three':False,'four':True};fake_sys=types.SimpleNamespace(modules={k:object() for k in aliases});fake_import=types.SimpleNamespace(util=types.SimpleNamespace(spec_from_file_location=changed_spec))
    def after():
        if divergent:object.__setattr__(mods[1],'api',object())
        if action_failure:raise RuntimeError('synthetic action failure')
    caught=None
    try:exercise(adapter,None,None,mods,original_api,spec,aliases,present,prior,fake_sys,fake_import,after)
    except RuntimeError as exc:caught=str(exc)
    expected_error=init_failure is not None or partial is not None or action_failure or divergent or close_failure or set_failure is not None
    need((caught is not None)==expected_error,label+' outcome')
    need(Cache.__init__ is original_init,label+' original constructor restored')
    need([i for event,i in events if event=='restore']==list(range(6)),label+' all six restorations attempted')
    need(all(m.api is original_api for i,m in enumerate(mods) if i!=set_failure),label+' remaining aliases restored')
    need(fake_import.util.spec_from_file_location is spec,label+' spec restored')
    need(fake_sys.modules=={'one':sentinel,'four':sentinel},label+' prior module aliases restored')
    need(len([x for x in events if x[0]=='close'])==len(instances),label+' every captured instance close attempted')
    need(all(x.fd is None for x in instances),label+' captured simulated fd closed')
    results.append({'case':label,'PASS':True,'all_six_attempted':True,'captured_instances':len(instances),'caught':caught})
run('successful installation and cleanup')
run('installer rejects before constructor',partial='preconstructor')
run('constructor abort before fd',init_failure='before_fd')
run('constructor abort after fd',init_failure='after_fd')
for count in (0,1,3,6):run('installer abort after '+str(count)+' alias writes',partial=count)
run('action throws after installation',action_failure=True)
run('divergent alias reported while all cleanup continues',divergent=True)
run('close throws while hook/modules restored',close_failure=True)
run('one alias setter throws while remaining aliases and close attempted',set_failure=2)
need(path.read_bytes()==raw,'Runner source unchanged')
print(json.dumps({'mode':'optimized' if __debug__ is False else 'ordinary','runner_pin':{'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()},'controls_passed':len(results),'results':results,'only_capture_and_finally_AST_executed_with_in_memory_fakes':True,'no_runner_project_import_backend_fd_cache_API_phase_service_currentview_actions':True,'scientific_or_whole_package_review_events_added':0},indent=2))
