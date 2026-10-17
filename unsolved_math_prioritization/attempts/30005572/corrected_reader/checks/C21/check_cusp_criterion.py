"""Independent finite checks for the proposed PASS5 cusp-reflection criterion.
These are verification cases, not a replacement for global lattice or CM arguments.
"""
from itertools import product
import json

checks = {"local_primitive_markings":0,"all_divisor_cases":0,"valuation_vectors":0}
for p, max_n in [(2,6),(3,4),(5,3),(7,2)]:
    for n in range(1,max_n+1):
        modulus = p**n
        for u,v in product(range(modulus), repeat=2):
            if u % p == 0 and v % p == 0:
                continue
            r=0
            a=u
            while r<n and a % p == 0:
                r+=1
                a//=p
            e=int(p==2)
            actual = (2*u)%modulus==0 or any((u*b-2*v)%modulus==0 for b in range(modulus))
            predicted = r >= n-e or r <= e
            if actual != predicted:
                raise RuntimeError((p,n,u,v,r,actual,predicted))
            checks['local_primitive_markings']+=1

# Each prime can have v_q(2)=0,1,2. A quadratic field limits which tuples
# can occur, but checking additional tuples is harmless for the combinatorics.
for length in range(1,4):
    for data in product(list(product(range(1,7),range(3))), repeat=length):
        ns,es=zip(*data)
        actual=True
        for rs in product(*(range(n+1) for n in ns)):
            covered=all(r>=n-e for r,n,e in zip(rs,ns,es)) or all(r<=e for r,e in zip(rs,es))
            checks['valuation_vectors']+=1
            actual=actual and covered
        active=[(n,e) for n,e in data if n>e]
        predicted=len(active)<=1 and all(n<=2*e+1 for n,e in active)
        if actual!=predicted:
            raise RuntimeError((data,actual,predicted))
        checks['all_divisor_cases']+=1
print(json.dumps({'status':'PASS','checks':checks,'limitations':['Finite local and valuation tests only','No actual K2 values computed','No CM descent, compactification map or novelty certification inferred']},indent=2))
