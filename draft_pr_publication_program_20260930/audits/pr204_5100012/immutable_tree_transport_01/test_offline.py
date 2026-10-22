"""Offline only: frozen native trees and actual directory/warm/diff AST functions.
No gh, network, helper phase, live adapter installation or production cache seed.
"""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import ast,base64,copy,datetime,gzip,hashlib,json,os,subprocess,sys,tempfile,threading,types
if sys.flags.optimize or not sys.dont_write_bytecode:raise RuntimeError('Ordinary Python -B required')
import tree_transport as t
D=Path(__file__).resolve().parent;A=D.parent;AUDITS=A.parent
source=A/'original_git_metadata/ALL_AUTHENTICATED_NONRECURSIVE_TREES.json'
TREES=json.loads(source.read_bytes());ORIGINAL=json.loads((A/'original_git_metadata/ORIGINAL_COMMIT.json').read_bytes())['tree']['sha'];BASE=json.loads((A/'original_git_metadata/RANGE_BASE_COMMIT.json').read_bytes())['tree']['sha']
CUSTODY=json.loads((A/'ORIGINAL_SUBMISSION_CUSTODY.json').read_bytes());PATHS=CUSTODY['complete_original_delta'];EXPECTED=set(PATHS)
SOURCES={
 'base':AUDITS/'pr152_5000006/prepare_scoped_merge.py',
 'warm':AUDITS/'pr177_10400049/prepare_final_scoped_merge.py',
 'validator':AUDITS/'pr179_10800007/prepare_final_scoped_merge.py'}
def functions(path,names,ns):
    tree=ast.parse(path.read_text());chosen=[x for x in tree.body if isinstance(x,ast.FunctionDef) and x.name in names]
    t.require({x.name for x in chosen}==set(names),'Offline function fixture missing source')
    exec(compile(ast.Module(body=chosen,type_ignores=[]),str(path),'exec'),ns)
class FakeAPI:
    def __init__(self):self.calls=[];self.lock=threading.Lock()
    def __call__(self,endpoint,method='GET',body=None):
        with self.lock:self.calls.append((endpoint,method,copy.deepcopy(body)))
        match=t.REQUEST.fullmatch(endpoint)
        if method=='GET' and body is None and match:return copy.deepcopy(TREES[match.group(1)])
        return {'offline_passthrough':endpoint,'method':method,'body':copy.deepcopy(body)}
def graph(api):
    base=types.ModuleType('offline_base152');base.__file__=str(SOURCES['base']);base.api=api;base.require=t.require;base.TREE_CACHE={};base.REPO='repos/'+t.REPO
    functions(SOURCES['base'],['directory','lookup','changed_leaves'],base.__dict__)
    pg177=types.ModuleType('offline_progress177');pg177.m=base
    final177=types.ModuleType('offline_final177');final177.m=pg177;final177.require=t.require
    functions(SOURCES['warm'],['warm_selected_directories'],final177.__dict__)
    pg179=types.ModuleType('offline_progress179');pg179.h=final177
    final179=types.ModuleType('offline_final179');final179.m=pg179;final179.native_tree_cache=base.TREE_CACHE;final179.hashlib=hashlib;final179.re=t.re;final179.require=t.require
    functions(SOURCES['validator'],['verify_tree_object'],final179.__dict__)
    h=types.ModuleType('offline_top190');h.m=final179
    mods=[h,final179,pg179,final177,pg177,base]
    for mod in mods:mod.api=api
    h.lookup=base.lookup;h.changed_leaves=base.changed_leaves
    c=types.SimpleNamespace(selected_current=lambda:None)
    return c,h,mods
def phase(h):
    h.m.m.h.warm_selected_directories([BASE,ORIGINAL],PATHS)
    t.require(h.changed_leaves(BASE,ORIGINAL)==EXPECTED,'Full original changed-leaf fixture')
    for name,x in CUSTODY['files'].items():
        t.require(h.lookup(ORIGINAL,'unsolved_math_prioritization/attempts/5100012/'+name)==('100644','blob',x['git_blob']),'Selected identity fixture '+name)
    for sha,rows in h.m.native_tree_cache.items():h.m.verify_tree_object(sha,rows)
def rejects(fn,label):
    try:fn()
    except (RuntimeError,OSError,ValueError,KeyError,UnicodeError):return label
    raise RuntimeError('Attack accepted: '+label)
def main():
    owned_prefixes=('private_fixture_','private_badperm_','private_concurrent_','private_failure_')
    before={p.name for p in D.iterdir() if p.is_dir() and p.name.startswith(owned_prefixes)};controls=[]
    for sha,j in TREES.items():t.validate_tree(sha,j)
    plain=FakeAPI()
    for _ in range(4):c,h,mods=graph(plain);phase(h)
    original_calls=len(plain.calls);cached=FakeAPI();stats=[]
    with tempfile.TemporaryDirectory(prefix='private_fixture_',dir=D) as directory:
        for _ in range(4):
            c,h,mods=graph(cached);cache,restore=t.install_loaded(c,h,Path(directory))
            try:
                t.require(all(x.api is cache for x in mods) and h.lookup.__globals__['api'] is cache,'All six aliases/nested globals covered');phase(h);stats.append(dict(cache.stats))
            finally:restore()
            t.require(all(x.api is cached for x in mods),'All six original aliases restored')
        with t.TreeCache(cached,Path(directory)) as cache:
            for sha,j in TREES.items():t.require(cache('git/trees/'+sha)==j,'Full API JSON equality')
            first=next(iter(TREES));fp=Path(directory)/(first+'.json.gz');original=fp.read_bytes();start=len(cached.calls)
            fp.write_bytes(b'not-gzip');controls.append(rejects(lambda:cache('git/trees/'+first),'corrupt gzip fails closed without network fallback'));fp.write_bytes(original)
            fp.chmod(0o644);controls.append(rejects(lambda:cache('git/trees/'+first),'nonprivate file permissions rejected'));fp.chmod(0o600)
            fp.unlink();os.symlink(source,fp);controls.append(rejects(lambda:cache('git/trees/'+first),'symlink cache file rejected'));fp.unlink();fp.write_bytes(original);fp.chmod(0o600)
            env=json.loads(gzip.decompress(original));env['api_json_sha256']='0'*64;fp.write_bytes(gzip.compress(t.canonical(env)));controls.append(rejects(lambda:cache('git/trees/'+first),'full JSON checksum tamper rejected'));fp.write_bytes(original)
            env=json.loads(gzip.decompress(original));env['api_json']['tree'][0]['sha']='0'*40;kind=env['api_json']['tree'][0]['type'];env['api_json']['tree'][0]['url']=t.API_ROOT+{'tree':'trees','blob':'blobs','commit':'commits'}[kind]+'/'+'0'*40;env['api_json_sha256']=hashlib.sha256(t.canonical(env['api_json'])).hexdigest();fp.write_bytes(gzip.compress(t.canonical(env)));controls.append(rejects(lambda:cache('git/trees/'+first),'native OID tamper rejected despite forged envelope checksum'));fp.write_bytes(original)
            fp.write_bytes(gzip.compress(b'x'*(t.MAX_JSON+5000)));controls.append(rejects(lambda:cache('git/trees/'+first),'bounded gzip expansion enforced'));fp.write_bytes(original)
            t.require(len(cached.calls)==start,'Corrupt caches caused forbidden network fallback')
            # Exact endpoint/method/body filtering preserves every original noncache call.
            noncache=[('git/ref/heads/main','GET',None),('git/commits/'+first,'GET',None),('compare/a...b','GET',None),('pulls/204','GET',None),('contents/x?ref='+first,'GET',None),('git/trees/'+first+'?recursive=1','GET',None),('git/trees/main','GET',None),('git/trees/'+first,'GET',{}),('git/trees','POST',{'base_tree':first}),('git/commits','POST',{'tree':first})]
            nstart=len(cached.calls)
            for args in noncache:t.require(cache(*args)=={'offline_passthrough':args[0],'method':args[1],'body':args[2]},'Noncache transport changed')
            t.require(cached.calls[nstart:]==noncache,'Noncache calls retried/reordered/altered');controls.append('mutable/POST/query/body requests preserved exactly once')
    # Native schema/hash/order attacks independently of stored envelope.
    sha,j=next((a,b) for a,b in TREES.items() if len(b['tree'])>1)
    changes=[('wrong requested SHA',lambda x:x.update(sha='0'*40)),('truncated response',lambda x:x.update(truncated=True)),('reversed canonical order',lambda x:x['tree'].reverse()),('duplicate native path',lambda x:x['tree'].append(copy.deepcopy(x['tree'][0]))),('slash path',lambda x:x['tree'][0].update(path='../bad')),('wrong mode/type',lambda x:x['tree'][0].update(mode='100777')),('wrong API URL',lambda x:x.update(url='https://invalid.example/private'))]
    for label,mutate in changes:
        changed=copy.deepcopy(j);mutate(changed);controls.append(rejects(lambda:t.validate_tree(sha,changed),label))
    controls.append(rejects(lambda:t.TreeCache(FakeAPI(),D.parent/'private_forbidden'),'outside private cache root rejected before creation'))
    with tempfile.TemporaryDirectory(prefix='private_badperm_',dir=D) as d:
        os.chmod(d,0o755);controls.append(rejects(lambda:t.TreeCache(FakeAPI(),Path(d)),'nonprivate directory rejected'));os.chmod(d,0o700)
    with tempfile.TemporaryDirectory(prefix='private_concurrent_',dir=D) as d:
        api=FakeAPI();sha=next(iter(TREES))
        with t.TreeCache(api,Path(d)) as cache:
            with ThreadPoolExecutor(max_workers=8) as pool:results=list(pool.map(lambda _:cache('git/trees/'+sha),range(16)))
            t.require(len(api.calls)==1 and all(x==TREES[sha] for x in results),'Per-SHA concurrent single-flight/equality');controls.append('16 concurrent requests use one original tree call')
    with tempfile.TemporaryDirectory(prefix='private_failure_',dir=D) as d:
        attempts=[]
        def fails(*args):attempts.append(args);raise RuntimeError('Offline403')
        with t.TreeCache(fails,Path(d)) as cache:
            controls.append(rejects(lambda:cache('git/trees/'+sha),'transport exception propagated without retry'));t.require(len(attempts)==1 and not list(Path(d).glob('*.json.gz')),'Failed response cached or retried')
    tree_calls=sum(1 for endpoint,method,body in cached.calls if t.REQUEST.fullmatch(endpoint) and method=='GET' and body is None)
    t.require(original_calls==32 and tree_calls==8,'Expected observed four-process tree fixture savings')
    result={'UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'scope':'Offline transport only; no API/helper phase/live installation/production seed','frozen_tree_JSON_pin':{'bytes':source.stat().st_size,'sha256':hashlib.sha256(source.read_bytes()).hexdigest()},'unique_frozen_native_trees':len(TREES),'simulated_separate_phases':4,'original_tree_calls_without_adapter':original_calls,'original_tree_calls_with_adapter':tree_calls,'tree_calls_saved':original_calls-tree_calls,'tree_call_reduction_percent':75,'phase_cache_stats':stats,'full_API_JSON_caching_equality':True,'actual_AST_warm_lookup_full_delta_selected_and_validator_checks':True,'all_six_API_aliases_patched_and_restored':True,'controls_passed':controls,'no_mutating_retry':True,'no_remote_calls':True,'no_existing_helper_modified':True,'production_cache_created':False,'temporary_private_test_caches_removed':True,'research_case_percent_actual_baseline':60,'publication_or_mathematical_clearance':False}
    t.require({p.name for p in D.iterdir() if p.is_dir() and p.name.startswith(owned_prefixes)}==before,'Temporary private fixture directory leaked')
    f=D/'OFFLINE_TEST_RESULTS_03.json'
    with f.open('xb') as out:out.write((json.dumps(result,indent=2)+'\n').encode())
    f.chmod(0o444);print(json.dumps({k:result[k] for k in ['unique_frozen_native_trees','original_tree_calls_without_adapter','original_tree_calls_with_adapter','tree_calls_saved','tree_call_reduction_percent','no_remote_calls']}|{'controls_passed':len(controls)}))
if __name__=='__main__':main()
