"""Exact Q(sqrt2) arithmetic and full finite Sturmian languages."""
from fractions import Fraction as F
from functools import cmp_to_key
ZERO=(F(0),F(0));ONE=(F(1),F(0));ALPHA=(F(-1),F(1))
def add(x,y):return(x[0]+y[0],x[1]+y[1])
def sub(x,y):return(x[0]-y[0],x[1]-y[1])
def scale(x,a):return(x[0]*a,x[1]*a)
def sign(x):
 a,b=x
 if not b:return(a>0)-(a<0)
 if not a:return(b>0)-(b<0)
 if a>0 and b>0:return 1
 if a<0 and b<0:return -1
 c=a*a-2*b*b
 return((c>0)-(c<0)) if a>0 else -((c>0)-(c<0))
def floor(x):
 a,b=x;lo=min(a+b,a+2*b).__floor__()-1;hi=max(a+b,a+2*b).__ceil__()+1
 while lo+1<hi:
  m=(lo+hi)//2
  if sign(sub(x,(F(m),F(0))))>=0:lo=m
  else:hi=m
 return lo
def frac(x):return sub(x,(F(floor(x)),F(0)))
def language(n):
 cuts=[ZERO,ONE]+[sub(ONE,frac(scale(ALPHA,k))) for k in range(1,n+1)]
 cuts=sorted(cuts,key=cmp_to_key(lambda x,y:sign(sub(x,y))));words=set()
 for a,b in zip(cuts,cuts[1:]):
  u=scale(add(a,b),F(1,2));w=tuple(floor(add(u,scale(ALPHA,k+1)))-floor(add(u,scale(ALPHA,k))) for k in range(n));words.add(w)
 return words
