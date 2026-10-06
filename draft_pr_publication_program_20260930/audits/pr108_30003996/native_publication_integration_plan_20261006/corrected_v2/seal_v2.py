"""Seal only current V2 artifacts; scoped read-only Git and no native preparation."""
import sys
sys.dont_write_bytecode=True
from pathlib import Path
import datetime,json,os,shutil
import v2_guards as g
from bounded_process import BoundedRunner
D=Path(__file__).resolve().parent;V1=D.parent;A=V1.parent;C=A.parents[2]
def pin(path):
    data=path.read_bytes();return {'path':str(path.relative_to(D)),'bytes':len(data),'sha256':g.sha(data)}
def main():
    now=datetime.datetime.now(datetime.timezone.utc).isoformat();root=D/'seal_receipts';root.mkdir(exist_ok=False)
    policy={'max_process_count':4,'retain_bytes_per_stream':4096,'max_stdout_bytes':8192,'max_stderr_bytes':8192,'deadline_seconds':20,'terminate_grace_seconds':1}
    runner=BoundedRunner(root,C,policy)
    head=runner.run(['/usr/bin/git','rev-parse','HEAD'])[0].decode().strip()
    branch=runner.run(['/usr/bin/git','symbolic-ref','--short','HEAD'])[0].decode().strip()
    diff=runner.run(['/usr/bin/git','diff','--name-only','1026e5ff3cc3ff5b39501bd1f7218e773730c51a',head,'--','unsolved_math_prioritization/'])[0]
    g.require(branch=='main' and not diff,'Read-only native context changed; report before sealing')
    for path in D.glob('*.py'):compile(path.read_bytes(),str(path),'exec')
    original=g.loads((D/'V1_UNCHANGED_INPUT_PINS.json').read_bytes())
    for spec in original['V1_file_pins']:
        path=V1/g.relative(spec['path']);data=path.read_bytes()
        g.require(len(data)==spec['bytes'] and g.sha(data)==spec['sha256'],'Sealed V1 changed')
    for mode in ['NORMAL','OPTIMIZED']:
        result=g.loads((D/('TEST_RESULTS_'+mode+'.json')).read_bytes())
        g.require(result['tests']==23 and result['passed']==23 and result['exit_code']==0 and result['fixtures_only'] is True and
            result['test_source_sha256']==g.sha((D/'test_v2_guards.py').read_bytes()),'Current test custody mismatch')
    for name in ['CONFIG_TEMPLATE_DO_NOT_RUN.json','EXECUTION_INPUTS_TEMPLATE_DO_NOT_RUN.json']:
        obj=g.loads((D/name).read_bytes())
        try:
            if name.startswith('CONFIG'):g.validate_thin_config(obj)
            else:g.validate_execution_manifest(obj,(D/name).read_bytes())
        except ValueError:pass
        else:raise ValueError('Template must reject')
    ledger=g.loads((D/'FIELD_SPECIFIC_CORRECTION_LEDGER.json').read_bytes())
    g.require([x['finding'] for x in ledger['corrections']]==['F01','F02','F03','F04','F05','F06'],'Repair coverage')
    for spec in ledger['program_pins']:
        path=C/spec['path'];data=path.read_bytes();g.require(path.parent==D and len(data)==spec['bytes'] and g.sha(data)==spec['sha256'],'Current ledger program pin mismatch')
    (D/'TASK_COMPLETION.json').write_bytes(g.canonical({'schema':'pr108-native-integration-draft-v2-task-completion/v1','UTC':now,'actual_operator_PID':os.getpid(),
        'assigned_nonexecuted_draft_complete':True,'draft_completion_percent':100,'fresh_independent_V2_adversary_review_pending':True,
        'actual_future_execution_configuration_prepared':False,'actual_prepare_assess_export_install_executions':0,'new_central_proof_search_turns':0,
        'actual_Git_index_branch_remote_service_mutations':0,'actual_external_contact_or_outreach_preparation':0,
        'V1_files_verified_unchanged':len(original['V1_file_pins']),'all_six_repairs_addressed_in_draft':True,
        'offline_normal_tests':23,'offline_optimized_tests':23,'Darwin_hard_memory_limit_certified':False,
        'observed_main_HEAD':head,'native_diff_from_1026_empty':True,'observed_free_bytes':shutil.disk_usage(D).free,
        'actual_preexecution_and_native_runtime_claims_from_fixtures':False}))
    with (D/'RESEARCH_LOG.md').open('a') as stream:
        stream.write('\n'+now+' — Own-folder draft sealed,100% of assigned nonexecuted planning/repair delivery. Parent fresh independent V2 adversary and all actual publication/config/native gates remain pending. Native executions0, proof-search turns0. All81 V1 files verified unchanged at seal. Current readonly HEAD '+head+'; native diff empty; actual seal PID '+str(os.getpid())+'.\n')
    excluded={'OUTPUT_MANIFEST.json','SEAL_RECEIPT.json'}
    files=[]
    for path in sorted(D.rglob('*')):
        g.require(not path.is_symlink(),'V2 symlink')
        if path.is_file() and path.name not in excluded:files.append(pin(path))
    document={'schema':'pr108-v2-output-byte-manifest/v1','UTC':now,'actual_sealer_PID':os.getpid(),'root':str(D),
        'files':files,'file_count':len(files),'total_bytes':sum(x['bytes'] for x in files),'excludes':['OUTPUT_MANIFEST.json','SEAL_RECEIPT.json']}
    data=g.canonical(document);(D/'OUTPUT_MANIFEST.json').write_bytes(data)
    for spec in files:
        body=(D/spec['path']).read_bytes();g.require(len(body)==spec['bytes'] and g.sha(body)==spec['sha256'],'Seal readback mismatch')
    seal={'schema':'pr108-corrected-v2-seal/v1','UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'actual_sealer_PID':os.getpid(),
        'output_manifest':pin(D/'OUTPUT_MANIFEST.json'),'all_manifest_readbacks_verified':True,'file_count':len(files),'total_bytes':document['total_bytes'],
        'V1_file_count_verified_unchanged':81,'V1_manifest_sha256':g.sha((V1/'OUTPUT_MANIFEST.json').read_bytes()),
        'program_sha256':{name:g.sha((D/name).read_bytes()) for name in g.PROGRAMS},
        'actual_native_execution_count':0,'new_central_proof_search_turns':0,'fresh_independent_V2_adversary_review_pending':True}
    (D/'SEAL_RECEIPT.json').write_bytes(g.canonical(seal));print(json.dumps(seal))
if __name__=='__main__':main()
