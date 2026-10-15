"""Independent private exact replay of three separately sealed audit families."""
from pathlib import Path
import json,hashlib,datetime,subprocess,sys,os,shutil
A=Path(__file__).resolve().parent;W=A/'tmp/root_family';assert not W.exists();W.mkdir(parents=True);O=A/'root_family_streams';O.mkdir();sha=lambda b:hashlib.sha256(b).hexdigest();bindings=[]
def copy(rel,family,digest=None,size=None):
 p=Path(rel);assert not p.is_absolute() and '..' not in p.parts
 b=(A/family/p).read_bytes()
 if digest:assert sha(b)==digest,(family,rel)
 if size is not None:assert len(b)==size
 q=W/family/p;q.parent.mkdir(parents=True,exist_ok=True);q.write_bytes(b);bindings.append({'family':family,'path':str(p),'bytes':len(b),'sha256':sha(b)})
f='finite_hidden_review';m=json.loads((A/f/'PUBLIC_ALLOWLIST.json').read_bytes());copy('PUBLIC_ALLOWLIST.json',f,'0717279ba7392cf6f28018d0efe171d421e33e7b299bd79103b42fff548e6fb6')
for r in m['files']:copy(r['path'],f,r['sha256'],r['bytes'])
f='coding_mixtures_review';s=json.loads((A/f/'FINAL_AUDIT_SEAL.json').read_bytes());m=json.loads((A/f/'PUBLIC_ALLOWLIST.json').read_bytes())
for rel in m['allowlist']:copy(rel,f,s['public_artifact_hashes'].get(rel))
assert set(s['public_artifact_hashes'])==set(m['allowlist'])-{'FINAL_AUDIT_SEAL.json'}
f='memory_coupling_review';s=json.loads((A/f/'FINAL_SEAL.json').read_bytes());copy('FINAL_SEAL.json',f,'9cb65789f4baf87c086e46b553c0f9dedfe26ba63da47d4ea3511a36688830d2');copy('PUBLIC_MANIFEST.json',f,s['critical_sha256']['PUBLIC_MANIFEST.json']);m=json.loads((A/f/'PUBLIC_MANIFEST.json').read_bytes())
for r in m['public_files']:copy(r['path'],f,r['sha256'],r['bytes'])
for rel in m['additional_final_attestation_streams']:copy(rel,f,s['critical_sha256'][rel])
for rel,digest in s['critical_sha256'].items():assert sha((A/f/rel).read_bytes())==digest
T=W/'snapshot/unsolved_math_prioritization/attempts/30004435';shutil.copytree(A/'tmp/root_original',T)
runs=[('finite_hidden_review','controls/independent_controls.py','streams/independent_controls.stdout.json','streams/independent_controls.stderr.txt',[]),('finite_hidden_review','controls/replay_independent_inputs.py','streams/replay_independent_inputs.stdout.json','streams/replay_independent_inputs.stderr.txt',[]),('finite_hidden_review','controls/augmentation_and_code_comparison.py','streams/augmentation_and_code_comparison.stdout.json','streams/augmentation_and_code_comparison.stderr.txt',[]),('coding_mixtures_review','independent/controls.py','independent/controls.stdout.json','independent/controls.stderr.txt',[]),('coding_mixtures_review','independent/endpoint_controls.py','independent/endpoint_controls.stdout.json','independent/endpoint_controls.stderr.txt',[]),('memory_coupling_review','independent_controls.py','artifacts/independent_controls.stdout.json','artifacts/independent_controls.stderr.txt',[]),('memory_coupling_review','block_bound_controls.py','artifacts/block_bound_controls.stdout.json','artifacts/block_bound_controls.stderr.txt',[])]
receipts=[]
for family,code,out,err,args in runs:
 result=subprocess.run([sys.executable,'-B',str(W/family/code),*args],cwd=W/family,capture_output=True,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1'));label=family+'_'+Path(code).stem
 (O/(label+'.stdout')).write_bytes(result.stdout);(O/(label+'.stderr')).write_bytes(result.stderr)
 assert result.returncode==0 and result.stdout==(A/family/out).read_bytes() and result.stderr==(A/family/err).read_bytes(),(label,result.returncode,result.stderr.decode())
 receipts.append({'family':family,'code':code,'stdout_bytes':len(result.stdout),'stdout_sha256':sha(result.stdout),'stderr_bytes':len(result.stderr),'whole_stdout_stderr_exact':True})
r={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS_THREE_INDEPENDENT_MECHANISM_FAMILIES','workflow_percent':85,'unrestricted_discovery_percent':0,'all_universal_proofs_and_new_mathematical_programs_read_before_execution':True,'explicit_manifest_and_seal_bindings':bindings,'seven_complete_new_program_streams':receipts,'historical_author_package_already_independently_reproduced':'root_original_reproduction_receipt.json','author_mathematical_correction_required':False,'audit_side_errors_preserved_and_explicitly_corrected':True,'fresh_whole_package_and_live_metadata_gates_pending':True}
(A/'root_family_reproduction_receipt.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps({'status':r['status'],'bound_instances':len(bindings),'new_programs':len(receipts)},sort_keys=True))
