#!/usr/bin/env python3
"""Reproducible finite checks supporting, not replacing, PROOF.md.

Run with Python 3, SymPy, and NumPy: python verify_math.py
No downloaded source documents or datasets are required.
"""
import json
import math
import platform
import sympy as sp
import numpy as np

if not __debug__:
    raise RuntimeError('Run without -O or PYTHONOPTIMIZE; assertions must remain active.')


def check_zero(expr):
    assert sp.simplify(expr) == 0, expr


def coordinate_model(variables, metric, cubic):
    n = len(variables)
    f = []
    for degree in (1, 2, 3):
        from itertools import combinations_with_replacement
        for idx in combinations_with_replacement(range(n), degree):
            f.append(sp.prod(variables[i] for i in idx))
    indices = []
    for degree in (1, 2, 3):
        from itertools import combinations_with_replacement
        indices.extend(combinations_with_replacement(range(n), degree))
    gamma = lambda i,j,k: (
        sp.diff(metric[j,k],variables[i])
        +sp.diff(metric[i,k],variables[j])
        -sp.diff(metric[i,j],variables[k])-cubic(i,j,k))/2
    target = []
    for idx in indices:
        if len(idx) == 1:
            target.append(0)
        elif len(idx) == 2:
            target.append(metric[idx[0],idx[1]])
        else:
            i,j,k = idx
            target.append(sp.diff(metric[i,j],variables[k])+gamma(i,j,k))
    evaluation = sp.Matrix([
        [sp.diff(q,*[variables[i] for i in idx]) for q in f]
        for idx in indices])
    assert evaluation.det() != 0
    a = sp.simplify(evaluation.inv()*sp.Matrix(target))
    phi = -a
    residual_count = 0
    for i in range(n):
        check_zero(sum(phi[A]*sp.diff(f[A],variables[i]) for A in range(len(f))))
        residual_count += 1
        for j in range(n):
            check_zero(sum(sp.diff(f[A],variables[i])*sp.diff(phi[A],variables[j])
                           for A in range(len(f)))-metric[i,j])
            residual_count += 1
            for k in range(n):
                check_zero(sum(sp.diff(f[A],variables[i],variables[j])
                               *sp.diff(phi[A],variables[k]) for A in range(len(f)))
                           -gamma(i,j,k))
                gamma_star = sp.diff(metric[j,k],variables[i])-gamma(i,k,j)
                check_zero(sum(sp.diff(phi[A],variables[i],variables[j])
                               *sp.diff(f[A],variables[k]) for A in range(len(f)))
                           -gamma_star)
                residual_count += 2
    return f,phi,gamma,residual_count,evaluation.det()


x = sp.symbols('x', real=True)
# Unbounded cubic coefficient, positive metric on all R.
one = coordinate_model([x],sp.Matrix([[1]]),lambda i,j,k:x)
u,v = sp.symbols('u v', real=True)
# det(g)=exp(u+v)+u^2 exp(u)+v^2 exp(v)>0 globally.
g = sp.Matrix([[sp.exp(u)+v*v,u*v],[u*v,sp.exp(v)+u*u]])
f,phi,gamma,count,det_eval = coordinate_model([u,v],g,lambda i,j,k:1+i+j+k)
check_zero(g.det()-(sp.exp(u+v)+u*u*sp.exp(u)+v*v*sp.exp(v)))

# Full ambient symmetric completion at representative points.
# It is the exact block construction from Section 6, evaluated numerically.
F = sp.Matrix(f).jacobian([u,v])
P = phi.jacobian([u,v])
points = [(0.,0.),(1.,-1.),(-2.,2.),(3.,2.)]
samples = []
for point in points:
    sub = {u:point[0],v:point[1]}
    tangent = np.array(F.subs(sub),dtype=float)
    dphi = np.array(P.subs(sub),dtype=float)
    Q,R = np.linalg.qr(tangent,mode='complete')
    Qt,Qn = Q[:,:2],Q[:,2:]
    Rt = R[:2,:]
    HQ = dphi @ np.linalg.inv(Rt)
    A = Qt.T @ HQ
    Bt = Qn.T @ HQ
    assert np.max(np.abs(A-A.T)) < 1e-8
    t = float(np.trace(np.linalg.inv(A))*np.sum(Bt**2))
    lam = 1+t
    H = Qt@A@Qt.T + Qn@Bt@Qt.T + Qt@Bt.T@Qn.T + 2*lam*Qn@Qn.T
    H=(H+H.T)/2
    minimum=float(np.linalg.eigvalsh(H).min())
    residual=float(np.max(np.abs(H@tangent-dphi)))
    assert minimum>0
    assert residual<1e-6
    samples.append({'point':point,'lambda':lam,'minimum_eigenvalue':minimum,
                    'H_df_minus_dphi_max_abs':residual})

# Homogeneous scaling and cubic cancellation in Turn 1.
t,z,eps=sp.symbols('t z eps',real=True,nonzero=True)
check_zero((z/sp.sqrt(2))**2+(-z/sp.sqrt(2))**2-z*z)
check_zero((z/sp.sqrt(2))**3+(-z/sp.sqrt(2))**3)
check_zero(eps**(-3)*(eps*t)**3-t**3)

out={
    'status':'PASS',
    'python':platform.python_version(),'sympy':sp.__version__,'numpy':np.__version__,
    'exact_residuals_checked':one[3]+count,
    'one_dimensional_derivative_jet_determinant':str(one[4]),
    'two_dimensional_derivative_jet_determinant':str(det_eval),
    'symbolic_checks':['conormal exactness','metric','specified connection',
                       'specified dual connection','positive test metric determinant',
                       'quadratic/cubic scaling and cancellation'],
    'positive_hessian_completion_samples':samples,
    'dimension_bound_samples':{str(n):math.comb(2*n+4,3) for n in range(1,6)},
    'limitations':'Finite symbolic and numerical checks do not prove the global theorem; '
                  'its global bundle, topology, and extension arguments are in PROOF.md.'
}
print(json.dumps(out,indent=2))
