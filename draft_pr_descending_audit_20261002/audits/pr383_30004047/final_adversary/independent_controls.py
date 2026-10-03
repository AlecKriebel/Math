#!/usr/bin/env python3
"""Fresh source-first falsification controls. No imports from author/review code.
All objective and certificate arithmetic uses Fraction. Enumerations are finite controls.
"""
from fractions import Fraction as F
from itertools import product, combinations
from pathlib import Path
import json, hashlib, datetime
OUT=Path(__file__).resolve().parent

def solve(a,b):
 a=[[F(v) for v in row]+[F(rhs)] for row,rhs in zip(a,b)];n=len(b)
 for j in range(n):
  p=next((i for i in range(j,n) if a[i][j]),None)
  if p is None:return None
  a[j],a[p]=a[p],a[j];r=a[j][j];a[j]=[v/r for v in a[j]]
  for i in range(n):
   if i!=j and a[i][j]:
    r=a[i][j];a[i]=[x-r*y for x,y in zip(a[i],a[j])]
 return [row[-1] for row in a]

def maximin(M):
 """Enumerate exact optimal vertices of simplex max min row coverage."""
 n,m=len(M),len(M[0]);best=F(-1);w=None
 for t in range(1,min(n,m)+1):
  for supp in combinations(range(m),t):
   for tight in combinations(range(n),t):
    a=[[1]*t+[0]]+[[M[i][j] for j in supp]+[-1] for i in tight]
    z=solve(a,[1]+[0]*t)
    if z is None or min(z)<0:continue
    q=[F(0)]*m
    for j,v in zip(supp,z):q[j]=v
    objective=min(sum(q[j]*M[i][j] for j in range(m)) for i in range(n))
    if objective==z[-1] and objective>best:best,w=objective,q
 assert w is not None
 return best,w

def lp_with_cert(M):
 v,p=maximin(M)
 # Complement-transpose independently constructs feasible minimax dual.
 vbar,d=maximin([[1-M[i][j] for i in range(len(M))] for j in range(len(M[0]))])
 upper=max(sum(d[i]*M[i][j] for i in range(len(M))) for j in range(len(M[0])))
 assert sum(p)==sum(d)==1 and min(p)>=0 and min(d)>=0
 assert v==upper==1-vbar
 return v,p,d

def masks(n):return range(1,1<<n)
def fm(v):return str(v)
def check_graphs():
 receipts=[];accepted=0;total=0;exact=[]
 for n in range(1,5):
  for b in range(1,4):
   for c in range(1,4):
    count=hits=0; examples={}
    for AB in product(masks(b),repeat=n):
     x=F(min(v.bit_count() for v in AB),b)
     for BC in product(masks(c),repeat=b):
      y=F(min(v.bit_count() for v in BC),c)
      reach=[0]*c
      for a,v in enumerate(AB):
       dest=0
       for j in range(b):
        if v>>j&1:dest|=BC[j]
       for j in range(c):
        if dest>>j&1:reach[j]|=1<<a
      z=F(max(v.bit_count() for v in reach),n)
      for k in range(1,7):
       if x+k*y>1 and k*x+y>=1:
        assert z>=F(1,k),(n,b,c,AB,BC,x,y,z,k)
        hits+=1
        if k*x+y==1 and x+k*y>1 and k not in examples:examples[k]={'AB':AB,'BC':BC,'x':str(x),'y':str(y),'z':str(z)}
      count+=1
    total+=count;accepted+=hits
    receipts.append({'A':n,'B':b,'C':c,'graphs':count,'domain_instances':hits,'weak_boundary_examples':examples})
 # k1 rational strictness control: complementary blocks fail endpoint.
 AB=(1,2);BC=(1,2);reach=(1,2)
 assert F(1,2)+F(1,2)==1 and max(v.bit_count() for v in reach)==1
 return {'graphs':total,'domain_instances':accepted,'dimensions':receipts,'k1_endpoint_counterexample':{'AB':AB,'BC':BC,'x':'1/2','y':'1/2','maximum_predecessor':'1/2'}}

def weighted():
 # Exhaustively vary graph support topology; all weights stay exact and nonuniform.
 weight_sets=[(1,1,1,1),(1,1,1,2),(1,2,2,3),(1,1,3,5),(1,2,3,4),(2,3,5,7)]
 certs=[];count=0;rank2=0;nonlaminar=0;endpoint=0
 for nums in weight_sets:
  p=[F(v,sum(nums)) for v in nums]
  for k in (2,3,4):
   small=[s for s in masks(4) if sum(p[a] for a in range(4) if s>>a&1)<F(1,k)]
   maxima=[s for s in small if not any(s!=t and s&t==s for t in small)]
   poss=[s for s in masks(4) if s.bit_count()<=2 and any(s&t==s for t in maxima)]
   for m in range(1,min(4,len(poss))+1):
    for supp in combinations(poss,m):
     if not all(any(v>>a&1 for v in supp) for a in range(4)):continue
     admissible=[s for s in maxima if any(v&s==v for v in supp)]
     if not all(any(v&s==v for s in admissible) for v in supp):continue
     A=[[int(v>>a&1) for v in supp] for a in range(4)]
     B=[[int(v&s==v) for s in admissible] for v in supp]
     x,q,dx=lp_with_cert(A);y,r,dy=lp_with_cert(B)
     assert not (x+k*y>1 and k*x+y>=1),(p,k,supp,x,y)
     count+=1;rank2+=any(v.bit_count()==2 for v in supp)
     nonlaminar+=any(s&t and s&t not in (s,t) for s,t in combinations(admissible,2))
     endpoint+=x+k*y==1
     certs.append({'weights':list(map(str,p)),'k':k,'B_supports':supp,'maximal_allowed_unions':admissible,'x':str(x),'y':str(y),'q':list(map(str,q)),'r':list(map(str,r)),'dual_x':list(map(str,dx)),'dual_y':list(map(str,dy))})
 (OUT/'weighted_full_certificates.json').write_text(json.dumps(certs,indent=2)+'\n')
 return {'exact_systems':count,'with_rank_two':rank2,'with_overlapping_incomparable_unions':nonlaminar,'strict_boundary_equalities':endpoint,'certificate_file':'weighted_full_certificates.json'}

def laminar():
 # All disjoint partitions of A<=6, with arbitrary positive normalized weights.
 tested=0;strict=0;boundary=0;receipts=[]
 for n in range(2,7):
  # Restricted growth sequences enumerate every set partition.
  def partitions(prefix):
   if len(prefix)==n:yield prefix;return
   for v in range(max(prefix)+2):yield from partitions(prefix+[v])
  for labels in partitions([0]):
   if len(set(labels))<2:continue
   for nums in ([1]*n,list(range(1,n+1)),[1]*(n-1)+[n+1]):
    p=[F(i,sum(nums)) for i in nums];blocks=[]
    for label in sorted(set(labels)):blocks.append(sum(1<<i for i,v in enumerate(labels) if v==label))
    for k in (2,3,4):
     if any(sum(p[a] for a in range(n) if s>>a&1)>=F(1,k) for s in blocks):continue
     # Disjoint supports restrict each block's B mass >=x, so x<=1/#blocks;
     # C classes each cover one block, yielding y<=1/#blocks.
     t=len(blocks);x=y=F(1,t)
     assert t>=k+1 and x+k*y<=1 and k*x+y<=1
     tested+=1;boundary+=x+k*y==1;strict+=x+k*y<1
     receipts.append({'A':n,'weights':list(map(str,p)),'k':k,'blocks':blocks,'max_x':str(x),'max_y':str(y)})
 (OUT/'laminar_disjoint_controls.json').write_text(json.dumps(receipts,indent=2)+'\n')
 return {'nonvacuous_disjoint_systems':tested,'strict_below_domain':strict,'boundary_equalities':boundary}

def deletion():
 # Exact independent conditioning identities across real graph cuts.
 count=nonempty=positive_y=0;receipts=[]
 for AB in product(masks(3),repeat=3):
  for BC in product(masks(3),repeat=3):
   x=F(min(v.bit_count() for v in AB),3);y=F(min(v.bit_count() for v in BC),3)
   for c0 in range(3):
    J=sum(1<<b for b,v in enumerate(BC) if v>>c0&1)
    I=sum(1<<a for a,v in enumerate(AB) if v&J)
    aa=[a for a in range(3) if not (I>>a&1)];bb=[b for b in range(3) if not (J>>b&1)]
    if not aa or not bb:continue
    q=F(J.bit_count(),3);xp=x/(1-q)
    assert all(F(sum(bool(AB[a]>>b&1) for b in bb),len(bb))>=xp for a in aa)
    for cut in masks(3):
     cc=[c for c in range(3) if not (cut>>c&1)]
     if not cc:continue
     eps=F(cut.bit_count(),3);yp=max(F(0),(y-eps)/(1-eps))
     assert all(F(sum(bool(BC[b]>>c&1) for c in cc),len(cc))>=yp for b in bb)
     count+=1;positive_y+=yp>0
     if len(receipts)<12 and yp>0:receipts.append({'AB':AB,'BC':BC,'c0':c0,'C_cut':cut,'x':str(x),'y':str(y),'B_deleted':str(q),'epsilon':str(eps),'x_new_bound':str(xp),'y_new_bound':str(yp)})
    nonempty+=1
 return {'all_conditioning_checks':count,'nonempty_A_B_cuts':nonempty,'positive_remaining_y_checks':positive_y,'sample_exact_graphs':receipts}

def main():
 start=datetime.datetime.now(datetime.timezone.utc).isoformat()
 results={'start_utc':start,'actual_graphs':check_graphs(),'weighted_rank_two':weighted(),'laminar_partition':laminar(),'conditional_deletion':deletion()}
 results['completed_utc']=datetime.datetime.now(datetime.timezone.utc).isoformat()
 print(json.dumps(results,indent=2))
if __name__=='__main__':main()
