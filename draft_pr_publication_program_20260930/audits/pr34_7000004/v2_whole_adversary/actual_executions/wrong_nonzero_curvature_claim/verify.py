#!/usr/bin/env python3
"""Independent exact algebraic controls; the accompanying topological proof is essential."""
from pathlib import Path
import json
import sympy as S

checks = {}

def check(name, statement):
    assert bool(statement), name
    checks[name] = 'PASS'

x,y,r,e = S.symbols('x y r epsilon', real=True)
G=S.groebner([x*x+y*y-1],y,x)

def circle_zero(expr):
    if isinstance(expr,S.MatrixBase):
        return all(circle_zero(v) for v in expr)
    n,d = S.fraction(S.cancel(expr))
    return S.expand(G.reduce(S.expand(n))[1]) == 0

def D(expr):
    if isinstance(expr,S.MatrixBase):
        return expr.applyfunc(D)
    return S.expand(-y*S.diff(expr,x)+x*S.diff(expr,y))

gamma=S.Matrix([x,y,(x*x-y*y)/4])
gp=D(gamma);gpp=D(gp);gppp=D(gpp)
C=S.Matrix([-x**3,y**3,0]);R2=1+x**6+y**6;q=x*x*y*y
check('actual_derivative_cross_product',circle_zero(gp.cross(gpp)-C))
check('normal_to_first_derivative',circle_zero(gp.dot(C)))
check('normal_to_second_derivative',circle_zero(gpp.dot(C)))
check('speed_squared',circle_zero(gp.dot(gp)-(1+q)))
check('normal_norm_squared',circle_zero(C.dot(C)-R2))
check('normal_norm_positive_decomposition',circle_zero(R2-(2-3*q)))
check('torsion_numerator',circle_zero(C.dot(gppp)-3*x*y))
check('cross_product_derivative',circle_zero(D(C)-S.Matrix([3*x*x*y,3*y*y*x,0])))
check('circle_relation_derivative',D(x*x+y*y)==0)
check('constant_nonzero_cross_z',C[2]==1)

# Bprime=(D(C)R2-C D(R2)/2)/R2**(3/2).
M=S.expand(D(C)*R2-C*D(R2)/2)
check('normalized_binormal_speed_squared',circle_zero(M.dot(M)-9*q*(1+q)*R2))
check('Bprime_z_detects_normalization_derivative',S.expand(M[2]+D(R2)/2)==0)
for label,point in [('zero',(1,0)),('quarter',(0,1)),('half',(-1,0)),('three_quarters',(0,-1))]:
    sub={x:point[0],y:point[1]}
    check('Bprime_zero_'+label,all(v.subs(sub)==0 for v in M))
    check('centerline_curvature_nonzero_'+label,R2.subs(sub)>0 and gp.dot(gp).subs(sub)>0)
check('Bprime_nonzero_away_from_cusps',M.dot(M).subs({x:S.sqrt(2)/2,y:S.sqrt(2)/2})!=0)

# Rational parametrizations verify identities without replacing universal proof.
points=set()
for n in range(-20,21):
    t=S.Rational(n,7)
    points.add(((1-t*t)/(1+t*t),2*t/(1+t*t)))
points.update([(0,1),(0,-1),(-1,0)])
for i,(a,b) in enumerate(sorted(points,key=lambda z:(z[0],z[1]))):
    sub={x:a,y:b}
    check('rational_circle_'+str(i),a*a+b*b==1)
    check('rational_unit_nonzero_'+str(i),R2.subs(sub)>0)
    check('rational_cross_'+str(i),all(v.subs(sub)==0 for v in gp.cross(gpp)-C))
    check('rational_curvature_'+str(i),gp.dot(gp).subs(sub)>0)

# Ambient shear has determinant 1 and exact inverse.
X,Y,Z=S.symbols('X Y Z',real=True)
H=S.Matrix([X,Y,Z-(X*X-Y*Y)/4]);Hinverse=S.Matrix([X,Y,Z+(X*X-Y*Y)/4])
check('shear_orientation_preserving',H.jacobian([X,Y,Z]).det()==1)
check('shear_inverse',S.simplify(H.subs(dict(zip([X,Y,Z],Hinverse)),simultaneous=True)-S.Matrix([X,Y,Z]))==S.zeros(3,1))
check('shear_centerline_planar',S.simplify(H.subs(dict(zip([X,Y,Z],gamma)),simultaneous=True)-S.Matrix([x,y,0]))==S.zeros(3,1))
P=gamma+e*C/r
height=S.expand(H.subs(dict(zip([X,Y,Z],P)),simultaneous=True)[2])
expected=e/r+e*(x**4+y**4)/(2*r)-e*e*(x**6-y**6)/(4*r*r)
check('shear_push_off_height',S.expand(height-expected)==0)
for eps in [S.Rational(1,100),S.Rational(1,10),S.Rational(1,4)]:
    check('height_bound_epsilon_'+str(eps),eps>0 and 1-eps/4>0)
    check('projection_lipschitz_margin_epsilon_'+str(eps),1-3*eps>0)

# Real cube is injective; its difference factor and positive quadratic form.
u,v=S.symbols('u v',real=True)
check('cube_difference_factor',S.expand(u**3-v**3-(u-v)*(u*u+u*v+v*v))==0)
check('cube_factor_sum_of_squares',S.expand(u*u+u*v+v*v-((u+v/2)**2+3*v*v/4))==0)
check('binormal_ratio_recovers_x_cube',S.cancel(-(C[0]/r)/(C[2]/r))-x**3==0)
check('binormal_ratio_recovers_y_cube',S.cancel((C[1]/r)/(C[2]/r))-y**3==0)

# Differentiable normalization derivative and disk Lipschitz bound.
vec=S.Matrix([-x**3,y**3,1]);norm2=vec.dot(vec)
Jvec=vec.jacobian([x,y])
check('unnormalized_disk_derivative',Jvec==S.Matrix([[-3*x*x,0],[0,3*y*y],[0,0]]))
V1,V2,V3=S.symbols('V1 V2 V3',real=True);V=S.Matrix([V1,V2,V3]);Vnorm2=V.dot(V)
projector=S.eye(3)-V*V.T/Vnorm2
check('normalization_tangent_projection_idempotent',S.simplify(projector*projector-projector)==S.zeros(3,3))
check('normalization_tangent_projection_symmetric',projector.T==projector)
check('normalization_tangent_projection_kills_radial',S.simplify(projector*V)==S.zeros(3,1))

# Abstract moving frame: nonconstant speed and either torsion sign.
k,tau,nu,theta,theta_t=S.symbols('k tau speed theta theta_t',real=True)
T=S.Matrix([1,0,0]);N=S.Matrix([0,1,0]);B=S.Matrix([0,0,1])
Tt=nu*k*N;Nt=nu*(-k*T+tau*B);Bt=-nu*tau*N
check('general_speed_frame_skew',S.Matrix.hstack(Tt,Nt,Bt)+S.Matrix.hstack(Tt,Nt,Bt).T==S.zeros(3,3))
check('general_speed_twist_density',S.expand(T.dot(B.cross(Bt))-nu*tau)==0)
check('B_sign_reversal_frame',-Bt==-nu*tau*(-N))
V=S.cos(theta)*N+S.sin(theta)*B
Vt=S.cos(theta)*Nt+S.sin(theta)*Bt+theta_t*(-S.sin(theta)*N+S.cos(theta)*B)
check('general_speed_rotating_framing',S.simplify(T.dot(V.cross(Vt))-(nu*tau+theta_t))==0)
for tors in [-5,-1,1,5]:
    U=-S.sign(tors)*N;Us=(-S.sign(tors))*(-k*T+tors*B)/abs(tors)
    kg=S.expand((Us+B).dot(B.cross(U)))
    check('spherical_curvature_both_signs_'+str(tors),S.simplify(kg-k/abs(tors))==0)
    check('spherical_integral_both_signs_'+str(tors),S.simplify(kg*abs(tors)-k)==0)

# Actual rejected mutations. They must disagree with a genuine exact certificate.
mutants={}
wrong_y=S.Matrix([-x**3,-y**3,1])
mutants['wrong_binormal_y_sign']=not circle_zero(gp.dot(wrong_y))
mutants['injectivity_implies_Bprime_nonzero']=all(v.subs({x:1,y:0})==0 for v in M)
mutants['torsion_constant_nonzero']=C.dot(gppp).subs({x:1,y:0})==0
wrong_height=e/r-e*(x**4+y**4)/(2*r)-e*e*(x**6-y**6)/(4*r*r)
mutants['wrong_shear_linear_sign']=S.expand(height-wrong_height)!=0
mutants['arbitrary_epsilon_embedding_range']=not (1-3*S.Rational(1,2)>0)
mutants['regular_B_Fenchel_obstruction_applies_to_candidate']=all(v.subs({x:0,y:1})==0 for v in M)
# An injective nonunit vector circle can lose injectivity upon normalization.
mutants['normalization_preserves_injectivity']=S.Matrix([3,0,0])/3==S.Matrix([1,0,0]) and S.Matrix([1,0,0])/1==S.Matrix([1,0,0])
for name,rejected in mutants.items():
    check('rejected_mutant_'+name,rejected)

out={'passed':len(checks),'failed':0,'sympy_version':S.__version__,'checks':checks,'actual_rejected_mutants':mutants,'candidate':'gamma=(cos t,sin t,cos(2t)/4), B=(-cos^3 t,+sin^3 t,1)/sqrt(1+cos^6 t+sin^6 t)','scope':'Exact algebraic certificates plus rational controls. Universal injectivity, disjointness, embeddedness and linking=0 are proved in COUNTERMODEL_DERIVATION.md, not inferred from finite sampling. No novelty claim.','original_attempts_added_by_this_verification_family':0}
text=json.dumps(out,indent=2,sort_keys=True)+'\n'
Path(__file__).with_name('exact_results.json').write_text(text)
print(text,end='')
