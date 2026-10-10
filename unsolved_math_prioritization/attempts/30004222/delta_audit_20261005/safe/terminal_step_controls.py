#!/usr/bin/env python3
"""Additional independent test of the literal single-step norm at sigma_s=0.
Compare the ordinary-power norm of Eq.5.11, its factorial conversion to divided
powers, the fixed-step binomial quotient, and the root product. Unlike the
retained checker, do not append an extra zero row; include tau_s>0.
"""
from collections import Counter
from fractions import Fraction
from itertools import product
import json

def partitions(r,b):
    return [p for p in product(range(b+1),repeat=r) if list(p)==sorted(p,reverse=True)]

def factorial(n):
    assert n>=0,n
    return Counter(range(1,n+1))

def compact(x):
    return {m:e for m,e in sorted(x.items()) if m!=1 and e}

def binomial(a,b):
    assert 0<=b<=a
    ans=factorial(a);ans.subtract(factorial(b));ans.subtract(factorial(a-b));return ans

def qvalue(a,q):
    ans=Fraction(1)
    for m,e in a.items():
        ans*=sum(q**(m-1-2*i) for i in range(m))**e
    return ans

def run():
    count=bottom=0;per_rows={}
    for s in range(1,6):
      subtotal=0
      for tau in partitions(s,6):
       for sigma in partitions(s,6):
        if sigma[-1]!=0 or any(sigma[i]>tau[i] for i in range(s)):
            continue
        if any(sigma[i]<tau[i+1] for i in range(s-1)):
            continue
        N=[tau[i]-sigma[i] for i in range(s)]
        # Literal ordinary-power norm squared in published Eq.(5.11).
        ordinary=Counter()
        for k in range(s-1):ordinary.update(factorial(N[k]))
        for i in range(s-1):
          for k in range(i+1,s-1):
            ordinary.update(factorial(sigma[i]-sigma[k]+k-i))
            ordinary.subtract(factorial(tau[i]-sigma[k]+k-i))
          for k in range(i+1,s):
            ordinary.update(factorial(tau[i]-tau[k]+k-i-1))
            ordinary.subtract(factorial(sigma[i]-tau[k]+k-i-1))
        # N' = product [N_i]! / ordinary_normalizer; hence inverse square.
        converted=ordinary.copy()
        for i in range(s-1):
            converted.subtract(factorial(N[i]));converted.subtract(factorial(N[i]))
        quotient=Counter()
        for i in range(s-1):
          for k in range(i+1,s):
            c=tau[i]-tau[k]+k-i
            quotient.update(binomial(c-1,N[i]))
            if k<s-1:quotient.subtract(binomial(c+N[k],N[i]))
        alpha=[sum(v>=j for v in sigma) for j in range(1,tau[0]+1)]
        beta=[sum(v>=j for v in tau) for j in range(1,tau[0]+1)]
        mu=[b-a for a,b in zip(alpha,beta)]
        root=Counter()
        for a in range(len(alpha)):
          for b in range(a+1,len(alpha)):
            if mu[a]==0 and mu[b]==1:
                d=alpha[a]-alpha[b]+b-a
                assert d>=2
                root[d]+=1;root[d-1]-=1
        assert compact(converted)==compact(quotient)==compact(root),(tau,sigma)
        for q in (Fraction(1),Fraction(2)):
            assert qvalue(compact(converted),q)==qvalue(compact(root),q)
        count+=1;subtotal+=1
        bottom+=int(tau[-1]>0)
      per_rows[str(s)]=subtotal
    return {'status':'PASS','direct_terminal_cases':count,'nonzero_last_row_cases':bottom,
            'q_rational_evaluations':2*count,'rows_1_through_5_entry_bound':6,
            'case_counts_by_rows':per_rows,
            'identity_checked':'ordinary_power_norm_squared / product([N_i]!)^2 = (N_prime)^(-2) = B = K',
            'scope':'Bounded exact factor diagnostics; universal identity remains the written proof.'}

if __name__=='__main__':print(json.dumps(run(),indent=2,sort_keys=True))
