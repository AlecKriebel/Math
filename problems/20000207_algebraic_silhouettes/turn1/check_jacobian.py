import json
from fractions import Fraction
from math import comb
count=0
def ck(x):
 global count
 count+=1
 assert x

def rank(cols):
 a=[[Fraction(c[i]) for c in cols] for i in range(len(cols[0]))]; r=0
 for j in range(len(cols)):
  k=next((k for k in range(r,len(a)) if a[k][j]),None)
  if k is None:continue
  a[r],a[k]=a[k],a[r];v=a[r][j];a[r]=[x/v for x in a[r]]
  for k in range(len(a)):
   if k!=r:
    v=a[k][j];a[k]=[x-v*y for x,y in zip(a[k],a[r])]
  r+=1
 return r

def mono(d,k,c=1):
 v=[0]*(d+1);v[k]=c;return v

def add(*vs):return [sum(z) for z in zip(*vs)]
rows=[]
for d in range(5,81):
 f=add(mono(d,0),mono(d,d))
 cols=[mono(d,2),mono(d,3),mono(d,4),mono(d,5),mono(d,d-1,d),mono(d,1,d),add(mono(d,0,d),mono(d,d,-d))]
 r=rank([f]+cols)-1
 ck(r==min(7,d));rows.append({'delta':d,'projective_rank':r})
 # First-order substitution of f((1+e*a)s+e*b*t,e*c*s+(1-e*a)t).
 for a,b,c in [(1,0,0),(0,1,0),(0,0,1),(2,-3,5)]:
  out=[0]*(d+1)
  # Expanding the two pure powers: exactly one perturbation factor.
  out[0]+=d*a;out[1]+=comb(d,1)*b
  out[d-1]+=comb(d,1)*c;out[d]-=d*a
  expected=add([a*x for x in cols[6]],[b*x for x in cols[5]],[c*x for x in cols[4]])
  ck(out==expected)
 # Independently substitute w=e*(a*s+b*t) into w*s^(d-3)t^2,
 # z=e*(c*s+d0*t) into z*s^(d-5)t^4.
 for a,b,c,d0 in [(1,0,0,0),(0,1,0,0),(0,0,1,0),(0,0,0,1),(2,3,5,7)]:
  out=[0]*(d+1)
  for normal,(s0,t0),base in [(1,(a,b),2),(1,(c,d0),4)]:
   out[base]+=s0;out[base+1]+=t0
  ck(out==[a*cols[0][i]+b*cols[1][i]+c*cols[2][i]+d0*cols[3][i] for i in range(d+1)])
 ck(rank([f])==1)
print(json.dumps({'assertions':count,'ranks':rows,'scope':'Finite exact controls; all-degree proof is the distinct-exponent argument.'},indent=2))
