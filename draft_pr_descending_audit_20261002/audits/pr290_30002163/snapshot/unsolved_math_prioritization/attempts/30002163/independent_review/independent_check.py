"""Independent exact direct-distance certificates and arithmetic controls.
Uses certified rational cosine upper bounds, not the author's proof-derived pair bound.
"""
from fractions import Fraction as F
from math import factorial,isqrt
from collections import Counter
import json
C=Counter()
def ck(x,n):
    assert x,n
    C[n]+=1
def atan_partial(x,k):return sum(((-1)**j*x**(2*j+1)/F(2*j+1)) for j in range(k+1))
# Machin's identity pi=16atan(1/5)-4atan(1/239), with alternating-series enclosures.
aL,aU=atan_partial(F(1,5),21),atan_partial(F(1,5),20)
bL,bU=atan_partial(F(1,239),21),atan_partial(F(1,239),20)
pL,pU=16*aL-4*bU,16*aU-4*bL
ck(3<pL<pU<F(22,7),'Machin_pi_enclosure_order')
ck(pU-pL<F(1,10**28),'Machin_pi_enclosure_width')
# Exact tangent multiple-angle control for the identity; branch is in (0,pi/2).
def tan_add(a,b):return (a+b)/(1-a*b)
t=F(1,5)
for _ in range(3):t=tan_add(t,F(1,5))
ck(tan_add(t,-F(1,239))==1,'Machin_exact_tangent_identity')
def cos_upper(r,q):
    # theta in [0,pi]. cos decreases there; evaluate an upper Taylor polynomial at theta_lower.
    x=2*pL*r/q
    return sum((-1)**j*x**(2*j)/factorial(2*j) for j in range(13))
f=[0,1]
for _ in range(31):f.append(f[-1]+f[-2])
pairs=0;maxq=0
for n in range(3,15):
    q,p=f[n],f[n-1];maxq=q
    bounds={}
    for m in range(1,q):
        r=min(p*m%q,(-p*m)%q);v=cos_upper(r,q)
        bounds[m]=(v.numerator,v.denominator)
    for i in range(q):
        for j in range(i+1,q):
            H=q*(i+j-1)-2*i*j;P=i*(q-i)*j*(q-j);num,den=bounds[j-i]
            ck(H==q*(j-i-1)+2*i*(q-j) and H>=0,'direct_distance_nonnegative_left_side')
            # D²>=4/q is equivalent to H>=2sqrt(P)cos(theta).
            if num>0:ck(H*H*den*den>=4*P*num*num,'direct_distance_positive_cosine_squared_certificate')
            else:ck(H>=0,'direct_distance_nonpositive_cosine_certificate')
            pairs+=1
    ck(4*F(1,q)*(1-F(1,q))+F(4,q*q)==F(4,q),'north_pole_exact_attainment')
# Integer identity checked at both signed representatives, not just nearest positive residue.
for n in range(3,26):
    q,p=f[n],f[n-1];sgn=(-1)**n
    ck(p*p+p*q-q*q==sgn,'Cassini_exact_sign')
    for m in range(1,isqrt(q)+1):
        if m*m>=q:continue
        ell=(m*p)//q
        for L in [ell,ell+1,ell-1]:
            s=m*p-L*q;B=L*L+L*m-m*m;r=abs(s)
            ck(B!=0,'nonzero_integer_quadratic_form')
            ck(q*q*B==sgn*m*m-(2*p+q)*m*s+s*s,'both_signed_residue_identity')
            if q>=8 and 4*r<q:ck(4*m*r>q,'dangerous_regime_exact_margin')
# Rational latitude discriminant and pole limits, independently using integer numerators.
for q in range(2,25):
    for i in range(q):
        for j in range(i+1,q+1):
            T=i*(q-j)+j*(q-i);m=j-i;P=i*(q-i)*j*(q-j)
            ck(T*T-q*q*m*m==4*P,'integer_latitude_discriminant')
            ck(T-q*m==2*i*(q-j)>=0,'pole_safe_nonnegative_discriminant_branch')
print(json.dumps({'status':'PASS','assertions':sum(C.values()),'direct_pair_certificates':pairs,'largest_direct_pair_size':maxq,'counts':dict(sorted(C.items())),'scope':'Direct finite chord-distance lower certificates with rational Machin/Taylor cosine bounds, signed Cassini controls and polar algebra. Uniform proof is separately audited in prose.'},sort_keys=True,indent=2))
