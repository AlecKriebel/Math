"""Exact finite diagnostics of analytic identities; NOT certificate6.1/7.1 replay."""
from fractions import Fraction as F
from itertools import product
from collections import Counter
import json,sys
C=Counter()
def check(ok,k):
 C[k]+=1
 if not ok:raise RuntimeError(k)
def finite_prod(xs):
 out=F(1)
 for x in xs:out*=x
 return out
# Jensen's outside-cluster comparison by rational products, not sampled logs.
roots=[F(-1),F(-1,2),F(0),F(1,2),F(1)]
for n in range(2,6):
 for rs in product(roots,repeat=n):
  mean=sum(rs,F(0))/n
  for x in [F(-3),F(-2),F(2),F(3)]:
   check(finite_prod(abs(x-r)for r in rs)<=abs(x-mean)**n,'outside_component_collapse_product')
check(abs(F(0)-F(0))**2<abs((F(0)+1)*(F(0)-1)),'REJECT_Jensen_across_roots_domain')
# Weighted circle/adjoint formulas evaluated independently through cosine moments.
a=F(9,8);c=(a+2)/2;r=(2-a)/2
rho=[F(1,10),F(1,2)];sigma=[F(2,5),F(3,7)]
xs=[c-r*(z+1/z)/2 for z in rho];Ks=[r*(1-z*z)/(2*z)for z in rho]
check(xs[0]<0<xs[1]<a,'generic_exterior_kernel_points')
check(all(K*K==(a-x)*(2-x)for K,x in zip(Ks,xs)),'Poisson_K_identity')
D=sum(s*K/(a-x)for s,K,x in zip(sigma,Ks,xs));Gamma=sum(s/K for s,K in zip(sigma,Ks))
R0=D-sum(sigma);Bpi=D-sum(s*(1-z)/(1+z)for s,z in zip(sigma,rho))
check(R0==2*sum(s*z/(1-z)for s,z in zip(sigma,rho)) and R0>0,'adjoint_mass_formula')
check(Bpi==4*sum(s*z/(1-z*z)for s,z in zip(sigma,rho)),'adjoint_endpoint_density_formula')
def U_coeff(n):
 # U_(n-1)(cos theta) in the cosine basis, from elementary trig expansion.
 return {j:(1 if j==0 else 2)for j in range(n-1,-1,-2)}
def S_sum(n,z):return sum(coef*z**j for j,coef in U_coeff(n).items())
for n in range(1,41):
 for z in rho:
  closed=(1+z*z-2*z**(n+1))/(1-z*z)if n%2 else 2*z*(1-z**n)/(1-z*z)
  check(S_sum(n,z)==closed,'U_Poisson_moment_closed_form')
for seed in range(12):
 coeff=[F((seed+3)*(j+2)%11-5,j+1)for j in range(16)]
 DM=-sum(s/K*(coeff[0]+2*sum(coeff[n]*z**n for n in range(1,len(coeff))))for s,K,z in zip(sigma,Ks,rho))
 pairing=-2/r*sum(coeff[n]*(D*(1 if n%2 else 0)-sum(s*S_sum(n,z)for s,z in zip(sigma,rho)))for n in range(1,len(coeff)))
 F2=coeff[0]+2*sum((-1)**n*coeff[n]for n in range(1,len(coeff)))
 check(DM-pairing==-Gamma*F2,'corrected_adjoint_identity')
check(-Gamma!=0,'REJECT_uncorrected_adjoint_constant_F')
check(-Gamma<0 and Gamma>0,'endpoint_sign_requires_target_last_root_at_most_two')
# Squared-sinc polarization is a coefficient identity for any real sequences.
for x in [F(-2,3),F(0),F(3,7),F(1)]:
 for y in [F(-1,2),F(1,5),F(1)]:
  Aqr=-x*y;Aqq=-x*x;Arr=-y*y
  check(2*Aqr-Aqq-Arr==(x-y)**2,'circle_Fourier_square_polarization')
# Ordinary circle mass normalization; four quadrants require factor2.
for ap,bp,Q,R,H in [(F(5,4),F(7,3),F(1,3),F(2,5),F(1,8)),(F(3,2),F(2),F(1,2),F(1,4),F(1,6))]:
 # Formal pi cancels; choose a positive rational stand-in to check dimensional algebra.
 pi=F(22,7);p=ap*Q/pi;rr=bp*R/pi
 check(p*rr==ap*bp*Q*R/pi**2,'physical_circle_mass_normalization')
 raw=F(-7,11);Eover=2*raw/(Q*R);even_integral=4*raw
 check(Eover==even_integral/(2*Q*R),'even_extension_factor_two')
 check(Eover!=even_integral/(4*Q*R),'REJECT_missing_circle_factor_two')
# Positive-platform example: q=1/20,A=5/6; positivity uses an exact log sign.
q=F(1,20);s=(1-q)/(1+q);H=2*q/(1+q)**2;A=F(5,6);left=2*s*s-1
check(A<s and 1-A/s>0,'positive_platform_density')
check(H**6>q**5,'positive_platform_C_exact_log_sign')
recip=1/(2*s)
check(1-2*A*s*recip==1-A,'positive_platform_probability_mass')
for z in [F(-3),F(-2),F(0),F(1,3),F(2),F(4)]:
 for S in [F(-2),F(-1,3),F(1,2),F(3)]:
  lhs=A/(z+1)+1/S-2*A*s/(z+1)*(recip+1/S)
  check(lhs==(1-2*A*s/(z+1))/S,'Cauchy_partial_fraction_derivative_identity')
check(2*A*s-1<left,'positive_platform_critical_point_before_conductor')
# L1 potential convergence alone cannot give sign-set convergence at a plateau.
for n in [2,10,100,10000]:
 value=-F(1,n)
 check(abs(value)<1 and value<0,'REJECT_zero_platform_sign_continuity_counterexample')
# Soft-chart real-branch implication is elementary: q(cosh+sinh)<1.
for ch,sh in [(F(5,4),F(3,4)),(F(13,12),F(5,12)),(F(17,15),F(8,15))]:
 check(ch*ch-sh*sh==1,'rational_hyperbolic_pair')
 for qq in [F(1,100),F(1,20),F(1,10)]:
  if 1-qq*ch>0 and qq*sh<1-qq*ch:check(qq*(ch+sh)<1,'soft_chart_atanh_branch_implication')
# Exact k-cover joins and uniqueness family scope are independent of rounded margins.
check(F(36,25)<F(29,20),'elementary_affine_overlap')
def gapfree(intervals,left,right):
 reach=left
 for a,b in sorted(intervals):
  if b<left:continue
  if a>reach:return False
  reach=max(reach,b)
 return reach>=right
cover=[(F(1),F(29,20)),(F(36,25),F(21,10)),(F(21,10),F(21,5))]
check(gapfree(cover,F(1),F(21,5)),'finite_k_cover_from_literal_endpoints')
bad=[(F(1),F(29,20)),(F(147,100),F(21,10)),(F(21,10),F(21,5))]
check(not gapfree(bad,F(1),F(21,5)),'REJECT_finite_k_gap_mutation')
check(F(1,50)<F(27,100)<F(28,100)<F(87,200),'bulk_chart_endpoint_order')
# Replacing narrow T by shortened high decimal would be a strictly weaker bridge.
T=F('1.83443047576266171109075363512901884952989750747');coarse=F('1.834430475762662')
check(T<coarse,'REJECT_short_decimal_as_exact_calibration_target')
print(json.dumps({'status':'PASS','optimization':sys.flags.optimize,'checks':sum(C.values()),'categories':dict(sorted(C.items())),'scope':['Exact finite algebra and domain counterexamples only.','No author code, stationary-point search or certificate6.1/7.1 numerical replay.','Generic kernel points are not asserted to be certified reference roots.','Rational pi stand-in checks cancellation algebra, not pi numerics.','Written analytic arguments and primary theorem statements are decisive.']},indent=2))
