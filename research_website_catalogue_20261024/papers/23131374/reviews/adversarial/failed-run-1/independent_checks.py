"""Own exact/independent curvature controls. No submitted code imports.
Finite controls corroborate, and do not prove all r or global curvature.
"""
from pathlib import Path
import json, math
from itertools import product
import sympy as S
import mpmath as mp

def require(test,label):
 if not bool(test):raise RuntimeError(label)
def zero(expr,label):require(S.simplify(expr)==0,label)

x,y,rho,eps=S.symbols('x y rho eps',real=True,positive=True)
q=x*x+y*y+rho*rho;s=S.sqrt(q);L=S.log(q)/2;z=x+S.I*y
# Universal induction has arbitrary j; these exact recurrences are finite controls.
recurrences=[]
P={(0,):x,(1,):y};prev_bound=1
for j in range(1,7):
 largest=0
 for word,p in P.items():
  poly=S.Poly(S.expand(p),x,y,rho);norm=sum(abs(c) for c in poly.coeffs())
  require(poly.total_degree()==j,'homogeneous log numerator degree')
  require(norm<=prev_bound,'5j coefficient recurrence bound')
  largest=max(largest,norm)
 recurrences.append({'order':j,'ordered_derivatives':len(P),'largest_actual_coefficient_l1':str(largest),'bound':str(prev_bound)})
 if j<6:
  P={word+(i,):S.expand(q*S.diff(p,[x,y][i])-2*j*[x,y][i]*p) for word,p in P.items() for i in range(2)}
  prev_bound*=5*j
# Origin jet uses fixed rho>0 and exact leading coefficient; eps log(rho)=-1.
jets=[]
for r in range(1,9):
 fdisp=eps*x**(r+1)*S.log(x*x+rho*rho)/2
 jet=S.diff(fdisp,x,r+1).subs(x,0)
 zero(jet-eps*S.log(rho)*math.factorial(r+1),'regularized origin jet')
 jets.append({'r':r,'jet_over_eps_log_rho':str(S.simplify(jet/(eps*S.log(rho)))),'with_eps_log_rho_minus_one':-math.factorial(r+1)})
# Wirtinger factor checks, notably 1/2 for log sqrt(q).
for r in [1,2,4]:
 disp=eps*z**(r+1)*L
 zero((S.diff(disp,x)+S.I*S.diff(disp,y))/2-eps*z**(r+2)/(2*q),'Wirtinger half factor')
# Exact inverse-coordinate pullback Laplacian on a nonorthogonal nonlinear shear.
u,v,alpha=S.symbols('u v alpha',real=True)
F=S.Matrix([x+alpha*y*y,y]);J=F.jacobian([x,y]);H=J.inv();A=H*H.T
B=S.Matrix([-sum(H[i,a]*S.diff(F[a],[x,y][j],[x,y][k])*A[j,k] for a,j,k in product(range(2),repeat=3)) for i in range(2)])
test=x*x+x*y+3*y*y+x
direct=S.diff(test.subs({x:u-alpha*v*v,y:v}),u,2)+S.diff(test.subs({x:u-alpha*v*v,y:v}),v,2)
direct=direct.subs({u:F[0],v:F[1]},simultaneous=True)
operator=sum(A[i,j]*S.diff(test,[x,y][i],[x,y][j]) for i,j in product(range(2),repeat=2))+sum(B[i]*S.diff(test,[x,y][i]) for i in range(2))
zero(operator-direct,'exact HHtranspose plus full inverse drift')
require(S.simplify((H.T*H-A)[1,1])!=0,'wrong matrix order distinguished')
zero(B[0]+2*alpha,'inverse-coordinate drift coefficient')
require(B[0]!=0,'dropping drift fails already on v=x')
# Convex radius exact Hessian and eigenvectors; no isotropic lower bound assumed.
D2s=S.hessian(s,[x,y]);rad=S.Matrix([x,y]);tang=S.Matrix([-y,x])
for i in range(2):
 zero((D2s*rad-rho*rho*rad/s**3)[i],'radial radius Hessian eigenvalue')
 zero((D2s*tang-tang/s)[i],'tangent radius Hessian eigenvalue')
zero(S.trace(D2s)-(x*x+y*y+2*rho*rho)/s**3,'radius Laplacian')
zero(S.trace(D2s)-1/s-rho*rho/s**3,'radius Laplacian lower bound')
# Prior direct controlling polynomial, not prior numerical checker output.
sigma=S.symbols('sigma',nonnegative=True)
priorpoly=S.expand((sigma+2)**2*(sigma+1)**3-sigma*(sigma*sigma+3*sigma+3)**2)
require(priorpoly==sigma**4+4*sigma**3+7*sigma**2+7*sigma+4,'prior radius dominance identity')
# Slow-twist shear exact determinant and tensor defect.
t=S.symbols('t',real=True);shear=S.Matrix([[1,0],[t,1]])
require(shear.det()==1,'twist orientation')
require(shear.T*shear==S.Matrix([[1+t*t,t],[t,1]]),'twist tensor formula')
# Real-current-map formula, inner disk only: local curvature controls, not global proof.
Fr=S.Matrix([x+eps*(x*x-y*y)*L,y+2*eps*x*y*L]);Jr=Fr.jacobian([x,y])
k=2*L+(x*x+y*y)/(2*q);hr=S.log((1+eps*x*k)**2+(eps*y*k)**2)/2
derivatives=[Fr[i] for i in range(2)]+list(Jr)+[S.diff(Fr[a],[x,y][i],[x,y][j]) for a,i,j in product(range(2),repeat=3)]
hparts=[S.diff(hr,t) for t in [x,y]]+list(S.hessian(hr,[x,y]))
calc=S.lambdify([x,y,rho,eps],derivatives+hparts,'mpmath',cse=True)
def point(n,bg,rx,ry,prec):
 with mp.workdps(prec):
  rr=mp.exp(-n);ee=mp.mpf(1)/n;xx=rx*rr;yy=ry*rr;ss=mp.sqrt(xx*xx+yy*yy+rr*rr);vals=calc(xx,yy,rr,ee)
  jj=mp.matrix(2,2,vals[2:6]);hh=jj**-1;aa=hh*hh.T;f2=vals[6:14]
  bb=[-sum(hh[i,a]*f2[4*a+2*j+k]*aa[j,k] for a,j,k in product(range(2),repeat=3)) for i in range(2)]
  coeff=mp.mpf('0.5') if bg=='plane' else mp.mpf(1);qq=1+xx*xx+yy*yy
  gradb=[2*coeff*xx/qq,2*coeff*yy/qq];hessb=[[2*coeff*(int(i==j)/qq-2*[xx,yy][i]*[xx,yy][j]/qq**2) for j in range(2)] for i in range(2)]
  dh=vals[14:16];d2h=mp.matrix(2,2,vals[16:20]);bad=sum(aa[i,j]*(hessb[i][j]+d2h[i,j]) for i,j in product(range(2),repeat=2))+sum(bb[i]*(gradb[i]+dh[i]) for i in range(2))
  hs=mp.eye(2)/ss-mp.matrix([[xx*xx,xx*yy],[xx*yy,yy*yy]])/ss**3
  ls=sum(aa[i,j]*hs[i,j] for i,j in product(range(2),repeat=2))+sum(bb[i]*[xx,yy][i]/ss for i in range(2))
  corrected=bad+32*ee*ls
  return {'n':n,'background':bg,'z_over_rho':[str(rx),str(ry)],'L_b_plus_h':mp.nstr(bad,32),'L_b_plus_h_plus_32epss':mp.nstr(corrected,32),'scaled_radius_operator_sL_s':mp.nstr(ss*ls,32),'metric_jacobian_det':mp.nstr(mp.det(jj),32),'uncorrected_negative':bool(bad<0),'corrected_positive':bool(corrected>0)}
numerical=[]
for n in [8,12,20]:
 for bg in ['plane','sphere']:
  for rx,ry in [(-2,0),(0,1),(2,0)]:
   a=point(n,bg,rx,ry,85);b=point(n,bg,rx,ry,125)
   require(a==b,'85 versus125digit sign/value stability');require(a['corrected_positive'],'inner correction positivity control');numerical.append(a)
require(any(r['uncorrected_negative'] for r in numerical),'negative-curvature control without correction')
result={'scope':'Independent exact identities plus18 inner-disk high-precision samples; not universal theorem/global-annulus/priority proof','ordered_log_recurrence_controls':recurrences,'origin_jets_r1_through8':jets,'Wirtinger_half_factor_checked':True,'nonlinear_inverse_operator_exact':True,'wrong_matrix_order_detected':True,'omitted_drift_detected_on_linear_test':True,'radius_Hessian_PSD_radial_tangent_identities_exact':True,'twist_orientation_and_tensor_exact':True,'prior_dominating_polynomial_identity':str(priorpoly),'inner_curvature_controls':numerical,'arbitrary_fixed_K32_not_claimed_global_certificate':True,'precision_comparison_digits':[85,125],'supplied_code_imported_or_executed':False}
Path(__file__).with_name('independent_results.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
