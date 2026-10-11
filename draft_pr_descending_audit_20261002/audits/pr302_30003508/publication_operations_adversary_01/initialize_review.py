from pathlib import Path
from datetime import datetime, timezone
import gzip, hashlib, json, os, stat

W = Path(__file__).resolve().parent
R = Path('/Users/alec/Documents/Math')
A = W.parent
D = A / 'publication_preparation'
F = A / 'preprint_package_v02'
EXPECTED = {
 'publication_guard.py': (5095, '7d3f38c8dd1fd1e7dee396d50844a6849e627baca1838715d298c6bb7964e240'),
 'run_zenodo_step.py': (2664, '2907989c64ea3c9794ae17e9aff839715943dad07b6ca409bf765edab79bf48a'),
 'verify_public_record.py': (4939, 'e8a7bdfe5e39b5e9865ac57902ff0f0e33fa99a639bf37c07734c51495a040f0'),
 'append_tracker.py': (6305, 'f3b8f5cabd2552f509c2453841c6e6dfc228d9b6d3d0c57a1f64228e247e931c')}
def pin(p):
 p = Path(p); b = p.read_bytes()
 if p.is_symlink() or not p.is_file(): raise RuntimeError('Literal input required')
 return dict(path=str(p), bytes=len(b), sha256=hashlib.sha256(b).hexdigest(), mode=stat.S_IMODE(p.stat().st_mode))
def write(n, x):
 with (W/n).open('x') as f: json.dump(x,f,indent=2,ensure_ascii=False); f.write('\n'); f.flush(); os.fsync(f.fileno())
inputs=[]
src = W/'reviewed_sources'; src.mkdir(exist_ok=False)
for n,(size,digest) in EXPECTED.items():
 p=D/n; r=pin(p)
 if (r['bytes'],r['sha256']) != (size,digest): raise RuntimeError('Prepared source changed')
 q=src/(n+'.gz');q.write_bytes(gzip.compress(p.read_bytes(),mtime=0));q.chmod(0o444)
 inputs.append(dict(input=r, full_source_archive=pin(q)))
for p in [R/'zenodo_deposit_tool/zenodo.py', R/'zenodo_deposit_tool/README.md', F/'SECOND_CANDIDATE_MANIFEST.json', F/'record_metadata.json', F/'README.md']:
 q=src/(p.parent.name+'_'+p.name+'.gz');q.write_bytes(gzip.compress(p.read_bytes(),mtime=0));q.chmod(0o444)
 inputs.append(dict(input=pin(p),full_source_archive=pin(q)))
m=json.loads((F/'SECOND_CANDIDATE_MANIFEST.json').read_bytes())
for r in m['files']:
 if pin(r['path'])!=r or r['mode']!=0o444: raise RuntimeError('Candidate changed')
write('INITIAL_INPUTS.json',dict(UTC=datetime.now(timezone.utc).isoformat(),actual_recorder_PID=os.getpid(),prepared_source_count=4,inputs=inputs,all_23_candidate_files=m['files'],candidate_manifest=pin(F/'SECOND_CANDIDATE_MANIFEST.json'),scientific_clearance_exists=(A/'ROOT_FINAL_PREPRINT_PUBLICATION_CLEARANCE.json').exists(),service_scope_prepared_only=True,no_service_Git_PR_or_control_mutation=True,operator_execution_or_publication_authority=False,estimates_percent=dict(operations_review=20,authoritative_publication_workflow=None)))
write('EXPLORATORY_READ_FAILURE.json',dict(tool_chunk_id='2332d8',tool_reported_exit_code=1,actual_PID_not_supplied_by_tool=True,source_kind='post-hoc exact tool-request excerpt, not a prelaunch archive',code="p=Path('/Users/alec/.nvm/versions/node/v22.16.0/lib/node_modules/@googleworkspace/cli/bin/gws');b=p.read_bytes();print(json.dumps({'path':str(p),'resolved':str(p.resolve()),'is_symlink':p.is_symlink(),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest(),'mode':stat.S_IMODE(p.stat().st_mode)}));print(b.decode()[:12000])",complete_error='UnicodeDecodeError: utf-8 codec cannot decode byte 0xcf in position 0: invalid continuation byte',known_stdout_binary_pin=dict(path='/Users/alec/.nvm/versions/node/v22.16.0/lib/node_modules/@googleworkspace/cli/bin/gws',resolved='/Users/alec/.nvm/versions/node/v22.16.0/lib/node_modules/@googleworkspace/cli/bin/gws',is_symlink=False,bytes=15371280,sha256='0f27b8b0815bf09cdf95da48d3c604f05ceb8f16bf5c9f0ba355b1f957cdd47e',mode=0o755),qualification='Exploratory read wrongly tried to decode the native Mach-O CLI as UTF-8. It did not execute that binary. Retained here without invented PID, request time or prelaunch custody. Subsequent review treats CLI as a pinned native binary.'))
(W/'RESEARCH_LOG.md').write_text('# PR302 prepared publication operator adversary 01\n\n'+datetime.now(timezone.utc).isoformat()+' — Authenticated all four requested source bodies, repository kit and README, exact metadata, and all 23 frozen public files. Scientific clearance is absent. Review 20%; no execution or publication authority. All writes remain in this review namespace. Exploratory CLI text decoding failed because the CLI is a native binary; the actual reported error is retained with its limited tool provenance.\n')
print(json.dumps(dict(status='AUTHENTICATED_ORIGINAL_PREPARED_SOURCES',actual_PID=os.getpid(),input_count=len(inputs),candidate_files=len(m['files']))))
