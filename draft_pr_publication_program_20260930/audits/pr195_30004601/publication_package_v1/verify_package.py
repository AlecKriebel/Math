"""Check an extracted verification archive and replay its exact certificates.
Run with Python3.11+ using -E -S -B -P. No third-party dependencies or writes.
"""
from pathlib import Path
import hashlib,json,subprocess,sys

def main():
    if sys.version_info < (3,11):
        raise SystemExit('Python3.11 or later is required for the documented isolation options.')
    root=Path(__file__).resolve().parent
    inventory=json.loads((root/'ARCHIVE_INVENTORY.json').read_bytes())
    for name,pin in inventory['files'].items():
        rel=Path(name)
        assert not rel.is_absolute() and '..' not in rel.parts
        p=root/rel;assert p.is_file() and not p.is_symlink(),name
        data=p.read_bytes()
        assert len(data)==pin['bytes'] and hashlib.sha256(data).hexdigest()==pin['sha256'],name
    runs=[]
    for folder,script,certificate in [
        ('exact_reproduction_audit_01','reproduce_exact.py','EXACT_CERTIFICATE.json'),
        ('exact_reproduction_audit_01','orthogonal_checks.py','ORTHOGONAL_CERTIFICATE.json'),
        ('priority_audit_01','compare_known_examples.py','KNOWN_EXAMPLE_CERTIFICATES.json'),
        ('priority_audit_01','octic_scalar_check.py','OCTIC_CERTIFICATES.json')]:
        d=root/'audits'/folder
        p=subprocess.run([sys.executable,'-E','-S','-B','-P',str(d/script),'--verify',str(d/certificate)],cwd=d,capture_output=True,text=True,check=True)
        result=json.loads(p.stdout)
        assert result.get('verified') is True,result
        runs.append({'script':folder+'/'+script,'result':result})
    print(json.dumps({'inventory_files_verified':len(inventory['files']),'exact_replays':runs,'verification_writes':False,'priority_certified':False},indent=2))

if __name__=='__main__':main()
