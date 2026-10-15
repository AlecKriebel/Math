#!/usr/bin/env python3
"""Local frame diagnostics only; no global linking or injectivity certificate."""
import json
from pathlib import Path
import sympy as s
k,tau,taup=s.symbols('k tau taup',real=True)
T=s.Matrix([1,0,0]);N=s.Matrix([0,1,0]);B=s.Matrix([0,0,1])
Tp=k*N;Np=-k*T+tau*B;Bp=-tau*N
assert T.cross(N)==B and B.cross(T)==N
assert Tp.dot(B)==0 and Bp.dot(T)==0
assert s.simplify(Tp.dot(N)+T.dot(Np))==0
assert s.simplify(Np.dot(B)+N.dot(Bp))==0
assert Np.dot(B)==tau
Bpp=-taup*N-tau*Np
assert s.expand(Bpp.dot(B.cross(Bp)))==tau*tau*k
# Constant unit binormal of the unit circle.
u=s.symbols('u',real=True);g=s.Matrix([s.cos(u),s.sin(u),0]);cross=g.diff(u).cross(g.diff(u,2))
assert s.simplify(cross-B)==s.zeros(3,1)
out={'scope':'Local algebra only; the source question remains unresolved','darboux_orthogonality':True,'twist_density':'tau','spherical_curvature_numerator':'tau^2 k','planar_circle_binormal_constant':True,'all_passed':True,'sympy_version':s.__version__}
Path(__file__).with_name('verification.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
