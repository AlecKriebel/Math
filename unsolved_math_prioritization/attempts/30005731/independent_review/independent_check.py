"""Independent finite controls, subordinate to the written geometric review."""
import sympy as s
import json, hashlib
from pathlib import Path
import argparse
a=argparse.ArgumentParser();a.add_argument('--author-dir',type=Path);a.add_argument('--source-dir',type=Path);args=a.parse_args()
p=args.author_dir;q=args.source_dir
checks=[]
def eq(a,b,n):
 d=s.simplify(s.trigsimp(a-b))
 assert (all(v==0 for v in d) if isinstance(d,s.MatrixBase) else d==0),n
 checks.append(n)
b,B=s.symbols('b B',real=True)
g=s.Matrix([5-s.cos(b),s.sin(b)]);t=g.diff(b);W=g+(B-b)*t
norm=lambda v:(v.T*v)[0]
eq(norm(t),1,'circle_speed')
eq(s.det(s.Matrix.hstack(t,t.diff(b))),-1,'circle_signed_curvature')
eq(W.diff(b),(B-b)*s.Matrix([s.cos(b),-s.sin(b)]),'involute_derivative')
eq(norm(W-s.Matrix([5,0])),1+(B-b)**2,'involute_outside_circle')
eq(norm(W.diff(b)),(B-b)**2,'involute_speed_squared')
eq(s.diff(norm(W-s.Matrix([4,0])),b),2*(B-b)*(s.cos(b)-1),'lower_route_distance_monotonicity')
eq(norm(g-s.Matrix([4,0])),4*s.sin(b/2)**2,'circle_lower_route_distance')
eq(norm(g),26-10*s.cos(b),'circle_radial_distance')
z=s.symbols('z',real=True);eta=(4*z*(1-z))**4
for j in range(4):
 for c in [0,1]:eq(s.diff(eta,z,j).subs(z,c),0,f'bump_endpoint_derivative_{j}_{c}')
eq(s.integrate(eta,(z,0,1))/100,s.Rational(32,7875),'independent_bump_mass')
eq(100*s.integrate(s.diff(eta,z)**2,(z,0,1)),s.Rational(5242880,9009),'independent_bump_energy')
sg,U,Delta=s.symbols('sigma U Delta',positive=True)
eq(sg*(U-Delta)-(sg*U-Delta),-(sg-1)*Delta,'endpoint_defect')
source=[]
for f in (json.loads((p/'source_manifest.json').read_text())['files'] if p is not None and q is not None else []):
 data=(q/f['file']).read_bytes();ok=hashlib.sha256(data).hexdigest()==f['sha256'] and len(data)==f['bytes'];assert ok
 source.append({'filename':f['file'],'hash_verified':ok})
# Fresh high-precision diagnostics of analytic constants; not the proof certificate.
import mpmath as m
m.mp.dps=60
beta=m.acos(m.mpf(1)/5);BB=beta+m.mpf(7)/10;UU=m.sqrt(24)-1+m.mpf(7)/10
GG=m.mpf(23)/20*UU-3-BB;aa=m.sqrt(2*GG)
assert beta<m.mpf('1.38')<m.mpf('1.39')<BB-aa
assert 3+2*m.sin(BB/2)-UU>m.mpf('.1')
print(json.dumps({'status':'PASS','symbolic_assertions':len(checks),'assertions':checks,'source_hashes':source,'diagnostic_constants':{'beta0':str(beta),'B_minus_a':str(BB-aa),'G':str(GG),'lower_route_gap_at_B':str(3+2*m.sin(BB/2)-UU)},'scope':'Independent identities and source hashes. Continuous geodesic and feasibility conclusions depend on the separately audited written proofs.'},indent=2))
