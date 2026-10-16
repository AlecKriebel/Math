#!/usr/bin/env python3
"""Portable exact finite checks for the Goh-1992/candidate source comparison.

Python >=3.9, standard library only. No source-file, PDF, or canonical-manuscript
access. Emits a full JSON record on stdout; failure returns a nonzero status.
This is not a proof of the analytic theorems explicitly listed in the record.
"""
from fractions import Fraction as F
import json
import sys

class G:
    def __init__(self, re=0, im=0):
        if isinstance(re, G):
            self.re, self.im = re.re, re.im
        else:
            self.re, self.im = F(re), F(im)
    def __add__(self, other):
        other=G(other); return G(self.re+other.re,self.im+other.im)
    __radd__=__add__
    def __neg__(self): return G(-self.re,-self.im)
    def __sub__(self,other): return self+-G(other)
    def __rsub__(self,other): return G(other)+-self
    def __mul__(self,other):
        other=G(other)
        return G(self.re*other.re-self.im*other.im,self.re*other.im+self.im*other.re)
    __rmul__=__mul__
    def __truediv__(self,other):
        other=G(other); q=other.re**2+other.im**2
        return G((self.re*other.re+self.im*other.im)/q,(self.im*other.re-self.re*other.im)/q)
    def __pow__(self,n):
        if n<0: return (G(1)/self)**(-n)
        v=G(1)
        for _ in range(n): v=v*self
        return v
    def __eq__(self,other):
        other=G(other); return self.re==other.re and self.im==other.im
    def conj(self): return G(self.re,-self.im)
    def json(self): return {'real':str(self.re),'imag':str(self.im)}

class P:
    """Laurent polynomials over Q(i), sparse canonical monomials."""
    def __init__(self, value=0):
        if isinstance(value,P): self.d=dict(value.d)
        elif isinstance(value,dict): self.d={k:G(v) for k,v in value.items() if G(v)!=0}
        else: self.d={} if G(value)==0 else {():G(value)}
    def __add__(self,other):
        out=dict(self.d)
        for k,v in P(other).d.items(): out[k]=out.get(k,G())+v
        return P(out)
    __radd__=__add__
    def __neg__(self): return P({k:-v for k,v in self.d.items()})
    def __sub__(self,other): return self+-P(other)
    def __rsub__(self,other): return P(other)+-self
    def __mul__(self,other):
        out={}
        for ka,va in self.d.items():
            for kb,vb in P(other).d.items():
                ex=dict(ka)
                for k,n in kb: ex[k]=ex.get(k,0)+n
                key=tuple(sorted((k,n) for k,n in ex.items() if n))
                out[key]=out.get(key,G())+va*vb
        return P(out)
    __rmul__=__mul__
    def __pow__(self,n):
        if n<0:
            if len(self.d)!=1: raise ValueError('Negative powers need one monomial')
            (key,val),=self.d.items()
            return P({tuple((k,m*n) for k,m in key):val**n})
        out=P(1)
        for _ in range(n): out=out*self
        return out
    def __truediv__(self,other): return self*(P(other)**-1)
    def __eq__(self,other): return self.d==P(other).d
    def coeff(self,var,degree):
        out={}
        for key,val in self.d.items():
            ex=dict(key)
            if ex.get(var,0)==degree:
                ex.pop(var,None);out[tuple(sorted(ex.items()))]=val
        return P(out)
    def derivative(self,var):
        out=P()
        for key,val in self.d.items():
            ex=dict(key); n=ex.get(var,0)
            if n:
                ex[var]=n-1
                out=out+P({tuple(sorted((k,m) for k,m in ex.items() if m)):val*n})
        return out
    def at(self, **values):
        out=P()
        for key,val in self.d.items():
            term=P(val)
            for name,n in key: term=term*(P(values[name]) if name in values else X(name))**n
            out=out+term
        return out
    def json(self):
        return [{'monomial':dict(k),'coefficient':v.json()} for k,v in sorted(self.d.items())]

def X(name): return P({((name,1),):G(1)})

def encoded(x):
    if isinstance(x,P): return x.json()
    if isinstance(x,G): return x.json()
    if isinstance(x,F): return str(x)
    if isinstance(x,dict): return {k:encoded(v) for k,v in x.items()}
    if isinstance(x,(tuple,list)): return [encoded(v) for v in x]
    return x

checks=[]
def identity(name,left,right,**witness):
    checks.append({'name':name,'pass':left==right,'left':encoded(left),'right':encoded(right),**encoded(witness)})
def test(name,condition,**witness):
    checks.append({'name':name,'pass':bool(condition),**encoded(witness)})

I=P(G(0,1))
z,a2,a3,a4,s,n,m,b1,b2,r,h,u,e,v,t,w=[X(k) for k in ['z','a2','a3','a4','s','n','m','b1','b2','r','h','u','e','v','t','w']]
f=z+a2*z**2+a3*z**3+a4*z**4
pj={}
for j in (2,3,4):
    pj[j]=sum(((f**(k+1)).coeff('z',j)*s**k for k in range(1,j)),P())
identity('source_P2_from_coefficient_definition',pj[2],s)
identity('source_P3_from_coefficient_definition',pj[3],s**2+2*a2*s)
identity('source_P4_from_coefficient_definition',pj[4],s**3+3*a2*s**2+(2*a3+a2**2)*s)
z0=X('z0')
identity('source_ell3_double_tip_even_quartic',(z-z0)**2*(z+z0)**2,(z**2-z0**2)**2)
identity('source_ell3_integrated_rational_equation',z**2*(z+z0**2/z+X('c3')).derivative('z')**2,(z**2-z0**2)**2/z**2)
En=2*b2+(n-1)*(a2*b1**2-b2)+r*b1**2-2*a2*b1-r*b1
Em=2*b2+(m-1)*(a2*b1**2-b2)+h*b1**2-2*a2*b1-h*b1
D=(n-m)*(a2*b1**2-b2)+(r-h)*(b1**2-b1)
identity('source_equation_5_subtraction',En-Em,D)
alpha_num=(m-3)*r-(n-3)*h
identity('source_equation_7_elimination_without_denominators',(n-m)*En-(n-3)*D,(2*(n-m)*a2-alpha_num)*b1*(b1-1),note='Requires n!=m and b1!=0 before division; b1=1 is handled separately.')
A=2*a3+a2**2-6*a2
B=3*a2-3
aa=1+I*e*A
bb=I*e*B
cc=I*e
PL=pj[2]-3*I*e*pj[3]+I*e*pj[4]
identity('candidate_source_polynomial_matches_candidate_Q',PL,aa*s+bb*s**2+cc*s**3)
Q=-aa*w**-3-bb*w**-4-cc*w**-5
pull=Q.at(w=-v**-2)*(2*v**-3)**2
identity('candidate_double_cover_pullback',pull,4*(aa-bb*v**2+cc*v**4))
identity('candidate_Koebe_limit_polynomial',(aa-bb*v**2+cc*v**4).at(a2=2,a3=3),1+I*e*(-2-3*v**2+v**4))
# Goh equation (2) for a generic Koebe rotation, with conjugate(u)=u^-1.
lams={2:P(1),3:-3*I*e,4:I*e}
clams={2:P(1),3:3*I*e,4:-I*e}
aks={1:P(1),2:2*u,3:3*u**2,4:4*u**3}
caks={1:P(1),2:2*u**-1,3:3*u**-2,4:4*u**-3}
R=sum((lams[j]*sum((k*aks[k]*z**(k-j) for k in range(1,j)),P())+(j-1)*lams[j]*aks[j]+clams[j]*sum((k*caks[k]*z**(j-k) for k in range(1,j)),P()) for j in (2,3,4)),P())
# Cancellation of (1-uz)^2 against the logarithmic derivative is exact.
LHS=(1+u*z)**2*(lams[4]*(1-u*z)**4*z**-3+(lams[3]+6*u*lams[4])*(1-u*z)**2*z**-2+(lams[2]+4*u*lams[3]+10*u**2*lams[4])*z**-1)
res=LHS-R
C3=res.coeff('z',3)
C2=res.coeff('z',2)
identity('Koebe_rotation_highest_Schiffer_residual',C3,I*e*(u**6+1))
identity('Koebe_rotation_next_Schiffer_residual',C2,-3*I*e*(u**4+1)+4*u**-1*C3)
identity('Koebe_impossibility_exact_Bezout',(1-u**2-u**4)*(u**4+1)+(u**2+1)*(u**6+1),P(2),consequence='For e!=0 a critical Koebe rotation would have u^6+1=u^4+1=0; Bezout gives 2=0. The rotation unit-circle assumption was used only in conjugate(u)=u^-1.')
# Formal perturbation coefficients and finite rational controls; not a global existence proof.
d=t+F(1,2)*t**3-F(1,10)*t**5
q=t**2-F(2,5)*t**4
identity('candidate_first_order_P0',-2*d.derivative('t'),-2-3*t**2+t**4)
identity('candidate_first_order_q',d.derivative('t')-d/t,q)
identity('candidate_q_at_1',q.at(t=1),P(F(3,5)))
identity('candidate_q_at_7_over_4',q.at(t=F(7,4)),P(F(-441,640)))
# The most direct lower-degree perturbative route in the source has one term.
d3=-2*t+F(1,6)*t**3
identity('source_degree3_perturbation_P0',-2*d3.derivative('t'),4-t**2)
identity('source_degree3_perturbation_q',d3.derivative('t')-d3/t,F(1,3)*t**2,note='First-order local diagnostic only. Does not prove monotonicity or refute any source theorem.')
eps=F(1,10**24);eta=F(1,10**12)
test('epsilon_eta_relation',eta**2==eps,epsilon=eps,eta=eta)
controls={
 'P_coefficient_uncertainty':F(106)+24*9,
 'P0_disk_bound':F(2)+3*9+81,
 'P0_derivative_disk_bound':F(6)*3+4*27,
 'dprime_disk_bound':F(1)+F(3,2)*9+F(1,2)*81,
 'sqrt_quadratic_absorption':F(111**2,2)*eta,
 'inverse_absorption':F(18315)*eta,
 'derivative_absorption':F(45621)*eta,
 'Z_numerator_bound':2*(F(7,4)*162+487),
 'Z_quadratic_bound':2*7*333,
 'positive_endpoint_margin':F(3,5)-2000*eta-F(1,2),
 'negative_endpoint_margin':F(441,640)-2000*eta-F(1,2),
 'slit_tip_upper_bound':F(7,25)+7*eta,
 'constructed_arc_radius_lower_bound':F(25,81),
 'tip_radius_gap':F(25,81)-F(3,10),
 'orientation_numerator_inequality':F(222)*eps/(1-111*eps),
 'rouche_error':F(333)*eps,
 'trajectory_V_bound':F(7,4)+333*eps,
}
identity('exact_rational_constants_322',P(controls['P_coefficient_uncertainty']),P(322))
identity('exact_rational_constants_110',P(controls['P0_disk_bound']),P(110))
identity('exact_rational_constants_126',P(controls['P0_derivative_disk_bound']),P(126))
identity('exact_rational_constants_55',P(controls['dprime_disk_bound']),P(55))
identity('exact_rational_constants_1541',P(controls['Z_numerator_bound']),P(1541))
identity('exact_rational_constants_4662',P(controls['Z_quadratic_bound']),P(4662))
for name in ['sqrt_quadratic_absorption','inverse_absorption','derivative_absorption']:
    test(name,controls[name]<1,value=controls[name],upper=1)
test('candidate_P_remainder_absorption',322*eta<1,coefficient_uncertainty=322*eta)
test('candidate_Z_error_absorption',1541+4662*eta<2000,left=1541+4662*eta,right=2000)
test('candidate_both_endpoint_signs_have_half_epsilon_margin',controls['positive_endpoint_margin']>0 and controls['negative_endpoint_margin']>0,positive_margin=controls['positive_endpoint_margin'],negative_margin=controls['negative_endpoint_margin'])
test('candidate_actual_tip_separation_control',controls['slit_tip_upper_bound']<F(3,10)<controls['constructed_arc_radius_lower_bound'],tip_upper=controls['slit_tip_upper_bound'],radius_separator=F(3,10),arc_lower=controls['constructed_arc_radius_lower_bound'],gap=controls['tip_radius_gap'])
test('candidate_orientation_control',controls['orientation_numerator_inequality']<223*eps<1,computed_bound=controls['orientation_numerator_inequality'],stated_bound=223*eps)
test('candidate_rouche_control',controls['rouche_error']<1,computed_bound=controls['rouche_error'])
test('candidate_trajectory_radius_control',controls['trajectory_V_bound']<F(9,5),computed_bound=controls['trajectory_V_bound'])
# Complex leading normalization reverses the order of two genuine S members.
Lk=G(2,-5*eps)
normalized=Lk/G(0,eps)
test('complex_division_does_not_preserve_Re_objective',Lk.re>0 and normalized.re<0,L_at_Koebe=Lk,normalized_L_at_Koebe=normalized,L_at_identity=G(0),normalized_L_at_identity=G(0))
# Finite low-degree arithmetic underpinning the relevant Goh applications.
import math
cases=[{'n':N,'ell':ell,'gcd':math.gcd(N-1,ell-1),'covered_by':'Theorem 3' if math.gcd(N-1,ell-1)==1 else 'Theorem 4' if ell==3 else 'not covered here'} for N in (3,4,5) for ell in range(2,N)]
test('all_equal_degree_3_4_5_cases_covered',all(c['covered_by']!='not covered here' for c in cases),cases=cases)
identity('candidate_top_normalized_penultimate',P(G(0,-3*eps))/P(G(0,eps)),P(-3))
# Formula for Theorem 1 when candidate n=4 and m>4.
identity('candidate_unequal_degree_alpha_numerator',((m-3)*r-(4-3)*h).at(r=-3),-3*(m-3)-h,note='Divide by 4-m; equivalently alpha=(3(m-3)+h)/(m-4). No simultaneous-support hypothesis is supplied by this identity.')

out={
 'schema':'goh1992-source-candidate-exact-audit-v1',
 'arithmetic':'Exact rational and Gaussian-rational sparse Laurent polynomials; Python standard library only.',
 'source_sha256':'94af0c114ce2ced1cb7f2337568c4ce0b8e0615c1ec32542f226d9bf177a0503',
 'historical_candidate_tex_sha256':'c46d521e893a46466cf26b50c54294d1923e93dad4076e4b5dfa16c52d42830a',
 'checks':checks,
 'rational_controls':encoded(controls),
 'all_pass':all(x['pass'] for x in checks),
 'analytic_inputs_not_proved':[
  'Compactness of S and coefficient/area theorems.',
  'Support-slit/Schiffer theorem, positivity, slit-tip regularity, and trajectory identification.',
  'Goh two-equation algebraic continuation and rational-support classification.',
  'Kirwan-Pell strict support bound and Brown classification cited by Goh.',
  'Analytic uniform remainder estimates are checked only through their finite algebra and rational inequalities, not formalized.',
 ],
 'priority_scope':'Full Goh paper read separately. This finite checker alone proves neither historical priority nor an actual support-slit counterexample.',
}
print(json.dumps(out,indent=2,sort_keys=True))
sys.exit(0 if out['all_pass'] else 1)
