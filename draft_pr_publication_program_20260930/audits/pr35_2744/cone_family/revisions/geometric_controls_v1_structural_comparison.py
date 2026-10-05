#!/usr/bin/env python3
"""Exact geometric-component diagnostics, not a knot census or universal solution."""
from pathlib import Path
import json
import sympy as s
checks={}
def ck(label, predicate):
    if not bool(predicate): raise AssertionError(label)
    checks[label]='PASS'
x,y,t,z,alpha=s.symbols('x y t z alpha',real=True)
# A connected path changes irreducible component exactly at a singular point.
f=x*y
left=s.Matrix([t,0]);right=s.Matrix([0,t])
ck('path_left_on_union',s.expand(f.subs({x:left[0],y:left[1]}))==0)
ck('path_right_on_union',s.expand(f.subs({x:right[0],y:right[1]}))==0)
ck('path_continuous_at_node',left.subs(t,0)==right.subs(t,0))
ck('different_components',left.subs(t,-1)[0]!=0 and right.subs(t,1)[1]!=0)
ck('node_is_singular',s.Matrix([s.diff(f,x),s.diff(f,y)]).subs({x:0,y:0})==s.zeros(2,1))
ck('off_node_left_regular',s.Matrix([s.diff(f,x),s.diff(f,y)]).subs({x:-1,y:0})!=s.zeros(2,1))
ck('off_node_right_regular',s.Matrix([s.diff(f,x),s.diff(f,y)]).subs({x:0,y:1})!=s.zeros(2,1))
# Local Euclidean fold: real compact branches and imaginary regenerating branches.
mu=alpha+z*z
ck('fold_derivative_zero',s.diff(mu,z).subs(z,0)==0)
ck('fold_second_derivative_nonzero',s.diff(mu,z,2)==2)
ck('real_fold_increases_angle',s.expand(mu.subs(z,t)-alpha)==t*t)
ck('imaginary_fold_decreases_angle',s.expand(mu.subs(z,s.I*t)-alpha)==-t*t)
# A rational unitary character arc remains nonconstant under the finite sign quotient.
c=(1-t*t)/(1+t*t);d=2*t/(1+t*t)
U=s.diag(c+s.I*d,c-s.I*d)
ck('rational_family_unitary',s.simplify(U.conjugate().T*U)==s.eye(2))
ck('rational_family_det1',s.simplify(U.det())==1)
ck('character_varies',s.simplify(s.trace(U).diff(t))==-8*t/(1+t*t)**2)
q=s.factor(s.trace(U)**2)
ck('projected_character_varies',s.factor(s.diff(q,t))==-32*t*(1-t*t)/(1+t*t)**3)
ck('finite_sign_not_collapsed',s.simplify(s.trace(-U)**2-q)==0 and q.subs(t,s.Rational(1,3))!=q.subs(t,s.Rational(1,2)))
ck('conjugation_preserves_unitary',s.simplify(U.conjugate().conjugate().T*U.conjugate())==s.eye(2))
# Real/elliptic generators do not imply simultaneous compactness.
A=s.Matrix([[0,-1],[1,0]]);B=s.Matrix([[0,-4],[s.Rational(1,4),0]])
ck('elliptic_pair_det1',A.det()==1 and B.det()==1)
ck('elliptic_pair_real_trace',A.trace()==0 and B.trace()==0)
ck('product_noncompact',s.trace(A*B)==-s.Rational(17,4) and s.trace(A*B)<-2)
# O(2) inside SO(3): its disconnected component consists of half turns.
Q=s.Matrix([[0,1],[1,0]])
R=s.diag(1,1,1);R[:2,:2]=Q;R[2,2]=Q.det()
ck('embedded_o2_orthogonal',R.T*R==s.eye(3))
ck('embedded_o2_orientation',R.det()==1)
ck('embedded_o2_half_turn',R.trace()==-1 and R*s.Matrix([0,0,1])==-s.Matrix([0,0,1]))
ck('half_turn_not_oriented_axis_rotation',R[2,2]!=1)
# Scalar q=1 Schlaefli model: decreasing hyperbolic angle increases volume.
L=s.symbols('L',positive=True)
ck('hyperbolic_schlafli_sign',s.simplify((-L/2)*(-1))==L/2)
# Correct identity in Porti2004 Lemma4.2. Its last displayed sign is a typo.
b,a,u=s.symbols('b a u',real=True)
ell=2*s.pi+b*(u-s.pi)
V=lambda v:s.integrate(ell,(u,a,v))/2
expr=s.simplify(V(alpha)-V(2*s.pi-alpha))
ck('spherical_schlafli_identity',expr==2*s.pi*(alpha-s.pi))
ck('printed_final_sign_not_identity',s.simplify(expr-2*s.pi*(s.pi-alpha))!=0)
# Non-finite projection can collapse a curve: finiteness is essential.
ck('nonfinite_projection_collapse',s.Matrix([0,t])[0]==0 and s.Matrix([0,t]).diff(t)!=s.zeros(2,1))
result={'passed':len(checks),'failed':0,'sympy_version':s.__version__,'checks':checks,'scope':'Exact diagnostics and source-typo qualification only. Universal component continuation and cone analytic existence are proved/cited in PROOF.md, not inferred from finite cases; no new knot proof or counterexample.'}
Path(__file__).with_name('geometric_results.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
