#!/usr/bin/env python3
"""Exact covariance, whitening and Lyapunov controls for the scoped EKI result."""
from pathlib import Path
from hashlib import sha256
from collections import Counter
from fractions import Fraction as Q
import json
import sympy as s
C=Counter()
def ck(cat,ok):
    assert bool(ok),cat
    C[cat]+=1
def zero(A):return all(s.simplify(v)==0 for v in A)
def norm2(A):return s.expand(sum(v*v for v in A))
def psd2(A):
    return A==A.T and A[0,0]>=0 and A[1,1]>=0 and A.det()>=0
def covariance(us,hs):
    J=len(us);um=sum(us,s.zeros(us[0].rows,1))/J;hm=sum(hs,s.zeros(hs[0].rows,1))/J
    cu=sum([(u-um)*(v-hm).T for u,v in zip(us,hs)],s.zeros(us[0].rows,hs[0].rows))/J
    cp=sum([(v-hm)*(v-hm).T for v in hs],s.zeros(hs[0].rows))/J
    return cu,cp,um,hm
rootGamma=s.Matrix([[2,1],[1,2]]);Gamma=rootGamma**2;J=3;M2=s.Integer(2);z=s.Matrix([s.Rational(2,3),s.Rational(-1,4)])
for seed in range(31):
    us=[s.Matrix([((seed+1)*(j+2))%7-3,((seed+3)*(j+1))%9-4]) for j in range(J)]
    hs=[s.Matrix([s.Rational(((seed+j*j)%5)-2,2),s.Rational(((2*seed+3*j)%5)-2,2)]) for j in range(J)]
    cu,cp,um,hm=covariance(us,hs);U2=sum(norm2(u) for u in us)
    ck('centered_variance_identity',s.expand(sum(norm2(u-um) for u in us)-(U2-J*norm2(um)))==0)
    ck('centered_observation_identity',s.expand(sum(norm2(v-hm) for v in hs)-(sum(norm2(v) for v in hs)-J*norm2(hm)))==0)
    ck('cross_covariance_growth',norm2(cu)<=M2*U2/J)
    ck('observation_covariance_bound',psd2(M2*s.eye(2)-cp) and psd2(cp))
    rawhs=[rootGamma*v for v in hs]
    cup,cpp,_,_=covariance(us,rawhs)
    ck('whitening_covariances',zero(cup*rootGamma.inv()-cu) and zero(rootGamma.inv()*cpp*rootGamma.inv()-cp))
    for h in (s.Rational(1,16),s.Rational(1,4),s.Rational(1,2),s.Rational(1),s.Rational(2)):
        R=(s.eye(2)+h*cp).inv();K=cu*R
        ck('resolvent_noncommuting_whitening',zero(cup*(Gamma+h*cpp).inv()*rootGamma-K))
        ck('resolvent_contraction',psd2(s.eye(2)-R*R))
        ck('resolvent_consistency',zero(R-s.eye(2)+h*cp*R))
        ck('diffusion_linear_growth',J*norm2(K)<=M2*U2)
        ck('diffusion_consistency',norm2(K-cu)<=h*h*M2*M2*norm2(cu))
        f=sum(norm2(K*(z-v)) for v in hs)
        ck('drift_linear_growth',f<=2*M2*(norm2(z)+M2)*U2)
        # Exact raw and whitened drifts agree for each particle.
        rawz=rootGamma*z
        for rawv,v in zip(rawhs,hs):
            ck('drift_whitening',zero(cup*(Gamma+h*cpp).inv()*(rawz-rawv)-K*(z-v)))

# Consensus ensembles, including the zero ensemble, make every update coefficient zero.
for x in range(-4,5):
    us=[s.Matrix([x,2*x])]*J;hs=[s.Matrix([s.Rational(1,2),s.Rational(-1,3)])]*J
    cu,cp,_,_=covariance(us,hs)
    ck('consensus_zero_coefficients',zero(cu) and zero(cp))

h,R,a=s.symbols('h R a',positive=True)
us=[s.Matrix([R]),s.Matrix([-a*R])];hs=[s.Matrix([R]),s.Matrix([0])]
cu,cp,_,_=covariance(us,hs)
cv=(1+a)*R**2/4;sv=R**2/4
ck('positive_part_covariance',s.simplify(cu[0]-cv)==0 and s.simplify(cp[0]-sv)==0)
LV=-2*R**2*cv+2*cv**2
ck('quadratic_generator_identity',s.factor(LV-(1+a)*(a-3)*R**4/8)==0)
D=1+h*sv
means=[R-h*cv*R/D,-a*R];variance=h*cv**2/D**2
delta=s.factor(sum(x*x for x in means)+2*variance-(1+a*a)*R*R)
claimed=h*R**4*((1+a)*(a-3)/8+h*R**2*(1+a)*(a-1)/16)/D**2
ck('discrete_conditional_energy_identity',s.factor(delta-claimed)==0)
ratio=s.factor(delta.subs({a:5,h:R**(-4)})/(R**(-4)*(1+26*R*R)))
ck('failure_of_uniform_quadratic_one_step_bound',s.limit(ratio/R**2,R,s.oo)==s.Rational(3,52))
ck('failure_of_quadratic_generator_bound',s.limit((LV/(1+(1+a*a)*R*R)).subs(a,5)/R**2,R,s.oo)==s.Rational(3,52))
for rr in range(1,41):
    for aa in (s.Rational(7,2),s.Integer(4),s.Integer(5),s.Integer(9)):
        hh=s.Rational(1,rr**4)
        ck('positive_drift_exact_controls',claimed.subs({R:rr,a:aa,h:hh})>0)
        # Discrete infinitesimal drift agrees with the exact continuous generator.
        ck('infinitesimal_generator_match',s.simplify(s.limit(delta/h,h,0).subs({R:rr,a:aa})-LV.subs({R:rr,a:aa}))==0)

# Compactly supported observation diagnostic: G(0)=1, G(1/2)=0.
us=[s.Matrix([0]),s.Matrix([s.Rational(1,2)])];hs=[s.Matrix([1]),s.Matrix([0])]
cu,cp,_,_=covariance(us,hs)
ck('compact_forward_covariance',cu[0]==-s.Rational(1,8) and cp[0]==s.Rational(1,4))
mu=-h*cu[0]/(1+h*cp[0]);var=h*cu[0]**2/(1+h*cp[0])**2
ck('compact_forward_Gaussian_mean',s.factor(mu-h/(8*(1+h/4)))==0)
ck('compact_forward_Gaussian_variance',s.factor(var-h/(64*(1+h/4)**2))==0)
for k in range(1,65):
    ck('compact_forward_positive_variance',var.subs(h,s.Rational(1,k))>0)
# Brownian covariance convention: h^{-1} Gamma observation noise produces
# h Cup (Gamma+h Cpp)^{-1} times Gamma^{1/2}/sqrt(h), hence sqrt(h) gain.
cup=s.Matrix([[1,2],[3,-1]]);cpp=s.Matrix([[2,1],[1,3]])
for hh in (s.Rational(1,4),s.Rational(1,9),s.Rational(1,16)):
    A=cup*(cpp+Gamma/hh).inv()
    noise=A*Gamma*A.T/hh
    gain=cup*(Gamma+hh*cpp).inv()
    ck('observation_noise_scaling',zero(noise-hh*gain*Gamma*gain.T))
root=Path(__file__).resolve().parent
out={'verdict':'PASS','assertions':sum(C.values()),'categories':dict(C),
 'artifact_sha256':sha256((root/'PARTIAL.md').read_bytes()).hexdigest(),'sympy_version':s.__version__,
 'scope':'Exact covariance, resolvent and energy algebra only. No finite test certifies stochastic path convergence or disproves general EKI convergence.'}
(root/'verification.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))

