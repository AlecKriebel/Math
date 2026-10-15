"""Close genuine zero-required review03 and fresh ROOT replay custody only."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,stat,gzip,tarfile
D=Path(__file__).resolve().parent;V=D/'native_integration_review_03';W=D/'native_integration_root_replay_03'
sha=lambda b:hashlib.sha256(b).hexdigest()
def pin(p):
 p=Path(p);s=p.lstat();assert stat.S_ISREG(s.st_mode) and not p.is_symlink(),str(p);b=p.read_bytes()
 return dict(bytes=len(b),sha256=sha(b),mode=format(stat.S_IMODE(s.st_mode),'04o'))
def check(p,e):assert pin(p)=={k:e[k] for k in ['bytes','sha256','mode']},str(p)
for n,h in {'REVIEW_REPORT.md':'e5480ab8ee45e09c00c275603902fcb1910b07aa4df600323fee418e16a0412f','INPUT_INVENTORY.json':'62e795982038275ac47a0f07c99ab5a9ba50160afba05689ac671ae48fb638e8','OUTPUT_INVENTORY.json':'b4f9bc78fa116055ad3c00afdb0676f1d9a7f7f6b0a7493bb1e1f20d2d4b3b1a'}.items():assert pin(V/n)['sha256']==h
o=json.loads((V/'OUTPUT_INVENTORY.json').read_bytes());i=json.loads((V/'INPUT_INVENTORY.json').read_bytes());f=json.loads((V/'FINAL_AUTHENTICATION.json').read_bytes())
assert o['writes_stopped'] and o['mandatory_findings']==0 and o['optional_findings']==1 and len(o['files'])==237
assert {str(p.relative_to(V)) for p in V.rglob('*') if p.is_file()}==set(o['files'])|{'OUTPUT_INVENTORY.json'}
assert all(stat.S_IMODE(p.stat().st_mode)==0o555 for p in [V,*[q for q in V.rglob('*') if q.is_dir()]])
for rel,e in o['files'].items():check(V/rel,e)
assert len(i['inputs'])==301
for absolute,e in i['inputs'].items():check(absolute,e)
source=D/'native_integration_preparation/integrate_pr305.py';assert pin(source)==dict(bytes=18292,sha256='0ea02436c0ac1e0070169df466c34ba141c43291e16515b3fd1cce2135071897',mode='0644')
assert f['mandatory_findings']==0 and f['immutable_input_files']==301 and f['no_production_native_integration_executed']
outer=[]
for p in sorted(V.glob('*_execution.json')):
 j=json.loads(p.read_bytes());assert 0<j['actual_PID']<100000000 and j['cwd']==str(V)
 assert j['exit_code']==(1 if p.name=='optimized_guard_actual001_execution.json' else 0)
 assert datetime.fromisoformat(j['ended_utc'])>=datetime.fromisoformat(j['started_utc'])
 programs=[Path(arg) for arg in j['argv'] if str(arg).endswith('.py')];assert len(programs)==1
 assert pin(programs[0])['bytes']==j['program_bytes'] and pin(programs[0])['sha256']==j['program_sha256']
 prefix=p.name[:-len('_execution.json')]
 for k in ['stdout','stderr']:
  b=(V/(prefix+'.'+k)).read_bytes();assert len(b)==j[k+'_bytes'] and sha(b)==j[k+'_sha256']
 if p.name=='optimized_guard_actual001_execution.json':assert b'Optimized execution is forbidden' in (V/(prefix+'.stderr')).read_bytes()
 outer.append(dict(path=str(p),pin=pin(p),actual_PID=j['actual_PID'],exit_code=j['exit_code']))
assert len(outer)==7 and len({x['actual_PID'] for x in outer})==7
toys=[]
for p in sorted(V.glob('real_capture_cases*/*/NATIVE_EXECUTION.json')):
 j=json.loads(p.read_bytes());assert 0<j['actual_PID']<100000000 and j['actual_pgid']==j['actual_sid']==j['actual_PID']
 assert j['candidate_source']['sha256']==pin(source)['sha256']
 toy=Path(j['argv'][3]);assert pin(toy)['sha256']==j['toy_program']['sha256'] and j['cwd']==str(p.parent)
 assert j['child_identity']['pgid']==j['child_identity']['sid']==j['actual_PID']
 assert j['actual_exit_code']==(-9 if p.parent.name in ['timeout','started_record_io'] else 7 if p.parent.name=='nonzero_code_guard' else 0)
 assert not (p.parent/'FORBIDDEN_LATE_WRITE').exists()
 for k in ['stdout','stderr']:
  b=(p.parent/('native.'+k)).read_bytes();assert len(b)==j['full_'+k+'_bytes'] and sha(b)==j['full_'+k+'_sha256']
 assert any(x['pgid']==j['actual_PID'] and x['result']=='sent' for x in j['group_signals'])
 toys.append(dict(path=str(p),pin=pin(p),actual_PID=j['actual_PID'],exit_code=j['actual_exit_code']))
assert len(toys)==20 and len({x['actual_PID'] for x in toys})==20
m=json.loads((V/'COMPLETED_MOCK_FIXTURE_MANIFEST.json').read_bytes());assert len(m['files'])==7375
archive=V/m['archive'];assert pin(archive)['bytes']==m['archive_bytes'] and pin(archive)['sha256']==m['archive_sha256']
expected={e['path']:e for e in m['files']};members={}
with tarfile.open(archive,'r:gz') as tar:
 files=[e for e in tar.getmembers() if e.isfile()];assert len(files)==7375 and {e.name for e in files}==set(expected)
 for e in files:
  b=tar.extractfile(e).read();q=expected[e.name];assert len(b)==q['bytes'] and sha(b)==q['sha256'] and format(e.mode,'04o')==q['mode'];members[e.name]=b
assert sum(len(b) for b in members.values())==m['logical_fixture_bytes']
streams=0
def checkstreams(j,read):
 global streams
 if not isinstance(j.get('stdout'),dict):return
 for k in ['stdout','stderr']:
  e=j[k];stored=read(e['path']);raw=gzip.decompress(stored)
  assert len(stored)==e['stored_bytes'] and sha(stored)==e['stored_sha256']
  assert len(raw)==e['logical_bytes'] and sha(raw)==e['logical_sha256'];streams+=1
for rel,b in members.items():
 if rel.endswith(('_execution.json','_interrupted.json')):
  j=json.loads(b);checkstreams(j,lambda absolute:members[str(Path(absolute).relative_to(V))])
for p in V.rglob('*_execution.json'):
 j=json.loads(p.read_bytes());checkstreams(j,lambda absolute:Path(absolute).read_bytes())
for p in V.rglob('*_interrupted.json'):
 j=json.loads(p.read_bytes());checkstreams(j,lambda absolute:Path(absolute).read_bytes())
replay=json.loads((D/'ROOT_NATIVE_REVIEW03_FRESH_REPLAY_CUSTODY.json').read_bytes());assert replay['status']=='PASS_ROOT_FRESH_NATIVE_REVIEW03_REPLAYS_COMPLETE_CUSTODY' and replay['case_count']==27
for rel,e in replay['all_payload_pins'].items():check(W/rel,e)
for e in replay['outer_replay_captures']:check(e['path'],e['pin'])
for e in replay['genuine_new_toy_native_groups']:check(e['path'],e['pin'])
assert replay['operator']==pin(source) and replay['production_main_not_executed']
receipt=dict(status='PASS_ROOT_AUTHENTICATED_CLOSED_NATIVE_REVIEW03_AND_FRESH27_CONTROL_REPLAY',UTC=datetime.now(timezone.utc).isoformat(),unresolved_mandatory_findings=0,optional_findings=1,optional_secondary_macOS_kill_diagnostic_disclosed_and_accepted=True,report_fully_read=True,closed_payloads=237,input_bindings=301,native_outer_including_final_close=outer,genuine_reviewer_toy_groups=toys,whole_archive_body_mode_files=7375,whole_logical_and_stored_streams_reauthenticated=streams,root_fresh_replay_case_count=27,root_fresh_replay_payloads=7480,operator=pin(source),report=pin(V/'REVIEW_REPORT.md'),inventory=pin(V/'OUTPUT_INVENTORY.json'),replay_custody=pin(D/'ROOT_NATIVE_REVIEW03_FRESH_REPLAY_CUSTODY.json'),no_shared_mutation_or_write_lease_issued=True)
out=D/'ROOT_NATIVE_REVIEW03_CUSTODY.json';assert not out.exists();out.write_text(json.dumps(receipt,indent=2)+'\n')
bindings=[V/n for n in ['CRITERIA.json','REVIEW_REPORT.md','OUTPUT_INVENTORY.json','INPUT_INVENTORY.json','FINAL_AUTHENTICATION.json','CAPTURE_RESULTS.json','CAPTURE_RESULTS_v02.json','INTEGRATION_MOCK_RESULTS.json']]+[out,D/'ROOT_NATIVE_REVIEW03_FRESH_REPLAY_CUSTODY.json',D/'ROOT_ACTUAL_PUBLICATION_TRACKER_FINAL_CUSTODY.json',D/'ROOT_NATIVE_REVIEW01_CUSTODY.json',D/'ROOT_NATIVE_REVIEW02_CUSTODY.json']
clear=dict(status='PASS_EXACT_PR305_NATIVE_INTEGRATION_OPERATOR',UTC=receipt['UTC'],PR=305,original_head='cc083024dbd00de06ad444cd4070f51f60d209eb',original_author_turn_count='1/5',unresolved_mandatory_findings=0,operator=pin(source),acceptance_preparation=pin(D/'ROOT_ACCEPTANCE_PREPARED.md'),snapshot_manifest=pin(D.parent/'snapshot_manifest.json'),closed_review_evidence={str(p):pin(p) for p in bindings},new_clean_native_review_round=3,earlier_adverse_native_reviews_repaired_and_preserved=True,root_fresh_independent_execution_reproduction=27,optional_diagnostic_does_not_authorize_retry=True,cooperative_execution_model_only=True,actual_integration_not_performed=True,fresh_Git_authorized_lease_and_peer_explicit_release_still_required=True)
p=D/'ROOT_PR305_NATIVE_INTEGRATION_CLEARANCE.json';assert not p.exists();p.write_text(json.dumps(clear,indent=2)+'\n')
with (D/'RESEARCH_LOG.md').open('a') as log:log.write('\n'+receipt['UTC']+' — NEW native review03 closed zero required findings; ROOT fully read report, authenticated237 frozen payloads/301 inputs/7 outer+20 genuine toy process receipts/7375 complete fixture archive bodies+modes/all streams; fresh ROOT27-control replay authenticated7480 payloads. Exact0ea operator cleared cooperatively, optional secondary-kill diagnostic disclosed/accepted. No actual merge or new lease. Peer50path window still requires explicit release. Math100%,boundedpriority100%,workflow85%.\n')
print(json.dumps({k:v for k,v in receipt.items() if k not in ['native_outer_including_final_close','genuine_reviewer_toy_groups']},indent=2))
print(json.dumps(dict(clearance_path=str(p),clearance_pin=pin(p)),indent=2))
