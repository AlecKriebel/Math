#!/usr/bin/python3
"""Independent private predicate/OS models. Production sources are TEXT ONLY."""
import copy,ctypes,datetime,hashlib,json,math,os,pathlib,re,stat,sys
F=pathlib.Path(__file__).resolve().parent;A=F.parent;R=A.parents[2]
checks=0;rejected=[]
def ck(v,n):
    global checks
    assert bool(v),n;checks+=1
def bad(fn,n):
    global checks
    try:fn()
    except (ValueError,TypeError,KeyError,AssertionError):checks+=1;rejected.append(n);return
    raise AssertionError('Mutant accepted '+n)
def path(v):
    if type(v) is not str or not v or '\\' in v or '\0' in v:raise ValueError('Path')
    p=pathlib.PurePosixPath(v)
    if p.is_absolute() or str(p)!=v or {'.','..','.git','__pycache__'}&set(p.parts):raise ValueError('Canonical relative path')
    return v
def row(r):
    if type(r) is not dict or set(r)!={'path','bytes','sha256','full_mode'}:raise ValueError('Exact row')
    path(r['path'])
    if type(r['bytes']) is not int or r['bytes']<0 or type(r['full_mode']) is not int or not 0<=r['full_mode']<=4095 or type(r['sha256']) is not str or re.fullmatch('[0-9a-f]{64}',r['sha256']) is None:raise ValueError('Typed row')
    return r
def mode(v):
    if type(v) is not int or v!=0o444:raise ValueError('Exact full mode')
    return True
def typed(a,b):
    if type(a) is not type(b):return False
    if isinstance(a,dict):return a.keys()==b.keys() and all(typed(a[k],b[k]) for k in a)
    if isinstance(a,list):return len(a)==len(b) and all(typed(x,y) for x,y in zip(a,b))
    return a==b
def strict(raw):
    def pairs(ps):
        d={}
        for k,v in ps:
            if k in d:raise ValueError('Duplicate key')
            d[k]=v
        return d
    def const(v):raise ValueError('Nonfinite')
    def floating(v):
        n=float(v)
        if not math.isfinite(n):raise ValueError('Overflow')
        return n
    return json.loads(raw,object_pairs_hook=pairs,parse_constant=const,parse_float=floating)
def capture(c):
    if c['actual_execution'] is not True or c['completed'] is not True or c['operator_unchanged'] is not True or c['stdin_supplied'] is not False:raise ValueError('Actual completion flags')
    if type(c['pid']) is not int or c['pid']<=0 or type(c['exit_code']) is not int or c['exit_code']!=0 or type(c['operator_pid']) is not int or c['operator_pid']!=60012:raise ValueError('Actual typed integer fields')
    if c['cwd']!=str(R):raise ValueError('Actual cwd')
    if c['schema']=='pr49-root-actual-unchanged-helper/v1':
        row(c['source'])
        if c['source_unchanged'] is not True or c['argv']!=['/usr/bin/python3','-B',str(R/c['source']['path'])]:raise ValueError('Unchanged helper identity')
    elif c['schema']=='pr49-root-actual-readonly-git/v1':
        if c['source'] is not None or c['source_unchanged'] is not None or type(c['argv']) is not list or len(c['argv'])<2 or c['argv'][0]!='git' or c['argv'][1] not in {'show','ls-tree','diff','merge-base'}:raise ValueError('Readonly explicit null/null')
    else:raise ValueError('Schema')
    start=datetime.datetime.fromisoformat(c['started_utc']);end=datetime.datetime.fromisoformat(c['finished_utc'])
    if start.utcoffset()!=datetime.timedelta(0) or end.utcoffset()!=datetime.timedelta(0) or start>end:raise ValueError('Aware UTC chronology')
    for k in ['stdout','stderr']:row(c[k])
    if c['stderr']['bytes']!=0:raise ValueError('Success stderr')
    return True
fixture=F/'private_controls_v2';fixture.mkdir(exist_ok=False);p=fixture/'mode_fixture';p.write_bytes(b'Owned mode sweep; recorded observations are historical, final mode0444.\n');observed=[]
for bits in range(4096):
    os.chmod(p,bits);actual=stat.S_IMODE(p.stat().st_mode);ck(actual==bits,'Actual full mode roundtrip');observed.append({'requested':bits,'observed':actual})
    if bits==0o444:ck(mode(bits),'Only0444 accepted')
    else:bad(lambda bits=bits:mode(bits),'full_mode_%04o'%bits)
os.chmod(p,0o444)
for v in [True,False,292.0,'0444',None]:bad(lambda v=v:mode(v),'noninteger_mode_'+str(v))
for v in ['a','a/b.json','a-b_c','tmp/owned/control.json']:ck(path(v)==v,'Valid paths')
for v in ['', '/', '../x','a/../b','a/./b','a//b','./a','a/','a\\b','a\0b','.git/x','x/__pycache__/a',1,True,None]:bad(lambda v=v:path(v),'bad_path_'+repr(v))
sample={'path':'a/b','bytes':1,'sha256':'a'*64,'full_mode':292};ck(row(sample)==sample,'Valid exact row')
for k,v in [('bytes',True),('bytes',False),('bytes',-1),('bytes',1.0),('sha256','z'*64),('sha256','A'*64),('full_mode',True),('full_mode',4096),('full_mode',-1),('path','a/../b')]:
    m=dict(sample);m[k]=v;bad(lambda m=m:row(m),'row_'+k+'_'+repr(v))
for m in [dict(sample,extra=1),{k:v for k,v in sample.items() if k!='path'}]:bad(lambda m=m:row(m),'row_extra_or_missing')
for raw in [b'{"a":1,"a":2}',b'{"a":NaN}',b'{"a":Infinity}',b'{"a":1e999}']:bad(lambda raw=raw:strict(raw),'strict_JSON_'+repr(raw))
ck(not typed(True,1) and not typed(0,0.0) and typed({'a':[0,None,True]}, {'a':[0,None,True]}),'Recursive scalar types')
result=strict((A/'root_original_actual_reproduction/ROOT_REPRODUCTION_RESULT.json').read_bytes());allcaps=result['complete_actual_Git_captures']+result['complete_actual_helper_captures']
for c in allcaps:
    ck(capture(c),'Actual ROOT capture class accepted')
    for k,v in [('pid',True),('pid',0),('exit_code',False),('operator_pid',True),('completed',False),('actual_execution',False),('operator_unchanged',False),('schema','wrong'),('cwd','/tmp'),('stdin_supplied',True)]:
        m=copy.deepcopy(c);m[k]=v;bad(lambda m=m:capture(m),'capture_'+k+'_'+c['schema'])
    for k in ['source','source_unchanged']:
        m=copy.deepcopy(c);m[k]=None if c['schema'].endswith('unchanged-helper/v1') else True;bad(lambda m=m:capture(m),'capture_wrong_'+k+'_'+c['schema'])
    m=copy.deepcopy(c);m['argv']=['git','reset','--hard'];bad(lambda m=m:capture(m),'destructive_or_wrong_argv')
    if c['source'] is not None:
        ck(c['source']['full_mode']==420,'Historical launch mode remains literal420')
        ck(stat.S_IMODE((R/c['source']['path']).stat().st_mode)==292,'Current closure mode separately292')
pins=strict((F/'STATIC_INPUT_BINDINGS.json').read_bytes());ck(set(pins['closed_inputs'])=={'original','boundary','hyperbolic','ROOT'},'Four actual schema inputs')
for r in pins['fixed_rows']:
    row(r);q=R/r['path'];b=q.read_bytes();ck(len(b)==r['bytes'] and hashlib.sha256(b).hexdigest()==r['sha256'] and stat.S_IMODE(q.stat().st_mode)==r['full_mode'],'Every fixed body and full mode')
for info in pins['closed_inputs'].values():
    for r in info['members']:ck(mode(r['full_mode']),'Each closed normalized member mode')
drafts=sorted(F.glob('DRAFT_ROOT*.json'))
for q in drafts:
    d=strict(q.read_bytes());ck(d['approved_by_root'] is False and d['created_utc'] is None,'False/null genuine approval unavailable')
    if 'root_flags' in d:ck(all(v is False for v in d['root_flags'].values()),'All future read flags false')
ck('ROOT_SCOPE_ACCEPTED_EXACT_KNOWN_RESULT_ONLY' not in (F/'DRAFT_ROOT_CURRENT_KNOWN_RESULT_SCOPE_CERTIFICATE.md').read_text(),'Draft lacks acceptance marker')
for receipt,count in [('verification.json',69),('review/independent_results.json',187)]:
    a=strict((A/'source_snapshot'/receipt).read_bytes());b=strict((F/'operative_proposal'/receipt).read_bytes());ck(typed(a,b) and a['passed']==count==len(a['checks']),'Whole literal typed diagnostic receipt')
for q in (F/'original_archive').rglob('*'):
    if q.is_file():ck(q.read_bytes()==(A/'source_snapshot'/q.relative_to(F/'original_archive')).read_bytes(),'All16 archive bodies literal')
builder=(F/'prepare_current_packet.py').read_text();operator=(F/'capture_root_builder_operation.py').read_text()
for token in ['members','payload_files','mode-string','mandatory_corrections','mandatory_mathematical_corrections','source_unchanged','is None','fn(os.fsencode(src),os.fsencode(dst),4)','new_source_adversary','full_target_prior_result_verified','frozen_inner_command_copy_is_prepublication_prefix']:
    ck(token in builder or token in operator,'Normative text '+token)
for token in ['PR48','pr48','2961','30004403','6570','HISTORICAL=','UNSOLVED partial']:
    ck(token not in builder and token not in operator,'No transplanted PR48 scientific token')
# Genuine macOS behavior in owned private directory. No production import/call.
ck(sys.platform=='darwin','Actual macOS');lib=ctypes.CDLL(None,use_errno=True);rename=lib.renamex_np;rename.argtypes=[ctypes.c_char_p,ctypes.c_char_p,ctypes.c_uint];rename.restype=ctypes.c_int
src=fixture/'rename_source';dst=fixture/'existing_sentinel';src.write_bytes(b'source');dst.write_bytes(b'sentinel')
ck(rename(os.fsencode(src),os.fsencode(dst),4)!=0 and src.read_bytes()==b'source' and dst.read_bytes()==b'sentinel','Actual exclusive rename refuses replacement')
fresh=fixture/'absent_destination';ck(rename(os.fsencode(src),os.fsencode(fresh),4)==0 and fresh.read_bytes()==b'source' and not src.exists(),'Actual exclusive rename into absent destination')
link=fixture/'owned_symlink';link.symlink_to('absent_destination');ck(link.is_symlink(),'Actual symlink created and detected');link.unlink()
patch=strict((F/'CURRENT_QUEUE_PATCH.json').read_bytes());header=['Rank','ID / code','Problem','EV','Impact (/10)','Difficulty','Proposed','Status','Turns','Chat','Findings','DOI'];old=patch['row_before'].split('|');new=patch['row_prospective'].split('|');allowed={header.index(k)+1 for k in ['Status','Turns','Findings']}
ck(all(x==y for i,(x,y) in enumerate(zip(old,new)) if i not in allowed),'Only named queue cells changed, ChatDOI preserved')
for q in (F/'native4_proposal/preimage').iterdir():
    b=q.read_bytes();pros=(F/'native4_proposal/prospective'/q.name).read_bytes()
    if 'QUEUE.md' not in q.name:ck(b==pros,'State/history/inventory prospective unchanged')
# Additional independent contracts, using only private models and owned fixtures.
def topo(root,expected):
    actual=set();dirs=set()
    for q in root.rglob('*'):
        if q.is_symlink():raise ValueError('Symlink topology')
        name=q.relative_to(root).as_posix();path(name)
        if q.is_file():actual.add(name)
        elif q.is_dir():dirs.add(name)
        else:raise ValueError('Special topology')
    wanted={str(v) for n in actual for v in pathlib.PurePosixPath(n).parents if str(v)!='.'}
    if actual!=set(expected) or dirs!=wanted:raise ValueError('Exact files and nonempty directory topology')
    return True
tree=fixture/'topology';tree.mkdir();(tree/'body').write_bytes(b'owned');ck(topo(tree,{'body'}),'Exact private topology')
(tree/'extra').mkdir();bad(lambda:topo(tree,{'body'}),'private_empty_extra_directory');(tree/'extra').rmdir()
(tree/'extra').write_bytes(b'owned');bad(lambda:topo(tree,{'body'}),'private_extra_file');(tree/'extra').unlink()
(tree/'link').symlink_to('body');bad(lambda:topo(tree,{'body','link'}),'private_symlink_member');(tree/'link').unlink()
def authority(d,closed):
    if d.get('approved_by_root') is not True or d.get('operative_preparation_directory')!='current_preparation_family':raise ValueError('ROOT approval')
    now=datetime.datetime.now(datetime.timezone.utc);t=datetime.datetime.fromisoformat(d['created_utc'])
    if t.utcoffset()!=datetime.timedelta(0) or not closed<=t<=now:raise ValueError('New actual authority chronology')
    return True
closed=datetime.datetime.now(datetime.timezone.utc)-datetime.timedelta(seconds=2)
authority_sample={'approved_by_root':True,'operative_preparation_directory':'current_preparation_family','created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()};ck(authority(authority_sample,closed),'Private authority model positive is not actual approval')
for key,value in [('approved_by_root',1),('approved_by_root',False),('operative_preparation_directory','old_family'),('created_utc',(closed-datetime.timedelta(seconds=1)).isoformat()),('created_utc',(closed+datetime.timedelta(days=1)).isoformat()),('created_utc','2026-01-01T00:00:00')]:
    m=dict(authority_sample);m[key]=value;bad(lambda m=m:authority(m,closed),'authority_'+key+'_'+str(value))
for q in drafts:bad(lambda q=q:authority(strict(q.read_bytes()),closed),'Actual false-null DRAFT rejected '+q.name)
ck(type(None) is not type({}) and {}==strict(b'{}') and strict(b'null') is None,'ABSENT/fallback empty object/administrative null model distinctions')
prior={};ck('30000703' not in prior,'Model missing prior key distinct from present null');prior['30000703']=None;ck('30000703' in prior and prior['30000703'] is None,'Model present-null key never treated as absent')
def paired(a,b):
    for c in [a,b]:
        if c['actual_execution'] is not True or c['completed'] is not True or type(c['pid']) is not int or c['pid']<=0 or type(c['exit_code']) is not int or c['exit_code']!=0:raise ValueError('Two real completed captures')
    if datetime.datetime.fromisoformat(a['finished_utc'])>=datetime.datetime.fromisoformat(b['started_utc']) or a['pid']==b['pid']:raise ValueError('Distinct postexit child')
    return True
ca={'actual_execution':True,'completed':True,'pid':100,'exit_code':0,'started_utc':closed.isoformat(),'finished_utc':(closed+datetime.timedelta(microseconds=1)).isoformat()};cb=dict(ca,pid=101,started_utc=(closed+datetime.timedelta(microseconds=2)).isoformat(),finished_utc=(closed+datetime.timedelta(microseconds=3)).isoformat());ck(paired(ca,cb),'Private separate after-exit model')
for k,v in [('pid',100),('pid',True),('exit_code',False),('completed',False),('started_utc',ca['finished_utc'])]:
    m=dict(cb);m[k]=v;bad(lambda m=m:paired(ca,m),'paired_capture_'+k)
out={'schema':'pr49-source-private-contract-controls/v1','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'assertions_passed':checks,'assertions_failed':0,'negative_models_rejected':len(rejected),'negative_model_labels':rejected,'full_mode_observations':observed,'production_builder_imported_compiled_executed':False,'production_operator_imported_compiled_executed':False,'model_acceptance_is_not_production_runtime_or_ROOT_authority':True,'actual_ROOT_capture_models_checked':36,'fixed_bodies_checked':len(pins['fixed_rows']),'builder_sha256':hashlib.sha256(builder.encode()).hexdigest(),'operator_sha256':hashlib.sha256(operator.encode()).hexdigest(),'private_mode_fixture_current_mode':'0444','SOURCE_adversary_verdict':None,'new_substantive_attempts':0,'audit_turns':0}
(F/'PRIVATE_CONTRACT_CONTROL_RESULTS_V2.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k not in ['negative_model_labels','full_mode_observations']}))
