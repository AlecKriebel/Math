"""Independent pure v4 control challenges. No prepare/execute/assess/config/gates."""
import sys
sys.dont_write_bytecode=True
from pathlib import Path
import ast,copy,datetime,hashlib,importlib.util,json,os
D=Path(__file__).resolve().parent
S=D.parent/'native_publication_integration_plan_20261006/corrected_v4'
spec=importlib.util.spec_from_file_location('fresh_v4_guards',S/'v3_guards.py')
g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
checks=[]
def need(ok,msg):
    if not ok:raise RuntimeError(msg)
def check(name,fn):
    fn();checks.append({'name':name,'passed':True})
def rejects(name,fn):
    try:fn()
    except (ValueError,KeyError,TypeError):checks.append({'name':name,'rejected':True});return
    raise RuntimeError('accepted mutation: '+name)
def enc(x):return g.canonical(x)
def digest(x):return g.sha(enc(x))
policy={'deadline_seconds':7,'cpu_seconds':2,'address_space_bytes':256*1024*1024,'file_size_bytes':8*1024*1024,'open_files':32,'memory_limit_mode':'advisory_no_hard_memory_claim'}
capacity={'headroom_bytes':32*1024*1024,'max_artifact_count':512,'max_materialized_bytes':160*1024*1024,'wrapper_bytes_cap':65536,'receipt_json_bytes_cap':128*1024,'per_native_growth_bytes':256*1024,'max_package_files':64,'future_commit_overhead_bytes':16*1024*1024,'runtime_overhead_bytes':8*1024*1024}
process_policy={'deadline_seconds':30,'max_process_count':64,'max_stderr_bytes':65536,'max_stdout_bytes':32*1024*1024,'retain_bytes_per_stream':4096,'terminate_grace_seconds':1}
manifest=enc({'revision':g.WORKER_DATASET_REVISION,'records':173})
pins=[{'path':'unsolved_math_prioritization/'+n,'bytes':1000+101*i,'sha256':hashlib.sha256(n.encode()).hexdigest()} for i,n in enumerate(g.WORKER_NATIVE_NAMES)]
next(p for p in pins if p['path'].endswith('/manifest.json')).update(bytes=len(manifest),sha256=g.sha(manifest))
queue_sha=next(p for p in pins if p['path'].endswith('/queue.py'))['sha256']
effective={k:None for k in g.CHOICES};effective.update(execution_mode='review_bundle_only',scoped_rank_interpretation='preserve_baseline_labels_and_positions_not_global_rerank',native_baseline_pins=pins,queue_py_sha256=queue_sha,worker_policy=copy.deepcopy(policy),capacity_policy=copy.deepcopy(capacity))
execution={'schema':'pr108-immutable-execution-inputs/v3','template_only':False,'effective':effective,'program_files':[{'path':'audit/'+n} for n in g.PROGRAMS],'input_files':[]}
execution_bytes=enc(execution)
output=S/('candidate_'+g.sha(execution_bytes)[:16])
control=g.derive_worker_control(execution,execution_bytes,output,manifest)
oracle_caps={Path(p['path']).name:p['bytes']+(256*1024 if Path(p['path']).name in {'catalog.json','assessments.json','state.json','history.jsonl','assessment_history.jsonl','ranking.csv','summary.json','SHORTLIST.md','QUEUE.md'} else 0) for p in pins};oracle_caps['assessment.json']=128*1024
oracle={'schema':'pr108-native-assess-control/v3','fixture':False,'ROOT':str(output/'private_native_backend'),'SQL_cache':'/Users/alec/Documents/Math/unsolved_math_prioritization/cache/catalog.sqlite','dataset_revision':'37e53eabe540fb458758e198be61634bd02ee008','record_count':173,'queue_py_sha256':queue_sha,'execution_inputs_sha256':g.sha(execution_bytes),'worker_policy':copy.deepcopy(policy),'backend_file_caps':oracle_caps}
check('independent complete derivation oracle',lambda:need(enc(control)==enc(oracle),'oracle mismatch'))
check('correct control accepts',lambda:g.validate_worker_control(control,execution,execution_bytes,output,manifest))
inv=g.capacity_inventory(pins,[],{k:{'bytes':37} for k in g.GATE_ROLES},{},capacity,process_policy)
check('capacity cap formula correspondence',lambda:need({Path(e['path']).name:e['max_bytes'] for e in inv['entries'] if e['path'].startswith('private_native_backend/')}==oracle_caps,'inventory cap mismatch'))
check('16MiB commit plus 32MiB headroom plus 8MiB runtime allocation',lambda:need(inv['required_free_bytes']==inv['max_materialized_bytes']+56*1024*1024,'reserve allocation'))
# Detached policy, and no writes or calls to native worker/helper occur.
control['worker_policy']['cpu_seconds']=90
check('returned control does not mutate frozen policy',lambda:need(execution['effective']['worker_policy']['cpu_seconds']==2,'aliased policy'))
control=copy.deepcopy(oracle)
paths=[]
def walk(obj,path=()):
    if isinstance(obj,dict):
        for k,v in obj.items():walk(v,path+(k,))
    else:paths.append((path,obj))
walk(control)
def edit(obj,path,value,remove=False):
    t=obj
    for k in path[:-1]:t=t[k]
    if remove:del t[path[-1]]
    else:t[path[-1]]=value
for path,value in paths:
    variations=[None]
    if type(value) is int:variations += [value+1,float(value),True]
    elif type(value) is bool:variations += [True,0]
    else:variations += [value+'-mutated']
    for i,new in enumerate(variations):
        if enc(new)==enc(value):continue
        bad=copy.deepcopy(control);edit(bad,path,new)
        rejects('control '+'.'.join(path)+' variant '+str(i),lambda bad=bad:g.validate_worker_control(bad,execution,execution_bytes,output,manifest))
    bad=copy.deepcopy(control);edit(bad,path,None,True)
    rejects('control missing '+'.'.join(path),lambda bad=bad:g.validate_worker_control(bad,execution,execution_bytes,output,manifest))
for path in [(),('worker_policy',),('backend_file_caps',)]:
    bad=copy.deepcopy(control);t=bad
    for k in path:t=t[k]
    t['unreviewed_extra']=1
    rejects('control additional field '+str(path),lambda bad=bad:g.validate_worker_control(bad,execution,execution_bytes,output,manifest))
rejects('changed native manifest bytes',lambda:g.derive_worker_control(execution,execution_bytes,output,manifest+b' '))
for name,mutator in [
    ('queue pin mismatch',lambda e:e['effective'].update(queue_py_sha256='b'*64)),
    ('missing native pin',lambda e:e['effective']['native_baseline_pins'].pop()),
    ('duplicate native pin',lambda e:e['effective']['native_baseline_pins'].append(copy.deepcopy(e['effective']['native_baseline_pins'][0]))),
    ('wrong native path',lambda e:e['effective']['native_baseline_pins'][0].update(path='other/queue.py')),
    ('float growth',lambda e:e['effective']['capacity_policy'].update(per_native_growth_bytes=262144.0)),
    ('boolean growth',lambda e:e['effective']['capacity_policy'].update(per_native_growth_bytes=True)),
    ('float receipt cap',lambda e:e['effective']['capacity_policy'].update(receipt_json_bytes_cap=131072.0)),
]:
    bad=copy.deepcopy(execution);mutator(bad);b=enc(bad);o=S/('candidate_'+g.sha(b)[:16])
    rejects(name,lambda bad=bad,b=b,o=o:g.derive_worker_control(bad,b,o,manifest))
for key,value in [('records',True),('records',0),('records',-1),('records',173.0),('revision','wrong')]:
    m=g.loads(manifest);m[key]=value;mb=enc(m);bad=copy.deepcopy(execution)
    next(p for p in bad['effective']['native_baseline_pins'] if p['path'].endswith('/manifest.json')).update(bytes=len(mb),sha256=g.sha(mb))
    b=enc(bad);o=S/('candidate_'+g.sha(b)[:16])
    rejects('authenticated malformed manifest '+key+' '+str(value),lambda bad=bad,b=b,o=o,mb=mb:g.derive_worker_control(bad,b,o,mb))
for o in [Path('relative/candidate_'+g.sha(execution_bytes)[:16]),D/('candidate_'+g.sha(execution_bytes)[:16]),S/('candidate_'+'0'*16),S/'nested'/output.name]:
    rejects('candidate anchor '+str(o),lambda o=o:g.derive_worker_control(execution,execution_bytes,o,manifest))
rejects('noncanonical execution bytes',lambda:g.derive_worker_control(execution,execution_bytes+b' ',output,manifest))
def success():
    result={'schema':'pr108-native-assess-worker-receipt/v3','fixture':False,'outcome':'success','native_assess_returned_without_exception':True,'actual_operator_PID':7331,'execution_inputs_sha256':control['execution_inputs_sha256'],'validated_worker_control':copy.deepcopy(control),'worker_control_binding_sha256':digest(control),'requested_resource_policy':copy.deepcopy(policy),'ROOT':control['ROOT'],'queue_py_sha256':queue_sha,'native_function':'queue.py:assess','SQL_connection':'mode=ro&immutable=1','native_status_command_called':False,'applied_limits':{'RLIMIT_CPU':[2,2],'RLIMIT_FSIZE':[8*1024*1024]*2,'RLIMIT_NOFILE':[32,32]},'hard_memory_limit_claimed':False,'memory_policy':{'hard_memory_limit_claimed':False,'platform':sys.platform,'requested_advisory_bytes':256*1024*1024,'RLIMIT_RSS_used':False,'RLIMIT_AS_enforcement_certified':False,'RLIMIT_AS_requested':False}}
    process={'PID':7331,'exit_code':0,'termination_reason':None,'child_reaped':True,'deadline_seconds':7}
    return result,process
check('correct parent result accepts',lambda:g.validate_worker_result(*success()[:1],control,success()[1]))
for path,value in paths:
    result,proc=success();edit(result['validated_worker_control'],path,None)
    rejects('returned binding changed '+'.'.join(path),lambda result=result,proc=proc:g.validate_worker_result(result,control,proc))
for key in policy:
    result,proc=success();result['requested_resource_policy'][key]=None
    rejects('requested policy '+key,lambda result=result,proc=proc:g.validate_worker_result(result,control,proc))
for limit in ['RLIMIT_CPU','RLIMIT_FSIZE','RLIMIT_NOFILE']:
    for side in range(2):
        for kind in ['value','float','bool']:
            result,proc=success();v=result['applied_limits'][limit][side];result['applied_limits'][limit][side]=v+1 if kind=='value' else float(v) if kind=='float' else True
            rejects('applied '+limit+' '+str(side)+' '+kind,lambda result=result,proc=proc:g.validate_worker_result(result,control,proc))
    result,proc=success();del result['applied_limits'][limit]
    rejects('missing '+limit,lambda result=result,proc=proc:g.validate_worker_result(result,control,proc))
for key,value in [('worker_control_binding_sha256','f'*64),('ROOT','wrong'),('queue_py_sha256','f'*64),('execution_inputs_sha256','f'*64),('actual_operator_PID',7332),('outcome','failure'),('fixture',True),('native_function','wrong'),('SQL_connection','mode=rw'),('native_status_command_called',True),('native_assess_returned_without_exception',False),('hard_memory_limit_claimed',True)]:
    result,proc=success();result[key]=value
    rejects('result '+key,lambda result=result,proc=proc:g.validate_worker_result(result,control,proc))
for key,value in [('deadline_seconds',8),('exit_code',1),('termination_reason','deadline_exceeded'),('child_reaped',False),('PID',7332)]:
    result,proc=success();proc[key]=value
    rejects('actual process '+key,lambda result=result,proc=proc:g.validate_worker_result(result,control,proc))
for key,value in [('requested_advisory_bytes',1),('platform','other'),('hard_memory_limit_claimed',True),('RLIMIT_RSS_used',True),('RLIMIT_AS_enforcement_certified',True),('RLIMIT_AS_requested',True)]:
    if key=='RLIMIT_AS_requested' and sys.platform!='darwin':continue
    result,proc=success();result['memory_policy'][key]=value
    rejects('memory correspondence '+key,lambda result=result,proc=proc:g.validate_worker_result(result,control,proc))
# Direct source order check: exact execution body remains uncalled.
worker_tree=ast.parse((S/'native_assess_worker.py').read_text());execute=next(n for n in worker_tree.body if isinstance(n,ast.FunctionDef) and n.name=='execute')
locations={}
for node in ast.walk(execute):
    if isinstance(node,ast.Call):
        name=ast.unparse(node.func)
        if name in ['g.validate_worker_control','apply_resource_policy','spec.loader.exec_module']:locations[name]=node.lineno
check('worker control validation precedes limits and module load',lambda:need(locations['g.validate_worker_control']<locations['apply_resource_policy']<locations['spec.loader.exec_module'],'worker order'))
helper_tree=ast.parse((S/'prepare_review_bundle.py').read_text());prepare=next(n for n in helper_tree.body if isinstance(n,ast.FunctionDef) and n.name=='prepare')
parent_source=(S/'prepare_review_bundle.py').read_text()
check('parent independent derivation and control-byte predicate precedes acceptance',lambda:need(parent_source.index('expected_control=g.derive_worker_control')<parent_source.index("require((output/'WORKER_CONTROL.json').read_bytes()==encode(expected_control)")<parent_source.index('g.validate_worker_result(result,expected_control,proc)')<parent_source.index('afterass,afterstate='),'parent order'))
summary={'schema':'pr108-fresh-independent-v4-pure-control-tests/v1','UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'PID':os.getpid(),'optimized':not __debug__,'passed':True,'checks':len(checks),'control_leaf_count':len(paths),'worker_order':locations,'native_prepare_execute_assess_calls':0,'resource_setup_calls':0,'actual_config_control_gate_files_created':0,'Git_services_private_credentials_reads':0,'details':checks}
(D/('INDEPENDENT_OPTIMIZED_RESULTS.json' if not __debug__ else 'INDEPENDENT_NORMAL_RESULTS.json')).write_bytes(enc(summary))
print(json.dumps({k:v for k,v in summary.items() if k!='details'},sort_keys=True))
