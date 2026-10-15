#!/usr/bin/env python3
"""Authenticate an interrupted existing acceptance commit; never recreate it."""
from pathlib import Path
import importlib.util, json, os, signal, sys, time
A=Path(__file__).resolve().parents[1]; C=A.parents[2]
f=A/'native_post_assess_carryforward_v3_20261006/native_acceptance_actions_v4.py'
spec=importlib.util.spec_from_file_location('reviewed_native_actions',f)
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
def need(x,s): m.need(x,s)
def ap(p): return {'path':str(p.relative_to(A)),**m.pin(m.read(p,2*1024*1024))}
def read(p): return m.loads(m.read(p,2*1024*1024))
mode=sys.argv[1];gatepath=Path(sys.argv[2]);need(mode in ('inspect','publish'),'Explicit reconciliation mode')
need(dict(os.environ)==m.START_ENV and sys.flags.ignore_environment and sys.flags.no_site and sys.flags.dont_write_bytecode and sys.flags.safe_path,'Exact clean physical interpreter startup')
gate=read(gatepath); need(gatepath.is_relative_to(A) and gate['schema']=='pr110-existing-acceptance-reconciliation/v1' and gate['mode']==mode and gate['role']=='root' and gate['actual_review'] is True and gate['clearance'] is True and gate['required_findings']==[],'Explicit reviewed reconciliation decision')
need(m.datetime.timedelta(0)<=m.timestamp(m.now())-m.timestamp(gate['UTC'])<=m.datetime.timedelta(minutes=30),'Fresh reconciliation decision')
need(gate['program_pin']==ap(Path(__file__).resolve()) and gate['phase_program_pin']==ap(f),'Exact reconciliation and unchanged phase source')
old=A/'actual_action_commissions_20261006/acceptance_commit_ROOT_GATE.json'
need(gate['interrupted_action_gate_pin']==ap(old),'Exact interrupted action commission')
oldgate=read(old)
# Preserve the historical interrupted action gate; authenticate its static
# prerequisites through a freshly dated, dedicated in-memory copy on disk.
freshgate=A/'actual_action_inputs_20261006'/('reconciliation_'+mode+'_NATIVE_PREREQUISITES.json')
need(not freshgate.exists(),'Unique prerequisite record')
fresh={**oldgate,'UTC':gate['UTC'],'operation_label':'pr110_acceptance_reconcile_'+mode+'_20261006'}
m.save(freshgate,fresh)
_,packet,runtime,W,r,_=m.load_gate(freshgate,'acceptance_commit')
need(sys.executable==packet['runtime']['binaries']['python']['resolved_absolute_path'],'Exact physical interpreter')
root=read(A/'ROOT_ACTUAL_NATIVE_CANDIDATE_REVIEW_AUTHENTICATION_20261006.json')
need(root['native_candidate_actual_authenticated'] is True and root['required_findings']==[] and root['candidate_receipt_pin']==oldgate['candidate_receipt_pin'],'Original completed actual candidate root clearance')
if mode=='publish':
    ad=read(A/gate['repair_adversary_pin']['path'])
    need(ap(A/gate['repair_adversary_pin']['path'])==gate['repair_adversary_pin'] and ad['clearance'] is True and ad['actual_review'] is True and ad['required_findings']==[] and ad['reconciliation_program_pin']==ap(Path(__file__).resolve()),'Actual independent reconciliation source review')
    need(gate['preflight_receipt_pin']==ap(A/'actual_acceptance_reconciliation_20261006/inspect/RECEIPT.json'),'Exact successful read-only preflight')
    pre=read(A/gate['preflight_receipt_pin']['path']);need(pre['all_full_committed_bodies_reproduced'] is True and pre['remote_main']==packet['main_parent'] and pre['commit']==gate['existing_commit'],'Exact preflight state')
capture=m.Capture(A/'actual_acceptance_reconciliation_20261006'/mode)
def stopped(sig,frame):
    if m.SPAWN_CRITICAL: m.PENDING_SIGNAL=sig;return
    raise SystemExit('Actual reconciliation '+signal.Signals(sig).name)
signal.signal(signal.SIGTERM,stopped);signal.signal(signal.SIGINT,stopped)
m.save(capture.root/'START.json',{'UTC':m.now(),'actual_operator_PID':os.getpid(),'mode':mode,'gate_pin':ap(gatepath),'program_pin':ap(Path(__file__).resolve()),'no_recommit_or_reassess':True})
try:
    failure=A/'actual_acceptance_actions_20261006/pr110_acceptance_commit_20261006'
    outer=A/'actual_operations/root_actual_pr110_acceptance_commit_20261006'
    fail=read(failure/'FAILURE.json'); j=read(failure/'PROCESS_JOURNAL.json'); launches=read(failure/'PROCESS_LAUNCHES.json'); o=read(outer/'execution.json')
    need(fail['actual_operator_PID']==84526 and fail['error']=='SystemExit: Actual operator SIGTERM' and j['actual_operator_PID']==84526 and launches['actual_operator_PID']==84526,'Exact preserved interrupted action')
    need(o['child_PID']==84526 and o['exit_code']==1 and o['streams_fully_drained'] is False and o['termination_reason']=='outer_exception:RuntimeError' and o['cleanup_errors']==[{'action':'final_discovery','error':'Bounded real launch journal'}],'Honest incomplete outer record; journal-cap failure')
    need(len(j['records'])==131 and len(launches['launches'])==132 and launches['launches'][-1]['PID']==84786 and launches['launches'][-1]['state']=='launched_not_yet_reaped','Preserved incomplete final direct registration')
    for child in j['records']:
        need(child['exit_code']==0 and child['reaped'] and child['process_group_absence_confirmed'] and child['fully_drained'] and child['termination_reason'] is None and child['error'] is None,'All completed old children succeeded')
        for stream in child['streams'].values():
            need(m.pin(m.read(failure/stream['retained_file'],65536))==stream['retained'],'Full retained old child stream pin')
    need(not any('push' in child['argv'] for child in launches['launches']),'Interrupted action did not launch push')
    need(not (failure/'LOCAL_RECEIPT.json').exists() and not (failure/'RECEIPT.json').exists(),'No invented completed original acceptance receipt')
    ps=capture.run(['/bin/ps','-axo','pid=,ppid=,pgid='],C,m.START_ENV,deadline=2,stdout_cap=1024*1024)
    live=[tuple(map(int,line.split())) for line in ps.splitlines() if line.strip()]
    groups=set(o['recorded_PGIDs'])|{84526}|{x['PID'] for x in launches['launches']}
    need(all(m.group_absent(g) for g in groups) and not any(pid==84526 or ppid==84526 or pgid in groups for pid,ppid,pgid in live),'Fresh absence of all132 durable registrations and observed old groups')
    absence={'UTC':m.now(),'actual_operator_PID':os.getpid(),'recorded_groups':sorted(groups),'all_freshly_absent':True,'completed_old_children':131,'durable_old_registrations':132,'old_final_child_reap_historically_unconfirmed':True,'old_outer_full_stream_custody_claimed':False,'absence_scope':'Durable direct registrations and actually observed groups; no complete containment claim for unknown/reparented descendants.'}
    m.save(capture.root/'STOPPED_ACTION_FRESH_ABSENCE.json',absence)
    commit=gate['existing_commit'];need(commit=='f2cc75042ad93167c4126bfc1846fd09ac5c8325','Exact existing actual commit')
    need(m.git(capture,runtime,'symbolic-ref','--short','HEAD').strip()==b'main' and m.git(capture,runtime,'rev-parse','HEAD').decode().strip()==commit,'Own main is exact existing commit')
    remote=m.git(capture,runtime,'ls-remote',m.URL,'refs/heads/main').decode().split();need(remote==[packet['main_parent'],'refs/heads/main'],'No prior push; remote unchanged')
    need(not m.git(capture,runtime,'diff','--cached','--name-only','-z') and not m.git(capture,runtime,'diff','--name-only','--diff-filter=ACMRTUXB','-z'),'Empty index and no materialized drift')
    need(m.git(capture,runtime,'show','-s','--format=%P',commit).decode().split()==[packet['main_parent']],'Exact acceptance parent')
    need(m.git(capture,runtime,'show','-s','--format=%B',commit).decode().strip()==oldgate['commit_message'],'Exact acceptance message')
    exported=m.loads(m.audit(oldgate['export_receipt_pin']))
    need(exported['native_export_executed'] is True and exported['exported_paths']==r['affected_paths'],'Exact actual reviewed export')
    paths={x['path']:x['after'] for x in r['affected_paths']};paths[m.PREFIX+'NATIVE_ACCEPTANCE_RECEIPT.json']=m.pin(m.audit(oldgate['export_receipt_pin']))
    for entry in oldgate['additional_checkpoint_pins']:
        name=entry['path'];m.relpath(name);need(name.startswith(str(A.relative_to(C))+'/') and name not in paths,'Exact bounded extra audit scope');paths[name]={k:entry[k] for k in ('bytes','sha256')}
    need(len(paths)==337,'Full exact prior selection')
    changed={x.decode() for x in m.git(capture,runtime,'diff-tree','--no-commit-id','--name-only','-r','-z',commit).split(b'\0') if x}
    need(changed==set(paths),'Exact337 committed path delta')
    staged={x.decode() for x in m.read(failure/j['records'][9]['streams']['stdout']['retained_file'],65536).split(b'\0') if x}
    need(staged==changed,'Original actual staged selection reproduced')
    for name,expected in sorted(paths.items()):
        m.read(C/name,spec=expected,retain=False)
        need(m.pin(m.git(capture,runtime,'show',commit+':'+name))==expected,'Full existing committed body reproduction')
    tree=m.git(capture,runtime,'rev-parse',commit+'^{tree}').decode().strip();need(m.git(capture,runtime,'write-tree').decode().strip()==tree,'Complete existing index equals accepted tree')
    m.live_pr(capture,runtime,draft=True)
    result={'schema':'pr110-actual-main-acceptance-checkpoint/v1','UTC':m.now(),'actual_operator_PID':os.getpid(),'parent':packet['main_parent'],'commit':commit,'tree':tree,'pins':[{'path':n,**paths[n]} for n in sorted(paths)],'changed_paths':sorted(changed),'main_only':True,'remote_verified':False,'DOI':m.DOI,'tracker_range':m.RANGE,'packet_sha256':oldgate['packet_sha256'],'candidate_receipt_pin':oldgate['candidate_receipt_pin'],'merge_pending':True,'interrupted_original_action_preserved':True,'original_operator_PID':84526,'reconciliation_mode':mode,'all_full_committed_bodies_reproduced':True,'all132_durable_old_groups_freshly_absent':True,'old_outer_full_stream_custody_claimed':False,'remote_main':remote[0],'recommit_executed':False,'new_assess_calls':0,'reconciliation_program_pin':ap(Path(__file__).resolve())}
    m.save(capture.root/'LOCAL_RECEIPT.json',result)
    if mode=='publish':
        m.git(capture,runtime,'push','--force-with-lease=refs/heads/main:'+packet['main_parent'],m.URL,'HEAD:refs/heads/main',authenticated=True,deadline=60)
        need(m.git(capture,runtime,'ls-remote',m.URL,'refs/heads/main').decode().split()==[commit,'refs/heads/main'],'Actual single push readback')
        need(not m.git(capture,runtime,'diff','--cached','--name-only','-z'),'Actual postpush empty index')
        result.update({'UTC':m.now(),'remote_verified':True,'remote_main':commit,'single_existing_commit_push_executed':True})
    m.save(capture.root/'RECEIPT.json',result)
    print(json.dumps({k:result[k] for k in ('actual_operator_PID','commit','tree','remote_verified','reconciliation_mode','all_full_committed_bodies_reproduced')}))
except BaseException as error:
    m.save(capture.root/'FAILURE.json',{'UTC':m.now(),'actual_operator_PID':os.getpid(),'mode':mode,'error':type(error).__name__+': '+str(error)[:500],'do_not_blindly_repeat_mutations':True})
    raise
