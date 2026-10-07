#!/usr/bin/env python3
"""Exact supporting controls for PROOF.md. Requires Python 3 and SymPy 1.14.0.
These checks do not replace the universal zero-line/axis argument.
"""
from itertools import permutations, product
from pathlib import Path
import json
import sympy as s

count = 0

def check(ok):
    global count
    count += 1
    assert bool(ok), f"check {count} failed"

x,y,z,t = s.symbols('x y z t')
v=(x,y,z)
R=x**6+y**6+z**6-x**4*y**2-x**2*y**4-x**4*z**2-x**2*z**4-y**4*z**2-y**2*z**4+3*x**2*y**2*z**2
Z=[(1,u,w) for u in (1,-1) for w in (1,-1)]+[(1,u,0) for u in (1,-1)]+[(1,0,u) for u in (1,-1)]+[(0,1,u) for u in (1,-1)]
check(len(Z)==10)
check(len(set(Z))==10)
check(s.Poly(R,x,y,z).total_degree()==6)
check(all(sum(m)==6 for m in s.Poly(R,x,y,z).monoms()))
for perm in permutations(v):
    check(s.expand(R.xreplace(dict(zip(v,perm)))-R)==0)
for signs in product((1,-1),repeat=3):
    check(s.expand(R.xreplace({a:e*a for a,e in zip(v,signs)})-R)==0)
a,b,c,u,w=s.symbols('a b c u w')
F=a**3+b**3+c**3-a*a*b-a*b*b-a*a*c-a*c*c-b*b*c-b*c*c+3*a*b*c
check(s.expand(F-(a-b)**2*(a+b-c)-c*(a-c)*(b-c))==0)
check(s.expand(F.subs({a:x*x,b:y*y,c:z*z})-R)==0)
ordered=s.Poly(s.expand(F.subs({a:c+w+u,b:c+w})),u,w,c)
check(all(k>=0 for k in ordered.coeffs()))
check(str(ordered.as_expr())=='c*u**2 + c*u*w + c*w**2 + u**3 + 2*u**2*w')
D=[s.diff(R,a) for a in v]
K=[v[j]*D[i] for i in range(3) for j in range(3) if i!=j]
J=[v[j]*D[i]-v[i]*D[j] for i in range(3) for j in range(i+1,3)]
for p in Z:
    line=dict(zip(v,[t*a for a in p]))
    check(s.expand(R.subs(line))==0)
    for f in D+K+J:
        check(s.expand(f.subs(line))==0)
axis={x:t,y:0,z:0}
check(s.expand(R.subs(axis))==t**6)
check([s.expand(f.subs(axis)) for f in D]==[6*t**5,0,0])
for f in K+J:
    check(s.expand(f.subs(axis))==0)
ranks=[]
for d in range(4):
    mons=[x**i*y**j*z**(d-i-j) for i in range(d+1) for j in range(d+1-i)]
    E=s.Matrix([[m.subs(dict(zip(v,p))) for m in mons] for p in Z])
    ranks.append(E.rank())
    check(E.rank()==len(mons))
    if d==3:
        cubic_matrix=E.tolist()
        cubic_monomials=list(map(str,mons))
        determinant=E.det()
        check(determinant==-128)
        check(E*E.inv()==s.eye(10))
# Explicit coefficient lemma after imposing the six two-coordinate zeros.
A,B,C,D0=s.symbols('A B C D')
p=A*x*(x*x-y*y-z*z)+B*y*(y*y-x*x-z*z)+C*z*(z*z-x*x-y*y)+D0*x*y*z
vals=[]
for u0,w0 in product((1,-1),repeat=2):
    val=s.expand(p.subs({x:1,y:u0,z:w0}))
    check(val==-A-B*u0-C*w0+D0*u0*w0)
    vals.append((u0,w0,val))
for char,want in [(lambda u,w:1,-4*A),(lambda u,w:u,-4*B),(lambda u,w:w,-4*C),(lambda u,w:u*w,4*D0)]:
    check(s.expand(sum(char(u,w)*val for u,w,val in vals))==want)
check(s.expand(sum(v[i]*s.diff(R,v[i]) for i in range(3)))==6*R)
# Literal-product diagnostic, separate from the Robinson argument.
Q=(1-x*y)**2+y*y-s.Rational(1,2)
k1=y*s.diff(Q,x); k2=x*s.diff(Q,y)
check(s.expand(k1-2*y*y*(x*y-1))==0)
check(s.expand(k2-2*x*(x*(x*y-1)+y))==0)
check(s.expand(k2.subs(y,0))==-2*x*x)
check(s.cancel(k2.subs(y,1/x))==2)
check(Q.subs({x:0,y:0})==s.Rational(1,2))
check(Q.subs({x:2,y:s.Rational(1,2)})==s.Rational(-1,4))
check(s.cancel(Q.subs({x:1/t,y:t}))==t*t-s.Rational(1,2))
result={
 'verdict':'PASS_EXACT_SUPPORTING_CONTROLS',
 'assertions':count,
 'arithmetic':'exact integer/rational polynomial algebra only',
 'sympy_version':s.__version__,
 'cubic_evaluation_determinant':int(determinant),
 'homogeneous_evaluation_ranks_degrees_0_to_3':ranks,
 'zero_directions':Z,
 'cubic_monomials':cubic_monomials,
 'cubic_evaluation_matrix':[[int(a) for a in row] for row in cubic_matrix],
 'ordered_schur_expansion':str(ordered.as_expr()),
 'scope':'Algebraic controls for the analytic proof, not a finite-sampling proof or an SOS-degree cutoff.'
}
print(json.dumps(result,indent=2,sort_keys=True))
