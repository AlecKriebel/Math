#!/usr/bin/env python3
"""Authenticate the completed native assessment and its safely stopped scope check."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,importlib.util,os,subprocess
A=Path(__file__).resolve().parents[1];C=A.parents[2]
W=A/'native_execution_programs_v1/workspaces/candidate_d9eb646c1dd70e89'
O=A/'actual_operations/root_actual_private_native_candidate_20261006'
def need(x,m):
 if not x:raise RuntimeError(m)
def hp(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def file(p):return {'path':str(p.relative_to(A)),**hp(p.read_bytes())}
def obj(p):return json.loads(p.read_bytes())
def stamp(x):return datetime.fromisoformat(x)
def module(p):
 s=importlib.util.spec_from_file_location('root_failed_run_protocol',p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
p=module(A/'native_integration_preparation_20261006/protocol.py')
packet=obj(W/'EXECUTION_INPUTS.json');packet_sha=hp((W/'EXECUTION_INPUTS.json').read_bytes())['sha256']
outer=obj(O/'execution.json');launch=obj(O/'LAUNCH.json');journal=obj(W/'PROCESS_JOURNAL.json');launches=obj(W/'PROCESS_LAUNCHES.json')
result=obj(W/'WORKER_RESULT.json');control=obj(W/'WORKER_CONTROL.json');failure=obj(W/'FAILURE.json')
need(outer['child_PID']==journal['operator_PID']==failure['operator_PID']==23224,'Actual runner identity')
need(launch['child_PID']==outer['child_PID'] and launch['argv']==outer['argv'] and launch['cwd']==outer['cwd'],'Actual launch correspondence')
need(outer['packet_sha256']==packet_sha==failure['packet_sha256']==result['packet_sha256'],'Actual packet identity')
need(outer['exit_code']==1 and outer['reaped'] and outer['all_recorded_groups_absence_confirmed'] and outer['streams_fully_drained'] and outer['termination_reason'] is None and outer['cleanup_errors']==[],'Safely stopped actual outer')
for stream in ('stdout','stderr'):
 s=outer[stream];b=(O/s['path']).read_bytes();need(hp(b)=={k:s[k] for k in ('bytes','sha256')} and len(b)==s['observed_bytes'] and hp(b)['sha256']==s['observed_sha256'],'Full actual outer raw stream')
need(b'Target assessment changed beyond reviewed metadata' in (O/'stderr.bin').read_bytes(),'Actual failure text')
probes=outer['actual_ancestry_probes'];witness=False
for i,e in enumerate(probes):
 need(e['argv']==['/bin/ps','-axo','pid=,ppid=,pgid='] and e['exit_code']==0 and e['reaped'] and e['streams_fully_drained'] and e['termination_reason'] is None,'Actual ancestry process')
 for stream in ('stdout','stderr'):
  s=e[stream];b=(O/s['path']).read_bytes();need(hp(b)=={k:s[k] for k in ('bytes','sha256')} and s['observed_bytes']==len(b) and s['observed_sha256']==hp(b)['sha256'],'Full ancestry raw stream')
 witness|=23360 in e['descendant_PIDs']
need(witness,'Actual observed worker descendant')
need(len(journal['processes'])==17 and len(launches['launches'])==17,'Complete inner process records')
before={};replays=[]
for i,e in enumerate(journal['processes']):
 need(e['actual_process_record'] and not e['synthetic_fixture_only'] and e['exit_code']==0 and e['reaped'] and e['process_group_absence_confirmed'] and e['streams_fully_drained'] and e['termination_reason'] is None and e['cleanup_errors']==[],'Actual clean completed native child')
 need(launches['launches'][i]['PID']==e['PID'],'Prewait journal actual PID')
 for stream,s in e['streams'].items():
  body=(W/s['retained_path']).read_bytes();need(hp(body)=={k:s[k] for k in ('bytes','sha256')} and len(body)==min(s['observed_bytes'],4096),'Honest native retained prefix')
 if i in range(4,16):
  command=e['argv'];start=datetime.now(timezone.utc).isoformat();child=subprocess.Popen(command,cwd=e['cwd'],env={'PATH':'/usr/bin:/bin','LANG':'C','LC_ALL':'C','TZ':'UTC','__CF_USER_TEXT_ENCODING':'0x1F5:0x0:0x0','GIT_CONFIG_NOSYSTEM':'1','GIT_CONFIG_GLOBAL':'/dev/null'},stdout=subprocess.PIPE,stderr=subprocess.PIPE)
  body,err=child.communicate(timeout=30);end=datetime.now(timezone.utc).isoformat();s=e['streams']['stdout'];need(child.returncode==0 and not err and hp(body)=={'bytes':s['observed_bytes'],'sha256':s['observed_sha256']} and body[:4096]==(W/s['retained_path']).read_bytes(),'Full immutable Git replay')
  name=command[-1].split(':',1)[1].rsplit('/',1)[1];need(hp(body)=={k:packet['native_baseline'][name][k] for k in ('bytes','sha256')},'Native committed full preimage')
  before[name]=body;replays.append({'PID':child.pid,'argv':command,'cwd':e['cwd'],'UTC_start':start,'UTC_end':end,'exit_code':child.returncode,'reaped':True,'stdout':hp(body),'stderr':hp(err),'full_body_custody':command[-1]})
worker=journal['processes'][-1]
need(worker['PID']==result['actual_worker_PID']==23360 and result['native_assess_completed'] and result['native_assess_call_attempted'] and result['outcome']=='success','Exactly one successful actual assessment')
need(result['control_sha256']==hp((W/'WORKER_CONTROL.json').read_bytes())['sha256'] and p.equal(result['validated_control'],control),'Actual exact control')
need(stamp(worker['UTC_start'])<=stamp(result['UTC_start'])<=stamp(result['UTC_end'])<=stamp(worker['UTC_end']),'Actual worker chronology')
need(result['limits']['enforced']=={'RLIMIT_CPU':[90,90],'RLIMIT_FSIZE':[33554432,33554432],'RLIMIT_NOFILE':[64,64]} and result['limits']['memory']['hard_memory_limit_claimed'] is False,'Actual OS resource readbacks')
after={}
for name,spec in result['output_pins'].items():
 body=(W/'private_native_backend'/name).read_bytes();need(hp(body)==spec,'All actual native output bodies');after[name]=body
old=p.loads(before['assessments.json']);new=p.loads(after['assessments.json']);overlay=packet['assessment_overlay'];expected={**old[p.K],**overlay}
need('clear_holds' not in expected and type(new[p.K]['clear_holds']) is dict and new[p.K]['clear_holds']=={},'Only empty automatically generated clearance map')
need(set(new[p.K])==set(expected)|{'reviewed_at','clear_holds'} and p.equal({k:v for k,v in new[p.K].items() if k not in ('reviewed_at','clear_holds')},expected),'Exact target diagnostic delta')
try:p.validate_assessments(old,new,overlay)
except ValueError as e:need(str(e)=='Target assessment changed beyond reviewed metadata','Original guard reproduces exact failure')
else:raise RuntimeError('Original scope failure not reproduced')
original_validator=p.validate_assessments
def corrected(a,b,o):
 target=b[p.K];need(type(target.get('clear_holds')) is dict and target['clear_holds']=={} and 'clear_holds' not in a[p.K] and 'clear_holds' not in o,'Narrow empty-default normalization only')
 cleaned={**b,p.K:{k:v for k,v in target.items() if k!='clear_holds'}};original_validator(a,cleaned,o)
p.validate_assessments=corrected
event=p.imported_baseline(packet['import_UTC'],p.ORIGINAL_ROW_SHA,p.ORIGINAL_LOG_SHA)
scoped,drift=p.scoped_outputs(before,after,overlay,event,packet['campaign_note'],'10.5281/zenodo.23191247')
need(failure['candidate_must_not_be_exported'] is True and failure['native_export_executed'] is False and not (W/'CANDIDATE_RECEIPT.json').exists() and not (W/'offer').exists(),'Failed workspace remains nonexportable')
out={'schema':'pr110-root-failed-native-run-authentication/v1','UTC':datetime.now(timezone.utc).isoformat(),'actual_root_PID':os.getpid(),'packet_sha256':packet_sha,'actual_runner_PID':23224,'actual_worker_PID':23360,'actual_assess_once_success_authenticated':True,'safe_scope_stop_authenticated':True,'all12_actual_output_fullbodies_authenticated':True,'all17_children_reaped_and_groups_absent':True,'all26_ancestry_full_raw_streams_authenticated':len(probes)==26,'Git_full_preimage_replays':replays,'target_delta_only_reviewed_at_and_empty_clear_holds':True,'narrow_correction_pure_scope_replay_passed':True,'unrelated_projection_drift_restored':drift,'proposed_derived_pins':{n:hp(b) for n,b in scoped.items()},'memory_advisory_bytes':result['limits']['memory']['requested_advisory_bytes'],'observed_maximum_RSS_bytes':result['resource_usage']['maximum_RSS'],'memory_advisory_exceeded':result['resource_usage']['maximum_RSS']>result['limits']['memory']['requested_advisory_bytes'],'hard_memory_limit_claimed':False,'native_export_executed':False,'actual_continuation_not_yet_executed':True,'failed_workspace_remains_nonexportable':True,'checked_artifacts':[file(W/n) for n in ('EXECUTION_INPUTS.json','WORKER_CONTROL.json','WORKER_RESULT.json','PROCESS_JOURNAL.json','PROCESS_LAUNCHES.json','FAILURE.json')]+[file(O/n) for n in ('LAUNCH.json','execution.json','stdout.bin','stderr.bin')]}
(A/'ROOT_FAILED_NATIVE_RUN_AUTHENTICATION_20261006.json').write_bytes(p.canonical(out))
print(json.dumps({'actual_worker_PID':23360,'native_assess_actual_success':True,'scope_error_only_empty_default_clear_holds':True,'all_derived_scope_replay_passed':True,'memory_advisory_exceeded':out['memory_advisory_exceeded'],'actual_live_export':False}))
