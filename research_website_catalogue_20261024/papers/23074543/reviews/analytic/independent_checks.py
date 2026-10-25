#!/usr/bin/env python3
"""Exact bounded diagnostics; the universal proof is in EARLY_DERIVATION.md.

This file reads no manuscript, archive code, external data, or other reviews.
It writes one JSON receipt in its own directory. No claim follows from samples.
"""
from pathlib import Path
import datetime
import hashlib
import itertools
import json
import platform
import sys
import sympy as s

out = Path(__file__).resolve().parent
results = []

a,b,Y,Z,X = s.symbols('a b Y Z X')
P = (X**2+Y**2+Z**2-5)**2-4*(4-Y**2)*(1-Z**2)
g = s.groebner([a*a+Y*Y-4,b*b+Z*Z-1],a,b,Y,Z)
rem = g.reduce(s.expand(P.subs(X,a+b)))[1]
assert rem == 0
assert P.subs({X:0,Y:0,Z:1}) == 16
results.append({'id':'nongeneric_separator','method':'Exact polynomial division modulo a^2+Y^2=4 and b^2+Z^2=1','remainder':str(rem),'P_at_e3':16,'scope':'Universal algebraic identity conditional on the two circle relations; not a numerical support sample.'})

# Six Vandermonde columns give a prescribed rank-(2,2,2) system in R^5.
# The columns are intentionally not orthonormal.
V = s.Matrix([[s.Integer(t)**k for t in range(1,7)] for k in range(5)])
A = [V[:,2*i:2*i+2] for i in range(3)]
ranks=[]
for n in range(1,4):
    for J in itertools.combinations(range(3),n):
        AJ=s.Matrix.hstack(*[A[j] for j in J])
        rank=AJ.rank()
        assert rank==min(5,2*n)
        ranks.append({'J_1_based':[j+1 for j in J],'rank':rank})
AJ=s.Matrix.hstack(A[0],A[1])
u=AJ.T.nullspace()[0]
assert A[2].T*u != s.zeros(2,1)
v1=s.Matrix([s.Rational(3,5),s.Rational(4,5)])
v2=s.Matrix([s.Rational(5,13),s.Rational(12,13)])
assert (v1.T*v1)[0]==1 and (v2.T*v2)[0]==1
wparams=AJ.T.gauss_jordan_solve(v1.col_join(v2))
w=wparams[0].subs({p:0 for p in wparams[1]})
assert AJ.T*w==v1.col_join(v2)
eps=s.symbols('eps',positive=True)
for j,v in enumerate([v1,v2]):
    t=A[j].T*(u+eps*w)
    assert s.simplify(t-eps*v)==s.zeros(2,1)
    p=s.simplify(A[j]*t/s.sqrt((t.T*t)[0]))
    assert s.simplify(p-A[j]*v)==s.zeros(5,1)
t3=A[2].T*(u+eps*w)
q3=s.expand((t3.T*t3)[0])
assert q3.subs(eps,0)>0
p3=s.simplify(A[2]*t3/s.sqrt(q3))
p30=A[2]*(A[2].T*u)/s.sqrt(((A[2].T*u).T*(A[2].T*u))[0])
assert s.simplify(p3.applyfunc(lambda z:s.limit(z,eps,0,dir='+'))-p30)==s.zeros(5,1)
results.append({'id':'nonorthonormal_GP_two_vanishing_blocks','ranks':ranks,'u':list(map(str,u)),'w':list(map(str,w)),'third_block_squared_projection_at_zero':str(q3.subs(eps,0)),'exact_fixed_support_points':True,'remaining_support_limit_exact':True,'scope':'One exact GP example testing simultaneous two-block prescription with nonorthonormal ellipsoidal parametrizations; generic and universal arguments remain proofs in EARLY_DERIVATION.md.'})

# A lower-dimensional ellipsoid in R^4: ambient-null directions must not
# introduce spurious uniqueness or impose full-dimensionality.
u1,u2,u3,u4=s.symbols('u1 u2 u3 u4',real=True)
A0=s.Matrix([[2,0],[0,3],[0,0],[0,0]])
un=s.Matrix([u1,u2,u3,u4]);q=(A0.T*un).dot(A0.T*un)
p=A0*A0.T*un/s.sqrt(q)
ellipse=s.factor(p[0]**2/4+p[1]**2/9-1)
assert ellipse==0 and p[2]==p[3]==0
assert A0.rank()==2 and len(A0.T.nullspace())==2
results.append({'id':'lower_dimensional_nonround_disc','ellipse_identity_remainder':str(ellipse),'kernel_codimension':A0.rank(),'ambient_dimension':4,'scope':'Exact identity on q>0, covering all regular normals of this example; the singular kernel has no singleton exposed face.'})

t,c=s.symbols('t c',real=True)
right=(X-c)**2+Y**2-1;left=(X+c)**2+Y**2-1
xp=c+(1-t*t)/(1+t*t);yp=2*t/(1+t*t)
assert s.factor(right.subs({X:xp,Y:yp}))==0
assert s.factor((left-right))==4*X*c
assert s.factor_list(right)[0]==1 and len(s.factor_list(right)[1])==1
assert s.factor_list(left)[0]==1 and len(s.factor_list(left)[1])==1
results.append({'id':'rank_one_stadium_boundary','translated_circle_parametrization_remainder':'0','difference_of_defining_polynomials':str(s.expand(left-right)),'both_circle_polynomials_irreducible_over_C_for_fixed_real_c_nonzero':'Each is a smooth plane affine conic: its projective quadratic form has determinant -1, so it cannot factor into lines over C.','scope':'Symbolic identity plus a written smooth-conic argument; two-dimensional exposed arc families belong to distinct conics when c>0.'})

receipt={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'python':sys.executable,'python_version':platform.python_version(),'sympy_version':s.__version__,'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'status':'PASS_ALL_EXACT_DIAGNOSTICS','universal_proof_location':'EARLY_DERIVATION.md','sample_checks_are_not_universal_proofs':True,'results':results}
(out/'CHECK_RESULTS.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps(receipt,indent=2))
