"""Independent rational upper-bound witness only; no global certificate replay."""
from fractions import Fraction as F
import json,sys
N=90
class I:
 def __init__(self,a,b=None):
  self.lo=F(a);self.hi=F(a if b is None else b)
  if self.lo>self.hi:raise RuntimeError('inverted interval')
 def __add__(self,o):
  o=asI(o);return I(self.lo+o.lo,self.hi+o.hi)
 __radd__=__add__
 def __neg__(self):return I(-self.hi,-self.lo)
 def __sub__(self,o):return self+-asI(o)
 def __rsub__(self,o):return asI(o)+-self
 def __mul__(self,o):
  o=asI(o);v=[self.lo*o.lo,self.lo*o.hi,self.hi*o.lo,self.hi*o.hi];return I(min(v),max(v))
 __rmul__=__mul__
 def __truediv__(self,o):
  o=asI(o)
  if o.lo<=0<=o.hi:raise RuntimeError('division across zero')
  return self*I(1/o.hi,1/o.lo)
def asI(x):return x if isinstance(x,I)else I(x)
def local_log(y):
 if not 1<=y<=2:raise RuntimeError('log reduction domain')
 t=(y-1)/(y+1);t2=t*t;term=t;s=F(0)
 for j in range(N):s+=term/(2*j+1);term*=t2
 rem=2*term/((2*N+1)*(1-t2))
 return I(2*s,2*s+rem)
LN2=local_log(F(2))
def log_exact(x):
 x=F(x)
 if x<=0:raise RuntimeError('positive log input')
 k=x.numerator.bit_length()-x.denominator.bit_length()
 factor=F(2**k)if k>=0 else F(1,2**(-k));y=x/factor
 while y<1:k-=1;y*=2
 while y>=2:k+=1;y/=2
 return local_log(y)+k*LN2
q=F('0.02571553686652745032257637166391965344');H=2*q/(1+q)**2;s=(1-q)/(1+q)
A=log_exact(H)/log_exact(q)
p=F(17861896208523519533866067426369570685214609183110155278092269729,10**63)
m=F(11085120457314950695388194505227588799135079864873862940404965203,2*10**62)
eps=F(1,10**45);pl,ph=p-eps,p+eps;ml,mh=m-eps,m+eps
if not(0<A.lo<=A.hi<s and 1<pl<ph<1/q<ml<mh):raise RuntimeError('admissibility/branch boxes')
def eq(u):return A*log_exact((u-q)/abs(1-q*u))-log_exact(u)
Fs=[eq(pl),eq(ph),eq(ml),eq(mh)]
if not(Fs[0].hi<0<Fs[1].lo and Fs[2].lo>0>Fs[3].hi):raise RuntimeError('strict rational root signs')
upper=H*(mh+1/mh-pl-1/pl)
T=F('1.83443047576266171109075363512901884952989750747')
coarse=F('1.834430475762662')
if not upper<T<coarse:raise RuntimeError('upper target linkage')
# Exact positive rational witnesses, rounded DOWN; neither a root digit nor a hash is proof.
scale=10**65
sign_witnesses=[int(-Fs[0].hi*scale),int(Fs[1].lo*scale),int(Fs[2].lo*scale),int(-Fs[3].hi*scale)]
if min(sign_witnesses)<=0:raise RuntimeError('root sign witness rounding')
gap_scale=10**40;gap_lower=int((T-upper)*gap_scale)
if gap_lower<=0:raise RuntimeError('target positive gap witness')
# Concrete wrong root assignments must fail the genuine sign predicate.
wrong=[Fs[1].hi<0,Fs[0].lo>0,Fs[3].lo>0,Fs[2].hi<0]
if any(wrong):raise RuntimeError('swapped-sign negative control unexpectedly passes')
# Domain and reciprocal rejection are checked by executing their failing paths.
rejected=0
for action in [lambda:I(2,1),lambda:log_exact(0),lambda:I(1)/I(-1,1)]:
 try:action()
 except RuntimeError:rejected+=1
 else:raise RuntimeError('invalid arithmetic domain accepted')
print(json.dumps({'status':'PASS','optimization':sys.flags.optimize,'atanh_terms':N,'q':str(q),'root_sign_orientations':['negative','positive','positive','negative'],'positive_sign_witnesses_over_10_to_65':sign_witnesses,'T_minus_width_upper_at_least_numerator_over_10_to_40':gap_lower,'exact_target_T':str(T),'outward_width_upper_decimal_55':str(upper.numerator*10**55//upper.denominator+1)+'e-55','admissibility_A_upper_below_s':True,'strict_upper_linkage':True,'swapped_sign_negative_controls_rejected':4,'arithmetic_domain_controls_rejected':rejected,'scope':'A single fixed admissible one-cut candidate proves infimum<T via the separately written positive-platform empirical recovery. Does NOT prove global minimality, matching lower bound, nonattainment or proposed lower digits.'},indent=2))
