"""Independent analytic scalar and Hall-table reconstruction; no supplied imports."""
from itertools import combinations,product
from fractions import Fraction
from pathlib import Path
import json,re
import sympy as s
z=s.symbols('z')
segments={'A':(0,2),'B':(1,4),'C':(3,3),'D':(2,5),'T':(4,6)}
def prec(x,y):
 X=set(range(x[0],x[1]+1));Y=set(range(y[0],y[1]+1));U=X|Y
 return min(X)<min(Y) and not X<=Y and not Y<=X and len(U)==max(U)-min(U)+1
def graph(m,n):
 X=[(u,v)for u in m for v in n if prec(segments[u],segments[v])]
 Y=[(u,v)for u in m for v in n if prec(tuple(a-1 for a in segments[u]),segments[v])]
 N={x:[y for y in Y if(x[0]==y[0] and prec(segments[y[1]],segments[x[1]]))or(x[1]==y[1] and prec(segments[x[0]],segments[y[0]]))]for x in X}
 return X,Y,N
def is_ladder(m):
 return all((segments[u][0]-segments[v][0])*(segments[u][1]-segments[v][1])>0 for u,v in combinations(m,2))
orders=['TDCBA','TCDBA','TDBCA']
orderchecks=[]
for o in orders:
 for u,v in combinations(o,2):
  a,b=segments[u];c,d=segments[v]
  assert not(a<=c<=b<=d)
  assert not prec((a,b),(c,d))
  orderchecks.append([o,u,v])
germs=[]
for u,v in combinations('TDCBA',2):
 a,b=segments[u];c,d=segments[v];r=min(b-a+1,d-c+1)
 # Derive unitary Steinberg tensor exponents by centers + (m+n)/2-i.
 C=Fraction(a+b-c-d,2);m=b-a+1;n=d-c+1
 P=[C+Fraction(m+n,2)-i for i in range(1,r+1)]
 Q=[-C+Fraction(m+n,2)-i for i in range(1,r+1)]
 assert P==[b-c-j for j in range(r)] and Q==[d-a-j for j in range(r)]
 for q,chi in product([3,9],[1,-1]):
  def factor(h,inv):return 1-chi*s.Rational(q)**(-h)*(1/z if inv else z)
  expr=s.cancel(s.prod(factor(h,True)*factor(h+1,True)for h in Q)/s.prod(factor(h,False)*factor(h+1,False)for h in P))
  numerator,denominator=s.fraction(expr)
  def multiplicity(poly):
   k=0
   while s.simplify(poly.subs(z,1))==0:
    poly=s.cancel(poly/(z-1));k+=1
   return k
  order=multiplicity(numerator)-multiplicity(denominator)
  leading=s.limit(expr/(z-1)**order,z,1)
  germs.append({'pair':[u,v],'q':q,'chi':chi,'P':list(map(int,P)),'Q':list(map(int,Q)),'rational_function':str(s.factor(expr)),'order':order,'leading':str(leading)})
partitions=[]
for k in[1,2]:
 for m in combinations(segments,k):
  n=tuple(x for x in segments if x not in m)
  assert is_ladder(m)or is_ladder(n)
  directions=[]
  for p,q in[(m,n),(n,m)]:
   X,Y,N=graph(p,q)
   isolated=[list(x)for x in X if not N[x]]
   directions.append({'m':p,'n':q,'X':X,'Y':Y,'neighbors':[{ 'X':x,'Y':N[x]} for x in X],'isolated':isolated})
  assert any(d['isolated']for d in directions)
  partitions.append({'partition':[m,n],'ladder_sides':[x for x in[m,n]if is_ladder(x)],'directions':directions})
assert len(partitions)==15
# Validate displayed table independently, directly from actual current TeX.
text=(Path(__file__).parents[2]/'sources/support/paper.tex').read_text()
rows=[]
for line in text.splitlines():
 if not re.match(r'^\$[ABCDT]+/[ABCDT]+\$ &',line):continue
 fields=line.split(' & ');m,n=re.findall('[ABCDT]+',fields[1]);x=tuple(re.findall(r'\(([ABCDT]),([ABCDT])\)',fields[2])[0]);claimedY=re.findall(r'\(([ABCDT]),([ABCDT])\)',fields[3]);X,Y,N=graph(m,n)
 assert x in X and not N[x] and sorted(claimedY)==sorted(Y)
 rows.append({'partition':fields[0],'direction':[m,n],'X_isolated':x,'entireY':Y})
assert len(rows)==15
constraints=[('T','D'),('B','A'),('T','C'),('D','B'),('C','A')]
survivors=[]
for k in range(6):
 choices=[]
 for bits in product([0,1],repeat=4):
  eps=dict(zip('TDCBA',(0,)+bits))
  if all(eps[u]!=eps[v]for u,v in constraints[:k]):choices.append(eps)
 survivors.append(len(choices))
assert survivors==[16,8,4,2,1,0]
print(json.dumps({'status':'PASS_INDEPENDENT_FINITE_RECONSTRUCTION','Hom_space_computed':False,'40_symbolic_germs':germs,'30_order_checks':orderchecks,'15_partitions':partitions,'15_actual_manuscript_rows':rows,'coordinate_survivors':survivors},indent=2))
