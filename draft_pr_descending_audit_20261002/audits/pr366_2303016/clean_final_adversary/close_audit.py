from pathlib import Path
import datetime,hashlib,json,subprocess,sys
R=Path(__file__).resolve().parent
EXCLUDED={'IMMUTABLE_MANIFEST.json','FINAL_SEAL.json'}
def files():return sorted(p for p in R.rglob('*') if p.is_file() and not any(part in {'private_sources','private_replay','__pycache__'} for part in p.relative_to(R).parts) and str(p.relative_to(R)) not in EXCLUDED)
def write_manifest():
    payload={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'scope':'All public files in this audit directory; ignored private source/replay bytes not redistributed','excluded':sorted(EXCLUDED),'files':[{'path':str(p.relative_to(R)),'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in files()]}
    (R/'IMMUTABLE_MANIFEST.json').write_text(json.dumps(payload,indent=2)+'\n')
def verify():
    out=subprocess.run([sys.executable,str(R/'verify_audit.py')],capture_output=True)
    (R/'closure.stdout').write_bytes(out.stdout);(R/'closure.stderr').write_bytes(out.stderr)
    assert out.returncode==0,(out.returncode,out.stdout.decode(),out.stderr.decode())
    return out
write_manifest();verify()
write_manifest();out=verify()
# Second pass includes the now-existing output streams; their bytes remain stable.
out2=subprocess.run([sys.executable,str(R/'verify_audit.py')],capture_output=True)
assert out2.returncode==0 and out2.stdout==out.stdout and out2.stderr==out.stderr
seal={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS','manifest_sha256':hashlib.sha256((R/'IMMUTABLE_MANIFEST.json').read_bytes()).hexdigest(),'verifier_code_sha256':hashlib.sha256((R/'verify_audit.py').read_bytes()).hexdigest(),'verifier_exit':out.returncode,'verifier_stdout_sha256':hashlib.sha256(out.stdout).hexdigest(),'verifier_stderr_sha256':hashlib.sha256(out.stderr).hexdigest(),'explicit_manifest_self_and_final_seal_exclusion':True,'public_files':len(files())}
(R/'FINAL_SEAL.json').write_text(json.dumps(seal,indent=2)+'\n')
final_check=subprocess.run([sys.executable,str(R/'verify_audit.py')],capture_output=True)
assert final_check.returncode==0 and final_check.stdout==out.stdout and final_check.stderr==out.stderr
print(json.dumps(seal,indent=2))
