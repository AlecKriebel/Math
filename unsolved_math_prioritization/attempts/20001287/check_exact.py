#!/usr/bin/env python3
"""Exact finite checks for the proof identities; not a numerical proof of PL.

Run: python check_exact.py
Dependency: sympy. Output is deterministic and contains no network access.
"""
import itertools
import json
from pathlib import Path
import sympy as s


def require_zero(expr):
    assert s.expand(expr) == 0, s.expand(expr)


def require_zero_matrix(m):
    assert all(s.simplify(v) == 0 for v in m), m


results = {"scope": "Exact supporting algebra; the universal inequality and equality use the cited Prékopa–Leindler theorem."}
matrices = []
for n in range(1, 7):
    for family in range(3):
        a = s.eye(n)
        for i in range(n):
            for j in range(i):
                a[i,j] = s.Rational(((i+2)*(j+3)+family)%5-2, family+2)
        if family == 1:
            a = a * s.diag(*[s.Rational(i+2,i+1) for i in range(n)])
        if family == 2:
            u = s.eye(n)
            for i in range(n-1):
                u[i,i+1] = s.Rational((-1)**i,3)
            a = a*u
        g = a.T*a
        gi = g.inv()
        x = s.Matrix(s.symbols(f'x0:{n}'))
        y = s.Matrix(s.symbols(f'y0:{n}'))
        require_zero_matrix(a.T*a.inv().T-s.eye(n))
        require_zero_matrix(gi-a.inv()*a.inv().T)
        require_zero(g.det()-a.det()**2)
        slack = (x.T*g*x+y.T*gi*y-2*x.T*y)[0]
        certificate = ((y-g*x).T*gi*(y-g*x))[0]
        require_zero(slack-certificate)
        norm_certificate = ((a*x-a.inv().T*y).T*(a*x-a.inv().T*y))[0]
        require_zero(slack-norm_certificate)
        log_ratio = -((x.T*g*x)[0]+(y.T*gi*y)[0])/2+(x.T*y)[0]
        require_zero(log_ratio+certificate/2)
        # Positive definiteness follows from A^T A with det A nonzero;
        # also check every exact leading principal minor in these examples.
        assert a.det() != 0
        assert all(g[:k,:k].det()>0 for k in range(1,n+1))
        matrices.append({"n":n,"family":family,"det_A":str(a.det()),"identities":"pass"})
results["rational_gram_tests"] = matrices

# Universal scalar normalization, symbolically in n.
n=s.symbols('n',integer=True,positive=True)
assert s.simplify((s.pi/2)**n/(2*s.pi)**n-4**(-n))==0
results["normalization"]="(pi/2)^n/(2*pi)^n = 4^(-n)"

# Equality extraction: a quadratic agreeing with a diagonal quadratic on an
# open orthant has every off-diagonal coefficient zero.
x1,x2,g11,g22,g12,d1,d2=s.symbols('x1 x2 g11 g22 g12 d1 d2')
poly=g11*x1**2+2*g12*x1*x2+g22*x2**2-d1*x1**2-d2*x2**2
assert s.diff(poly,x1,x2)==2*g12
results["equality_coefficient_check"]="mixed derivative = 2*g_ij; diagonal rescaling has zero mixed derivatives"

# Exact combinatorial identities behind the auxiliary Hessian formula.
hessian=[]
for n0 in range(2,9):
    edges=list(itertools.combinations(range(n0),2))
    hs=s.symbols('h0:'+str(len(edges)))
    h=dict(zip(edges,hs)); H=s.zeros(n0)
    for (i,j),v in h.items(): H[i,j]=H[j,i]=v
    E=sum(v*v for v in hs); S=sum(hs); U=0; V=0
    for (e,a0),(f,b0) in itertools.combinations(h.items(),2):
        if set(e)&set(f): U+=a0*b0
        else: V+=a0*b0
    rows=(H*s.ones(n0,1)); rows2=sum(v*v for v in rows)
    require_zero(S*S-E-2*U-2*V)
    require_zero(rows2-2*E-2*U)
    require_zero(sum((H*H)[i,j] for i,j in edges)-U)
    aa=s.symbols('a')
    density_coefficient=(4*(E+2*aa*U+2*aa**2*V))/8-(2*E+2*aa*U)/2+(2*E)/4
    require_zero(density_coefficient-aa**2*V)
    product_coefficient=aa*U+2*aa**2*V-aa**2*S*S
    claimed=-(aa-aa**2)*E-(aa**2-aa/2)*rows2
    require_zero(product_coefficient-claimed)
    b=s.Rational(2,1)/s.pi
    require_zero((product_coefficient-(-(2*s.pi-4)*E-(4-s.pi)*rows2)/s.pi**2).subs(aa,b))
    hessian.append({"n":n0,"independent_edges":len(edges),"identities":"pass"})
results["hessian_tests"]=hessian

# Exact wedge normalization and a counterexample to the nonsimplicial extension.
alpha=s.symbols('alpha',real=True)
require_zero(4*alpha*(s.pi-alpha)/s.pi**2-(1-4*(alpha-s.pi/2)**2/s.pi**2))
assert 23**2> (16*s.sqrt(2))**2
results["wedge_identity"]="pass"
results["nonsimplicial_obstruction"]="((2-sqrt(2))/4)^2 > 1/64 follows from 529 > 512"
results["all_checks_passed"]=True
out=Path(__file__).with_name('exact_results.json')
out.write_text(json.dumps(results,indent=2,sort_keys=True)+'\n')
print(json.dumps({"all_checks_passed":True,"rational_matrices":len(matrices),"hessian_dimensions":len(hessian),"output":out.name},sort_keys=True))
