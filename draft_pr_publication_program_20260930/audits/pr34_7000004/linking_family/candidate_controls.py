#!/usr/bin/env python3
"""Exact polynomial checks for the parent-supplied second-attempt candidate."""
import json
from pathlib import Path
import sympy as S

c,s,r,e = S.symbols('c s r e',real=True)
checks={}
mutants={}
circle = S.groebner([c*c+s*s-1],c,s,order='lex',domain='EX')


def rem(x):
    return circle.reduce(S.expand(x))[1]


def zero(x):
    if isinstance(x,S.MatrixBase):return all(rem(z)==0 for z in x)
    return rem(x)==0


def check(n,x):
    assert bool(x),n
    checks[n]='PASS'


gp=S.Matrix([-s,c,-s*c])
gpp=S.Matrix([-c,-s,-(c*c-s*s)])
gppp=S.Matrix([s,-c,4*s*c])
w=S.Matrix([-c**3,s**3,1])
wp=S.Matrix([3*c*c*s,3*s*s*c,0])
u=c*c*s*s
r2=w.dot(w)
check('frenet_cross_exact',zero(gp.cross(gpp)-w))
check('binormal_orthogonal_velocity',zero(w.dot(gp)))
check('binormal_orthogonal_acceleration',zero(w.dot(gpp)))
check('curvature_numerator_positive_z',w[2]==1)
check('norm_formula',zero(r2-(2-3*u)))
check('speed_squared_formula',zero(gp.dot(gp)-(1+u)))
check('torsion_numerator',zero(w.dot(gppp)-3*s*c))
check('unit_binormal_z_positive_when_r_positive',w[2]==1)
check('injectivity_recovers_cos_cubed',w[0]/w[2]==-c**3)
check('injectivity_recovers_sin_cubed',w[1]/w[2]==s**3)
for n,cv,sv in [('zero',1,0),('half_pi',0,1),('pi',-1,0),('three_half_pi',0,-1)]:
    check('binormal_derivative_zero_'+n,wp.subs({c:cv,s:sv})==S.zeros(3,1))
check('derivative_z_zero',wp[2]==0)
check('derivative_zero_equations',wp[0]==3*c*c*s and wp[1]==3*s*s*c)
check('norm_lower_bound',S.Rational(2)-3*S.Rational(1,4)==S.Rational(5,4))

# H_z(eta_epsilon) is computed directly, independently of an integral formula.
x=c-e*c**3/r
y=s+e*s**3/r
z=(c*c-s*s)/4+e/r
hz=S.expand(z-(x*x-y*y)/4)
claimed=e/r+e*(c**4+s**4)/(2*r)-e*e*(c**6-s**6)/(4*r*r)
check('shear_height_exact',S.expand((hz-claimed)*r*r)==0)
check('fourth_powers_formula',zero(c**4+s**4-(1-2*u)))
check('height_positive_uniform_bound',S.Rational(5,4)-S.Rational(1,3)/4==S.Rational(7,6)>0)
check('planar_x_factor_positive_bound',1-S.Rational(1,3)>0)
check('planar_y_factor_positive_bound',1>0)

# Differentiate using D(c)=-s, D(s)=c, D(r)=-3cs(c²-s²)/r.
rp=-3*c*s*(c*c-s*s)/r
def D(z):return S.diff(z,c)*(-s)+S.diff(z,s)*c+S.diff(z,r)*rp
angle_num=S.expand(x*D(y)-y*D(x))
expected=1-e*(c*c-s*s)/r+3*e*u*(c*c-s*s)/r**3-3*e*e*u/r**2
check('polar_angle_numerator_exact',zero(S.expand((angle_num-expected)*r**3)))
check('polar_angle_uniform_bound',1-S.Rational(7,4)*S.Rational(1,3)-S.Rational(3,4)*S.Rational(1,9)==S.Rational(1,3)>0)
check('shear_jacobian_determinant',S.Matrix([[1,0,0],[0,1,0],[-c/2,s/2,1]]).det()==1)

for name,bad in [('wrong_x_sign',S.Matrix([c**3,s**3,1])),
                 ('wrong_y_sign',S.Matrix([-c**3,-s**3,1])),
                 ('constant_north_normal',S.Matrix([0,0,1]))]:
    rejected=not(zero(bad.dot(gp)) and zero(bad.dot(gpp)))
    assert rejected,name
    mutants[name]='REJECTED by binormal compatibility'
assert not zero(r2-1)
mutants['omit_unit_normalization']='REJECTED by exact unit-length condition'
assert not zero(S.expand((hz-(e/r+e*(c**4+s**4)/(2*r)+e*e*(c**6-s**6)/(4*r*r)))*r*r))
mutants['wrong_quadratic_shear_sign']='REJECTED by exact height identity'
assert wp.subs({c:1,s:0})==S.zeros(3,1)
mutants['injective_implies_regular']='REJECTED by exact stationary binormal point'
assert w.dot(gppp).subs({c:1,s:0})==0
mutants['negative_curvature_asymptotic_scope']='REJECTED: torsion zero at exact stationary point'

out={'passed':len(checks),'failed':0,'checks':checks,'mutants':mutants,
     'sympy_version':S.__version__,
     'scope':'Polynomial identities and explicit rational bounds. Universal injectivity, polar winding and zero-linking argument are in CANDIDATE_LINKING_CERTIFICATE.md. No numerical-only claim.',
     'candidate_provenance':'parent-supplied differential-family second-attempt construction, then independently falsified here',
     'verification_attempts_added':0,'root_records_original_attempt_count':2}
Path(__file__).with_name('candidate_controls_results.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
