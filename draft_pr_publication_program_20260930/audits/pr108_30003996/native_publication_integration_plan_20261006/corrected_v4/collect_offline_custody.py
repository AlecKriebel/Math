"""One own-folder offline read/fixture checkpoint; no native/Git/services/config preparation."""
import sys
sys.dont_write_bytecode=True
from pathlib import Path
import datetime,hashlib,json,os,shutil,collections
import v3_guards as g
from bounded_process import BoundedRunner
from test_v4_guards import fixture_environment_policy
D=Path(__file__).resolve().parent;A=D.parent.parent;C=A.parents[2];R=Path('/Users/alec/Documents/Math')
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def write(name,obj):(D/name).write_bytes(g.canonical(obj))
def pin(path,group):
    g.regular(path);data=path.read_bytes()
    return {'path':str(path),'bytes':len(data),'sha256':g.sha(data),'group':group}
start=now();g.validate_python_startup(os.environ)
prior=g.loads((D/'PREDECESSOR_UNCHANGED_INPUT_PINS.json').read_bytes());inputs=[]
counts=collections.Counter()
for item in prior['files']:
    actual=pin(Path(item['path']),item['group']);g.require(actual==item,'Predecessor bytes changed')
    inputs.append(actual);counts[item['group']]+=1
adversary=A/'native_helper_v3_fresh_code_adversary_20261006'
g.require(g.sha((adversary/'OUTPUT_MANIFEST.json').read_bytes())=='8240f0629e367f964a290869dbf3b1a9e4c0c3e84311156ed93430e8d1ef9c28','Adversary manifest differs')
for name in [*g.PROGRAMS,'test_v4_guards.py','write_review_documents.py','PLAN.md','WORKER_CONTROL_CONTRACT.json','CORE_SOURCE_DIFF.patch','SOURCE_DIFF_MANIFEST.json','PREDECESSOR_UNCHANGED_INPUT_PINS.json','collect_offline_custody.py']:
    inputs.append(pin(D/name,'V3_source_and_policy'))
for p in [R/'AGENTS.md',R/'unsolved_math_prioritization/AGENTS.md',R/'unsolved_math_prioritization/README.md',R/'unsolved_math_prioritization/queue.py',
          A/'ROOT_ACTUAL_PUBLICATION_RECEIPT_20261006.json',A/'ROOT_ACTUAL_GOOGLE_SHEET_SERVICE_RECEIPT_20261006.json',
          *[A/'original_source_authentication_20261006'/x for x in ['ORIGINAL_BLOB_MANIFEST.json','QUEUE_STATUS_PROJECTION.json','SOURCEPAIR_AUTHENTICATION.json','SELECTED_IMPORTED_PRIOR_REPORT.json']]]:
    inputs.append(pin(p,'actual_read_context'))
# Templates are parsed and rejected through pure guard functions; no prepare entry point is called.
rejections={}
for name,function in [('CONFIG_TEMPLATE_DO_NOT_RUN.json',g.validate_thin_config),
        ('EXECUTION_INPUTS_TEMPLATE_DO_NOT_RUN.json',lambda o:g.validate_execution_manifest(o,g.canonical(o)))]:
    p=D/name;inputs.append(pin(p,'inert_template'))
    try:function(g.loads(p.read_bytes()))
    except ValueError as error:rejections[name]={'rejected':True,'error':str(error)}
    else:raise ValueError('Template unexpectedly accepted')
policy={'max_process_count':4,'retain_bytes_per_stream':4096,'max_stdout_bytes':8192,'max_stderr_bytes':16384,'deadline_seconds':30,'terminate_grace_seconds':1}
output=D/'execution_receipts';output.mkdir(exist_ok=False)
runner=BoundedRunner(output,D,policy,fixture_environment_policy());results=[]
for mode,extra in [('NORMAL',[]),('OPTIMIZED',['-O'])]:
    stdout,stderr,record=runner.run([sys.executable,*g.PYTHON_PREFIX,*extra,str(D/'test_v4_guards.py')],fixture=True)
    g.require(record['exit_code']==0 and b'Ran 32 tests' in stderr and stderr.rstrip().endswith(b'OK'),'Offline fixture suite failed')
    for stream,data in [('STDOUT',stdout),('STDERR',stderr)]:
        (output/(mode+'_'+stream+'_FULL.bin')).write_bytes(data)
        g.require(g.sha(data)==record[stream.lower()]['sha256_observed'],'Returned bounded full output differs from actual observed bytes')
    result={'mode':mode,'fixture_only':True,'actual_PID':record['PID'],'UTC_start':record['UTC_start'],'UTC_end':record['UTC_end'],
        'exit_code':record['exit_code'],'tests':32,'all_passed':True,'argv':record['argv'],
        'native_prepare_assess_export_install_executions':0,'service_calls':0,'Git_commands':0,
        'stdout':pin(output/(mode+'_STDOUT_FULL.bin'),'actual_fixture_output'),
        'stderr':pin(output/(mode+'_STDERR_FULL.bin'),'actual_fixture_output')}
    write(mode+'_FIXTURE_RESULTS.json',result);results.append(result)
# Verify all predecessor pins again after fixtures. These are read-only actual receipts, not fixture assumptions.
for item in prior['files']:g.require(pin(Path(item['path']),item['group'])==item,'Predecessor changed after fixtures')
free=shutil.disk_usage(D).free;end=now()
write('READ_SCOPE_MANIFEST.json',{'schema':'pr108-v4-actual-local-read-manifest/v1','UTC_start':start,'UTC_end':end,'actual_operator_PID':os.getpid(),
    'files':inputs,'predecessor_group_counts':dict(counts),'whole_adversary_manifest_authenticated':True,'no_Git_SQL_or_services_invoked':True})
write('CONTEXT_RECEIPT.json',{'schema':'pr108-v4-offline-custody-context/v1','UTC_start':start,'UTC_end':end,'actual_operator_PID':os.getpid(),
    'actual_local_read_and_fixture_checkpoint':True,'fixture_suites':results,'template_rejections':rejections,
    'predecessor_counts_verified_before_and_after':dict(counts),'all_predecessor_bytes_unchanged':True,
    'current_free_bytes_snapshot':free,'capacity_clearance':False,'future_commit_reserve_parent_intention_bytes':16*1024*1024,'reserve_context':'Parent bounded checkpoint implementation eliminates duplicate49MB retention; actual16MiB policy still requires fresh exact config/capacity review; existing guard minima unchanged',
    'parent_reported_main_context':'fb1eadba14d56b9f49409e31533242ac1b400e6b','fresh_Git_HEAD_receipt_by_this_agent':False,
    'parent_local_actual_publication_receipt_read_as_context_only':True,'parent_actual_DOI':'10.5281/zenodo.23181280',
    'parent_local_actual_Sheet_receipt_read_as_context_only':True,'parent_actual_Sheet_range':"'Math Puzzles'!A31:D31",'actual_B_blank':True,
    'independent_service_reauthentication_by_this_agent':False,'actual_runtime_configuration_prepared':False,
    'native_prepare_assess_export_install_executions':0,'Git_commands':0,'service_calls':0,'new_central_proof_search_turns':0,
    'contact_or_outreach_prepared_or_made':False,'new_V4_adversary_clearance':False})
with (D/'RESEARCH_LOG.md').open('a') as file:
    file.write('\n'+end+' — Actual own-folder custody completed: normal32/32 and optimized32/32 pass, actual PIDs '+str(results[0]['actual_PID'])+'/'+str(results[1]['actual_PID'])+'. Predecessor counts '+str(dict(counts))+' verified before/after. Current free bytes '+str(free)+' are a snapshot only; capacity clearance false. Pure templates rejected. Draft completion98%, pending immutable seal; native executions0, proof turns0.\n')
print(json.dumps({'actual_operator_PID':os.getpid(),'UTC_end':end,'normal_PID':results[0]['actual_PID'],'optimized_PID':results[1]['actual_PID'],'tests_per_mode':32,'predecessor_counts':dict(counts),'free_bytes_snapshot':free,'native_calls':0}))
