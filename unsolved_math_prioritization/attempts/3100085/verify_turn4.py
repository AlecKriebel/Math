from fractions import Fraction as F
from collections import Counter
import json

C=Counter()
def check(k,b):
    assert b,k
    C[k]+=1
for r in range(3,31):
    mu=F(r+1,2)
    check('uniform_integer_variance',sum((F(j)-mu)**2 for j in range(1,r+1))/r==F(r*r-1,12))
    for u in range(1,r):
        for v in range(1,r-u):
            s=r-u-v
            for x in (F(0),F(1,2),F(3),F(100)):
                outer=sum(1/(x+j) for j in range(1,r+1))/r
                if v>=u:
                    inner=sum(1/(x+j) for j in range(v+1,v+s+1))/s
                    check('convex_reciprocal_average_orientation',outer>inner)
            if u>=v:continue
            delta=v-u;nu=F(2*u+s+1,2)
            check('mean_displacement_identity',mu-nu==F(delta,2))
            M=max(r-1,(r*r-1)//(6*delta)+1)
            for t in (M,M+1,2*M,10*M):
                A=t-1
                check('finite_left_bound_strict_numerator',6*delta*t>r*r-1)
                check('mean_denominator_comparison',A+mu<=2*t)
                check('Taylor_lower_bound_positive',F(delta,2)/(A+mu)-F(r*r-1,24*t*t)>0)
out={'status':'PASS','exact_assertions':sum(C.values()),'counts':dict(sorted(C.items())),
     'scope':'Exact finite derivative-average, variance, and cutoff-constant checks. The written convexity and Taylor argument proves the all-span reduction; no extended binomial collision scan occurs here.'}
print(json.dumps(out,indent=2,sort_keys=True))
