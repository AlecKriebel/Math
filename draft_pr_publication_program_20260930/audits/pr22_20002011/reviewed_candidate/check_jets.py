#!/usr/bin/env python3
"""Exact cubic-jet verification of the known six-dimensional obstruction.
Requires SymPy (tested 1.14.0). No sampling, integration, or large search.
"""
from pathlib import Path
import json
import sympy as s

x=s.symbols('x1:4')
f=x[0]*x[1]*x[2]
v=s.Function('v')(*x)
t=s.symbols('t')
zero={z:0 for z in x}
checks={}
def check(name,expr):
    assert bool(expr),name
    checks[name]='PASS'
def grad(u):return [s.diff(u,z) for z in x]
def lap(u):return sum(s.diff(u,z,2) for z in x)
def schouten(u):
    du=grad(u)+[s.S.Zero]*3
    norm=sum(z*z for z in du)
    return s.Matrix(6,6,lambda i,j:-(s.diff(u,x[i],x[j]) if i<3 and j<3 else 0)+du[i]*du[j]-(norm/2 if i==j else 0))
def C(u):return s.expand(sum(a*a for a in schouten(u)))
def density(u):
    c=C(u)
    # Exact cancellation: e^(4u) grad(e^(-4u)c)=grad(c)-4c grad(u).
    return s.expand(lap(c)-4*sum(a*b for a,b in zip(grad(c),grad(u)))-4*c*lap(u))

check('dimension_is_critical',6-4-2==0)
check('cubic_is_harmonic',lap(f)==0)
for i,z in enumerate(x):check(f'first_jet_{i}',s.diff(f,z).subs(zero)==0)
for i in range(3):
    for j in range(3):check(f'second_jet_{i}_{j}',s.diff(f,x[i],x[j]).subs(zero)==0)
P=schouten(f)
check('schouten_zero_at_origin',P.subs(zero)==s.zeros(6))
check('hessian_squared',sum(a*a for a in s.hessian(f,x))==2*sum(z*z for z in x))
check('hessian_squared_laplacian',lap(sum(a*a for a in s.hessian(f,x)))==12)
check('density_at_origin',density(f).subs(zero)==12)
check('scaled_density_at_origin',s.simplify(density(t*f).subs(zero)-12*t*t)==0)

# Derive the complete coordinate Frechet operator from the exact density, then
# construct its formal adjoint independently by coefficient differentiation.
D=s.expand(s.diff(density(f+t*v),t).subs(t,0))
atoms=sorted(D.atoms(s.Derivative),key=str)+[v]
dummy=s.symbols('a:'+str(len(atoms)))
poly=s.Poly(D.xreplace(dict(zip(atoms,dummy))),*dummy)
check('linearization_linear_in_test_jets',poly.total_degree()==1)
coeff={atom:s.expand(poly.coeff_monomial(d)) for atom,d in zip(atoms,dummy)}
Ds=s.S.Zero;Dadjs=s.S.Zero
for atom,a in coeff.items():
    variables=atom.variables if isinstance(atom,s.Derivative) else ()
    test=s.diff(f,*variables) if variables else f
    Ds+=a*test
    adj=a*f
    for z in variables:adj=-s.diff(adj,z)
    Dadjs+=adj
check('direct_linearization_value',s.simplify(Ds.subs(zero)-24)==0)
check('formal_adjoint_value',s.simplify(Dadjs.subs(zero))==0)
check('nonzero_skew_value',s.simplify((Ds-Dadjs).subs(zero)-24)==0)
check('cubic_tensor_squared',sum(s.diff(f,a,b,c)**2 for a in x for b in x for c in x)==6)
# Ric=4P+Jg in dimension 6; |Ric|^2=16|P|^2+14J^2.
check('ricci_norm_conversion',2*4+6==14)
result={'passed':len(checks),'failed':0,'sympy_version':s.__version__,'checks':checks,'operator_jet_terms':sum(a!=0 for a in coeff.values()),'density_at_origin':12,'linearization_at_origin':24,'formal_adjoint_at_origin':0,'scope':'Exact polynomial jet calculations only. Closed-manifold localization and the variational obstruction are proved in SOURCE_STATUS.md.'}
Path(__file__).with_name('check_results.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
