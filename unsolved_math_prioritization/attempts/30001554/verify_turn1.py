from itertools import product
from word_tools import parameters,theta_borders,negative_periods,orbit_projection,tau_theta
from fractions import Fraction
import json
checks=0
def check(x):
 global checks
 assert x;checks+=1
out=[]
for th,N in [((1,0),13),((1,0,2),9),((1,0,3,2),7),((0,1),10)]:
 count=antecedent=0;best=Fraction(0);witness=None
 for n in range(1,N+1):
  for w in product(range(len(th)),repeat=n):
   t,p=parameters(w,th);count+=1
   check(1<=t<=p<=n)
   # Direct block-language definition, distinct from letterwise negative shift.
   u=w[:p];block=u+tuple(th[a] for a in u)
   check(w==(block*((n+len(block)-1)//len(block)))[:n])
   B=theta_borders(w,th)
   check(sorted(n-k for k in B)+[n]==negative_periods(w,th))
   if B:
    b=w[:min(B)]
    check(not any(b[-k:]==b[:k] for k in range(1,len(b))))
   if t==1:check(p==1)
   if n>=3*t:
    antecedent+=1;check(t==p)
    v=orbit_projection(w,th)
    q=next(q for q in range(1,n+1) if v[q:]==v[:n-q])
    check(q<=t)
   if t<p and Fraction(n,t)>best:best=Fraction(n,t);witness=dict(word=list(w),tau=t,least_alternating_period=p)
 out.append(dict(theta=list(th),maximum_length=N,word_count=count,antecedent_count=antecedent,best_failure_ratio_below_threshold=str(best),witness=witness))
family=[]
for i in range(2,31):
 w=tuple([0,1]*i+[0,1,1]+[0,1]*i+[0,0,1]+[0,1]*i+[0])
 t,p=parameters(w,(1,0));check((len(w),t,p)==(6*i+7,2*i+4,4*i+5));check(len(w)-3*t==-5)
 family.append(dict(i=i,n=len(w),tau=t,least_alternating_period=p))
# Shortest theta-border need not be theta-unbordered.
w=(0,1,1,0);B=theta_borders(w,(1,0));check(B==[2]);check(theta_borders(w[:2],(1,0))==[1])
print(json.dumps(dict(assertions=checks,exhaustive_cases=out,source_family_controls=family,scope='Finite checks support only the listed ranges; all-alphabet lemmas are proved in TURN_1.md.'),indent=2,sort_keys=True))
