"""Non-mutating standard-library replay; run without Python -O."""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

BASE = Path(__file__).resolve().parent
if not __debug__:
    raise RuntimeError('Assertions must be enabled: do not use -O')
env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1')
checks = [
 ('check_extensions.py', []), ('check_square.py', []), ('check_phase.py', []),
 ('computation/verify_certificate.py', [str(p.relative_to(BASE)) for p in sorted((BASE/'computation').glob('*_20_7.json'))]),
 ('computation/test_verifier.py', []),
 ('computation/verify_unsat_certificate.py', ['computation/dodecahedron_17_6_unsat.json']),
 ('computation/test_unsat_verifier.py', []),
 ('computation/check_numerator_gap.py', []), ('computation/check_exact_benchmark.py', []),
]
results=[]
for script,args in checks:
    result=subprocess.run([sys.executable, '-B', script, *args], cwd=BASE, env=env, text=True, capture_output=True)
    if result.returncode:
        raise RuntimeError(f'{script}: {result.stdout}\n{result.stderr}')
    expected={'check_extensions.py':'extension_checks.json','check_square.py':'square_checks.json'}.get(script)
    if expected and json.loads(result.stdout)!=json.loads((BASE/expected).read_text()):
        raise RuntimeError(f'{script}: stored result mismatch')
    results.append({'script':script,'arguments':args,'returncode':result.returncode,'stdout':result.stdout,'stderr':result.stderr})
for line in (BASE/'computation/SHA256SUMS').read_text().splitlines():
    digest,name=line.split(maxsplit=1)
    name=name.lstrip('*')
    if hashlib.sha256((BASE/'computation'/name).read_bytes()).hexdigest()!=digest:
        raise RuntimeError(f'Certificate hash mismatch: {name}')
print(json.dumps({'standard_library_only':True,'checks':results,'certificate_hashes_verified':8,'result':'PASS'},indent=2))
