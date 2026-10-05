"""Whole readback and noncircular immutable closure; no service/Git action.

Self-recorded UTC/PID are actual recorder observations, not external attestation.
The seal does not claim to know this process's future terminal exit code.
"""
from pathlib import Path
from datetime import datetime, timezone
import gzip,hashlib,json,os,stat,sys
W=Path(__file__).resolve().parent;A=W.parent;R=Path('/Users/alec/Documents/Math')
def require(x,msg):
 if not x:raise RuntimeError(msg)
def utc():return datetime.now(timezone.utc).isoformat()
def pin(p):
 p=Path(p);require(p.is_file() and not p.is_symlink(),'Literal file required');b=p.read_bytes()
 return dict(path=str(p),bytes=len(b),sha256=hashlib.sha256(b).hexdigest(),mode=stat.S_IMODE(p.stat().st_mode))
def load(p):return json.loads(Path(p).read_bytes())
def write(p,v):
 with p.open('x') as f:json.dump(v,f,indent=2,ensure_ascii=False);f.write('\n');f.flush();os.fsync(f.fileno())
require(not sys.flags.optimize,'Nonoptimized recorder required')
initial=load(W/'INITIAL_INPUTS.json');authenticated=[]
for row in initial['inputs']:
 require(pin(row['input']['path'])==row['input'],'Original input body/mode changed')
 require(pin(row['full_source_archive']['path'])==row['full_source_archive'],'Full input archive changed')
 body=gzip.decompress(Path(row['full_source_archive']['path']).read_bytes())
 require(len(body)==row['input']['bytes'] and hashlib.sha256(body).hexdigest()==row['input']['sha256'],'Decoded original source mismatch')
 authenticated.append(dict(input=row['input'],archive=row['full_source_archive'],entire_decoded_source_verified=True))
for row in initial['all_23_candidate_files']:require(pin(row['path'])==row,'Frozen candidate changed')
case=load(W/'ISOLATED_CASE_RESULTS.json');require(case['fixture_count']==41 and len(case['results'])==41 and case['actual_test_runner_PID']==63096 and case['all_cases_completed'] is True,'Case results incomplete')
C=W/'actual_isolated_cases_01';request=load(C/'request.json');started=load(C/'started.json');execution=load(C/'execution.json')
require(execution['actual_PID']==63096 and request['actual_launcher_PID']==63095 and started['actual_PID']==63096,'Actual native PID differs')
require(execution['exit_code']==0 and execution['timed_out'] is False,'Actual local suite failed')
for k,v in request.items():require(execution[k]==v,'Request/execution agreement differs')
require(started['start_UTC']==execution['start_UTC'],'Start marker differs')
times=[datetime.fromisoformat(x) for x in [request['requested_UTC'],execution['start_UTC'],execution['end_UTC']]]
require(all(t.utcoffset() is not None for t in times) and times==sorted(times),'UTC ordering differs')
require(request['cwd']==str(W) and request['argv']==['/opt/homebrew/bin/python3','-E','-B',str(W/'isolated_cases.py')],'Exact local invocation differs')
require(pin(request['resolved_interpreter']['path'])=={k:v for k,v in request['resolved_interpreter'].items() if k!='resolved_path'},'Interpreter body changed')
native_sources=[]
for row in request['prelaunch_full_sources']:
 inp=row['input'];arc=row['stored_full_source'];require(pin(inp['path'])=={k:v for k,v in inp.items() if k!='resolved_path'},'Actual prelaunch source changed before closure')
 require(pin(arc['path'])=={k:v for k,v in arc.items() if k!='resolved_path'},'Actual source storage changed')
 body=gzip.decompress(Path(arc['path']).read_bytes());require(body==Path(inp['path']).read_bytes(),'Entire archived executed source differs')
 native_sources.append(dict(input=inp,archive=arc,entire_decoded_source_verified=True,historical_input_mode_is_prelaunch_mode=True))
streams=[]
for n in ['stdout','stderr']:
 row=execution[n];require(pin(row['stored']['path'])=={k:v for k,v in row['stored'].items() if k!='resolved_path'},'Actual stream storage changed')
 body=gzip.decompress(Path(row['stored']['path']).read_bytes());require(len(body)==row['logical_bytes'] and hashlib.sha256(body).hexdigest()==row['logical_sha256'],'Actual full stream differs')
 streams.append(dict(name=n,entire_logical_stream_verified=True,**row))
require(gzip.decompress(Path(execution['stderr']['stored']['path']).read_bytes())==b'','Unexpected local stderr')
native_stdout=json.loads(gzip.decompress(Path(execution['stdout']['stored']['path']).read_bytes()));require(native_stdout['actual_PID']==63096 and native_stdout['cases']==41,'Runner stdout binding differs')
verdict=load(W/'VERDICT.json');require([x['id'] for x in verdict['mandatory_issues']]==['G1','G2'] and verdict['publication_clearance'] is False and verdict['actual_local_fixture_count']==41,'Verdict differs')
cli=pin('/Users/alec/.nvm/versions/node/v22.16.0/lib/node_modules/@googleworkspace/cli/bin/gws');require((cli['bytes'],cli['sha256'],cli['mode'])==(15371280,'0f27b8b0815bf09cdf95da48d3c604f05ceb8f16bf5c9f0ba355b1f957cdd47e',0o755),'CLI byte pin changed')
write(W/'AUTHENTICATION.json',dict(UTC=utc(),actual_recorder_PID=os.getpid(),status='PASS_ENTIRE_ORIGINAL_INPUTS_AND_ACTUAL_LOCAL_CASE_CUSTODY',original_inputs=authenticated,candidate_23_files=initial['all_23_candidate_files'],actual_native_process=dict(request=request,started=started,execution=execution),entire_native_sources=native_sources,entire_native_streams=streams,Workspace_binary_pin_only=cli,all_original_public_and_operator_bodies_and_modes_unchanged=True,actual_service_or_Git_calls=False,science_clearance_currently_exists=(A/'ROOT_FINAL_PREPRINT_PUBLICATION_CLEARANCE.json').exists(),publication_clearance=False))
with (W/'RESEARCH_LOG.md').open('a') as f:
 f.write('\n'+utc()+' — Actual local suite PID63096 completed all41 cases, exit0, full prelaunch source/interpreter/request/start/streams authenticated. G1 mandatory operator/evidence contract and G2 mandatory tracker full-evidence binding confirmed. Complete report/verdict/read scope retained. Review100%; approval readiness80%; authorized execution0%. Whole original nine inputs and all23 candidate files unchanged. No services/Git/PR/shared control touched. Closing only this namespace to444/555; historical prelaunch source modes remain historical, while final manifest gives current modes.\n');f.flush();os.fsync(f.fileno())
files=sorted(p for p in W.rglob('*') if p.is_file());require(all(not p.is_symlink() for p in W.rglob('*')),'Namespace contains symlink')
before=[pin(p) for p in files]
write(W/'OWN_MODE_FREEZE_RECONCILIATION.json',dict(UTC=utc(),actual_recorder_PID=os.getpid(),qualification='All own payload bodies remain identical while current own modes are intentionally frozen to0444. Native prelaunch input modes remain unchanged historical observations. Original reviewed external sources are not chmodded.',before_freeze=before,expected_final_mode=0o444))
files=sorted(p for p in W.rglob('*') if p.is_file())
for p in files:p.chmod(0o444)
rows=[pin(p) for p in files];require(all(r['mode']==0o444 for r in rows),'Own payload freeze failed')
require(sum(r['bytes'] for r in rows)<10*1024**2,'Ten MiB allowance exceeded')
manifest=dict(schema='pr302-publication-operations-review-immutable-payload/v1',UTC=utc(),actual_recorder_PID=os.getpid(),status='CLOSED_REQUIRED_G1_G2_REPAIRS_NO_AUTHORITY',payload_files=rows,payload_file_count=len(rows),payload_bytes=sum(r['bytes'] for r in rows),noncircular_exclusions=['OUTPUT_MANIFEST.json','CLOSURE_SEAL.json'],historical_own_execution_source_modes_preserved_in_archives=True,publication_clearance=False)
write(W/'OUTPUT_MANIFEST.json',manifest);(W/'OUTPUT_MANIFEST.json').chmod(0o444)
for row in rows:require(pin(row['path'])==row,'Whole immutable payload readback failed')
manifestpin=pin(W/'OUTPUT_MANIFEST.json')
directories=sorted([W,*[p for p in W.rglob('*') if p.is_dir()]],key=lambda p:len(p.parts),reverse=True)
seal=dict(schema='pr302-publication-operations-review-noncircular-seal/v1',UTC=utc(),actual_recorder_PID=os.getpid(),status='PASS_ENTIRE_PAYLOAD_READBACK_AND_SEALED_MANIFEST',manifest=manifestpin,payload_file_count=len(rows),total_closed_files=len(rows)+2,directories_expected_mode=0o555,directory_count=len(directories),all_payload_bytes_modes_read_back=True,actual_terminal_exit_code_not_recorded_here=True,publication_clearance=False,no_service_Git_PR_or_shared_control_mutation=True)
write(W/'CLOSURE_SEAL.json',seal);(W/'CLOSURE_SEAL.json').chmod(0o444)
for p in directories:p.chmod(0o555)
for row in rows:require(pin(row['path'])==row,'Postseal payload changed')
require(pin(W/'OUTPUT_MANIFEST.json')==manifestpin,'Manifest changed')
require(all(stat.S_IMODE(p.stat().st_mode)==0o555 for p in directories),'Directory seal failed')
sealpin=pin(W/'CLOSURE_SEAL.json')
print(json.dumps(dict(status='CLOSED_REQUIRED_GLOBAL_OPERATIONAL_REPAIRS',actual_recorder_PID=os.getpid(),REPORT=pin(W/'REPORT.md'),VERDICT=pin(W/'VERDICT.json'),OUTPUT_MANIFEST=manifestpin,CLOSURE_SEAL=sealpin,payload_files=len(rows),total_closed_files=len(rows)+2,directory_count=len(directories),payload_bytes=sum(r['bytes'] for r in rows),publication_clearance=False),indent=2))
