"""Hash and exact-output verification; Python standard library only."""
from pathlib import Path
import hashlib,json,subprocess,sys

root=Path(__file__).resolve().parent
manifest=json.loads((root/'manifest.json').read_bytes())
for entry in manifest['files']:
    path=root/entry['path']
    if not path.resolve().is_relative_to(root) or path.is_symlink():
        raise ValueError('Invalid package path: '+entry['path'])
    data=path.read_bytes()
    if len(data)!=entry['bytes'] or hashlib.sha256(data).hexdigest()!=entry['sha256']:
        raise ValueError('Package hash mismatch: '+entry['path'])
command=[sys.executable,'-E','-B',str(root/'verification/check_certificate.py')]
completed=subprocess.run(command,cwd=root,stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=60,check=False)
if completed.returncode!=0:
    sys.stderr.buffer.write(completed.stderr)
    raise RuntimeError('Certificate checker failed: '+str(completed.returncode))
expected=(root/'verification/expected_output.json').read_bytes()
if completed.stdout!=expected or completed.stderr:
    raise ValueError('Certificate output differs from the complete expected output')
result=json.loads(completed.stdout)
print(json.dumps({'status':'PASS','full_files_verified':len(manifest['files']),
                  'certificate_status':result['status'],'local_LDL_pivots':result['positive_local_LDL_pivots'],
                  'initial_minors':result['initial_minors_authenticated'],'Schur_traces':result['Schur_traces_authenticated'],
                  'scope':'Portable file identities and finite exact certificate. Analytic proof and priority require reading the manuscript and priority note.'},sort_keys=True,indent=2))
