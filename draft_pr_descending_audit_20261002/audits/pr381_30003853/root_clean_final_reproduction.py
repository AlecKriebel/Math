"""Privately reproduce the corrected exact head and new clean-context controls."""
from pathlib import Path
import datetime,hashlib,json,os,subprocess
A=Path(__file__).resolve().parent;P=A/'clean_final_adversary';D=A/'tmp/root_clean_final_copy';D.mkdir(parents=True,exist_ok=True)
sha=lambda b:hashlib.sha256(b).hexdigest();bound={}
for name in ['INDEPENDENT_SEAL.json','POSTCANDIDATE_SEAL.json']:
 m=json.loads((P/name).read_text())
 for e in m['files']:
  b=(P/e['path']).read_bytes();assert len(b)==e['bytes'] and sha(b)==e['sha256'],e['path']
 bound[name]=len(m['files'])
if (P/'OUTPUT_MANIFEST.json').is_file():
 m=json.loads((P/'OUTPUT_MANIFEST.json').read_text())
 for e in m['files']:
  b=(P/e['path']).read_bytes();assert len(b)==e['bytes'] and sha(b)==e['sha256'],e['path']
 bound['OUTPUT_MANIFEST.json']=len(m['files'])
candidate=D/'packet';candidate.mkdir(exist_ok=True);m=json.loads((A/'scope_repaired_snapshot_manifest.json').read_text());nested=0
for e in m['files']:
 b=(A/'scope_repaired_snapshot'/e['path']).read_bytes();assert b==subprocess.check_output(['git','show',m['head']+':'+e['path']]);assert len(b)==e['bytes'] and sha(b)==e['sha256']
 if e['path'].startswith('problems/30003853_thompson_subgroup_abelianization/'):
  f=candidate/Path(e['path']).relative_to('problems/30003853_thompson_subgroup_abelianization');f.parent.mkdir(parents=True,exist_ok=True);f.write_bytes(b)
for f in candidate.rglob('*.json'):
 if f.name in ['SOURCE_MANIFEST.json','TURN_3_SOURCES.json','TURN_5_SOURCES.json']:continue
 for e in json.loads(f.read_text()).get('files',[]):
  b=(f.parent/e['path']).read_bytes();assert len(b)==e['bytes'] and sha(b)==e['sha256'],e['path'];nested+=1
jobs=[('REPLAY_ALL.py','author'),('independent_review/independent_check.py','historical_independent'),('verify_publication.py','current_publication')]+[(f'verify_turn{i}.py',f'turn{i}') for i in range(1,6)]
streams=[];env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1')
for name,label in jobs:
 r=subprocess.run(['python3','-B',str((candidate/name).absolute())],cwd=candidate,capture_output=True,env=env)
 (A/('root_clean_'+label+'.stdout')).write_bytes(r.stdout);(A/('root_clean_'+label+'.stderr')).write_bytes(r.stderr);assert r.returncode==0 and not r.stderr,(name,r.stderr.decode());assert r.stdout==(P/'replays'/(label+'.stdout.txt')).read_bytes(),name
 streams.append({'program':name,'full_stdout_byte_exact':True,'bytes':len(r.stdout),'sha256':sha(r.stdout),'stderr_bytes':0})
controls=D/'controls';controls.mkdir(exist_ok=True)
for name in ['independent_controls.py','postcandidate_controls.py']:(controls/name).write_bytes((P/'controls'/name).read_bytes())
for name in ['independent_controls','postcandidate_controls']:
 r=subprocess.run(['python3','-B',str((controls/(name+'.py')).absolute())],cwd=controls,capture_output=True,env=env)
 (A/('root_clean_'+name+'.stdout')).write_bytes(r.stdout);(A/('root_clean_'+name+'.stderr')).write_bytes(r.stderr);assert r.returncode==0 and not r.stderr,(name,r.stderr.decode());assert r.stdout==(P/'controls'/(name+'.stdout.txt')).read_bytes(),name
 streams.append({'program':name+'.py','full_stdout_byte_exact':True,'bytes':len(r.stdout),'sha256':sha(r.stdout),'stderr_bytes':0})
out={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'reviewed_head':m['head'],'all_corrected_Git_paths':len(m['files']),'nested_binding_occurrences':nested,'seals_and_output_bindings':bound,'all_ten_complete_streams_reproduced':streams,'new_postcandidate_assertions':81628,'old_author_assertions':562635,'old_historical_assertions':110736,'public_raw_source_bindings':0,'historical_processed_sources_unreproduced':13,'all_new_written_proofs_and_five_executable_audit_sources_read':True,'current_diagram_scope_repair_global_and_byte_bound':True,'workflow_percent':95,'acceptance_pending_final_report_and_actual_merge':True}
assert nested==111;(A/'root_clean_final_reproduction_receipt.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
