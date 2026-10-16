#!/usr/bin/env python3
"""Additional independent controls for ordering and hypothesis boundaries."""
import json
import sympy as S
x,y,t,u=S.symbols('x y t u')
checks={}
def ck(name,value):
    if not value:
        raise AssertionError(name)
    checks[name]='PASS'
def compose(f,g):
    return tuple(S.expand(a.subs({x:g[0],y:g[1]},simultaneous=True)) for a in f)
def mod_t(f,m):
    return tuple(S.Poly(a,t).rem(S.Poly(t**m,t)).as_expr() for a in f)
E=(x+t*y**2,y)
G=(x,y+t*x)
Ei=(x-t*y**2,y)
Gi=(x,y-t*x)
phi=compose(E,G)
correct_inverse=compose(Gi,Ei)
wrong_inverse=compose(Ei,Gi)
ck('correct_reverse_factor_inverse_exact',compose(phi,correct_inverse)==(x,y))
ck('correct_inverse_other_side_exact',compose(correct_inverse,phi)==(x,y))
ck('wrong_factor_order_rejected_mod_t3',mod_t(compose(wrong_inverse,phi),3)!=(x,y))
ck('first_order_shear_addition_independent_of_order',mod_t(compose(E,G),2)==mod_t(compose(G,E),2))
ck('higher_order_shear_products_do_not_commute',mod_t(compose(E,G),3)!=mod_t(compose(G,E),3))
F=(x,-y/S.Integer(2))
ck('r0_determinant_trace_shortcut_rejected',S.Matrix([2*x,y/2]).jacobian((x,y)).det()==1 and
   S.diff(F[0],x)+S.diff(F[1],y)!=0)
nonlinear=x+u*x**2
inverse=x-u*x**2
ck('nonreduced_n1_nonlinear_map_is_automorphism',
   S.Poly(S.expand(nonlinear.subs(x,inverse)-x),u).rem(S.Poly(u**2,u)).as_expr()==0)
ck('nonreduced_n1_nonlinear_map_not_special',
   S.Poly(S.diff(nonlinear,x)-1,u).rem(S.Poly(u**2,u)).as_expr()!=0)
ck('no_division_by_nilpotent_coefficient',
   S.Poly(u*u,u).rem(S.Poly(u**2,u)).as_expr()==0 and
   S.Poly(u,u).rem(S.Poly(u**2,u)).as_expr()!=0)
print(json.dumps({'schema':'independent-shear-edge-mutations-v1','status':'PASS',
 'sympy_version':S.__version__,'total_assertions':len(checks),'checks':checks,
 'scope':'Specific falsification controls supplement the universal proof, not exhaustive claims.'},indent=2,sort_keys=True))
