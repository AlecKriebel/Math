#!/usr/bin/env python3
"""Independent null-Lagrangian and failed-shortcut controls, not PDE solving."""
from pathlib import Path
import sympy as s
import json,hashlib
count=0

def ck(v):
 global count
 assert v
 count+=1

f=s.symbols('f0:9');h=s.symbols('h0:9');F=s.Matrix(3,3,f);H=s.Matrix(3,3,h);t=s.symbols('t')
# Levi-Civita formula independently constructs cofactors and their linearization.
def cof(A):
 return s.Matrix(3,3,lambda i,j:s.expand(sum(s.LeviCivita(i,a,b)*s.LeviCivita(j,c,d)*A[a,c]*A[b,d] for a,b,c,d in __import__('itertools').product(range(3),repeat=4))/2))
C=cof(F);DC=s.Matrix(3,3,lambda i,j:s.expand(sum(s.diff(C[i,j],f[k])*h[k] for k in range(9))))
for i in range(9):ck(s.expand(C[i]-F.cofactor_matrix()[i])==0)
for i in range(9):ck(s.expand(cof(F+H)[i]-C[i]-DC[i]-cof(H)[i])==0)
ck(s.expand((F+H).det()-F.det()-sum(C[i]*H[i] for i in range(9))-sum(cof(H)[i]*F[i] for i in range(9))-H.det())==0)

x,y,z=s.symbols('x y z');coords=(x,y,z);bubble=x*(1-x)*y*(1-y)*z*(1-z)
phi=s.Matrix([bubble,2*bubble,-3*bubble]);Dphi=phi.jacobian(coords)
fixtures=[s.Matrix([x+y*z,y+x*z,z+x*y]),s.Matrix([x+x*y,y+y*z,z+x*z]),s.Matrix([x+y**2,y+z**2,z]),s.Matrix([x+x**2+y*z,y+y**2+x*z,z+z**2+x*y])]
Ls=list(C)+[F.det()]
for u in fixtures:
 DF=u.jacobian(coords);sub=dict(zip(f,DF))
 for L in Ls:
  stress=s.Matrix(3,3,[s.diff(L,v) for v in f]).subs(sub,simultaneous=True)
  for i in range(3):ck(s.expand(sum(s.diff(stress[i,j],coords[j]) for j in range(3)))==0)
  integ=s.expand(sum(stress[i]*Dphi[i] for i in range(9)))
  ck(s.integrate(integ,(x,0,1),(y,0,1),(z,0,1))==0)
# Exact countercontrols: spatially varying determinant/cofactor multipliers.
phi1=s.Matrix([bubble,0,0]);phi2=s.Matrix([0,bubble,0])
ck(s.integrate(x*s.diff(phi1[0],x),(x,0,1),(y,0,1),(z,0,1))==s.Rational(-1,216))
ck(s.integrate(y*s.diff(phi2[1],y),(x,0,1),(y,0,1),(z,0,1))==s.Rational(-1,216))

# Strict convexity in all minors does not imply matrix-stress monotonicity.
# g(F,C,d)=(|F|^2+|C|^2+(d-10)^2)/2+1/d, on d>0.
d=s.symbols('d',positive=True);hp=d-10-1/d**2
ck(s.diff(hp,d)==1+2/d**3)
W=(sum(v*v for v in F)+sum(v*v for v in C)+(F.det()-10)**2)/2+1/F.det()
stress=s.Matrix(3,3,[s.diff(W,v) for v in f])
I=s.eye(3);R=s.diag(-1,-1,1)
SI=stress.subs(dict(zip(f,I)),simultaneous=True);SR=stress.subs(dict(zip(f,R)),simultaneous=True)
ck(I.det()==R.det()==1);ck(SI==-7*I);ck(SR==-7*R)
ck(sum((SR[i]-SI[i])*(R[i]-I[i]) for i in range(9))==-56)
ck(W.subs(dict(zip(f,I)),simultaneous=True)==W.subs(dict(zip(f,R)),simultaneous=True))
# These affine maps have different traces; this is no same-boundary counterexample.
ck(I!=R)
root=Path(__file__).parent
r={'verdict':'PASS','independent_assertions':count,'polynomial_maps':len(fixtures),
 'individual_minor_null_lagrangians':10,'variable_multiplier_nonzero_integral':'-1/216',
 'strictly_polyconvex_nonmonotone_stress_pairing':-56,
 'reviewed_artifact_sha256':hashlib.sha256((root/'author_replay/PARTIAL_RESULT.md').read_bytes()).hexdigest(),
 'checker_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
 'scope':'Exact identities and failure-of-shortcut controls, not a full-domain PDE uniqueness theorem or a same-boundary counterexample.'}
(root/'independent_results.json').write_text(json.dumps(r,indent=2,sort_keys=True)+'\n');print(json.dumps(r,sort_keys=True))
