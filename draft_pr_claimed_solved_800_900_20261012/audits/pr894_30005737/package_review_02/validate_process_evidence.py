from pathlib import Path
import datetime,hashlib,json
R=Path(__file__).resolve().parent;P=R/'private_tmp';seen=set();processes=[];replays=[]
def ph(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def dt(s):return datetime.datetime.fromisoformat(s)
def check(base,outer=False):
 m=json.loads(Path(str(base)+'.json').read_bytes())
 for k in ['stdout','stderr']:assert ph(Path(str(base)+'.'+k+'.bin').read_bytes())==m[k]
 assert type(m['pid']) is int and m['pid']>0 and m['pid'] not in seen;seen.add(m['pid'])
 assert type(m['returncode']) is int and dt(m['started_utc'])<=dt(m['ended_utc']) and m['elapsed_monotonic_ns']>0
 if 'launched_utc' in m:assert dt(m['started_utc'])<=dt(m['launched_utc'])<=dt(m['ended_utc'])
 assert not m.get('timeout',False);processes.append({'label':base.relative_to(P).as_posix(),'pid':m['pid'],'returncode':m['returncode'],'started_utc':m['started_utc'],'ended_utc':m['ended_utc'],'stdout':m['stdout'],'stderr':m['stderr']});return m
for name in ['current_normal','current_O','source_only','independent_math','boundaries_run']:
 m=check(P/name);assert m['returncode']==0
for label in ['verify_only','wrong_pin','verify_only_receipt','double_optimization','missing_no_site','hostile_capability','hostile_resistance']:
 m=check(P/'boundaries'/label);assert (m['returncode']==0)==(label in ['verify_only','hostile_capability','hostile_resistance'])
source=json.loads((R.parent/'SOURCE_MANIFEST.json').read_bytes())
for folder,mode in [(P/'replay_normal',0),(P/'replay_O',1),(P/'boundaries/resisted_receipts',0)]:
 wrapper=check(folder/'root-wrapper');assert wrapper['returncode']==0 and wrapper['stderr']['bytes']==0
 result=json.loads((folder/'root-wrapper.stdout.bin').read_bytes());assert result['root_flags']=={'optimize':mode,'isolated':1,'no_site':1,'dont_write_bytecode':1,'ignore_environment':1,'safe_path':True};assert result['root_compile_optimize']==mode
 events=result['events'];assert [e['kind'] for e in events]==['positive','positive','semantic_negative','require_false','corrupt','semantic_negative','require_false','corrupt']
 for i,e in enumerate(events):
  stem=folder/'processes'/('child-%02d'%i);cm=check(stem);assert cm==e['process'];flags=json.loads(Path(str(stem)+'.flags.json').read_bytes());assert flags==e['measured_flags']=={'optimize':[0,1,0,0,0,1,1,1][i],'isolated':1,'no_site':1,'dont_write_bytecode':1,'ignore_environment':1,'safe_path':True};assert (cm['returncode']==0)==(e['kind']=='positive');assert e['original_execution_began']==(e['kind']!='corrupt');assert dt(wrapper['started_utc'])<=dt(cm['started_utc'])<=dt(cm['ended_utc'])<=dt(wrapper['ended_utc'])
  stderr=Path(str(stem)+'.stderr.bin').read_bytes()
  if e['kind']=='semantic_negative':assert b'RuntimeError: semantic_negative: PA2' in stderr
  if e['kind']=='require_false':assert b'RuntimeError: explicit_false_control' in stderr
  if e['kind']=='corrupt':assert b'CORRUPT_REJECTED_BEFORE_EXECUTION' in stderr
 root=json.loads((folder/'processes/original-root.execution.json').read_bytes());assert root['measured_flags']==result['root_flags'] and root['compile_optimize']==mode and root['exception_type'] is None
 for k in ['stdout','stderr']:assert ph((folder/'processes'/('original-root.'+k+'.bin')).read_bytes())==root[k]
 for row in source['files']:assert ph((folder/'frozen'/row['path']).read_bytes())=={k:row[k] for k in ['bytes','sha256']}
 replays.append({'receipt_label':folder.relative_to(P).as_posix(),'wrapper_pid':wrapper['pid'],'wrapper_optimization':mode,'actual_replay_processes':9,'actual_children':8,'positives':2,'real_negative_controls':6,'all18_unchanged':True,'root_execution_inside_wrapper_not_extra_process':True,'raw_flags_and_outcomes_verified':True})
source_result=json.loads((P/'source_only.stdout.bin').read_bytes());assert source_result['status']=='PASS' and source_result['target_report']=='ABSENT' and source_result['source_bodies_copied'] is False and source_result['archival_code_read'] is False and source_result['archival_code_executed'] is False
out={'timestamp_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS','recorded_processes':len(processes),'all_actual_distinct_pids':True,'all_streams_authenticated_before_interpretation':True,'processes':processes,'replays':replays,'source_only':source_result,'scope':'Receipts and inspected recorder code validate actual local process evidence; not mathematical proof.'}
(R/'PROCESS_EVIDENCE_CHECKS.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({'status':'PASS','recorded_processes':len(processes),'genuine_replay_processes':27,'source_only_full_input_pins':True}))
