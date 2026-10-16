#!/usr/bin/env python3
"""Independent exact algebra for E-6322 pass3; qualitative proofs are in the report."""
from pathlib import Path
import json
import platform
import sympy as S
out={'scope':'E-6322 pass3 coupled, stress-threshold and exact-core certification',
     'software':{'python':platform.python_version(),'sympy':S.__version__},'checks':{}}
def ck(name,expr):
    d=S.factor(S.simplify(expr))
    assert d==0,(name,d)
    out['checks'][name]={'passed':True,'difference':str(d)}
def inner(A,B):return sum(x*y for x,y in zip(A,B))
def mck(name,A):ck(name,sum(z*z for z in A))

F=S.Matrix([[2,1,0],[0,3,1],[1,0,2]])
H=F.inv();J=F.det();K=H.det()
P=S.Matrix([[1,2,3],[4,5,6],[7,8,10]])
W=S.Integer(17)
E=W*S.eye(3)-F.T*P;T=P*F.T
SS=K*E*F.T
mck('inverse_outer_stress',SS*H.T-K*E)
mck('inverse_material_stress',H.T*SS-K*(W*S.eye(3)-T))
mck('inverse_eshelby_stress',K*W*S.eye(3)-H.T*SS-K*T)
u=S.symbols('u',real=True)
for i in range(3):
 for j in range(3):
    R=S.zeros(3);R[i,j]=1
    HH=H+u*R
    # Linear test Wtilde(G)=W+P:(G-F) has prescribed arbitrary value and gradient atF.
    VV=HH.det()*(W+inner(P,HH.inv()-F))
    ck('inverse_chain_rule_'+str(i)+str(j),S.diff(VV,u).subs(u,0)-inner(SS,R))
Dphi=S.Matrix([[3,1,2],[0,4,1],[2,1,5]])
ck('primal_test_contraction',inner(P*F.T,Dphi*F.inv())-inner(P,Dphi))
ck('inverse_test_contraction',inner(E,Dphi*F)-inner(E*F.T,Dphi))

M=S.Matrix([[1,2,0],[0,-1,1],[2,0,1]])
N=S.Matrix([[0,1,2],[3,1,0],[1,-1,2]])
s,t=S.symbols('s t',real=True)
X=(S.eye(3)+s*N)*F*(S.eye(3)+t*M).inv()
f=(S.eye(3)+t*M).det()*inner(X,X)**2
mixed=S.diff(S.diff(f,s).subs(s,0),t).subs(t,0)
normF2=inner(F,F); P4=4*normF2*F
A=N*F; B=F*M
HessAB=8*inner(F,A)*inner(F,B)+4*normF2*inner(A,B)
ck('mixed_coupled_second_derivative',mixed-(S.trace(M)*inner(P4,A)-HessAB-inner(P4,N*F*M)))

r=S.symbols('r',positive=True)
tinv=(6*r+3)/5;q=(2*r+1)/3
ck('inverse_moment_exponent',(5*tinv-3)/6-r)
ck('cauchy_moment_exponent',(3*q-1)/2-r)
ck('duality_threshold_factorization',(6*r+3)*(2*r-2)-5*(2*r+1)-(2*r+1)*(6*r-11))
ck('primal_threshold_t',tinv.subs(r,S.Rational(11,6))-S.Rational(14,5))
ck('primal_threshold_q',q.subs(r,S.Rational(11,6))-S.Rational(14,9))
ck('inverse_stress_moment',1+S.Rational(1,6)-S.Rational(7,6))
ck('piola_stress_moment',S.Rational(3,2)+S.Rational(1,3)-S.Rational(11,6))
ck('sharp_inverse_stress_power',7*S.Rational(3,7)-3)
ck('sharp_primal_stress_power',11*S.Rational(3,11)-3)

JJ,jj=S.symbols('J j',positive=True)
ck('relative_inverse_square_barrier',JJ**(-2)-jj**(-2)+2*jj**(-3)*(JJ-jj)-(JJ-jj)**2*(2*JJ+jj)/(jj**3*JJ**2))
x1,x2,x3,a,b,c,d=S.symbols('x1 x2 x3 a b c d',positive=True)
xs=[x1,x2,x3];S0=sum(xs);T0=x1*x2+x1*x3+x2*x3
HP=a*S0**3+b*T0**S.Rational(3,2)+c*x1*x2*x3
U=[]
for i,xi in enumerate(xs):
    ui=6*a*S0**2*xi+3*b*S.sqrt(T0)*xi*(S0-xi)+2*c*x1*x2*x3
    ck('principal_stress_'+str(i+1),2*xi*S.diff(HP,xi)-ui);U.append(ui)
for i,j,k in [(0,1,2),(0,2,1),(1,2,0)]:
    ck('principal_difference_'+str(i+1)+str(j+1),U[i]-U[j]-(xs[i]-xs[j])*(6*a*S0**2+3*b*S.sqrt(T0)*xs[k]))
mean=S0/3;dev=[x-mean for x in xs];D2=sum(x*x for x in dev)
ck('tracefree_determinant_identity',x1*x2*x3-S0**3/27+S0*D2/6-dev[0]*dev[1]*dev[2])
ck('pairwise_deviatoric_identity',sum((xs[i]-xs[j])**2 for i,j in [(0,1),(0,2),(1,2)])-3*D2)
tau=S.symbols('tau',real=True)
ck('determinant_refinement_factorization',S.Rational(1,27)-tau**2/6-tau**3/(3*S.sqrt(6))-(1-S.sqrt(6)*tau)*(2+S.sqrt(6)*tau)**2/108)
ll=S.symbols('lambda',positive=True)
A0=27*a+3*S.sqrt(3)*b+c
conformal=3*d*ll**(-6)-A0*ll**6
ck('conformal_strict_derivative',S.diff(conformal,ll)+18*d*ll**(-7)+6*A0*ll**5)

# Unit rank-one direction with cosinez between its two factors.
z,eps=S.symbols('z eps',real=True);tt=S.symbols('tt',positive=True)
norm2=3*tt**2+2*tt*eps*z+eps**2
cofnorm2=3*tt**4+4*tt**3*eps*z+tt**2*eps**2*(1+z*z)
det=tt**3+tt**2*eps*z
law=a*norm2**3+b*cofnorm2**S.Rational(3,2)+c*det**2+d*det**(-2)
LH=S.diff(law,eps,2).subs(eps,0)
claimed=(54*a+3*S.sqrt(3)*b)*tt**4+((72*a+7*S.sqrt(3)*b+2*c)*tt**4+6*d*tt**(-8))*z*z
ck('general_rank_one_ellipticity',LH-claimed)
ck('rank_one_shear_value',LH.subs(z,0)-(54*a+3*S.sqrt(3)*b)*tt**4)
ck('rank_one_longitudinal_value',LH.subs(z,1)-(126*a+10*S.sqrt(3)*b+2*c)*tt**4-6*d*tt**(-8))

m,al2,al3=S.symbols('m alpha2 alpha3',real=True);total=m+al2+al3
eta=2*(3*m+al2+2*al3-6)
ck('tied_minimum_impossible',eta.subs(al2,m)-4*(2*m+al3-3))
ck('barrier_gap_strict_decomposition',6-total-3*m-((6-3*m-al2-2*al3)+(al3-m)))
leading=5*m-6
ck('a_first_row_gap',3*m+2*al2-6-leading-2*(al2-m))
ck('b_first_row_gap',2*m+3*al2-6-leading-3*(al2-m))
ck('c_first_row_gap',2*total-m-6-leading-(2*total-6*m))
ck('barrier_first_row_gap',6-2*total-m-leading-2*(6-total-3*m))
rr=S.symbols('rr',positive=True)
ck('scalar_spherical_radial_coefficient',S.diff(rr**2*m*rr**(5*m-5),rr)/rr**2-m*(5*m-3)*rr**(5*m-6))
ck('scalar_critical_exponent',(m*(5*m-3)).subs(m,S.Rational(3,5)))
ck('removable_flux_exponent',2+(5*m-5)-(5*m-3))
ck('weighted_feasible_example_eta',eta.subs({m:S.Rational(3,5),al2:S.Rational(5,4),al3:S.Rational(5,4)})+S.Rational(9,10))
out['all_checks_passed']=True
Path(__file__).with_name('verification.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({'all_checks_passed':True,'exact_checks':len(out['checks'])},indent=2))
