from fractions import Fraction as F
from itertools import product
from collections import Counter
import json

C=Counter()
def check(k,b):
    assert b,k
    C[k]+=1
def norm(v):return sum(x*x for x in v)/len(v)
def sub(v,w):return tuple(a-b for a,b in zip(v,w))

for n in (1,2,3):
    vectors=list(product((F(0),F(1,2),F(2)),repeat=n))[:12]
    for baseline in vectors:
        for candidate in vectors:
            distance=norm(sub(candidate,baseline))
            for target in vectors:
                rb=norm(sub(baseline,target));rc=norm(sub(candidate,target))
                check('posterior_squared_triangle',rc<=2*rb+2*distance)
                for tau in (F(0),F(1,4),F(1)):
                    chosen=candidate if distance<=tau else baseline
                    check('guard_output_distance',norm(sub(chosen,baseline))<=tau)
                    check('guard_regret_transfer',norm(sub(chosen,target))<=2*rb+2*tau)

for n in range(2,101):
    check('positive_n_element_grid_window',max(F(k,n**4) for k in range(1,n+1))==F(1,n**3))
    check('uniform_convergence_constant',n*(n+3)<=4*n*n)
    for M in (F(1,2),F(1),F(3)):
        es2=(n*M)**2+n*M
        eps=F(1,n**4)
        bound=4*(n+3)*eps*es2
        check('adaptive_correction_inverse_n_bound',bound<=16*(M*M+M)/n)

posterior=((F(0),F(1,2)),(F(1),F(1,3)),(F(3),F(1,6)))
mu=sum(t*p for t,p in posterior);var=sum((t-mu)**2*p for t,p in posterior)
for a in (F(i,7) for i in range(22)):
    check('conditional_excess_risk_identity',sum((a-t)**2*p for t,p in posterior)-var==(a-mu)**2)

out={'status':'PASS','exact_assertions':sum(C.values()),'counts':dict(sorted(C.items())),
 'scope':'Exact finite stability/guard/regret identities and constants. Full source-family approximation and asymptotic input are established in Turn4; these checks do not certify unrestricted-grid CV.'}
print(json.dumps(out,indent=2,sort_keys=True))
