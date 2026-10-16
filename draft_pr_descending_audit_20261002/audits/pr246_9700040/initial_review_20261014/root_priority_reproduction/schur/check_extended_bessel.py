#!/usr/bin/env python3
"""Independent Decimal evaluation of BO(2004) Theorem 3.3 gap determinant.
Checks the parameter x->interior time (log x)/2 and half-integer cutoff.
No candidate code or nonstandard package is imported.
"""
from decimal import Decimal as Q, getcontext
from functools import lru_cache
from pathlib import Path
import datetime,json
getcontext().prec=65

@lru_cache(None)
def J(x,n):
    if n<0:return (-1 if (-n)%2 else 1)*J(x,-n)
    t=x.sqrt()**n
    for k in range(2,n+1):t/=k
    ans=t
    for k in range(1,180):
        t*= -x / (Q(k)*Q(n+k));ans+=t
        if abs(t)<Q('1e-70'):break
    return ans

def kernel(x,h,y,l,terms=100):
    if x>=y:
        q=(y/x).sqrt();power=q.sqrt();out=Q(0)
        for n in range(terms):
            out+=power*J(x,h+n+1)*J(y,l+n+1);power*=q
        return out
    q=(x/y).sqrt();power=q.sqrt();out=Q(0)
    for n in range(terms):
        out-=power*J(x,h-n)*J(y,l-n);power*=q
    return out

def det(a):
    n=len(a);out=Q(1)
    for i in range(n):
        j=max(range(i,n),key=lambda j:abs(a[j][i]))
        if not a[j][i]:return Q(0)
        if i!=j:a[i],a[j]=a[j],a[i];out=-out
        piv=a[i][i];out*=piv
        for j in range(i+1,n):
            c=a[j][i]/piv
            for k in range(i+1,n):a[j][k]-=c*a[i][k]
    return out

def known(x,y):
    # Candidate's independently derived r=(1,2) control.
    d=y-x;t=Q(1);s=t
    for n in range(1,100):t*=d/(n*n);s+=t
    return (-y).exp()*s

results=[]
for H in (8,12,18):
    E=[(Q('0.5'),h) for h in range(0,H+1)]+[(Q('1.5'),h) for h in range(1,H+1)]
    a=[[Q(int(i==j))-kernel(x,h,y,l) for j,(y,l) in enumerate(E)] for i,(x,h) in enumerate(E)]
    ans=det(a);control=known(Q('.5'),Q('1.5'))
    # Union event above H forces N(1.5)>=H+2, so exact gap cutoff error
    # is at most its Poisson tail. Numerical series errors here unvalidated.
    t=Q(1);tail=Q(0)
    for n in range(1,160):
        t*=Q('1.5')/n
        if n>=H+2:tail+=t
    tail*=Q('-1.5').exp()
    assert abs(ans-control)<tail+Q('1e-55')
    results.append({'H':H,'matrix_order':len(E),'gap_determinant':str(ans),'r12_control':str(control),'difference':str(abs(ans-control)),'exact_probability_cutoff_tail_bound':str(tail)})
obj={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'source':'Borodin-Olshanski math-ph/0402064v2, Thm3.3 eq3.4','parameter_mapping':'theta_j=x_j; t_j=0.5 log(x_j); lattice coordinate=h+0.5; forbidden h>=r_j-1','cases':results,'all_passed':True,'limitations':'Decimal arithmetic and Bessel-series truncation are numerical checks, not validated interval numerics. Analytic identity and finite permutation checks carry the proof.'}
Path(__file__).with_name('EXTENDED_BESSEL_CHECK.json').write_text(json.dumps(obj,indent=2)+'\n')
print(json.dumps(obj,indent=2))
