#!/usr/bin/env python3
"""Optional exact Saito check for the two-cubic boundary; requires SymPy."""
from itertools import combinations
import json
import sympy as s
x,y,z=s.symbols('x y z'); variables=(x,y,z)
forms=[x,y,z,x-y,x-z,y-z,x+y-z]
monomials=[x**i*y**j*z**(3-i-j) for i in range(4) for j in range(4-i)]
unknown=s.symbols('c:30')
generic=[sum(unknown[i*10+j]*m for j,m in enumerate(monomials)) for i in range(3)]
def restrict(p,a):
    v=next(v for v in variables if s.diff(a,v))
    return s.expand(p.subs(v,s.solve(a,v)[0]))
eq=[]
for a in forms:
    eq.extend(s.Poly(restrict(sum(s.diff(a,v)*t for v,t in zip(variables,generic)),a),*variables).coeffs())
mat,_=s.linear_eq_to_matrix(eq,unknown)
null=mat.nullspace()
assert len(null)==8
basis=[]
for vec in null:
    basis.append([sum(vec[i*10+j]*m for j,m in enumerate(monomials)) for i in range(3)])
Q=s.prod(forms)
euler=[x,y,z]
for a,b in combinations(basis,2):
    det=s.factor(s.Matrix.hstack(s.Matrix(euler),s.Matrix(a),s.Matrix(b)).det())
    if det:
        ratio=s.cancel(det/Q)
        assert not ratio.free_symbols and ratio
        checks=0
        for f in forms:
            for theta in (euler,a,b):
                assert restrict(sum(s.diff(f,v)*t for v,t in zip(variables,theta)),f)==0
                checks+=1
        print(json.dumps({'degrees':[1,3,3],'cubic_derivation_space_dimension':len(null),
                          'basis':[[str(t) for t in theta] for theta in (euler,a,b)],
                          'determinant_over_Q':str(ratio),'tangency_checks':checks},indent=2))
        break
else:
    raise AssertionError('No independent cubic pair found')
