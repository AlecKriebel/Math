from pathlib import Path
import datetime,hashlib,json,subprocess,sys
R=Path(__file__).resolve().parent
EXCLUDED={'PUBLIC_MANIFEST.json','FINAL_SEAL.json'}
def files():return sorted(p for p in R.rglob('*') if p.is_file() and not set(p.relative_to(R).parts)&{'private','__pycache__'} and p.relative_to(R).as_posix() not in EXCLUDED)
def manifest():
    m={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'scope':'Complete public post-merge evidence; ignored raw API/private bytes not redistributed','excluded':sorted(EXCLUDED),'files':[{'path':p.relative_to(R).as_posix(),'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in files()]}
    (R/'PUBLIC_MANIFEST.json').write_text(json.dumps(m,indent=2)+'\n')
def verify():
    z=subprocess.run([sys.executable,str(R/'verify_post_merge.py')],capture_output=True)
    (R/'closure.stdout').write_bytes(z.stdout);(R/'closure.stderr').write_bytes(z.stderr)
    assert z.returncode==0,(z.returncode,z.stdout.decode(),z.stderr.decode());return z
manifest();verify();manifest();result=verify()
seal={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS','manifest_sha256':hashlib.sha256((R/'PUBLIC_MANIFEST.json').read_bytes()).hexdigest(),'verifier_code_sha256':hashlib.sha256((R/'verify_post_merge.py').read_bytes()).hexdigest(),'verifier_exit':0,'verifier_stdout_sha256':hashlib.sha256(result.stdout).hexdigest(),'verifier_stderr_sha256':hashlib.sha256(result.stderr).hexdigest(),'public_files':len(files()),'explicit_self_exclusions':sorted(EXCLUDED),'post_merge_review_percent':100,'credited_method_percent':100,'new_theorem_percent':0}
(R/'FINAL_SEAL.json').write_text(json.dumps(seal,indent=2)+'\n')
final=subprocess.run([sys.executable,str(R/'verify_post_merge.py')],capture_output=True)
assert final.returncode==0 and final.stdout==result.stdout and final.stderr==result.stderr
print(json.dumps(seal,indent=2))
