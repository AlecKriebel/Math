"""Exact finite diagnostics of the report's symbolic fixed-genus proof; not all-genus proof."""
import json
from fractions import Fraction
from math import comb

def check(condition, message):
    if not condition:
        raise AssertionError(message)

def multiply(a,b):
    out=[0]*(len(a)+len(b)-1)
    for i,x in enumerate(a):
        for j,y in enumerate(b): out[i+j]+=x*y
    return out

rows=[]
for g in range(2,54):
    m=(3*(g-1)+4)//5
    degree_bound=g-m-2
    check(max(0,degree_bound+1)==(2*g-2)//5, 'residual dimension')
    if g<4:continue
    r=5*m-3*(g-1)
    R=[2,-3,4][:min(3,degree_bound+1)]
    P=multiply([0]+[comb(m,k)*(-1)**(m-k) for k in range(m+1)],R)
    check(P[0]==0 and len(P)-1<=g-1,'boundary degree')
    # The m-th derivative at X=1 divided by m! is R(1), because P=X(X-1)^m R.
    derivative=sum(P[k]*comb(k,m) for k in range(m,len(P)))
    leading=5**(2*g-2)*derivative
    check(leading==5**(2*g-2)*sum(R), 'leading functional')
    for j in range(m):check(sum(P[k]*comb(k,j) for k in range(j,len(P)))==0,'orbifold vanishing')
    check(0<=r<=4 and (r-(2*g-2))%5==0,'character')
    rows.append({'g':g,'m':m,'r':r,'dimension':degree_bound+1,'R':R,'leading_shift':str(leading)})
print(json.dumps({'status':'PASS','scope':'finite diagnostics, fixed-genus incomplete boundary package only','rows':rows},indent=2))
