#!/usr/bin/env python3
"""Independent exact controls for the scope audit of KP-1.85.
No new knot or character arc is certified by these finite checks.
"""
from pathlib import Path
from itertools import product
import json
import sympy as s
checks = {}
def ck(name, value):
    if not bool(value):
        raise AssertionError(name)
    checks[name] = 'PASS'
def simp(M):
    return M.applyfunc(s.simplify)
# Conjugation of traceless Hermitian matrices identifies the projective
# unitary action with SO(3), including the central sign invariance.
P = [s.Matrix([[0,1],[1,0]]), s.Matrix([[0,-s.I],[s.I,0]]), s.diag(1,-1)]
def adjoint(U):
    return s.Matrix(3,3,lambda i,j:s.simplify(s.trace(P[i]*U*P[j]*U.inv())/2))
triples = [(0,0,0),(1,0,0),(0,1,0),(0,0,1),(1,1,0),(1,1,1),(2,1,-1),(-1,2,3),(2,-3,4)]
matrices=[]
for k,xyz in enumerate(triples):
    n=sum(v*v for v in xyz); den=1+n
    a=s.Rational(1-n,den); b,c,d=[s.Rational(2*v,den) for v in xyz]
    U=s.Matrix([[a+s.I*b,c+s.I*d],[-c+s.I*d,a-s.I*b]])
    R=adjoint(U); matrices.append(U)
    ck(f'unit_quaternion_{k}',a*a+b*b+c*c+d*d==1)
    ck(f'su2_{k}',simp(U.conjugate().T*U)==s.eye(2) and U.det()==1)
    ck(f'adjoint_real_{k}',simp(R.conjugate()-R)==s.zeros(3))
    ck(f'adjoint_orthogonal_{k}',simp(R.T*R)==s.eye(3))
    ck(f'adjoint_orientation_{k}',s.factor(R.det())==1)
    ck(f'central_sign_invisible_{k}',adjoint(-U)==R)
    ck(f'faithful_mod_center_control_{k}',(R==s.eye(3))==(U==s.eye(2) or U==-s.eye(2)))
for k in range(len(matrices)-1):
    U,V=matrices[k:k+2]
    ck(f'adjoint_product_{k}',adjoint(U*V)==simp(adjoint(U)*adjoint(V)))
# A sign character on two meridional generators: arbitrary word products
# change only by a central sign, and trace squares do not change.
U,V=matrices[4],matrices[7]
for n in range(1,5):
    for bits in product((0,1),repeat=n):
        M=N=s.eye(2)
        for bit in bits:
            W=(U,V)[bit]; M=M*W; N=N*(-W)
        label=''.join(map(str,bits))
        ck(f'sign_word_{label}',simp(N-(-1)**n*M)==s.zeros(2) and s.simplify(s.trace(N)**2-s.trace(M)**2)==0)
# Free-group rank-two character quotient: finite sign orbits, which may
# shrink at special points. This guards against treating all fibers as free.
def invariants(v):
    x,y,z=v; return (x*x,y*y,z*z,x*y*z)
def orbit(v):
    x,y,z=v
    return {(a*x,b*y,a*b*z) for a,b in product((-1,1),repeat=2)}
for k,v in enumerate([(2,3,5),(0,3,5),(0,0,5),(0,0,0)]):
    orb=orbit(v); inv=invariants(v)
    ck(f'quotient_relation_{k}',inv[3]**2==inv[0]*inv[1]*inv[2])
    ck(f'quotient_sign_orbit_{k}',all(invariants(w)==inv for w in orb))
    ck(f'quotient_fiber_size_{k}',len(orb)==(4,4,2,1)[k])
# Independent exact derivation of the real isolated point and noncompact
# simultaneous-conjugacy control.
x,y,t=s.symbols('x y t',real=True)
f=y*y+x*x*(1+x)
ck('node_origin_singular',f.subs({x:0,y:0})==0 and all(s.diff(f,z).subs({x:0,y:0})==0 for z in (x,y)))
ck('strict_isolation_decomposition',s.expand(f-y*y-x*x/2-x*x*(x+s.Rational(1,2)))==0)
disc=s.discriminant(f,y)
ck('discriminant_odd_factor',s.factor(disc)==-4*x*x*(x+1) and s.Poly(disc,x).diff().eval(-1)!=0)
ck('distant_arc_identity',s.expand(f.subs({x:-1-t*t,y:t*(1+t*t)}))==0)
ck('distant_arc_regular_at_zero',s.diff(t*(1+t*t),t).subs(t,0)==1)
A=s.Matrix([[0,-1],[1,0]]); D=s.diag(2,s.Rational(1,2)); B=D*A*D.inv()
ck('elliptic_separate_conjugacy',A.det()==B.det()==1 and A.trace()==B.trace()==0)
ck('noncompact_product_diagonal',A*B==s.diag(-s.Rational(1,4),-4))
ck('noncompact_product_trace',s.trace(A*B)==-s.Rational(17,4) and s.trace(A*B)<-2)
result={'passed':len(checks),'failed':0,'sympy_version':s.__version__,'checks':checks,'scope':'Exact algebraic diagnostics only; no universal knot theorem, census computation, or new compact-real arc.'}
Path(__file__).with_name('independent_results.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'passed':len(checks),'failed':0,'sympy_version':s.__version__}))
