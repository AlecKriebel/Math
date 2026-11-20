#!/usr/bin/env python3
"""Exact supplementary algebra for the attributed Rubel 2.73 reconstruction.

Run with Python 3.10+ and SymPy 1.14.0. Output is deterministic JSON.
No network, floating point sampling, orbit search, or external data are used.
The analytic proof is in PROOF.md; these checks do not formally verify it.
"""
import json
import sympy as s

checks = []
def check(name, statement):
    if not bool(statement):
        raise AssertionError(name)
    checks.append(name)

def zero(name, expr):
    check(name, s.expand(expr) == 0)

x, y, r, t, R, k = s.symbols('x y r t R k')
f = s.Matrix([y, (y*y-x)/2])
g = s.Matrix([x*x-2*y, x])
M = s.Matrix([[0, 1], [-s.Rational(1, 2), 0]])
fg = f.subs({x:g[0], y:g[1]}, simultaneous=True)
gf = g.subs({x:f[0], y:f[1]}, simultaneous=True)
for i in range(2):
    zero(f'f_after_g_coordinate_{i}', fg[i]-[x,y][i])
    zero(f'g_after_f_coordinate_{i}', gf[i]-[x,y][i])
zero('polynomial_map_jacobian', f.jacobian([x,y]).det()-s.Rational(1,2))
check('linear_part_square', M*M == -s.eye(2)/2)
check('linear_part_inverse', M.inv() == s.Matrix([[0,-2],[1,0]]))
zero('linear_part_determinant', M.det()-s.Rational(1,2))
zero('local_contraction_margin', s.Rational(3,4)*r-(r*r/2+s.Rational(2,3)*r)-r*(1-6*r)/12)
check('local_second_coordinate_bound_at_endpoint', s.Rational(1,6)/2+s.Rational(2,3)==s.Rational(3,4))
check('linear_operator_first_weighted_coordinate', s.Rational(3,4)<=s.Rational(3,4))
check('linear_operator_second_weighted_coordinate', s.Rational(2,3)<=s.Rational(3,4))
check('inverse_operator_first_weighted_coordinate', s.Rational(3,4)*2==s.Rational(3,2))
check('inverse_operator_second_weighted_coordinate', s.Rational(4,3)<=s.Rational(3,2))
ratio=s.Rational(3,2)*s.Rational(3,4)**2
check('telescoping_ratio',ratio==s.Rational(27,32))
check('telescoping_ratio_less_than_one',0<ratio<1)
check('telescoping_leading_constant',s.Rational(1,2)*s.Rational(3,2)==s.Rational(3,4))
check('geometric_tail_constant',s.Rational(3,4)/(1-ratio)==s.Rational(24,5))
check('local_ball_first_coordinate',s.Rational(4,3)*s.Rational(1,6)<25)
check('local_ball_second_coordinate',s.Rational(1,6)<5)
check('small_first_coordinate_escape_margin',25-(10+5)>0)
zero('middle_trap_factorization', t*t-t-20-(t-5)*(t+4))
zero('outer_trap_factorization', t*t-3*t+20-(90+(t-10)*(t+7)))
check('outer_trap_strict_margin',90>10)
check('missing_point_outside_box',not (0<25 and 10<5))
check('missing_point_outside_cone',not (0>=10+10))
check('box_scaled_width',s.Rational(5,25)<1)
check('cone_scaled_gap',s.Rational(10,25)==s.Rational(2,5))
L=s.Matrix([y/25,x/25])
zero('linear_change_jacobian',L.jacobian([x,y]).det()+s.Rational(1,625))
A=s.Matrix([x+y*y,y])
zero('shear_jacobian',A.jacobian([x,y]).det()-1)
zero('shear_tube_identity',A[0]-A[1]**2-x)
Ua,Ub,Va,Vb,z=s.symbols('Ua Ub Va Vb z')
zero('differential_defect', (Ub+z*Vb)*Va-(Ua+z*Va)*Vb+(Ua*Vb-Ub*Va))
Gw,Gzw,Ha,Hb=s.symbols('Gw Gzw Ha Hb')
zero('factorized_defect',(Gw*Hb)*(Gzw*Ha)-(Gw*Ha)*(Gzw*Hb))
check('final_nonzero_defect',-(-s.Rational(1,625))==s.Rational(1,625)>0)
# After the threshold t=R+2, the uniform infinity lower bound is positive
# and increases quadratically in the extra slope magnitude k>=0.
zero('normality_escape_bound', (t*t-(R+1)*t-1).subs(t,R+2+k)-(R+1+(R+3)*k+k*k))
print(json.dumps({'problem_id':2302073,'status':'PASS','assertions':len(checks),
  'arithmetic':'exact symbolic rational polynomial identities and rational comparisons',
  'checks':checks,
  'limitations':'Supplementary algebra only; analytic convergence, global bijectivity and spherical normality require PROOF.md.'},indent=2,sort_keys=True))
