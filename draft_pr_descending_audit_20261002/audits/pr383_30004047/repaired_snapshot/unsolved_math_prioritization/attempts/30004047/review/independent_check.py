import itertools,json,math
from fractions import Fraction as Q
n=0
def ck(b):
 global n
 assert b;n+=1
# Triple families on six vertices, all compatible subfamilies by backtracking.
trip=[frozenset(c) for c in itertools.combinations(range(6),3)]
def rec(f,start):
 if f:
  union=set().union(*f); inter=set(f[0]).intersection(*f)
  ck(len(inter)>=2 or len(union)<=4)
 for j in range(start,len(trip)):
  if all(len(trip[j]|s)<=4 for s in f):rec(f+[trip[j]],j+1)
rec([],0)
# The complete-uniform endpoints: test maximal allowed x,y exactly.
for N in range(1,45):
 for r in range(1,N+1):
  for h in range(r,N+1):
   x=Q(math.comb(h,r),math.comb(N,r));y=Q(r,N)
   for k in range(1,12):
    if k*h<N:ck(not(x+k*y>1 and k*x+y>=1))
# Independently reconstruct actual reached sets after removing two middle labels.
A=[frozenset(c) for c in itertools.combinations(range(11),9)]
B=[frozenset(c) for c in itertools.combinations(range(11),4)]
p=frozenset(range(4));q=frozenset(range(4,8));rest=[b for b in B if b not in (p,q)]
sp={i for i,a in enumerate(A) if p<=a};sq={i for i,a in enumerate(A) if q<=a}
ck((len(sp),len(sq),len(sp&sq),len(sp|sq))==(21,21,3,39))
for c in range(11):
 reach={i for i,a in enumerate(A) if any(c in b and b<=a for b in rest)}
 ck(len(reach)==45);ck(len(reach|sp|sq)==(51 if c in p|q else 55))
# Check strict/weak deletion thresholds without floating point.
for k in range(2,9):
 for xi,yi,ei in itertools.product(range(1,11),range(1,11),range(10)):
  x,y,e=Q(xi,10),Q(yi,10),Q(ei,10)
  if e>=x:continue
  xp=(x-e)/(1-e)
  ck((xp+k*y>1)==(e<(x+k*y-1)/(k*y)))
  ck((k*xp+y>=1)==(e<=(k*x+y-1)/(k+y-1)))
print(json.dumps({'assertions':n,'result':'PASS','scope':'Independent bounded controls, no author code imports'},indent=2))
