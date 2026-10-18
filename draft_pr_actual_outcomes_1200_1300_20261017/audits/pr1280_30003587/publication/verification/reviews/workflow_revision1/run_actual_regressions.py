#!/usr/bin/env python3
"""Run the actual deployed offline workflow serially in three interpreter modes."""
from pathlib import Path
import datetime,hashlib,json,subprocess,sys
R=Path(__file__).resolve().parent;A=R.parents[1];P=A/'publication';local=R/'runs';local.mkdir(exist_ok=True)
def need(value,message):
    if not value:raise RuntimeError(message)
def binding(path):return {'path':path.relative_to(R).as_posix(),'bytes':path.stat().st_size,'sha256':hashlib.sha256(path.read_bytes()).hexdigest()}
records=[];first=None
for name,flags in [('normal',[]),('O',['-O']),('OO',['-OO'])]:
    started=datetime.datetime.now(datetime.timezone.utc).isoformat();out=local/('actual_workflow_'+name+'_stdout.json');err=local/('actual_workflow_'+name+'_stderr.txt')
    with out.open('w') as stdout,err.open('w') as stderr:run=subprocess.run([sys.executable,'-B',*flags,str(P/'workflow_regression.py'),'--worker'],stdout=stdout,stderr=stderr)
    need(run.returncode==0,'Actual '+name+' workflow failed; see '+str(err))
    result=json.loads(out.read_text());need(result['status']=='PASS','Actual workflow not PASS')
    if first is None:first=result
    else:need(result==first,'Actual workflow results differ by optimization')
    record={'mode':name,'flags':flags,'started_at_utc':started,'completed_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'returncode':run.returncode,'stdout':binding(out),'stderr':binding(err),'status':result['status']};records.append(record)
    (local/'ACTUAL_WORKFLOW_RUN_PROGRESS.json').write_text(json.dumps({'runs':records},indent=2)+'\n');print(name+' PASS',flush=True)
source_paths=[P/name for name in ['prepare_package.py','build_package.py','compile_note.py','verification/verify.py','append_tracker.py','update_pr_publication.py','check_public_downloads.py','workflow_regression.py']]+[A/'_local/ready_and_merge.py',A.parents[1]/'publication_coordinators/pr1280.py',A.parents[1]/'publication_coordinators/verify_pr1280_merge.py']
ready=first['ready_and_expected_head_merge']
receipt={'schema':'math-pr1280-repaired-workflow-replay-v1','at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS','all_modes_identical':True,'runs':records,'source_bindings':[{'path':str(path),'bytes':path.stat().st_size,'sha256':hashlib.sha256(path.read_bytes()).hexdigest()} for path in source_paths],'counts_per_mode':{'identity_action_cases':len(first['identity_action_matrix']['cases']),'postmerge_cases':len(first['postmerge_complete_main']['cases']),'deposit_coordinator_cases':len(first['deposit_coordinator_actual_kit_mocked_clients']),'ready_negative_controls':len(ready['negative_controls']),'ready_positive_controls':len(ready['positive_controls']),'ready_blob_corruptions':ready['all_fourteen_commit_blobs_corrupted_separately']},'scope':first['scope'],'ready_scope':'Actual deployed guarded main invokes the full operative updater under read-only facade. Every Git/service operation in these tests is mocked; this receipt grants no real release clearance.'}
(R/'ACTUAL_WORKFLOW_REPLAY.json').write_text(json.dumps(receipt,indent=2)+'\n');print(json.dumps(receipt,indent=2))
