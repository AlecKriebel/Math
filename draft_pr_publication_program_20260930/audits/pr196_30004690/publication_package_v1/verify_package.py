"""Authenticate extracted authored supplement and replay scalar certificates.
Python3.11+ standard library; no network and no writes.
"""
from pathlib import Path
import hashlib,json,subprocess,sys
def require(condition,message):
    if not condition:raise RuntimeError(message)
def main():
    require(sys.version_info >= (3,11),'Python3.11 or later required')
    root=Path(__file__).resolve().parent
    inventory=json.loads((root/'ARCHIVE_INVENTORY.json').read_bytes())['files']
    for name,pin in inventory.items():
        rel=Path(name);require(not rel.is_absolute() and '..' not in rel.parts,'unsafe path')
        p=root/rel;require(p.is_file() and not p.is_symlink() and p.resolve().is_relative_to(root),'missing/unsafe '+name)
        b=p.read_bytes();require(len(b)==pin['bytes'] and hashlib.sha256(b).hexdigest()==pin['sha256'],'identity '+name)
    specs=[('audits/legendre_regularity_audit_01/exact_scalar_verifier.py','audits/legendre_regularity_audit_01/EXACT_SCALAR_CERTIFICATE.json',False),('audits/legendre_regularity_audit_01/exact_scalar_verifier.py','audits/legendre_regularity_audit_01/EXACT_SCALAR_CERTIFICATE.json',True),('original_submitted_head/independent_review/scalar_duality_check.py','original_submitted_head/independent_review/scalar_duality_output.json',False)]
    runs=[]
    for script,certificate,optimize in specs:
        args=[sys.executable,'-E','-S','-B','-P']+(['-O'] if optimize else [])+[str(root/script)]
        p=subprocess.run(args,cwd=root,capture_output=True,text=True,check=True)
        require(not p.stderr,'unexpected stderr '+script)
        value=json.loads(p.stdout);require(value==json.loads((root/certificate).read_bytes()),'certificate mismatch '+script)
        runs.append({'script':script,'optimization_enabled':optimize,'certificate_exact_match':True,'result':value})
    print(json.dumps({'inventory_files_verified':len(inventory),'exact_scalar_replays':runs,'scalar_only':True,'geometric_or_PDE_computation_certified':False,'historical_priority_certified':False,'verification_writes':False},indent=2))
if __name__=='__main__':main()
