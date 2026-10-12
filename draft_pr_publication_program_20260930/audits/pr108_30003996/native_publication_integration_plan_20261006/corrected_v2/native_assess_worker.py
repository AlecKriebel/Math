#!/usr/bin/env python3
"""UNEXECUTED native worker draft. Fresh reviewed control + parent deadline required."""
from pathlib import Path
import argparse, importlib.util, os, resource, sqlite3, sys, types
from bounded_process import now
import v2_guards as g
from v2_guards import require, loads, canonical, sha, regular, K
D=Path(__file__).resolve().parent
A=D.parent.parent
C=A.parents[2]

def validate_policy(policy):
    require(set(policy) == {'deadline_seconds','cpu_seconds','address_space_bytes','file_size_bytes','open_files','memory_limit_mode'}, 'Worker policy fields')
    require(policy['memory_limit_mode']=='advisory_no_hard_memory_claim','No untested hard memory claim')
    require(all(type(v) is int for k,v in policy.items() if k!='memory_limit_mode'), 'Worker integer resource limits')
    require(1 <= policy['deadline_seconds'] <= 120 and 1 <= policy['cpu_seconds'] <= 90 and
        128*1024*1024 <= policy['address_space_bytes'] <= 1024*1024*1024 and
        1 <= policy['file_size_bytes'] <= 32*1024*1024 and 16 <= policy['open_files'] <= 64, 'Worker limits')

def apply_resource_policy(policy):
    """Harmless fixture may call setup; native execute is never used by fixtures."""
    validate_policy(policy); applied={}
    for name,limit in [('RLIMIT_CPU',policy['cpu_seconds']),('RLIMIT_FSIZE',policy['file_size_bytes']),('RLIMIT_NOFILE',policy['open_files'])]:
        which=getattr(resource,name);resource.setrlimit(which,(limit,limit));actual=resource.getrlimit(which)
        require(actual==(limit,limit),'Enforced resource setup not applied: '+name);applied[name]=list(actual)
    memory={'platform':sys.platform,'requested_advisory_bytes':policy['address_space_bytes'],'hard_memory_limit_claimed':False,
        'RLIMIT_RSS_used':False,'RLIMIT_AS_enforcement_certified':False}
    if sys.platform=='darwin':
        memory.update(RLIMIT_AS_requested=False,reason='Darwin may reject or ignore address-space/RSS limits; no hard memory bound is certified.')
    else:
        try:
            resource.setrlimit(resource.RLIMIT_AS,(policy['address_space_bytes'],policy['address_space_bytes']))
            memory.update(RLIMIT_AS_requested=True,RLIMIT_AS_readback=list(resource.getrlimit(resource.RLIMIT_AS)),setup_accepted=True)
        except (ValueError,OSError) as error:
            memory.update(RLIMIT_AS_requested=True,setup_accepted=False,setup_error=str(error)[:240])
    return {'enforced_limit_readbacks':applied,'memory_policy':memory}

def execute(control_path):
    # No fixture entry point invokes this function.
    control = loads(regular(control_path.absolute()) and control_path.read_bytes())
    require(control['schema'] == 'pr108-native-assess-control/v2' and control['fixture'] is False, 'Actual worker control required')
    policy = control['worker_policy']; validate_policy(policy)
    output = control_path.absolute().parent
    require(output.parent==D and control_path.name=='WORKER_CONTROL.json' and
        output.name=='candidate_'+control['execution_inputs_sha256'][:16], 'Worker control outside its sole reviewed candidate root')
    execution_bytes=(output/'EXECUTION_INPUTS.json').read_bytes();execution=g.loads(execution_bytes)
    g.validate_execution_manifest(execution,execution_bytes)
    require(sha(execution_bytes)==control['execution_inputs_sha256'],'Worker immutable execution manifest changed')
    config=g.loads((output/'CONFIG.json').read_bytes());g.validate_thin_config(config)
    require(config['execution_inputs']['sha256']==sha(execution_bytes) and config['execution_inputs']['bytes']==len(execution_bytes),'Worker thin config correspondence')
    programs={}
    for pin in execution['program_files']:
        path=C/g.relative(pin['path']);require(path.parent==D and path.name in g.PROGRAMS and g.regular(path).st_size==pin['bytes'],'Worker exact program location/size')
        data=path.read_bytes();require(sha(data)==pin['sha256'],'Worker program changed after preflight');programs[path.name]=sha(data)
    final_pin=config['gates']['final'];final_path=C/g.relative(final_pin['path'])
    require(final_path.is_relative_to(A) and g.regular(final_path).st_size==final_pin['bytes'] and final_pin['bytes']<=65536,'Worker final gate location/cap')
    final_bytes=final_path.read_bytes();require(sha(final_bytes)==final_pin['sha256'],'Worker final gate pin changed')
    final=g.loads(final_bytes)
    require(final.get('schema')=='pr108-publication-root-gate/v2' and final.get('role')=='final' and
        final.get('execution_inputs_sha256')==sha(execution_bytes) and final.get('reviewed_program_sha256')==programs and
        final.get('main_parent')==execution['effective']['main_parent'] and final.get('actual_root_review') is True and
        final.get('native_integration_clearance') is True and final.get('clearance') is True and
        not any(final.get(x) is True for x in ['fixture','simulated','dry_run']),'Worker lacks final actual manifest-bound native clearance')
    backend = output/'private_native_backend'
    require(str(backend) == control['ROOT'] and backend.is_dir() and not backend.is_symlink(), 'Private backend root')
    began = now(); result = {'schema':'pr108-native-assess-worker-receipt/v2','actual_operator_PID':os.getpid(),
        'UTC_start':began, 'fixture':False, 'native_function':'queue.py:assess', 'ROOT':str(backend),
        'SQL_connection':'mode=ro&immutable=1', 'native_status_command_called':False,
        'queue_py_sha256':control['queue_py_sha256'], 'execution_inputs_sha256':control['execution_inputs_sha256'],
        'requested_resource_policy':policy, 'applied_limits':{}, 'hard_memory_limit_claimed':False}
    try:
        setup=apply_resource_policy(policy)
        result['applied_limits']=setup['enforced_limit_readbacks'];result['memory_policy']=setup['memory_policy']
        code = (backend/'queue.py').read_bytes(); require(sha(code) == control['queue_py_sha256'], 'Worker source changed')
        sys.dont_write_bytecode = True
        spec = importlib.util.spec_from_file_location('pr108_pinned_queue_worker', backend/'queue.py')
        mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod); mod.ROOT = backend
        cache = Path(control['SQL_cache'])
        require(str(cache) == '/Users/alec/Documents/Math/unsolved_math_prioritization/cache/catalog.sqlite', 'Exact read-only shared SQL path')
        def ro(): return sqlite3.connect('file:'+str(cache)+'?mode=ro&immutable=1',uri=True)
        def check_cache():
            db = ro()
            try:
                require(db.execute('SELECT revision FROM metadata').fetchone() == (control['dataset_revision'],) and
                    db.execute('SELECT count(*) FROM records').fetchone()[0] == control['record_count'], 'Worker SQL revision/count')
            finally: db.close()
        mod.connect, mod.require_cache = ro, check_cache
        caps = control['backend_file_caps']
        # Source-pinned write override preserves native JSON serialization, one temporary file at a time.
        def bounded_write(path,obj):
            require(path.parent == backend and path.name in caps, 'Worker native write outside reviewed backend')
            data = (mod.json.dumps(obj,ensure_ascii=False,indent=2)+'\n').encode()
            require(len(data) <= caps[path.name], 'Worker per-file cap: '+path.name)
            tmp = path.with_suffix(path.suffix+'.tmp')
            require(not tmp.exists(), 'Stale worker atomic slot')
            tmp.write_bytes(data); tmp.replace(path)
        mod.write = bounded_write
        mod.assess(types.SimpleNamespace(id=K,file=str(backend/'assessment.json')))
        result.update(native_assess_returned_without_exception=True, outcome='success')
    except BaseException as error:
        result.update(native_assess_returned_without_exception=False,outcome='failure',
                      error_type=type(error).__name__,error=str(error)[:1200])
        result['UTC_end'] = now(); (output/'WORKER_RESULT.json').write_bytes(canonical(result))
        raise
    result['UTC_end'] = now(); (output/'WORKER_RESULT.json').write_bytes(canonical(result))

if __name__ == '__main__':
    parser=argparse.ArgumentParser(description=__doc__); parser.add_argument('--control',type=Path,required=True)
    execute(parser.parse_args().control)
