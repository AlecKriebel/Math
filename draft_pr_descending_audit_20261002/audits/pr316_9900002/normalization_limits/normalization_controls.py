#!/usr/bin/env python3
"""Exact controls of normalization hypotheses; not a universal-scale proof."""
from fractions import Fraction as F
import json

checks=0
controls=[]
def ck(v):
    global checks
    assert v
    checks+=1

def moments(law,g):
    ck(sum(law.values(),F(0))==1)
    ck(all(p>=0 for p in law.values()))
    mean=sum((p*g(x) for x,p in law.items()),F(0))
    second=sum((p*g(x)**2 for x,p in law.items()),F(0))
    return mean,second-mean**2

def atom_control(c,e,outliers):
    # Deliberately allow zero, huge or signed outliers and unbounded moments.
    ck(0<=e<=1)
    ck(sum(outliers.values(),F(0))==1)
    law={c:1-e}
    for x,p in outliers.items(): law[x]=law.get(x,F(0))+e*p
    g=lambda x:F(x,1)/(1+abs(x))
    mean,var=moments(law,g)
    ck(law.get(c,F(0))>=1-e)
    ck(abs(mean-g(c))<=2*e)
    ck(var<=4*e)
    if min(law)>=0:
        f=lambda x:F(x,1)/(1+x)
        fm,fv=moments(law,f)
        ck(fv<=e)
    return law,mean,var

# These controls challenge unjustified moment requirements and every ratio branch.
for n in range(2,41):
    e=F(1,n)
    atom_control(F(0),e,{F(n**4):F(1)})
    atom_control(F(3),e,{F(0):F(1,2),F(n**4):F(1,2)})
    law,_,_=atom_control(F(n),e,{F(0):F(1)})
    ck(law[F(n)]==1-e)
    atom_control(F((-1)**n),e,{F(-n**3):F(1,2),F(n**4):F(1,2)})
    # Concentration at zero before normalization can hide a two-point limit.
    v={F(1,n):F(1,2),F(2,n):F(1,2)}
    normalized={x/F(1,n):p for x,p in v.items()}
    ck(normalized=={F(1):F(1,2),F(2):F(1,2)})
    _,var=moments(normalized,lambda x:x/(1+x))
    ck(var==F(1,144))
    ck(max(v)<=F(2,n))
controls.append('zero, finite, infinity, signed/oscillating centers; huge rare exceptions')
controls.append('weak concentration at zero is insufficient after rescaling')

# A mixed atom-at-zero target has positive bounded-transform variance.
_,mixed_var=moments({F(0):F(1,2),F(1):F(1,2)},lambda x:x/(1+x))
ck(mixed_var==F(1,16))
ck(mixed_var>0)
controls.append('mixed nondegenerate zero/positive target fails concentration hypothesis')

# Nondecreasing phi does not force convergence of comparison-scale ratios.
last=None
ratios=[]
for n in range(1,7):
    a=F(2**(4**n))
    c=F(1 if n%2 else 2)
    phi=a/c
    if last is not None: ck(phi>last)
    last=phi
    ck(a/phi==c)
    ratios.append(int(c))
ck(ratios==[1,2,1,2,1,2])
controls.append('monotone phi with alternating positive ratios')

# A sparse unbounded deterministic atom sequence cannot be discarded.
centers=[F(n if n&(n-1)==0 else 0) for n in range(1,65)]
ck([centers[n-1] for n in (1,2,4,8,16,32,64)]==list(map(F,(1,2,4,8,16,32,64))))
ck(all(centers[n-1]==0 for n in (3,5,6,7,9,10)))
controls.append('sparse unbounded centers versus full-sequence tightness')

# The source-first probability-concentration lemma is strictly stronger.
for n in range(2,41):
    law={F(3)*(1-F(1,n)):F(1,2),F(3)*(1+F(1,n)):F(1,2)}
    ck(max(law.values())==F(1,2))
    ck(max(abs(x-3) for x in law)==F(3,n))
controls.append('positive probability concentration without any asymptotic exact atom')

print(json.dumps({'status':'PASS','assertions':checks,'controls':controls,
 'scope':'Exact finite adversarial controls of hypotheses only; universal normalization proof is in FINAL_NORMALIZATION_REPORT.md.'},sort_keys=True,indent=2))
