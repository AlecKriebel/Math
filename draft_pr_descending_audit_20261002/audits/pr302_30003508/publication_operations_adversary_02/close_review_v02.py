from pathlib import Path
from datetime import datetime,timezone
import gzip,hashlib,json,os,stat
R=Path('/Users/alec/Documents/Math');W=Path(__file__).resolve().parent;A=W.parent
def utc():return datetime.now(timezone.utc).isoformat()
def pin(p):
 p=Path(p);assert p.is_file() and not p.is_symlink();b=p.read_bytes();return dict(path=str(p),bytes=len(b),sha256=hashlib.sha256(b).hexdigest(),mode=stat.S_IMODE(p.stat().st_mode))
def write(p,obj):
 with p.open('x') as f:f.write(json.dumps(obj,indent=2)+'\n');f.flush();os.fsync(f.fileno())
initial=json.loads((W/'INITIAL_INPUTS.json').read_bytes());source_checks=[]
for row in initial['sources']:
 assert pin(row['input']['path'])==row['input'];assert pin(row['full_body_archive']['path'])==row['full_body_archive'];assert gzip.decompress(Path(row['full_body_archive']['path']).read_bytes())==Path(row['input']['path']).read_bytes();source_checks.append(row['input'])
for row in initial['candidate_files']+initial['science_evidence_pins']+initial['runtime_targets']:assert pin(row['path'])==row
original_manifest=json.loads((A/'publication_operator_version_01/ARCHIVE_MANIFEST.json').read_bytes())
for row in original_manifest['files']:
 p=Path(row['archived_path']);actual=pin(p);assert actual['bytes']==row['bytes'] and actual['sha256']==row['sha256'] and actual['mode']==row['archived_mode']
assert not (A/'ROOT_FINAL_PUBLICATION_OPERATIONS_CLEARANCE.json').exists() and not (A/'publication_actual').exists()
native=[]
for name in ('actual_isolated_cases_01','actual_consistent_cases_01'):
 d=W/name;req=json.loads((d/'request.json').read_bytes());start=json.loads((d/'started.json').read_bytes());result=json.loads((d/'execution.json').read_bytes());assert all(result[k]==v for k,v in req.items());assert start==dict(actual_PID=result['actual_PID'],start_UTC=result['start_UTC'],state='STARTED_OUTCOME_PENDING');assert result['exit_code']==0 and result['timed_out'] is False and result['automatic_retry'] is False;times=[datetime.fromisoformat(result[k]) for k in ('requested_UTC','start_UTC','end_UTC')];assert all(t.tzinfo is not None for t in times) and times[0]<=times[1]<=times[2]
 for source in result['full_prelaunch_sources']:
  assert pin(source['full_source_archive']['path'])['sha256']==source['full_source_archive']['sha256'];b=gzip.decompress(Path(source['full_source_archive']['path']).read_bytes());assert len(b)==source['input']['bytes'] and hashlib.sha256(b).hexdigest()==source['input']['sha256'];assert Path(source['input']['path']).read_bytes()==b
 for name in ('stdout','stderr'):
  row=result[name];assert pin(row['stored']['path'])['sha256']==row['stored']['sha256'];b=gzip.decompress(Path(row['stored']['path']).read_bytes());assert len(b)==row['logical_bytes'] and hashlib.sha256(b).hexdigest()==row['logical_sha256']
 assert pin(result['resolved_executable']['path'])['sha256']==result['resolved_executable']['sha256'];native.append(dict(request=pin(d/'request.json'),started=pin(d/'started.json'),execution=pin(d/'execution.json'),actual_PID=result['actual_PID'],actual_launcher_PID=result['actual_launcher_PID'],exit_code=result['exit_code'],timed_out=result['timed_out']))
results=[json.loads((W/p).read_bytes()) for p in ('ISOLATED_CASE_RESULTS.json','CONSISTENT_CASE_RESULTS.json')];assert sum(x['case_count'] for x in results)==96 and all(not x['unexpected_dispositions'] for x in results)
verdict=json.loads((W/'VERDICT.json').read_bytes());assert verdict['mandatory_issues']==[] and verdict['nonmandatory_issues']==[] and verdict['publication_clearance'] is False
t=utc();log=W/'RESEARCH_LOG.md';log.write_text(log.read_text()+'\n'+t+' — Final body/mode readback authenticates11 primary source/archive inputs, all23 public files,14 original scientific evidence pins,3 runtime targets and4 original archived operators. Both actual process tapes/source bodies/streams authenticate with96 expected cases. Preparing noncircular manifest and seal; review100%, adjudication readiness100%, actual service execution0%. Freeze modes are closure modes, historical fixture and launch modes remain historical.\n')
for p in W.rglob('*'):
 assert not p.is_symlink()
 if p.is_file():p.chmod(0o444)
assert not (W/'OUTPUT_MANIFEST.json').exists() and not (W/'CLOSURE_SEAL.json').exists()
payload=sorted(p for p in W.rglob('*') if p.is_file())
directories=sorted([W]+[p for p in W.rglob('*') if p.is_dir()]);rows=[dict(relative_path=str(p.relative_to(W)),**pin(p)) for p in payload]
manifest=dict(schema='pr302-publication-operations-closed-evidence/v2',UTC=utc(),actual_closure_self_recorder_PID=os.getpid(),status='FROZEN_PAYLOAD_NONCIRCULAR_INVENTORY',namespace=str(W),files=rows,directories=[dict(path=str(p),relative_path=str(p.relative_to(W)),mode=0o555) for p in directories],excluded_from_payload=['OUTPUT_MANIFEST.json','CLOSURE_SEAL.json'],payload_file_count=len(rows),publication_clearance=False)
write(W/'OUTPUT_MANIFEST.json',manifest);(W/'OUTPUT_MANIFEST.json').chmod(0o444)
seal=dict(schema='pr302-publication-operations-closure-seal/v2',UTC=utc(),actual_closure_self_recorder_PID=os.getpid(),status='CLOSED_EXACT_REPAIRED_OPERATOR_REVIEW_NO_UNRESOLVED_ISSUES',namespace=str(W),output_manifest=pin(W/'OUTPUT_MANIFEST.json'),primary_documents=[pin(W/n) for n in ('REPORT.md','DERIVATION.md','READ_SCOPE.md','VERDICT.json')],native_receipts_observed_before_freeze=native,actual_test_count=96,actual_test_processes=[83756,85633],all_source_candidate_science_runtime_original_archive_pins_unchanged=True,production_operations_gate_and_OUT_absent=True,all_payload_modes=0o444,all_directory_modes=0o555,publication_clearance=False,closure_limit='Actual self-observation while closing; the outer tool observes the eventual terminal outcome. No future self-exit or independent OS/clock attestation is fabricated.',historical_modes='Prelaunch/native/fixture pins retain actual test-time modes; own copied files freeze to0444 now. This is not a claim of mutable live approval at the synthetic paths after closure.')
write(W/'CLOSURE_SEAL.json',seal);(W/'CLOSURE_SEAL.json').chmod(0o444)
for p in reversed(directories):p.chmod(0o555)
for row in rows:assert pin(row['path'])=={k:v for k,v in row.items() if k!='relative_path'}
for p in W.rglob('*'):
 assert not p.is_symlink();assert stat.S_IMODE(p.stat().st_mode)==(0o555 if p.is_dir() else 0o444)
assert stat.S_IMODE(W.stat().st_mode)==0o555
files=list(p for p in W.rglob('*') if p.is_file());stored=sum(p.stat().st_size for p in files);physical=sum(getattr(p.stat(),'st_blocks',0)*512 for p in files);assert stored<=20*1024*1024 and physical<=20*1024*1024
print(json.dumps(dict(status=seal['status'],actual_closure_self_recorder_PID=os.getpid(),file_count=len(files),directory_count=len(directories),stored_bytes=stored,physical_bytes=physical,manifest=pin(W/'OUTPUT_MANIFEST.json'),seal=pin(W/'CLOSURE_SEAL.json'),publication_clearance=False)))
