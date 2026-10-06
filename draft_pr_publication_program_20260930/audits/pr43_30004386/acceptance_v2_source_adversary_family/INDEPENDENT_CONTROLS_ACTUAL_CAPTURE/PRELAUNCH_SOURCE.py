"""New handwritten adversarial contracts; no execution of any proposed helper."""
from pathlib import Path,PurePosixPath
import ast,copy,ctypes,datetime as dt,hashlib,json,math,os,stat
D=Path(__file__).resolve().parent;A=D.parent;R=A.parents[2];V=A/'acceptance_preparation_family_v2'
checks=[];negative=[];observations=[]
def need(ok,label):
    if not ok:raise ValueError(label)
    checks.append(label)
def reject(label,fn):
    try:fn()
    except (ValueError,TypeError,KeyError,IndexError,FileNotFoundError,NotADirectoryError):negative.append(label)
    else:raise ValueError('Mutant accepted '+label)
def eq(a,b):
    if type(a) is not type(b):return False
    if type(a) is dict:return a.keys()==b.keys() and all(eq(a[k],b[k]) for k in a)
    if type(a) is list:return len(a)==len(b) and all(eq(x,y) for x,y in zip(a,b))
    return a==b
def strict(raw):
    def pairs(values):
        out={}
        for key,value in values:
            if key in out:raise ValueError('Duplicate key')
            out[key]=value
        return out
    def floatnum(value):
        n=float(value)
        if not math.isfinite(n):raise ValueError('Nonfinite')
        return n
    return json.loads(raw,object_pairs_hook=pairs,parse_float=floatnum,
      parse_constant=lambda x:(_ for _ in ()).throw(ValueError(x)))
def require_same(a,b):
    if not eq(a,b):raise ValueError('Exact recursive types/keys/values')
def utc(value):
    if type(value) is not str or not value or value!=value.strip():raise ValueError('UTC string')
    t=dt.datetime.fromisoformat(value[:-1]+'+00:00' if value.endswith('Z') else value)
    if t.tzinfo is None or t.utcoffset()!=dt.timedelta(0):raise ValueError('UTC aware')
    return t
def canonical(name):
    if type(name) is not str or not name or '\\' in name or '\0' in name:raise ValueError('Bad member')
    p=PurePosixPath(name)
    if p.is_absolute() or p.as_posix()!=name or set(p.parts)&{'.','..','.git','__pycache__'}:raise ValueError('Noncanonical')
    return p
def resolve(base,literal):
    prefix=str(base)+'/'
    if type(literal) is not str or not literal.startswith(prefix) or '\\' in literal or '\0' in literal:raise ValueError('Literal outside')
    if base.is_symlink() or not base.is_dir() or base.resolve()!=base:raise ValueError('Base unsafe')
    for p in base.parents:
        if p.is_symlink() or not p.is_dir():raise ValueError('Ancestor unsafe')
    parts=literal[len(prefix):].split('/');current=base
    if not parts or any(not p or p in {'.git','__pycache__'} for p in parts):raise ValueError('Private/empty')
    for i,p in enumerate(parts):
        if not current.is_dir() or current.is_symlink():raise ValueError('Traverse real directory')
        if p=='.':continue
        if p=='..':
            if current==base:raise ValueError('Escape prefix')
            current=current.parent
        else:current=current/p
        if not current.exists() or current.is_symlink():raise ValueError('Missing/symlink')
        if current!=base and base not in current.parents:raise ValueError('Escape')
        if i<len(parts)-1 and not current.is_dir():raise ValueError('Nondirectory')
    if current==base or not current.is_file() or current.resolve()!=current:raise ValueError('Final regular')
    return current
for raw in [b'{"x":1,"x":2}',b'{"x":{"a":1,"a":2}}',b'NaN',b'Infinity',b'-Infinity',b'1e9999']:
    reject('strict_JSON_'+raw.decode(),lambda raw=raw:strict(raw))
for bad in [True,0.0,'0',None]:reject('typed_zero_'+repr(bad),lambda bad=bad:require_same({'used':bad},{'used':0}))
for name in ['', '/absolute','../file','a/../file','a/./file','a//file','a/','a\\file','a\0file','.git/file','a/__pycache__/file']:
    reject('member_'+repr(name),lambda name=name:canonical(name))
need(canonical('a/file').as_posix()=='a/file','Valid canonical path')
private=D/'PRIVATE_PATH_FIXTURES';private.mkdir();(private/'real').mkdir();(private/'real'/'file').write_bytes(b'Own regular fixture.\n');(private/'file').write_bytes(b'Own file.\n')
need(resolve(private,str(private)+'/real/../file')==private/'file','Legitimate in-root traversal')
need(resolve(private,str(private)+'/real/./file')==private/'real'/'file','Legitimate dot alias')
for label,name in [('escape_return',str(private)+'/../'+private.name+'/file'),('missing',str(private)+'/missing/file'),('non_directory',str(private)+'/file/../file'),('final_directory',str(private)+'/real'),('double_separator',str(private)+'//file'),('private_git',str(private)+'/.git/file'),('private_cache',str(private)+'/__pycache__/file'),('NUL',str(private)+'/fi\0le'),('backslash',str(private)+'/real\\file')]:
    reject('foreign_'+label,lambda name=name:resolve(private,name))
for label,target in [('ancestor_link',private/'real'),('final_link',private/'file')]:
    link=private/label;link.symlink_to(target,target_is_directory=target.is_dir())
    name=str(link)+'/file' if target.is_dir() else str(link)
    reject(label,lambda name=name:resolve(private,name));observations.append({'label':label,'actual_symlink_observed':link.is_symlink(),'target':str(target)})
    link.unlink()
(private/'SYMLINK_OBSERVATIONS.json').write_text(json.dumps(observations,indent=2)+'\n')
for mode in range(4096):need((stat.S_IMODE(stat.S_IFREG|mode)==0o444)==(mode==0o444),'Entire permission pattern '+oct(mode))
modes=D/'PRIVATE_MODE_FIXTURES';modes.mkdir();modeobservations=[]
for mode in [0o444,0o1444,0o2444,0o4444,0o644,0o777]:
    p=modes/('mode_'+oct(mode));p.write_bytes(b'Own actual permission fixture.\n');p.chmod(mode);actual=stat.S_IMODE(p.stat().st_mode)
    need(actual==mode,'Real full mode '+oct(mode));modeobservations.append({'path':p.relative_to(D).as_posix(),'actual_mode_before_closure':actual,'frozen_accepted':actual==0o444})
    if mode!=0o444:reject('mode_'+oct(mode),lambda actual=actual:need(actual==0o444,'Frozen literal444 required'))
# AST-only literal correlations independently reproduce the two old defects.
sources={name:ast.parse((V/name).read_bytes(),filename=name) for name in ['pr43_guards.py','integrate_reviewed_partial.py','state_mirror_reconciliation.py','seal_final_evidence.py','verify_post_acceptance.py']}
def scope(tree,target):
    values=[kw.value.value for n in ast.walk(tree) if isinstance(n,ast.Call) and isinstance(n.func,ast.Attribute) and isinstance(n.func.value,ast.Name) and n.func.value.id==target and n.func.attr=='update' for kw in n.keywords if kw.arg=='scope' and isinstance(kw.value,ast.Constant)]
    need(len(values)==1,'One literal '+target+' scope');return values[0]
written=scope(sources['state_mirror_reconciliation.py'],'proposal');expected=scope(sources['pr43_guards.py'],'expected')
need(written==expected,'Producer and guard full scope agreement')
reject('old_semicolon_scope',lambda:require_same(written.replace('PR43 ','PR43; ',1),expected))
snapshotnames=[n.right.value for n in ast.walk(sources['integrate_reviewed_partial.py']) if isinstance(n,ast.BinOp) and isinstance(n.op,ast.Div) and isinstance(n.left,ast.Attribute) and isinstance(n.left.value,ast.Name) and n.left.value.id=='g' and n.left.attr=='A' and isinstance(n.right,ast.Constant) and isinstance(n.right.value,str) and n.right.value.startswith('snapshot_manifest')]
need(snapshotnames==['snapshot_manifest.json'],'Exact actual overlay source snapshot')
need((A/snapshotnames[0]).is_file(),'Concrete filename exists');reject('old_absent_v2_snapshot',lambda:(A/'snapshot_manifest_v2.json').read_bytes())
guard_functions={n.name:n for n in sources['pr43_guards.py'].body if isinstance(n,ast.FunctionDef)}
rebuild=guard_functions['rebuild_saved_mirror_plan'];overrides=next(n.value for n in rebuild.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='overrides' for t in n.targets))
need(isinstance(overrides,ast.Dict) and len(overrides.keys)==2,'Only two historical Path read overrides')
need([n.value for n in ast.walk(overrides) if isinstance(n,ast.Constant) and isinstance(n.value,str)]==['unsolved_math_prioritization/state.json','unsolved_math_prioritization/history.jsonl'],'Exact two old native paths')
tryblock=next(n for n in rebuild.body if isinstance(n,ast.Try));need(len(tryblock.finalbody)==1 and ast.unparse(tryblock.finalbody[0])=='m.Path = actual_path','Finally restores native Path binding')
need(any(isinstance(n,ast.Call) and isinstance(n.func,ast.Attribute) and isinstance(n.func.value,ast.Name) and n.func.value.id=='m' and n.func.attr=='build_plan' for n in ast.walk(rebuild)),'Rebuild complete native plan')
# Fresh synthetic final-capture contract; it represents no actual future execution.
keys={'schema','argv','cwd','actual_execution','completed','pid','source_sha256','stdin_supplied','native13_before','main_head_before','started_utc','exit_code','finished_utc','source_unchanged','main_head_after','native13_after','stdout','stderr','readonly_git_queries','status'}
dated=strict((A/'ROOT_CURRENT_INPUT_PREIMAGES.json').read_bytes());native=[{k:z[k] for k in ['path','bytes','sha256']} for z in dated['files']]
now=dt.datetime.now(dt.timezone.utc);before=(now-dt.timedelta(seconds=2)).isoformat();finish=(now-dt.timedelta(seconds=1)).isoformat()
cap={'schema':'ROOT_actual_audit_administrative_capture_v1','argv':['/usr/bin/python3','-B',str(V/'seal_final_evidence.py'),'--execute'],'cwd':str(A),'actual_execution':True,'completed':True,'pid':123,'source_sha256':hashlib.sha256((V/'seal_final_evidence.py').read_bytes()).hexdigest(),'stdin_supplied':False,'native13_before':native,'main_head_before':'a'*40,'started_utc':before,'exit_code':0,'finished_utc':finish,'source_unchanged':True,'main_head_after':'a'*40,'native13_after':copy.deepcopy(native),'stdout':{'path':'stdout.bin','bytes':0,'sha256':hashlib.sha256(b'').hexdigest()},'stderr':{'path':'stderr.bin','bytes':0,'sha256':hashlib.sha256(b'').hexdigest()},'readonly_git_queries':[],'status':'PASS'}
def validcap(o):
    if type(o) is not dict or set(o)!=keys:raise ValueError('Capture keyset')
    for k,val in [('schema',cap['schema']),('actual_execution',True),('completed',True),('exit_code',0),('status','PASS'),('stdin_supplied',False),('source_unchanged',True),('cwd',str(A))]:require_same(o[k],val)
    if type(o['pid']) is not int or o['pid']<=0 or type(o['argv']) is not list or str(V/'seal_final_evidence.py') not in o['argv']:raise ValueError('Actual PID argv')
    require_same(o['native13_before'],o['native13_after']);require_same(o['main_head_before'],o['main_head_after'])
    if not utc(o['started_utc'])<=utc(o['finished_utc'])<=dt.datetime.now(dt.timezone.utc):raise ValueError('Capture clock ordering')
    for k in ['stdout','stderr']:
        z=o[k]
        if type(z) is not dict or set(z)!={'path','bytes','sha256'} or type(z['bytes']) is not int or z['bytes']<0:raise ValueError('Exact stream ref')
        require_same(z['path'],k+'.bin')
validcap(cap);need(True,'Synthetic final capture valid')
for label,field,val in [('bool_PID','pid',True),('zero_PID','pid',0),('bool_exit','exit_code',False),('integer_completed','completed',1),('unlaunched','actual_execution',False),('different_HEAD','main_head_after','b'*40),('reversed_clock','finished_utc',before[:-6]),('future_clock','finished_utc',(now+dt.timedelta(days=1)).isoformat()),('naive_clock','started_utc','2026-10-03T01:00:00'),('non_UTC_clock','started_utc','2026-10-03T01:00:00-07:00')]:
    mutant=copy.deepcopy(cap);mutant[field]=val;reject('capture_'+label,lambda mutant=mutant:validcap(mutant))
mutant=copy.deepcopy(cap);mutant['unknown_meaningful']=True;reject('capture_unknown_field',lambda:validcap(mutant))
mutant=copy.deepcopy(cap);mutant['native13_after'][0]['sha256']='0'*64;reject('capture_changed_native',lambda:validcap(mutant))
mutant=copy.deepcopy(cap);mutant['stdout']['bytes']=False;reject('capture_bool_stream_size',lambda:validcap(mutant))
for name in ['AUTHORING_ACTUAL_CAPTURE','CONTROLS_ACTUAL_CAPTURE','CLOSURE_ACTUAL_CAPTURE']:
    actual=strict((V/name/'CAPTURE.json').read_bytes());need(utc(actual['started_utc'])<=utc(actual['finished_utc'])<=now,'Actual V2 preparation clocks '+name)
    need(type(actual['pid']) is int and actual['pid']>0 and type(actual['exit_code']) is int and actual['exit_code']==0 and actual['source_unchanged'] is True,'Actual V2 preparation typed PID exit source '+name)
# Complete typed synthetic post-PR42 preservation model, no future receipt claims.
prior={str(1000+i):{'id':str(1000+i),'turns_used':2 if i<8 else 1 if i<33 else 0,'event':'acceptance_mirror_import','nested':{'preserved':[i,None,False]}} for i in range(33)}
need(sum(z['turns_used'] for z in prior.values())==41,'Synthetic33 target/41 turns baseline')
oldhistory=b'{"original":"synthetic complete prefix"}\n'
event={'id':'30004386','pr':43,'status':'already_solved','turns_used':0,'turn_limit':5,'event':'acceptance_mirror_import','evidence':{'historical_transitions_asserted':False,'import_is_present_day_mirror':True,'duplicate_ids':[]}}
after={**copy.deepcopy(prior),'30004386':copy.deepcopy(event)}
append=json.dumps(event,sort_keys=True).encode()+b'\n';history=oldhistory+append
def validnative(state,hist,events):
    if type(state) is not dict or set(state)!=set(prior)|{'30004386'}:raise ValueError('Native memberships')
    for k,val in prior.items():require_same(state[k],val)
    require_same(state['30004386'],event);require_same(events,[event])
    if hist!=oldhistory+append or not hist.startswith(oldhistory):raise ValueError('History exact prefix/one event')
    if len(state)!=34 or any(type(z['turns_used']) is not int for z in state.values()) or sum(z['turns_used'] for z in state.values())!=41:raise ValueError('Typed budgets')
validnative(after,history,[event]);need(True,'Synthetic complete native preservation passes')
mutant=copy.deepcopy(after);mutant['1000']['nested']['preserved'][2]=0;reject('native_old_nested_bool_retyped',lambda:validnative(mutant,history,[event]))
mutant=copy.deepcopy(after);mutant['30004386']['turns_used']=False;reject('native_bool_used',lambda:validnative(mutant,history,[event]))
mutant=copy.deepcopy(after);mutant['extra']={};reject('native_extra_target',lambda:validnative(mutant,history,[event]))
reject('native_lost_history_prefix',lambda:validnative(after,append,[event]));reject('native_duplicate_event',lambda:validnative(after,history+append,[event,event]))
inv={'items':[{'number':i,'stage':'complete' if i<32 else 'pending','preserved':{'i':i}} for i in range(1,181)],'completed_count':32,'current_pr':43}
# Use exactly32 precompleted synthetic identities, leaving PR43 pending.
inv['items'][31]['stage']='complete';need(sum(z['stage']=='complete' for z in inv['items'])==32,'Synthetic32 primary inventory')
derived=copy.deepcopy(inv);chosen=next(z for z in derived['items'] if z['number']==43);chosen.update(stage='complete',outcome='already_solved_accepted_partial');derived.update(completed_count=33,current_pr=44)
def validinv(obj):
    require_same(obj,derived)
    if type(obj['completed_count']) is not int or len(obj['items'])!=180:raise ValueError('Typed inventory counts')
validinv(derived);need(all(eq(a,b) for a,b in zip(inv['items'],derived['items']) if a['number']!=43),'All179 unrelated inventory entries preserved')
mutant=copy.deepcopy(derived);mutant['items'][150]['preserved']['i']+=1;reject('inventory_unrelated_changed',lambda:validinv(mutant))
mutant=copy.deepcopy(derived);mutant['completed_count']=33.0;reject('inventory_float_count',lambda:validinv(mutant))
draft=strict((V/'DRAFT_ROOT_IMMUTABLE_BINDINGS.json').read_bytes())
for key in ['whole_manifest','root_whole_inspection','root_capture_operator','previous_mirror','previous_post','previous_root_post']:need(draft[key] is None,'Actual unapproved null '+key)
for key in ['root_full_current_read_completed','root_full_whole_read_completed','root_acceptance_source_review_completed','independent_whole_current_pass','root_actual_PR42_predecessor_read_completed']:need(draft[key] is False,'Actual false future flag '+key)
def complete_predecessor(o):
    for key in ['previous_mirror','previous_post','previous_root_post']:
        ref=o[key]
        if type(ref) is not dict or set(ref)!={'path','bytes','sha256'}:raise ValueError('Actual predecessor reference required')
reject('unapproved_actual_draft_NULL_predecessors',lambda:complete_predecessor(draft))
result={'schema':'PR43_V2_SOURCE_ADVERSARY_INDEPENDENT_CONTROLS_v1','created_utc':dt.datetime.now(dt.timezone.utc).isoformat(),'actual_pid':os.getpid(),'predicates':len(checks),'negative_controls':negative,'negative_control_count':len(negative),'permission_predicates':4096,'actual_private_permission_observations':modeobservations,'private_symlink_observations':observations,'AST_only_two_repairs_correlated':True,'historical_native_plan_exact_two_read_overrides_and_finally_restoration':True,'native_inventory_capture_models_explicitly_synthetic':True,'future_predecessor_or_ROOT_approval_certified':False,'production_candidate_native_scripts_imported_compiled_executed':False,'original_substantive_attempts':0,'new_substantive_attempts':0,'audit_turns':0}
(D/'INDEPENDENT_CONTROL_RESULT.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
