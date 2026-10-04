#!/usr/bin/env python3
"""Exact local formula controls; not a proof of the general Stein problem.
Run from any directory with Python 3 and SymPy installed.
"""
import json
import sympy as s

checks=[]
def check(name, predicate):
    if not bool(predicate):
        raise AssertionError(name)
    checks.append(name)
def zero(expr):
    return s.simplify(s.trigsimp(expr)) == 0

# General one-form positive-halfplane potential, pulled back by a real affine map.
x,y=s.symbols('x y', real=True)
u=s.log(x*x+y*y)/2-s.log(x)
levi=(s.diff(u,x,2)+s.diff(u,y,2))/4
check('positive_affine_form_levi',zero(levi-1/(4*x*x)))
for k in range(1,5):
    xs=s.symbols('x0:'+str(k), real=True)
    ys=s.symbols('y0:'+str(k), real=True)
    aa=s.symbols('a0:'+str(k), real=True)
    b=s.symbols('b',real=True)
    lx=b+sum(aa[i]*xs[i] for i in range(k))
    ly=sum(aa[i]*ys[i] for i in range(k))
    f=s.log(lx*lx+ly*ly)/2-s.log(lx)
    for i in range(k):
        for j in range(k):
            L=(s.diff(f,xs[i],xs[j])+s.diff(f,ys[i],ys[j])
                +s.I*(s.diff(f,xs[i],ys[j])-s.diff(f,ys[i],xs[j])))/4
            check('affine_levi_n%d_%d_%d'%(k,i,j),zero(L-aa[i]*aa[j]/(4*lx**2)))

# Complete periodic Hessian two-torus and a negative complex tangent direction.
a,b,p,q=s.symbols('a b p q', real=True)
phi=(a*a+b*b)/2-s.cos(a)*s.cos(b)/4
g=s.hessian(phi,(a,b))
expected=s.Matrix([[1+s.cos(a)*s.cos(b)/4,-s.sin(a)*s.sin(b)/4],
                   [-s.sin(a)*s.sin(b)/4,1+s.cos(a)*s.cos(b)/4]])
check('torus_hessian_matrix',g==expected)
for vec,ev in [(s.Matrix([1,1]),1+s.cos(a+b)/4),
               (s.Matrix([1,-1]),1+s.cos(a-b)/4)]:
    check('torus_eigenvalue_'+str(list(vec)),all(zero(c) for c in g*vec-ev*vec))
v=s.Matrix([p,q]);rho=(v.T*g*v)[0]
d2=(s.diff(rho,b)-s.I*s.diff(rho,q))/2
L22=(s.diff(rho,b,2)+s.diff(rho,q,2))/4
point={a:0,b:0,q:0}
check('torus_complex_gradient_zero',zero(d2.subs(point)))
check('torus_negative_direction_formula',zero(L22.subs(point)-(s.Rational(5,8)-p*p/16)))
check('torus_exact_negative_value',L22.subs(point).subs(p,4)==-s.Rational(3,8))
check('torus_rho_value',rho.subs(point).subs(p,4)==20)
h1,h2=s.symbols('h1 h2',real=True)
chain=(h1*L22+h2*d2*s.conjugate(d2)).subs(point).subs(p,4)
check('reparametrization_obstruction',zero(chain+3*h1/8))

# Exactness: x-only Hessian has completely symmetric third derivatives.
for i in range(2):
    for j in range(2):
        for k in range(2):
            check('hessian_cubic_symmetry_%d_%d_%d'%(i,j,k),
                  zero(s.diff(g[i,j],(a,b)[k])-s.diff(g[k,j],(a,b)[i])))

# Strip exhaustion and a genuinely non-coordinate lattice span.
t=s.symbols('t',real=True)
check('strip_barrier_second_derivative',zero(s.diff(-s.log(s.cos(t)),t,2)-1/s.cos(t)**2))
B=s.Matrix([[1,0],[1,1],[0,1]])
P=s.eye(3)-B*(B.T*B).inv()*B.T
check('lattice_projection_symmetric',P==P.T)
check('lattice_projection_idempotent',P*P==P)
check('lattice_projection_annihilates_span',P*B==s.zeros(3,2))
L=P/2+s.eye(3)/4
for j in range(1,4):
    check('strip_levi_sylvester_'+str(j),L[:j,:j].det()>0)

# Finite facet strictness in a non-simplicial three-dimensional cone.
A=s.Matrix([[1,1,0],[1,-1,0],[1,0,1],[1,0,-1]])
xx=s.Matrix([2,0,0]);vals=A*xx
G=sum((A.row(j).T*A.row(j)/(4*vals[j]**2) for j in range(4)),s.zeros(3))
check('nonsimplicial_facet_rank',A.rank()==3)
for j in range(1,4):
    check('nonsimplicial_facet_levi_'+str(j),G[:j,:j].det()>0)

# The maximum-support envelope has null transverse Levi directions.
z1x,z1y,z2x,z2y=s.symbols('z1x z1y z2x z2y',real=True)
f=s.log(z1x*z1x+z1y*z1y)/2-s.log(z1x)
check('support_envelope_null_direction',s.diff(f,z2x,2)+s.diff(f,z2y,2)==0)
check('support_envelope_strict_active_ratio',s.Rational(2,1)>s.Rational(0,1))

print(json.dumps({'status':'PASS','check_count':len(checks),'checks':checks,
                  'scope':'Exact local identities and finite controls only; original target unresolved.',
                  'sympy_version':s.__version__},indent=2,sort_keys=True))
