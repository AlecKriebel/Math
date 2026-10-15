"""Reproduce the sealed prior gate privately; adapt only its repository path."""
from pathlib import Path
import datetime,hashlib,json,os,shutil,subprocess,sys
A=Path(__file__).resolve().parent;P=A/'final_adversary';D=A/'tmp/root_prior_final_copy';ROOT=A.parents[2]
D.mkdir(parents=True,exist_ok=True)
manifest=json.loads((P/'OUTPUT_MANIFEST.json').read_text())
for e in manifest['files']:
 b=(P/e['path']).read_bytes();assert len(b)==e['bytes'] and hashlib.sha256(b).hexdigest()==e['sha256'],e['path']
 f=D/e['path'];f.parent.mkdir(parents=True,exist_ok=True);f.write_bytes(b)
for name in ['OUTPUT_MANIFEST.json','VERIFY_RECEIPT.json','VERIFY.stdout.json','VERIFY.stderr']:
 shutil.copyfile(P/name,D/name)
for name in ['ems46748.pdf','bgk.pdf','bleak.pdf','km.pdf','gs.pdf','golan.pdf','farley.pdf']:
 f=D/'private_sources'/name;f.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(P/'private_sources'/name,f)
source=(D/'VERIFY.py').read_text();assert source.count('ROOT = P.parents[3]')==1
code=source.replace('ROOT = P.parents[3]','ROOT = Path('+repr(str(ROOT))+')')
runner=D/'private_path_adapter.py';runner.write_text('from pathlib import Path\nexec(compile('+repr(code)+', '+repr(str(D/'VERIFY.py'))+', "exec"), {"__file__":'+repr(str(D/'VERIFY.py'))+',"__name__":"__main__"})\n')
r=subprocess.run([sys.executable,'-B',str(runner)],cwd=ROOT,capture_output=True,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1'))
(A/'root_prior_final_verify.stdout.json').write_bytes(r.stdout);(A/'root_prior_final_verify.stderr').write_bytes(r.stderr);assert r.returncode==0 and not r.stderr,r.stderr.decode()
actual=json.loads(r.stdout);assert actual==json.loads((P/'VERIFY.stdout.json').read_text())
out={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'prior_review_head':actual['head'],'all_public_output_bindings':len(manifest['files']),'entire_verifier_JSON_byte_semantics_equal':True,'all_candidate_and_independent_fullstreams_byte_exact':True,'distinct_independent_controls':actual['distinct_independent_assertions'],'source_fresh_matches':actual['private_fresh_PDFs_rechecked_if_retained'],'public_optional_raw_bindings':0,'execution_path_adaptation_only':'ROOT constant points to actual repository; original sealed VERIFY.py bytes retained and verified','verifier_sha256':hashlib.sha256((D/'VERIFY.py').read_bytes()).hexdigest(),'stdout_sha256':hashlib.sha256(r.stdout).hexdigest(),'mandatory_scope_repair_confirmed':True,'later_corrected_head_not_certified':True,'workflow_percent':90}
(A/'root_prior_final_reproduction_receipt.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
