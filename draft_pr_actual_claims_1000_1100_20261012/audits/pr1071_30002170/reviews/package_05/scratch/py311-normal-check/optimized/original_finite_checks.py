"""Fresh finite exact evidence for the submitted area/witness normalization.

Uses only Python standard library. This is an audit computation, not a replay
of any historical omitted program and not a replacement for the proof.
"""
from fractions import Fraction as F
from math import sqrt, pi, gamma, sin
from pathlib import Path
import json
from datetime import datetime, timezone

def derivative(p):
    return [F(k)*p[k] for k in range(1,len(p))]

def evaluate(p,x):
    y=F(0)
    for c in reversed(p): y=y*x+c
    return y

def product(p,q):
    z=[F(0)]*(len(p)+len(q)-1)
    for i,a in enumerate(p):
        for j,b in enumerate(q):z[i+j]+=a*b
    return z

def integral(p): return sum((c/F(k+1) for k,c in enumerate(p)),F(0))

phi=list(map(F,[0,0,0,0,1,-4,6,-4,1]))
ders=[phi]
for k in range(4):ders.append(derivative(ders[-1]))
endpoint_traces={str(k):[str(evaluate(ders[k],F(0))),str(evaluate(ders[k],F(1)))] for k in range(4)}
assert all(pair==['0','0'] for pair in endpoint_traces.values())
a=integral(product(ders[1],ders[1]));assert a==F(4,45045)
gnorm=integral(phi); fnorm=2*evaluate(phi,F(1,2));assert (gnorm,fnorm)==(F(1,630),F(1,128))
# In y=2x-1, phi''=(-1+9y²-15y⁴+7y⁶)/8.
phi2_y2=[F(-1,8),F(9,8),F(-15,8),F(7,8)]
peak=evaluate(phi2_y2,F(3,7)); valley=evaluate(phi2_y2,F(0))
gnorm3=4*peak-2*valley;assert (peak,valley,gnorm3)==(F(4,49),F(-1,8),F(113,196))
# phi''''=3(35y⁴-30y²+3), roots squared q±.
qminus=(15-2*sqrt(30))/35;qplus=(15+2*sqrt(30))/35
third=lambda q:1.5*sqrt(q)*(1-q)*(3-7*q)
fnorm3=4*(third(qminus)-third(qplus)); assert fnorm3>0

def rho(H,r):return ((abs(r+1))**(2*H)+(abs(r-1))**(2*H)-2*abs(r)**(2*H))/2

variance_checks=[]
for m in [1,2,3,8,23]:
    # Brownian independent increments, exact normalized T=1 covariance.
    direct=sum((F(1,m)**2 if j==k else F(0) for j in range(m) for k in range(m)),F(0))/4
    grouped=F(m,4*m*m)
    assert direct==grouped==F(1,4*m)
    # For H=1 (excluded), rho(r)=1: Q still vanishes, while area is recoverable.
    H1=F(m+2*sum((m-r) for r in range(1,m)),4*m**4)
    assert H1==F(1,4*m*m)
    # At H=1, increments have covariance delta²: there are m² terms.
    # The correction is (1/2) m*(1/m²)*Z1 Z2, hence variance 1/(4m²).
    # It vanishes although the harmonic witness fails; endpoint area is recoverable.
    variance_checks.append({'m':m,'Brownian_Q_variance':str(direct),'H1_Q_variance':str(H1)})

deterministic_sums=[]
for m in [1,2,3,5,11,101]:
    left=F(0);correction=F(0)
    for k in range(m):
        t=F(k,m);u=F(k+1,m)
        ft,fu=evaluate(ders[1],t),evaluate(ders[1],u)
        gt,gu=evaluate(phi,t),evaluate(phi,u)
        left+=ft*(gu-gt);correction+=(fu-ft)*(gu-gt)/2
    polygon=left+correction
    trapezoid=sum(((evaluate(ders[1],F(k,m))+evaluate(ders[1],F(k+1,m)))*(evaluate(phi,F(k+1,m))-evaluate(phi,F(k,m)))/2 for k in range(m)),F(0))
    assert polygon==trapezoid
    deterministic_sums.append({'m':m,'Euler_covariance_pairing':str(left),'polygon_covariance_pairing':str(polygon),'difference_from_a':str(left-a)})

signed_A=[[F(2),F(-1)],[F(-1),F(2)]]
signed_C=[[F(1),F(1,2)],[F(1,2),F(1)]]
traceAC=sum((signed_A[j][k]*signed_C[j][k] for j in range(2) for k in range(2)),F(0))
assert traceAC==3 and traceAC<=2*F(3)*F(3,2)
normalization_faults=[]
for n in [1,2,7,19]:
    euler=F(1,2*n);q=F(1,4*n);error_q_cov=q
    optimum=euler-2*error_q_cov+q
    assert optimum==F(1,4*n)
    normalization_faults.append({'n':n,'Euler_variance':str(euler),'Q_variance':str(q),'Euler_error_Q_covariance':str(error_q_cov),'optimum_variance':str(optimum),'unhalved_antisymmetric_residual_variance':str(4*optimum)})

floating_variances=[]
for H in [.251,1/3,.5,.749,.75,.9,.999]:
    for m in [1,2,7,19]:
        direct=sum(rho(H,j-k)**2 for j in range(m) for k in range(m))/(4*m**(4*H))
        grouped=(m+2*sum((m-r)*rho(H,r)**2 for r in range(1,m)))/(4*m**(4*H))
        assert abs(direct-grouped)<=2e-14*max(1,abs(direct))
        floating_variances.append({'H':H,'m':m,'direct':direct,'grouped':grouped,'difference':direct-grouped})

constant_checks=[]
for H in [.251,1/3,.5,.75,.9,.999]:
    alpha=2*H+1;D=2*pi/(gamma(1+2*H)*sin(pi*H))
    def pbar(norm,norm3):return pi**alpha*norm**2+2*norm3**2*pi**(alpha-6)*(1+1/(2*(5-alpha)))
    pf=pbar(float(fnorm),fnorm3);pg=pbar(float(gnorm),float(gnorm3));c=2*pi*float(a)/(D*sqrt(pf*pg))
    assert D>0 and pf>0 and pg>0 and c>0
    if H==.5:assert abs(D-2*pi)<1e-14 and c<.5
    constant_checks.append({'H':H,'D_H':D,'Pbar_f':pf,'Pbar_g':pg,'c_H':c})

out={'utc':datetime.now(timezone.utc).isoformat(),'exact_area_pairing':str(a),'endpoint_traces_phi_derivatives_0_to_3':endpoint_traces,'L1_f':str(fnorm),'L1_g':str(gnorm),'L1_gthird':str(gnorm3),'L1_fthird_radical_formula':'4*(F(qminus)-F(qplus)), F(q)=(3/2)sqrt(q)(1-q)(3-7q), q±=(15±2sqrt(30))/35','L1_fthird_numeric':fnorm3,'exact_Brownian_and_H1_variances':variance_checks,'exact_deterministic_finite_Euler_pairing_sums':deterministic_sums,'exact_signed_PSD_trace_example':{'A':[[str(z) for z in row] for row in signed_A],'C':[[str(z) for z in row] for row in signed_C],'traceAC':str(traceAC),'nMfMg':'9'},'exact_Brownian_normalization_fault_checks':normalization_faults,'finite_covariance_identity_float_cross_checks':floating_variances,'constant_float_checks':constant_checks,'meaning':'Finite evidence complements the analytic proof. H=.25 Q variance >=1/4 by diagonal term, so does not tend to zero. H=1 Q does tend to zero; failure there is D_H divergence and endpoint recovery, not a correction failure. Brownian optimal variance=1/(4n), Euler variance=1/(2n).'}
Path(__file__).with_name('FINITE_CHECKS.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({'a':str(a),'L1_f':str(fnorm),'L1_g':str(gnorm),'L1_gthird':str(gnorm3),'L1_fthird':fnorm3,'all_checks':'passed'},indent=2))
