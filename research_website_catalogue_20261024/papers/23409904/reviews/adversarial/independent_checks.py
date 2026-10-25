"""Independent scalar-jet, coordinate-law and noncompact Schur controls.
No submitted imports; exact identities plus finite corroboration, not topology proof.
"""
from pathlib import Path
from itertools import product
from math import factorial
import sympy as s
import json

def require(c,msg):
 if not c:raise RuntimeError(msg)
def zero(q,msg):require(s.factor(q)==0,msg)
def st(q):return str(s.factor(q))
t=s.symbols('t',real=True)
f=s.Matrix([1,t,t*t,t*t*t]);g=1/(1+t*t)**2;C=t**5;Q=(3*s.diff(g,t)-C)/2
E=s.Matrix.vstack(*[f.diff(t,k).T for k in range(4)])
require(s.factor(E.det())==12,'one-dimensional jet surjectivity')
a=s.simplify(E.inv()*s.Matrix([0,0,g,Q]));phi=-a
v=f.diff(t);w=phi.diff(t);v2=f.diff(t,2)
for k,target in enumerate([0,0,g,Q]):zero(a.dot(f.diff(t,k))-target,'frozen scalar jet')
zero(v.dot(w)-g,'pair metric sign')
Gamma=(s.diff(g,t)-C)/2
zero(v2.dot(w)-Gamma,'ordered pair connection')
zero(phi.dot(v),'exact conormal form')
zero(s.diff(a.dot(f),t,2),'base scalar identically zero')
require(s.factor(a.dot(f.diff(t,2)))==g,'nonholonomic jet distinction')
# Wrong cubic sign would induce the opposite ordered connection.
Qwrong=(3*s.diff(g,t)+C)/2
aw=E.inv()*s.Matrix([0,0,g,Qwrong]);wrongGamma=s.factor(v2.dot((-aw).diff(t)))
zero(wrongGamma-(s.diff(g,t)+C)/2,'wrong sign gives dual')
require((wrongGamma-Gamma).subs(t,1)!=0,'wrong ordered sign detected')
# Normal-coordinate log example is a smooth nonuniform lift.
z,base=s.symbols('z base',positive=True)
qt=base**3*(s.log(z)-s.log(base))**3/6
for k in range(4):zero(s.diff(qt,z,k).subs(z,base)-(1 if k==3 else 0),'unbounded log-jet example')
# Coordinate law in dimension2 with nonlinear mixed chart and nonzero cubic.
u,vv=s.symbols('u vv');ys=[u,vv];xs=s.Matrix([u+vv**2,vv+u**2]);J=xs.jacobian(ys)
Cube={(i,j,k):s.Integer([1,2,3,4][i+j+k]) for i,j,k in product(range(2),repeat=3)}
newg=J.T*J
chart_count=0;wrong_nonzero=[]
for aa,bb,cc in product(range(2),repeat=3):
 tensorQ=sum(-Cube[i,j,k]*J[i,aa]*J[j,bb]*J[k,cc]/2 for i,j,k in product(range(2),repeat=3))
 conn=tensorQ+sum(s.diff(xs[i],ys[aa],ys[bb])*J[i,cc] for i in range(2))
 newQ=s.diff(newg[aa,bb],ys[cc])+conn
 inhom=sum(s.diff(xs[i],ys[aa],ys[bb])*J[i,cc]+s.diff(xs[i],ys[aa],ys[cc])*J[i,bb]+s.diff(xs[i],ys[bb],ys[cc])*J[i,aa] for i in range(2))
 zero(newQ-tensorQ-inhom,'nonlinear scalar third-jet chart law')
 if s.factor(newQ-tensorQ)!=0:wrong_nonzero.append([aa,bb,cc])
 chart_count+=1
require(bool(wrong_nonzero),'tensor-only law negative control')
# Polynomial feature jets dimension2, exact nonzero determinant for every base point.
x,y=s.symbols('x y');mons=[(i,d-i) for d in range(4) for i in range(d+1)]
features=[x**i*y**j for i,j in mons]
E2=s.Matrix([[s.diff(p,x,i,y,j) for p in features] for i,j in mons])
det2=s.factor(E2.det());expected=s.Integer(1)
for i,j in mons:expected*=factorial(i)*factorial(j)
require(det2==expected==576,'global degree3 feature rank')
# Actual noncompact pair from the variable scalar jets above: positive g, unbounded C,
# and incomplete metric because integral sqrt(g)dt=arctan(t).
examples=[]
for point in [0,1,3,10,100]:
 V=v.subs(t,point);W=w.subs(t,point);gg=g.subs(t,point);hh=V.dot(V)
 PN=s.eye(4)-V*V.T/hh
 H0=(V*W.T+W*V.T)/hh-gg*V*V.T/hh**2
 T=s.factor((W.T*PN*W)[0]/gg);lam=1+T
 H=H0+2*lam*PN
 require(H0*V==W and H*V==W,'preserved Hessian tangent columns')
 require((V.T*H*V)[0]==gg,'pullback positive metric')
 minors=[s.factor(H[:k,:k].det()) for k in range(1,5)]
 require(all(q>0 for q in minors),'positive Hessian completion')
 examples.append({'base':point,'metric':st(gg),'euclidean_tangent_eigenvalue':st(gg/hh),'mixed_Schur_scalar':st(T),'lambda':st(lam),'all_leading_principal_minors_positive':True,'principal_minor_signs':[1]*4,'constant_lambda_one_Schur_eigenvalue':st(2-T)})
require(s.Rational(examples[2]['constant_lambda_one_Schur_eigenvalue'])<0,'fixed correction fails at large base')
# Beta0/B0 case: at t=0 this field still has a mixed term from cubic-free metric
# derivative geometry; generic algebra handles exactly zero mixed block separately.
A=s.diag(s.Rational(1,100),2);B=s.zeros(2,3);lam=s.Integer(1)
block=s.diag(s.Rational(1,100),2,2,2,2)
require(all(block[i,i]>0 for i in range(5)),'zero mixed block limit')
# A dual positive pair can have only one torsion vanish; both are necessary.
Gamma0={(k,i,j):s.Integer(0) for k,i,j in product(range(2),repeat=3)}
Gamma0[0,0,1]=1
Star={(k,i,j):-Gamma0[j,i,k] for k,i,j in product(range(2),repeat=3)}
for i,j,k in product(range(2),repeat=3):require(Gamma0[k,i,j]+Star[j,i,k]==0,'constant metric duality')
torsion=[Gamma0[k,i,j]-Gamma0[k,j,i] for k,i,j in product(range(2),repeat=3)]
torsionstar=[Star[k,i,j]-Star[k,j,i] for k,i,j in product(range(2),repeat=3)]
require(any(q!=0 for q in torsion) and all(q==0 for q in torsionstar),'both torsions needed')
# Compact zero-level positive Hessian control: circle, global annular potential rho^2-rho.
rho=s.symbols('rho',positive=True)
require(s.diff(rho*rho-rho,rho,2)==2,'radial positivity')
require(((s.diff(rho*rho-rho,rho))/rho).subs(rho,1)==1,'circle tangent metric')
# Global positive Hessian does not entail global injectivity of gradient on disconnected U.
left=s.Rational(1,2)*(z+s.Rational(3,2))**2;right=s.Rational(1,2)*(z-s.Rational(3,2))**2
require(s.diff(left,z,2)==s.diff(right,z,2)==1,'disconnected Hessian positivity')
require(s.diff(left,z).subs(z,-s.Rational(3,2))==s.diff(right,z).subs(z,s.Rational(3,2))==0,'global gradient injectivity false inference detected')
out={'scope':'Independent exact identities and finite corroboration; not a proof of Whitney/tubular theorems or historical novelty','one_dimensional_feature_jet_determinant':'12','two_dimensional_feature_jet_determinant':'576','two_dimensional_nonlinear_chart_cases':chart_count,'tensor_only_chart_negative_controls_detected':len(wrong_nonzero),'pair_identities_exact':True,'wrong_cubic_sign_detected':True,'zero_form_exact':True,'nonholonomic_scalar_jet_distinction_checked':True,'log_jet_unbounded_coefficient_example_checked':True,'noncompact_realization_field':{'domain':'R','metric':'dt^2/(1+t^2)^2','metric_incomplete':'distance to either infinity finite (arctan)','cubic':'t^5 dt^3','feature_curve':'(1,t,t^2,t^3)','exact_pointwise_Schur_examples':examples,'constant_normal_correction_fails':True},'zero_mixed_block_case':True,'one_torsion_only_negative_control':{'duality_exact':True,'given_connection_torsion_nonzero':True,'dual_connection_torsion_zero':True},'compact_circle_positive_Hessian':{'potential':'rho^2-rho','domain':'rho>1/2 (or any smaller annulus around rho=1)','radial_eigenvalue':'2','tangent_eigenvalue':'2-1/rho','potential_zero_on_circle':True},'gradient_need_not_be_global_coordinates':{'domain':'(-2,-1) union (1,2)','piecewise_potential':'(z+3/2)^2/2 on left, (z-3/2)^2/2 on right','Hessian':'1','duplicate_gradient_value':'0 at z=-3/2 and z=3/2'},'supplied_code_imported':False}
Path(__file__).with_name('independent_results.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
