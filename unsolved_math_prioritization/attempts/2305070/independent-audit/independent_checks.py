#!/usr/bin/env python3
"""Audit controls independent of the author's calculations; no source writes.
Exact algebraic tests are certificates only for their finite instances.
Quadrature and floating tests are diagnostics, not proofs of length/topology.
"""
from pathlib import Path
from fractions import Fraction as Q
from math import atan,pi,sqrt,exp,cos,sin
import hashlib,json,subprocess,sys,tempfile,shutil
BASE=Path(__file__).resolve().parent.parent
PUBLIC=BASE/'public'
FROZEN_MANIFEST='f6a39e0a6792db78f658e80dcc6f6efbc1299e1975aea31c1f06f24581aaf4ab'
FROZEN_PROOF='1e9ce20ecb43599cc42bda704730e67390008fd1a679779961ecf28293d7c347'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
assert sha(PUBLIC/'SHA256SUMS.json')==FROZEN_MANIFEST
assert sha(PUBLIC/'PROOF.md')==FROZEN_PROOF
m=json.loads((PUBLIC/'SHA256SUMS.json').read_text())
actual={str(p.relative_to(PUBLIC)) for p in PUBLIC.rglob('*') if p.is_file()}
assert actual==set(m['files'])|{'SHA256SUMS.json'}
assert not any(p.is_symlink() for p in PUBLIC.rglob('*'))
for name,spec in m['files'].items():
 assert sha(PUBLIC/name)==spec['sha256']
 assert (PUBLIC/name).stat().st_size==spec['bytes']
r=subprocess.run([sys.executable,str(PUBLIC/'verify.py')],capture_output=True,check=True)
assert r.stdout==(PUBLIC/'CHECKS.json').read_bytes()
r2=subprocess.run([sys.executable,str(PUBLIC/'verify_manifest.py')],capture_output=True,check=True)
assert json.loads(r2.stdout)=={'passed':True,'verified_files':9}
# Independent finite-interval quadrature: x=t/(1-t) transforms the proposed
# infinite integral into integral_0^1 2/(1+b^2*(1-t)^2) dt.
N=20000
errors=[]
for k in [-64,-17,-5,-2,-1,0,1,4,16,63]:
 b=pi*(k+.5)
 def f(t):return 2/(1+b*b*(1-t)**2)
 q=(f(0)+f(1)+sum((4 if i%2 else 2)*f(i/N) for i in range(1,N)))/(3*N)
 L=2*atan(abs(b))/abs(b)
 errors.append(abs(q-L));assert abs(q-L)<2e-10
 assert 0<L<2
 if k>=0:assert L>=1/(2*k+1)
# Exact Cayley circle and denominator identity, on independently chosen grid.
cases=0
for x in [Q(1,7),Q(2,3),Q(11,2)]:
 for y in [Q(-17,5),Q(0),Q(19,3)]:
  den=(x+1)**2+y*y
  zx=(x*x+y*y-1)/den;zy=2*y/den
  assert 1-zx*zx-zy*zy==4*x/den>0
  assert (zx-x/(x+1))**2+zy*zy==1/(x+1)**2
  cases+=1
# Audit verifier's claimed allowlist using disposable copies only.
with tempfile.TemporaryDirectory(prefix='rank580-audit-') as td:
 p=Path(td)/'public';shutil.copytree(PUBLIC,p)
 (p/'nested').mkdir();(p/'nested/SHA256SUMS.json').write_text('{}')
 (p/'__pycache__').mkdir();(p/'__pycache__/ignored.txt').write_text('extra')
 ignored=subprocess.run([sys.executable,str(p/'verify_manifest.py')],capture_output=True)
 assert ignored.returncode==0
result={
 'passed':True,
 'frozen_manifest_sha256':FROZEN_MANIFEST,
 'frozen_proof_sha256':FROZEN_PROOF,
 'strict_public_inventory_count':len(actual),
 'author_replay_exact_bytes_match':True,
 'author_manifest_replay':json.loads(r2.stdout),
 'independent_component_quadrature_cases':len(errors),
 'independent_component_quadrature_max_abs_error':max(errors),
 'independent_cayley_exact_cases':cases,
 'manifest_hardening_observation':'The supplied verifier ignores any nested SHA256SUMS.json and every file under __pycache__. The separate strict inventory confirms the actual frozen package contains no ignored extra files.',
 'scope':'Finite checks do not prove infinite divergence or component topology. Those claims were audited in the written proof.'
}
print(json.dumps(result,indent=2,sort_keys=True))
