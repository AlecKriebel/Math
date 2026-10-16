#!/usr/bin/env python3
"""Exact negative controls. No knot relation or new character arc is certified."""
from pathlib import Path
import json
import sympy as s
x,y,t=s.symbols('x y t',real=True);f=y*y+x*x*(1+x)
checks={}
def ck(name,value):
    assert bool(value),name
    checks[name]='PASS'
ck('isolated_point_on_curve',f.subs({x:0,y:0})==0)
ck('point_singular',s.diff(f,x).subs({x:0,y:0})==0 and s.diff(f,y).subs({x:0,y:0})==0)
ck('isolation_remainder',s.expand(f-(y*y+x*x/2)-x*x*(x+s.Rational(1,2)))==0)
ck('quadratic_discriminant',s.expand(s.discriminant(f,y)+4*x*x*(1+x))==0)
ck('simple_factor_in_discriminant',s.diff(1+x,x)==1)
ck('genuine_other_real_arc',s.expand(f.subs({x:-1-t*t,y:t*(1+t*t)}))==0)
A=s.Matrix([[0,-1],[1,0]]);B=s.Matrix([[0,-4],[s.Rational(1,4),0]])
ck('elliptic_generators',A.det()==1 and B.det()==1 and s.trace(A)==s.trace(B)==0)
ck('noncompact_product',s.trace(A*B)==-s.Rational(17,4))
D=s.diag(2,s.Rational(1,2));ck('generators_conjugate',D*A*D.inv()==B)
# Rational unit quaternions represented in SU(2), including sign twins.
qs=[(1,0,0,0),(0,1,0,0),(s.Rational(3,5),s.Rational(4,5),0,0),(s.Rational(1,2),)*4]
for j,(a,b,c,d) in enumerate(qs):
    U=s.Matrix([[a+s.I*b,c+s.I*d],[-c+s.I*d,a-s.I*b]])
    ck(f'unitary_{j}',s.simplify(U.conjugate().T*U)==s.eye(2) and s.simplify(U.det())==1)
    ck(f'sign_quotient_trace_square_{j}',s.trace(U)**2==s.trace(-U)**2)
    ck(f'sign_quotient_adjoint_{j}',(U*A*U.inv()-(-U)*A*(-U).inv()).applyfunc(s.simplify)==s.zeros(2))
r={'passed':len(checks),'failed':0,'sympy_version':s.__version__,'checks':checks,'scope':'Algebraic shortcut controls only; no theorem about a new knot, and no solution of KP-1.85.'}
Path(__file__).with_name('check_results.json').write_text(json.dumps(r,indent=2)+'\n')
print(json.dumps(r,indent=2))
