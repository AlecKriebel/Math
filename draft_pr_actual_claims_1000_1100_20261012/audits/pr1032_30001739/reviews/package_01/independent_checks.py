#!/usr/bin/env python3
"""New review calculation: no candidate/checker imports and no assertions."""
from fractions import Fraction as F
from itertools import combinations,product
import json

def require(x,m):
    if not x: raise ValueError(m)
S={'A':(0,2),'B':(1,4),'C':(3,3),'D':(2,5),'T':(4,6)}
def precede(x,y):
    a,b=x;c,d=y
    return a<c<=b+1 and b<d
def flo(x,y):
    a,b=x;c,d=y
    return a<=c<=b<=d

def graph(m,n,segments=S,shift=-1,reverse_first=False,reverse_second=False,self_edges=False):
    X=[(i,j) for i in m for j in n if precede(segments[i],segments[j])]
    Y=[(i,j) for i in m for j in n if precede(tuple(t+shift for t in segments[i]),segments[j])]
    edges={x:[] for x in X}
    for x in X:
      for y in Y:
        i,j=x;k,l=y
        p=precede(segments[j],segments[l]) if reverse_first else precede(segments[l],segments[j])
        q=precede(segments[k],segments[i]) if reverse_second else precede(segments[i],segments[k])
        if (i==k and p) or (j==l and q) or (self_edges and x==y): edges[x].append(y)
    def inject(xs,used):
      if not xs:return True
      x=xs[0]
      return any(inject(xs[1:],used|{y}) for y in edges[x] if y not in used)
    good=inject(X,set())
    hall=[]
    for k in range(1,len(X)+1):
      for subset in combinations(X,k):
        nbr=set(y for x in subset for y in edges[x])
        if len(nbr)<k:hall.append({'X':subset,'N':sorted(nbr)})
    require(good==(not hall),'Hall/injection inconsistency')
    return {'X':X,'Y':Y,'edges':[{'X':x,'Y':edges[x]} for x in X],'LC':good,'isolated':[x for x in X if not edges[x]],'Hall':hall}

def ladder(m):
    pairs=sorted(S[x] for x in m)
    return all(a<c and b<d for (a,b),(c,d) in zip(pairs,pairs[1:]))
def lists(i,j):
    a,b=S[i];c,d=S[j];r=min(b-a+1,d-c+1)
    return [b-c-k for k in range(r)],[d-a-k for k in range(r)]
def germ(i,j,q,zeta):
    P,Q=lists(i,j)
    # Each factor is 1-zeta*q^-k*z or 1-zeta*q^-k/z.
    num=F(1);den=F(1);nz=dz=0
    for h in Q:
      for k in (h,h+1):
        t=1-zeta*F(q)**(-k)
        if t==0:nz+=1;num*=1 # derivative w.r.t. z is +1 at z=1
        else:num*=t
    for h in P:
      for k in (h,h+1):
        t=1-zeta*F(q)**(-k)
        if t==0:dz+=1;den*=-1 # derivative w.r.t. z is -1 at z=1
        else:den*=t
    return {'P':P,'Q':Q,'order':nz-dz,'leading':str(num/den)}

orders=[list('TDCBA'),list('TCDBA'),list('TDBCA')]
order_rows=[]
for order in orders:
  for i,j in combinations(order,2):
    bad=flo(S[i],S[j]);require(not bad,'FLO basis order fails')
    order_rows.append({'order':order,'pair':[i,j],'FLO_precedes':bad})
pairs=[('T','D'),('B','A'),('T','C'),('D','B'),('C','A'),('D','C'),('C','B')]
germs=[{'pair':[i,j],'q':q,'zeta':z,**germ(i,j,q,z)} for i,j in combinations('TDCBA',2) for q in (3,9) for z in (1,-1)]
for i,j in pairs[:5]:
  require(germ(i,j,3,1)['order']>0,'needed vanishing fails')
  require(germ(i,j,3,-1)['order']==0,'equal-label unit fails')
for i,j in pairs[5:]:
  for q in (3,9):
    for z in (1,-1):require(germ(i,j,q,z)['order']==0,'nested unit fails')
labels=[]
cycle=[('T','D'),('D','B'),('B','A'),('A','C'),('C','T')]
for bits in product((0,1),repeat=4):
  e=dict(zip('ABCD',bits));e['T']=0
  satisfied=[i+j for i,j in cycle if e[i]!=e[j]]
  failed=[i+j for i,j in cycle if e[i]==e[j]]
  require(failed,'odd cycle coloring escaped')
  labels.append({'epsilon':e,'satisfied':satisfied,'failed':failed})
partitions=[]
allnames=list('ABCDT')
for size in (1,2):
  for m in combinations(allnames,size):
    n=tuple(s for s in allnames if s not in m)
    G=graph(m,n);H=graph(n,m)
    require(ladder(m) or ladder(n),'no ladder side')
    require(not(G['LC'] and H['LC']),'partition escaped')
    partitions.append({'m':m,'n':n,'ladder_m':ladder(m),'ladder_n':ladder(n),'forward':G,'reverse':H})
require(len(partitions)==15,'partition count')
# Independent endpoint-calibration grid. Wrong conventions are accepted only if
# they agree on all grid inputs; nonzero disagreement counts expose bad arrows.
grid=[(a,b) for a in range(3) for b in range(a,4)]
controls={k:[] for k in ('shift+1','shift0','reverse_first','reverse_second','self_edges')}
for u,v,w in product(grid,repeat=3):
  M={'u':u,'v':v,'w':w}
  base=graph(('u',),('v','w'),M)['LC']
  for key,kwargs in [('shift+1',{'shift':1}),('shift0',{'shift':0}),('reverse_first',{'reverse_first':True}),('reverse_second',{'reverse_second':True}),('self_edges',{'self_edges':True})]:
    alt=graph(('u',),('v','w'),M,**kwargs)['LC']
    # Reverse-second needs 2 first-side occurrences, rather than one.
    if key=='reverse_second':
      base2=graph(('v','w'),('u',),M)['LC'];alt=graph(('v','w'),('u',),M,**kwargs)['LC'];different=base2!=alt
    else:different=base!=alt
    if different and len(controls[key])<3:controls[key].append({'segments':M,'correct':base2 if key=='reverse_second' else base,'mutated':alt})
require(all(controls.values()),'uncalibrated negative control')
# Every equal-label constraint is necessary at least somewhere; deleting one edge
# leaves exactly one complementary pair, one coordinate after epsilon_T=0.
edge_controls=[]
for omitted in cycle:
  survivors=[]
  for row in labels:
    e=row['epsilon']
    if all(e[i]!=e[j] for i,j in cycle if (i,j)!=omitted):survivors.append(e)
  require(len(survivors)==1,'edge deletion control')
  edge_controls.append({'omitted':omitted,'survivors':survivors})
print(json.dumps({'schema':'new-package-review-independent-finite-v1','orders':order_rows,'germs':germs,'all16coordinates':labels,'partitions':partitions,'calibration_controls':controls,'edge_deletion_controls':edge_controls,'universal_Hom_computation':False},indent=2,sort_keys=True))
