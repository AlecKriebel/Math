#!/usr/bin/env python3
"""Independent exact tilt, first-moment, and coefficient-bound controls."""
from fractions import Fraction as F
from collections import defaultdict
from itertools import combinations
from math import factorial
import json

def coeff(a):
    c={0:1}
    for i in a:
        d=defaultdict(int,c)
        for s,v in c.items():d[s+i]+=v
        c=dict(d)
    return c

def main():
    assertions=0; tilt_records=[]; growth_records=[]
    # Exact probability law enumerated on all finite Bernoulli prefixes [n].
    # Unlike candidate controls, record equality of direct EM^q to its full
    # tilted expectation, not only the pigeonhole lower estimate.
    for n in range(1,11):
        realizations=[]
        for mask in range(1<<(n-1)):
            a=[1]+[i for i in range(2,n+1) if mask>>(i-2)&1]
            prob=F(1)
            for i in range(2,n+1):prob*=F(1,i) if i in a else F(i-1,i)
            realizations.append((a,prob,len(a),sum(a),max(coeff(a).values())))
        assert sum(row[1] for row in realizations)==1;assertions+=1
        for q in (1,2,3):
            lam=2**q
            z=F(1)
            for i in range(1,n+1):z*=F(i+lam-1,i)
            direct=sum(p*m**q for a,p,nn,s,m in realizations)
            tilted=sum((p*lam**nn/z)*(F(m,2**nn)**q) for a,p,nn,s,m in realizations)*z
            # Identity because (M/2^N)^q = M^q/lambda^N.
            assert direct==tilted;assertions+=1
            inverse=sum(p*lam**nn/F(s+1)**q for a,p,nn,s,m in realizations)
            assert direct>=inverse>=z/F(lam*n+1)**q;assertions+=2
            if q==2:
                assert z==F((n+1)*(n+2)*(n+3),6);assertions+=1
                tilt_records.append({'n':n,'EM2':str(direct),'Jensen_lower':str(z/F(4*n+1)**2),'ratio_lower_over_n':str(z/F(4*n+1)**2/n)})
    # Count all disjoint signed relations by their unordered sides, at fixed max,
    # independently of the author's 3^m oriented signed-word enumeration.
    relations=[]
    for n in range(3,13):
        bysum=defaultdict(list)
        for mask in range(1,1<<n):
            b=frozenset(i+1 for i in range(n) if mask>>i&1)
            bysum[sum(b)].append(b)
        weight=defaultdict(F)
        for vv in bysum.values():
            for u,v in combinations(vv,2):
                if u&v or max(u|v)!=n:continue
                pp=F(1)
                for a in u|v:pp/=a
                weight[len(u|v)]+=pp
        h=sum((F(1,i) for i in range(1,n)),F())
        for ell,w in sorted(weight.items()):
            bound=F(2**(ell-1)*(ell-1),factorial(ell-2)*n*n)*h**(ell-2)
            assert w<=bound;assertions+=1
            relations.append({'maximum':n,'length':ell,'exact_weight':str(w),'largest_two_bound':str(bound)})
    # A falsely multiplicative upper bound fails even for singleton blocks.
    a=(1,);b=(2,3)
    ma=max(coeff(a).values());mb=max(coeff(b).values());mc=max(coeff(a+b).values())
    assert mc>ma*mb;assertions+=1
    # Certified logs and C*: atanh expansion, exact rational error bounds.
    def log_interval(x,count=80):
        z=F(x-1,x+1)
        lo=2*sum((z**(2*j+1)/F(2*j+1) for j in range(count)),F())
        hi=lo+2*z**(2*count+1)/F((2*count+1)*(1-z*z))
        return lo,hi
    l2,u2=log_interval(2);l3,u3=log_interval(3)
    clo=(l3-1)*l2*l2;chi=(u3-1)*u2*u2
    assert F(47,1000)<clo<chi<F(48,1000);assertions+=1
    # Growing-length criterion c=1/4, certified without floating logarithms.
    assert (1+3*u2)/4<1;assertions+=1
    print(json.dumps({'all_passed':True,'assertions':assertions,
      'tilt_identity_and_second_moment_records':tilt_records,
      'independent_disjoint_relation_weights':relations,
      'false_multiplicative_upper_counterexample':{'left':a,'right':b,'left_max':ma,'right_max':mb,'union_max':mc},
      'upper_constant_certified_interval':['47/1000','48/1000'],
      'second_moment_asymptotic_lower_constant':'1/96',
      'limits':'Exact finite identities and independent first-moment counting; asymptotic probability claims require the written proofs.'},indent=2,sort_keys=True))

if __name__=='__main__':main()
