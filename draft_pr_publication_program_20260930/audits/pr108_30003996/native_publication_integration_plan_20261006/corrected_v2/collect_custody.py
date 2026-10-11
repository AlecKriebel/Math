"""Own-folder custody collector: scoped read-only Git + offline test processes only."""
import sys
sys.dont_write_bytecode=True
from pathlib import Path
import hashlib,json,os,shutil
from bounded_process import BoundedRunner,now
import v2_guards as g
D=Path(__file__).resolve().parent;V1=D.parent;A=V1.parent;C=A.parents[2];R=Path('/Users/alec/Documents/Math')
POLICY={'max_process_count':8,'retain_bytes_per_stream':4096,'max_stdout_bytes':65536,
        'max_stderr_bytes':65536,'deadline_seconds':30,'terminate_grace_seconds':1}

def main():
    root=D/'execution_receipts';root.mkdir(exist_ok=False)
    runner=BoundedRunner(root,C,POLICY);began=now()
    reads=[R/'AGENTS.md',R/'unsolved_math_prioritization/AGENTS.md',R/'unsolved_math_prioritization/README.md',
        A/'native_helper_static_adversary_20261006/REPORT.md',A/'native_helper_static_adversary_20261006/VERDICT.json',
        A/'native_helper_static_adversary_20261006/offline_adversary.py',A/'native_helper_static_adversary_20261006/RESULTS_NORMAL.json',
        A/'native_helper_static_adversary_20261006/RESULTS_OPTIMIZED.json',A/'native_helper_static_adversary_20261006/SOURCE_READ_SCOPE.json',
        A/'publication_ready_package_v2/PACKAGE_MANIFEST.json',A/'ROOT_PRIORITY_GATE_20261006.json',A/'ROOT_PUBLICATION_TRACKER_HEADER_AUTHENTICATION_20261006.json',
        A/'operational_cli_reference_relocation_20261006/private_generated/skills/gws-shared/SKILL.md',
        A/'actual_operations/tracker_append_schema_read/execution.json',A/'actual_operations/tracker_append_schema_read/stdout.bin',
        Path('/Users/alec/.agents/skills/gws-sheets/SKILL.md'),Path('/Users/alec/.agents/skills/gws-sheets-read/SKILL.md'),
        Path('/Users/alec/.agents/skills/gws-sheets-append/SKILL.md'),V1/'OUTPUT_MANIFEST.json',V1/'SEAL_RECEIPT.json']
    original=A/'original_source_authentication_20261006'
    reads += [original/x for x in ['ORIGINAL_BLOB_MANIFEST.json','QUEUE_STATUS_PROJECTION.json','SOURCEPAIR_AUTHENTICATION.json','SELECTED_IMPORTED_PRIOR_REPORT.json']]
    reads += sorted((original/'original_attempt').rglob('*'))
    reads += [D/x for x in g.PROGRAMS+['test_v2_guards.py']]
    pins=[]
    for path in reads:
        if path.is_dir():continue
        require_regular=g.regular(path);g.require(require_regular.st_size<=512*1024,'Custody read cap')
        data=path.read_bytes();pins.append({'path':str(path),'bytes':len(data),'sha256':g.sha(data)})
    (D/'READ_SCOPE_MANIFEST.json').write_bytes(g.canonical({'schema':'pr108-v2-actual-read-scope/v1','UTC_start':began,'UTC_end':now(),
        'actual_reader_PID':os.getpid(),'read_mode':'regular local bytes; no service operations','files':pins,
        'large_SQL_or_raw_source_bodies_copied':False}))
    branch=runner.run(['/usr/bin/git','symbolic-ref','--short','HEAD'])[0].decode().strip()
    head=runner.run(['/usr/bin/git','rev-parse','HEAD'])[0].decode().strip()
    diff=runner.run(['/usr/bin/git','diff','--name-only','1026e5ff3cc3ff5b39501bd1f7218e773730c51a',head,'--','unsolved_math_prioritization/'])[0]
    native_source=runner.run(['/usr/bin/git','show',head+':unsolved_math_prioritization/queue.py'])[0]
    for mode,args in [('NORMAL',[]),('OPTIMIZED',['-O'])]:
        out,err,record=runner.run([sys.executable,'-B',*args,str(D/'test_v2_guards.py')],fixture=True)
        g.require(record['exit_code']==0 and b'Ran 23 tests' in err and err.rstrip().endswith(b'OK'),'Offline test result')
        (D/('TEST_RESULTS_'+mode+'.json')).write_bytes(g.canonical({'schema':'pr108-v2-offline-fixture-result/v1','mode':mode,
            'actual_test_process_PID':record['PID'],'UTC_start':record['UTC_start'],'UTC_end':record['UTC_end'],
            'exit_code':record['exit_code'],'tests':23,'passed':23,'fixtures_only':True,
            'actual_native_prepare_executions':0,'actual_native_assess_executions':0,'actual_service_write_executions':0,
            'test_source_sha256':g.sha((D/'test_v2_guards.py').read_bytes()),'stdout_sha256':g.sha(out),'stderr_sha256':g.sha(err)}))
    sealed=g.loads((V1/'OUTPUT_MANIFEST.json').read_bytes());original_pins=g.loads((D/'V1_UNCHANGED_INPUT_PINS.json').read_bytes())
    # The V1 manifest predates V2; verify every named V1 file plus its two seal files.
    for pin in original_pins['V1_file_pins']:
        path=V1/pin['path'];g.require(path.is_relative_to(V1) and not path.is_relative_to(D),'V1 verification scope')
        data=path.read_bytes();g.require(len(data)==pin['bytes'] and g.sha(data)==pin['sha256'],'Sealed V1 changed: '+str(path))
    (D/'CONTEXT_RECEIPT.json').write_bytes(g.canonical({'schema':'pr108-v2-actual-read-context/v1','UTC':now(),'actual_operator_PID':os.getpid(),
        'branch':branch,'current_main_HEAD_observed':head,'native_revision_comparison':'1026e5ff3cc3ff5b39501bd1f7218e773730c51a',
        'native_diff_names_bytes':len(diff),'native_diff_names_sha256':g.sha(diff),'native_diff_empty':not diff,
        'native_queue_source_sha256_observed':g.sha(native_source),'observed_free_bytes':shutil.disk_usage(D).free,
        'V1_verified_unchanged_file_count':len(original_pins['V1_file_pins']),'V1_unchanged':True,
        'context_is_future_permission':False,'new_central_proof_search_turns':0,'actual_native_execution_count':0,
        'actual_publication_or_Sheet_service_calls':0,'all_writes_confined_to_corrected_v2':True}))
    print(json.dumps({'HEAD_observed':head,'native_diff_empty':not diff,'V1_verified_unchanged':len(original_pins['V1_file_pins']),'tests_normal_and_optimized':23}))
if __name__=='__main__':main()
