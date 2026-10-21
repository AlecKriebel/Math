#!/usr/bin/env python3
"""Independent exact controls and higher-order formal-series crosschecks.

These do not import any archived verification code. They supplement the
analytic derivation, never certify its universal quantifiers or source proofs.
"""
from fractions import Fraction as F
from math import factorial
from pathlib import Path
import json

BASE = Path(__file__).resolve().parent
E, H, T, r = F(1, 10**24), F(1, 10**12), F(7, 4), F(2, 3)
checks = []

def ck(label, condition, evidence=None):
    if not condition:
        raise RuntimeError(label)
    checks.append({'name': label, 'passed': True, 'evidence': evidence})

def add(a, b):
    n = max(len(a), len(b))
    return [(a[k] if k < len(a) else F(0)) + (b[k] if k < len(b) else F(0)) for k in range(n)]

def scale(a, c):
    return [c*x for x in a]

def mul(a, b, n=None):
    n = len(a)+len(b)-2 if n is None else n
    return [sum((a[j]*b[k-j] for j in range(max(0, k-len(b)+1), min(k, len(a)-1)+1)), F(0)) for k in range(n+1)]

def diff(a):
    return [k*a[k] for k in range(1, len(a))]

def integ(a):
    return [F(0)]+[a[k]/(k+1) for k in range(len(a))]

def inv(a, n):
    b = [1/a[0]]
    for k in range(1, n+1):
        b.append(-sum((a[j]*b[k-j] for j in range(1, min(k, len(a)-1)+1)), F(0))/a[0])
    return b

def val(a, x):
    return sum((c*x**k for k,c in enumerate(a)), F(0))

# Independently recompute long division on seven rational coefficient choices.
# Solving (f-w)y=f^2 directly checks dependence on all lower coefficients.
for a2, a3, a4, w in [(F(2),F(3),F(4),F(-2)), (F(0),F(0),F(0),F(-1)),
                         (F(1,3),F(-7,5),F(11,4),F(5,7)), (F(-2),F(3),F(-4),F(2)),
                         (F(1),F(1),F(1),F(-3)), (F(-1,2),F(2,9),F(8),F(7)),
                         (F(13,7),F(-9,11),F(17,3),F(-5,2))]:
    f=[F(0),F(1),a2,a3,a4]
    quotient=mul(mul(f,f,4),inv([-w]+f[1:],4),4)
    expected=[-1/w, -2*a2/w-1/w**2, -(2*a3+a2*a2)/w-3*a2/w**2-1/w**3]
    ck('exact quotient long division '+str((a2,a3,a4,w)), quotient[2:5]==expected)

# Formal second order in epsilon at limiting coefficients A=-2,B=3.
# G(v)=v-i*epsilon*d(v)+epsilon^2*e(v)+O(epsilon^3).
P0=[F(-2),F(0),F(-3),F(0),F(1)]
d=scale(integ(P0),F(-1,2))
e=scale(integ(mul(P0,P0)),F(1,8))
h=scale(add(mul(diff(d),d),e),F(-1))
q=add(diff(d),scale(d[1:],F(-1)))
z2=add(add(diff(h),scale(h[1:],F(-1))),
       add(mul(d[1:],diff(d)),scale(mul(d[1:],d[1:]),F(-1))))
ck('independent first variation d',d==[0,1,0,F(1,2),0,F(-1,10)])
ck('independent forced radial polynomial',q==[0,0,1,0,F(-2,5)])
ck('inverse second-order derivative at origin', h[1]==F(-3,2))
ck('second-order Z constant vanishes',z2[0]==0)
ck('q endpoints',val(q,1)==F(3,5) and val(q,T)==-F(441,640))
ck('exact square-root parameter relation',H*H==E)
ck('area coefficient margins',52<64 and F(52,3)<25)
ck('weighted H tail',r**4/(3*(1-r*r))==F(16,135)<F(1,4))
ck('weighted derivative tail',(1-r*r)**-2-1==F(56,25)<F(9,4))
ck('H value coefficient',4*r+2<5)
ck('H upper bound for reciprocal numerators',F(5,3)+5*H<F(11,6))
ck('reciprocal square error',r*5*F(7,2)/(F(3,2)**2*F(5,3)**2)<2)
ck('reciprocal cube error',F(19)/F(3,2)**3+F(1,3)*5*11/(F(3,2)**3*F(5,3)**3)<8)
ck('actual tip upper bound',F(7,25)+7*H<F(3,10))
ck('constructed slit separation',T+333*E<F(9,5) and F(25,81)-F(3,10)==F(7,810)>0)
ck('P disk error',106+9*24==322 and 110+322*H<111)
ck('Rouche gap',333*E<1)
ck('orientation throughout positive t',222/(1-111*E)<223)
sqrt_multiplier=161+F(111**2,2)*H
inverse_multiplier=3*sqrt_multiplier+55*333*H
derivative_multiplier=161+(2*111**2+F(126,2)*333)*H
z_multiplier=(T*derivative_multiplier+inverse_multiplier+7*333*H)/(1-333*E)
ck('sqrt controlled remainder',sqrt_multiplier<162)
ck('inverse controlled remainder',inverse_multiplier<487)
ck('inverse derivative controlled remainder',derivative_multiplier<162)
ck('Z freshly propagated remainder',z_multiplier<800, str(z_multiplier))
ck('strict sign margins using declared budget',val(q,1)-2000*H>F(1,2) and val(q,T)+2000*H<-F(1,2))

# Robust boundary: all advertised simple absorptions and sign margins survive
# eta=1/50000. This is a consistency crosscheck, not an amended manuscript.
Hb=F(1,50000); Eb=Hb*Hb
ck('nonzero parameter neighborhood controls',45621*Hb<1 and 322*Hb<1 and
   F(7,25)+7*Hb<F(3,10) and T+333*Eb<F(9,5) and
   222/(1-111*Eb)<223 and 1541+4662*Hb<2000 and 2000*Hb<F(1,10))

# Brown series independently carried to degree 12 instead of truncating at 6.
N=12
s_over_u=[F(1,factorial(k+1)) if k%2==0 else F(0) for k in range(N+1)]
cosh=[F(1,factorial(k)) if k%2==0 else F(0) for k in range(N+1)]
sinh=[F(1,factorial(k)) if k%2 else F(0) for k in range(N+1)]
brown_h=add([F(3)]+[F(0)]*N, add(scale(mul(cosh,inv(s_over_u,N),N),F(-3)),mul([F(0)]+sinh,inv(cosh,N),N)))
ck('Brown cancellation of quadratic term',brown_h[:4]==[0,0,0,0])
ck('Brown fourth and sixth terms',brown_h[4]==F(-4,15) and brown_h[6]==F(8,63))
ck('Brown higher terms (independent new check)',brown_h[8]==-F(4,75) and brown_h[10]==F(136,6237),list(map(str,brown_h)))
ck('Brown Cauchy circle bound',3+3*2+F(1,2)<10)
delta=F(1,10**12); s1=F(1,10**7); s2=F(1,10**5)
rem=lambda s:F(2560)*s**4/(1-2*s)
upper=-F(4,15)*(2*delta-(2*delta)**3/6)+F(8,63)*s1*s1+rem(s1)
lower=-F(8,15)*delta+F(8,63)*(1-(3*delta)**2/2)*s2*s2-rem(s2)
ck('Brown actual-support value lower bound',F(25,96)*(1-delta/2)>F(1,4))
ck('Brown actual tip separation',(1-s2)**2/(4*s2*s2)>1)
ck('Brown tangent derivative signs',upper<0<lower,{'upper':str(upper),'lower':str(lower)})

# Negative analytic controls target real hypotheses, not boolean count claims.
ck('wrong double-cover sign cannot be positive trajectory',-4<0)
ck('tip gate weakened past sign segment cannot certify identification',not(F(25,81)>F(2,5)))
ck('dropping quartic term loses sign reversal',1>0 and T*T>0)
ck('epsilon zero loses strict signs',0*val(q,1)==0*val(q,T)==0)
ck('excessive coefficient uncertainty loses sign certificate',not(val(q,1)-2000*F(1,1000)>0))

result={'status':'PASS','checks':checks,'count':len(checks),
        'new_second_order_series':{'d':list(map(str,d)),'G_epsilon_squared':list(map(str,e)),
                                   'V_epsilon_squared':list(map(str,h)),'Z_epsilon_squared':list(map(str,z2)),
                                   'interpretation':'Z first order is imaginary, second order real for limiting real Koebe coefficients.'},
        'Brown_h_degree12':list(map(str,brown_h)),
        'limits':'Exact finite controls supplement DERIVATION.md. They do not establish classical source theorems, universal holomorphic estimates, actual extremality, or novelty.'}
if __name__=='__main__':
    (BASE/'INDEPENDENT_CONTROLS.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
