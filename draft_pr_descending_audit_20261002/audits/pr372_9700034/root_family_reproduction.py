"""Verify exact independent audit bindings and reproduce all three new controls."""
from pathlib import Path
import concurrent.futures,datetime,hashlib,json,os,shutil,subprocess,sys
A=Path(__file__).resolve().parent;sha=lambda b:hashlib.sha256(b).hexdigest();O=A/'root_family_streams';O.mkdir(exist_ok=True)
families=[('measure_tail_review','audit_probability_controls.py','AUDIT_CONTROLS.json','private/replays'),('metric_moments_review','adversarial_controls.py','ADVERSARIAL_CONTROLS.json','private/replay_streams'),('geometric_capture_review','scripts/check_geometric_controls.py','GEOMETRIC_CONTROL_STREAM.json','private/replays')]
bindings=[];comparisons=[]
for family,code,receipt,streams in families:
 D=A/family;m=json.loads((D/'PUBLIC_MANIFEST.json').read_bytes());assert len({f['path'] for f in m['files']})==len(m['files'])
 for f in m['files']:
  p=Path(f['path']);assert not p.is_absolute() and '..' not in p.parts and 'private' not in p.parts and p.suffix not in ['.pdf','.html','.png','.jpg','.stdout','.stderr']
  b=(D/p).read_bytes();assert len(b)==f['bytes'] and sha(b)==f['sha256'],(family,f['path'])
 bindings.append({'family':family,'manifest_sha256':sha((D/'PUBLIC_MANIFEST.json').read_bytes()),'binding_instances':len(m['files'])})
 for i in range(1,6):
  b=(D/streams/f'check_turn_{i}.stdout').read_bytes();e=(A/'root_original_streams'/f'turn{i}.stdout').read_bytes()
  assert b==e and json.loads(b)==json.loads(e);assert (D/streams/f'check_turn_{i}.stderr').read_bytes()==b''
 comparisons.append({'family':family,'all_five_complete_author_stdout_stderr_json_equal_root':True})
def run(family_info):
 family,code,receipt,_=family_info;D=A/family;W=A/'tmp'/('root_control_'+family);assert not W.exists();p=W/code;p.parent.mkdir(parents=True);shutil.copyfile(D/code,p)
 start=datetime.datetime.now(datetime.timezone.utc).isoformat();r=subprocess.run([sys.executable,'-I',str(p)],cwd=W,capture_output=True,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1'))
 (O/(family+'.stdout')).write_bytes(r.stdout);(O/(family+'.stderr')).write_bytes(r.stderr);assert r.returncode==0 and r.stderr==b''
 expected=(D/receipt).read_bytes();assert r.stdout==expected and json.loads(r.stdout)==json.loads(expected)
 q=json.loads(r.stdout);return {'family':family,'code':code,'code_sha256':sha((D/code).read_bytes()),'start_utc':start,'end_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'returncode':0,'stdout_sha256':sha(r.stdout),'stdout_bytes':len(r.stdout),'stderr_empty':True,'whole_stdout_and_json_exact':True,'complete_result':q}
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:runs=list(pool.map(run,families))
out={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS_FULL_THREE_FAMILY_CONTROLS_AND_BINDINGS','workflow_percent':80,'general_discovery_percent':0,'all_original_source_baselines_proof_verdicts_reports_and_new_control_code_fully_read':True,'initial_combined_read_truncations_corrected_by_complete_smaller_rereads':True,'manifest_bindings':bindings,'total_binding_instances':sum(x['binding_instances'] for x in bindings),'complete_author_stream_comparisons':comparisons,'runs':runs,'new_control_assertions':sum(x['complete_result']['exact_assertions'] for x in runs),'scope':'All three material approach families independently reconstructed before code/old review. Finite controls support audited written universal deductions; no general solution, SIRSN counterexample or novelty claim.'}
(A/'root_family_reproduction_receipt.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({'status':out['status'],'all_new_programs':len(runs),'all_bindings':out['total_binding_instances'],'new_control_assertions':out['new_control_assertions']}))
