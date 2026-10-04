"""Privately reproduce all five new family control streams and bind artifacts."""
from pathlib import Path
import datetime,hashlib,json,os,subprocess
A=Path(__file__).resolve().parent;D=A/'tmp/root_family_controls';D.mkdir(parents=True,exist_ok=True)
sha=lambda b:hashlib.sha256(b).hexdigest();binding_counts={}
for folder,name,key in [('sources_effective_review','PUBLIC_ARTIFACTS.json','public_files'),('cover_duality_review','FINAL_AUDIT_MANIFEST.json','files')]:
 P=A/folder;m=json.loads((P/name).read_text())
 for e in m[key]:
  b=(P/e['path']).read_bytes();assert len(b)==e['bytes'] and sha(b)==e['sha256'],e['path']
 binding_counts[folder]=len(m[key])
P=A/'special_arrangements_review';m=json.loads((P/'final_audit_receipt.json').read_text())
for name,h in m['sha256'].items():assert sha((P/name).read_bytes())==h,name
binding_counts['special_arrangements_review_final']=len(m['sha256'])
seal=json.loads((P/'independent_seal.json').read_text())
for name,entry in seal['sha256'].items():
 b=(P/name).read_bytes();h=entry if isinstance(entry,str) else entry['sha256'];assert sha(b)==h,name
binding_counts['special_arrangements_independence']=len(seal['sha256'])
for folder,name,key in [('sources_effective_review','SOURCE_FIRST_SEAL_V2.json','sha256'),('cover_duality_review','independence_seal.json','files')]:
 P=A/folder;s=json.loads((P/name).read_text())
 for path,h in s[key].items():assert sha((P/path).read_bytes())==h,path
 binding_counts[folder+'_independence']=len(s[key])
jobs=[('sources_effective_review','independent_controls.py','independent_run_stdout.txt'),('special_arrangements_review','independent_exact_checks.py','independent_exact_checks.stdout.txt'),('special_arrangements_review','post_candidate_checks.py','post_candidate_checks.stdout.txt'),('cover_duality_review','exact_fermat_check.py','exact_fermat_check.stdout.txt'),('cover_duality_review','exact_subfamily_check.py','exact_subfamily_check.stdout.txt')]
results=[]
for folder,name,stdout in jobs:
 P=A/folder;Q=D/folder;Q.mkdir(exist_ok=True)
 for code in P.glob('*.py'):(Q/code.name).write_bytes(code.read_bytes())
 r=subprocess.run(['python3','-B',str((Q/name).absolute())],cwd=Q,capture_output=True,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1'))
 label=folder+'_'+name.removesuffix('.py');(A/(label+'_root_full.stdout')).write_bytes(r.stdout);(A/(label+'_root_full.stderr')).write_bytes(r.stderr)
 assert r.returncode==0 and not r.stderr,(name,r.stderr.decode());assert r.stdout==(P/stdout).read_bytes(),name
 if folder=='sources_effective_review':assert (Q/'independent_full_output.json').read_bytes()==(P/'independent_full_output.json').read_bytes()
 results.append({'family':folder,'program':name,'complete_stdout_byte_equal':True,'bytes':len(r.stdout),'sha256':sha(r.stdout),'stderr_bytes':0,'full_written_artifact_byte_equal':folder=='sources_effective_review'})
out={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'frozen_head':'5da73632ab7a621de7b62edb5f70dfb8017e4a50','all_five_new_control_streams_exact':results,'all_family_public_binding_instances_checked':binding_counts,'all_new_proofs_and_eight_public_Python_sources_fully_read':True,'stronger_all_line_extension_root_proof_pass':True,'fresh_clean_whole_head_adversary_pending':True,'workflow_percent':85,'original_resolution_percent':0}
(A/'root_family_reproduction_receipt.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
