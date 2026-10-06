#!/usr/bin/env python3
"""Main-only scoped metadata checkpoint after actual PR110 merged readback."""
from pathlib import Path
import importlib.util, os, signal, sys
A=Path(__file__).resolve().parents[1];C=A.parents[2]
phase=A/'native_post_assess_carryforward_v3_20261006/native_acceptance_actions_v4.py'
spec=importlib.util.spec_from_file_location('reviewed_phase',phase);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
def need(v,s):m.need(v,s)
need(dict(os.environ)==m.START_ENV and sys.flags.ignore_environment and sys.flags.no_site and sys.flags.dont_write_bytecode and sys.flags.safe_path,'Exact clean startup')
gatepath=Path(sys.argv[1]);gate=m.loads(m.read(gatepath,2*1024*1024))
need(gatepath.is_relative_to(A) and gate['schema']=='pr110-final-scoped-checkpoint/v1' and gate['role']=='root' and gate['actual_review'] is True and gate['clearance'] is True and gate['required_findings']==[],'Actual explicit root checkpoint decision')
need(m.datetime.timedelta(0)<=m.timestamp(m.now())-m.timestamp(gate['UTC'])<=m.datetime.timedelta(minutes=30),'Fresh checkpoint decision')
need(gate['program_pin']=={'bytes':len(Path(__file__).read_bytes()),'sha256':m.pin(Path(__file__).read_bytes())['sha256']},'Exact checkpoint source')
packet=m.loads(m.read(A/'native_actual_input_preparation_20261006/root_fresh_native_preflight_20261006/EXECUTION_INPUTS.json',512*1024));runtime=packet['runtime'];m.validate_runtime(runtime)
merge=m.loads(m.audit(gate['actual_merge_receipt_pin']))
need(merge['native_acceptance_and_merge_complete'] is True and merge['GitHub_MERGED_confirmed'] is True and merge['remote_push_complete'] is True and merge['tree_equality_verified'] is True and merge['merge_commit']==gate['expected_main'],'Actual exact-tree merged acceptance before metadata checkpoint')
capture=m.Capture(A/'actual_final_checkpoint_v2_20261006')
def stopped(sig,frame):
    if m.SPAWN_CRITICAL:m.PENDING_SIGNAL=sig;return
    raise SystemExit('Actual final checkpoint '+signal.Signals(sig).name)
signal.signal(signal.SIGTERM,stopped);signal.signal(signal.SIGINT,stopped)
m.save(capture.root/'START.json',{'UTC':m.now(),'actual_operator_PID':os.getpid(),'gate_pin':m.pin(m.read(gatepath,2*1024*1024))})
try:
    parent=gate['expected_main'];m.main_preflight(capture,runtime,parent)
    live=m.live_pr(capture,runtime,state='MERGED');need(live['mergeCommit']['oid']==merge['merge_commit'] and live['mergedAt']==merge['mergedAt'],'Actual GitHub merge metadata')
    paths={}
    global_paths={str((A.parents[1]/n).relative_to(C)) for n in ('CURRENT_PROGRESS.json','RESEARCH_LOG.md')}
    need(isinstance(gate['pins'],list) and 0<len(gate['pins'])<=128,'Bounded explicit final checkpoint selection')
    for row in gate['pins']:
        m.relpath(row['path']);n=row['path'];need(n not in paths and (n in global_paths or n.startswith(str(A.relative_to(C))+'/')),'Final dedicated audit/global progress scope')
        expected={k:row[k] for k in ('bytes','sha256')};m.read(C/n,spec=expected,retain=False);paths[n]=expected
    changed={x.decode() for x in m.git(capture,runtime,'diff','--name-only','--diff-filter=ACMRTUXB','-z').split(b'\0') if x};need(changed<=set(paths),'No foreign materialized edits')
    names=sorted(paths);need(sum(len(n)+1 for n in names)<=65536,'Bounded exact add argv')
    m.git(capture,runtime,'add','-f','--',*names)
    staged={x.decode() for x in m.git(capture,runtime,'diff','--cached','--name-only','-z').split(b'\0') if x};need(staged and staged<=set(paths),'Exact selected stage scope')
    need(not m.git(capture,runtime,'diff','--cached','--name-only','--diff-filter=D','-z'),'No deletions')
    message='Record PR110 publication, exact-tree merge, and completed audit'
    need(gate['commit_message']==message,'Exact checkpoint message')
    m.git(capture,runtime,'-c','user.name='+m.AUTHOR['name'],'-c','user.email='+m.AUTHOR['email'],'commit','-m',message,deadline=60)
    commit=m.git(capture,runtime,'rev-parse','HEAD').decode().strip();need(m.git(capture,runtime,'show','-s','--format=%P',commit).decode().split()==[parent],'Exact single checkpoint parent')
    actual={x.decode() for x in m.git(capture,runtime,'diff-tree','--no-commit-id','--name-only','-r','-z',commit).split(b'\0') if x};need(actual==staged,'Exact final committed paths')
    for n,expected in paths.items():need(m.pin(m.git(capture,runtime,'show',commit+':'+n))==expected,'Full final committed bytes')
    result={'schema':'pr110-actual-final-metadata-checkpoint/v1','UTC':m.now(),'actual_operator_PID':os.getpid(),'parent':parent,'commit':commit,'changed_paths':sorted(actual),'pins':[{'path':n,**paths[n]} for n in names],'remote_verified':False,'main_only':True,'primary_checkout_mutated':False,'DOI':m.DOI,'tracker_range':m.RANGE,'completed_PRs':18,'dated_eligible_total':99,'workflow_estimate_percent':18/99*100,'persistent_goal_complete':False,'writer_release_pending':True}
    m.save(capture.root/'LOCAL_RECEIPT.json',result)
    m.git(capture,runtime,'push','--force-with-lease=refs/heads/main:'+parent,m.URL,'HEAD:refs/heads/main',authenticated=True,deadline=60)
    need(m.git(capture,runtime,'ls-remote',m.URL,'refs/heads/main').decode().split()==[commit,'refs/heads/main'],'Final metadata remote readback')
    need(not m.git(capture,runtime,'diff','--cached','--name-only','-z') and not m.git(capture,runtime,'diff','--name-only','--diff-filter=ACMRTUXB','-z'),'Final metadata index and materialized state clean')
    result.update({'UTC':m.now(),'remote_verified':True});m.save(capture.root/'RECEIPT.json',result)
    print(m.json.dumps({k:result[k] for k in ('actual_operator_PID','parent','commit','remote_verified','completed_PRs','persistent_goal_complete')}))
except BaseException as error:
    m.save(capture.root/'FAILURE.json',{'UTC':m.now(),'actual_operator_PID':os.getpid(),'error':type(error).__name__+': '+str(error)[:500],'do_not_blindly_repeat_mutations':True});raise
