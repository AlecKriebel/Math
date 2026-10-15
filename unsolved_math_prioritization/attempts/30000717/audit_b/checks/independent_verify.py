#!/usr/bin/env python3
"""Second-audit exact controls, derived independently of the author's program."""
import json
from itertools import permutations, product
import sympy as s

x,y,z,t,a,b,c=s.symbols('x y z t a b c')
V=(x,y,z)
R=sum(u**6 for u in V)-sum(u**4*w**2 for u,w in permutations(V,2))+3*x**2*y**2*z**2
P=[(1,e,f) for e,f in product((1,-1),repeat=2)]+[(0,1,1),(0,1,-1),(1,0,1),(1,0,-1),(1,1,0),(1,-1,0)]
monomials=[x**3,y**3,z**3,x*x*y,x*x*z,y*y*x,y*y*z,z*z*x,z*z*y,x*y*z]
E=s.Matrix([[m.subs(dict(zip(V,p))) for m in monomials] for p in P])
checks=[]
def require(condition,label):
    assert condition,label
    checks.append(label)

require(E.det()==128,'Independent 10-by-10 evaluation determinant equals +128')
require(E.nullspace()==[],'Cubic evaluation map has trivial kernel')
ranks={}
for d in (0,1,2,3):
    mons=[x**i*y**j*z**(d-i-j) for i in range(d+1) for j in range(d-i+1)]
    A=s.Matrix([[m.subs(dict(zip(V,p))) for m in mons] for p in P])
    ranks[d]=A.rank()
    require(A.rank()==len(mons),f'Degree-{d} evaluation has full column rank')
F=sum(u**3 for u in (a,b,c))-sum(u*u*w for u,w in permutations((a,b,c),2))+3*a*b*c
require(s.expand(F-(a-b)**2*(a+b-c)-c*(a-c)*(b-c))==0,'Ordered Schur identity')
require(s.expand(F.subs({a:x*x,b:y*y,c:z*z})-R)==0,'Schur specialization equals R')
D=[s.diff(R,u) for u in V]
K=[V[j]*D[i] for i in range(3) for j in range(3) if i!=j]
J=[V[j]*D[i]-V[i]*D[j] for i in range(3) for j in range(i+1,3)]
for index,p in enumerate(P):
    substitutions=dict(zip(V,(t*u for u in p)))
    require(s.expand(R.subs(substitutions))==0,f'R vanishes identically on line {index}')
    require(all(s.expand(g.subs(substitutions))==0 for g in D),f'Gradient vanishes identically on line {index}')
    require(all(s.expand(g.subs(substitutions))==0 for g in J+K),f'Both ideal generator lists vanish on line {index}')
for i in range(3):
    substitutions={u:(t if i==j else 0) for j,u in enumerate(V)}
    require(s.expand(R.subs(substitutions))==t**6,f'R equals t^6 on axis {i}')
    require(all(s.expand(g.subs(substitutions))==0 for g in J+K),f'Both ideal generator lists vanish on axis {i}')
require(s.expand(sum(u*g for u,g in zip(V,D))-6*R)==0,'Euler identity for actual gradient ideal')
# Algebraic cross-check of the complete cubic coefficient lemma, without
# assuming the author's displayed normal form.
coeff=s.symbols('c0:10')
cubic=sum(ci*mi for ci,mi in zip(coeff,monomials))
low_constraints=[cubic.subs(dict(zip(V,p))) for p in P[4:]]
C=s.linear_eq_to_matrix(low_constraints,coeff)[0]
require(C.rank()==6,'The six two-coordinate conditions are independent')
normal=[x*(x*x-y*y-z*z),y*(y*y-x*x-z*z),z*(z*z-x*x-y*y),x*y*z]
normal_vectors=[s.Matrix([s.Poly(g,*V).coeff_monomial(m) for m in monomials]) for g in normal]
B=s.Matrix.hstack(*normal_vectors)
require(C*B==s.zeros(6,4) and B.rank()==4,'The asserted four-dimensional normal form equals the kernel')
Q=(1-x*y)**2+y*y-s.Rational(1,2)
k1=y*s.diff(Q,x);k2=x*s.diff(Q,y)
G=s.groebner([k1,k2],x,y)
require(list(G)==[x*x-x*y,y*y],'Independent Groebner basis for literal-product supplement')
require(Q.subs({x:0,y:0})==s.Rational(1,2),'Q is positive on its literal real variety')
require(Q.subs({x:2,y:s.Rational(1,2)})==s.Rational(-1,4),'Q has a negative value')
require(s.cancel(Q.subs({x:1/t,y:t}))==t*t-s.Rational(1,2),'Q has the asserted nonattaining asymptotic infimum')
print(json.dumps({'verdict':'PASS','sympy_version':s.__version__,'check_count':len(checks),'checks':checks,'point_order':P,'monomial_order':list(map(str,monomials)),'matrix':[[int(e) for e in row] for row in E.tolist()],'determinant':int(E.det()),'evaluation_ranks':ranks,'tangency_minor_factorizations':[str(s.factor(g)) for g in J],'literal_Q_groebner_basis':list(map(str,G)),'scope':'Exact algebra controls. Universal finite-SOS and arbitrary-degree claims are established by the written proof, not sampling.'},indent=2,sort_keys=True))
