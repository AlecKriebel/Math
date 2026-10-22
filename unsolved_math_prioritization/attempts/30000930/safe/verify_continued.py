#!/usr/bin/env python3
"""Exact supporting checks, standard library only. Not a general Ext solver."""
from fractions import Fraction as Q
from itertools import product, combinations
from collections import Counter
from pathlib import Path
from math import comb
import argparse,json
# Laurent polynomials in alpha,beta,w,x,y, with exact rational coefficients.
N=5
class P:
 def __init__(self,d=None):self.d={k:Q(v) for k,v in (d or {}).items() if v}
 def __add__(a,b):
  if not isinstance(b,P):b=C(b)
  d=dict(a.d)
  for k,v in b.d.items():d[k]=d.get(k,Q(0))+v
  return P(d)
 __radd__=__add__
 def __neg__(a):return P({k:-v for k,v in a.d.items()})
 def __sub__(a,b):return a+-b if isinstance(b,P) else a+C(-b)
 def __mul__(a,b):
  if not isinstance(b,P):b=C(b)
  d={}
  for ka,va in a.d.items():
   for kb,vb in b.d.items():
    k=tuple(x+y for x,y in zip(ka,kb));d[k]=d.get(k,Q(0))+va*vb
  return P(d)
 __rmul__=__mul__
 def __eq__(a,b):return a.d==(b.d if isinstance(b,P) else C(b).d)
 def __bool__(a):return bool(a.d)
def C(x):return P({(0,)*N:x})
def var(i,p=1):k=[0]*N;k[i]=p;return P({tuple(k):1})
zero=C(0);one=C(1)
def clean(v):return {k:c for k,c in v.items() if c}
def add(a,b):
 c=dict(a)
 for k,v in b.items():c[k]=c.get(k,zero)+v
 return clean(c)
def scale(a,c):return clean({k:v*c for k,v in a.items()})
def table(alpha,beta):
 T=[[{} for _ in range(12)] for _ in range(12)]
 blocks=['AA']*4+['BB']*4+['AB']*2+['BA']*2
 r=beta*var(0,-1) if alpha==var(0) else one
 def setp(i,j,d):T[i][j]={k:(v if isinstance(v,P) else C(v)) for k,v in d.items()}
 for i,b in enumerate(blocks):
  setp(0 if b[0]=='A' else 4,i,{i:1});setp(i,0 if b[1]=='A' else 4,{i:1})
 for a,b,t in [(1,2,3),(5,6,7)]:setp(a,b,{t:1});setp(b,a,{t:1})
 for a in [1,2]:setp(a,8,{9:1});setp(10,a,{11:r})
 for b in [5,6]:setp(8,b,{9:1});setp(b,10,{11:r})
 setp(8,10,{1:beta,2:beta});setp(10,8,{5:beta,6:beta})
 setp(8,11,{3:alpha});setp(9,10,{3:beta});setp(10,9,{7:beta});setp(11,8,{7:alpha})
 return T
def mul(T,a,b):
 c={}
 for i,x in a.items():
  for j,y in b.items():c=add(c,scale(T[i][j],x*y))
 return c
def classify_check():
 alpha,beta=var(0),var(1);T=table(alpha,beta);S=table(one,one)
 U=[{i:one} for i in range(12)];degrees=[0,2,2,4,0,2,2,4,1,3,1,3]
 for i,j,k in product(range(12),repeat=3):assert mul(T,mul(T,U[i],U[j]),U[k])==mul(T,U[i],mul(T,U[j],U[k]))
 scales=[one]*10+[beta,alpha]
 for i,j in product(range(12),repeat=2):
  assert {k:v*scales[k] for k,v in T[i][j].items()}==scale(S[i][j],scales[i]*scales[j])
  assert all(degrees[k]==degrees[i]+degrees[j] for k in T[i][j])
 unit={0:one,4:one}
 assert all(mul(T,unit,u)==u==mul(T,u,unit) for u in U)
 return {'coefficient_ring':'Q[alpha^+/-1,beta^+/-1]','symbolic_associativity_triples':1728,'symbolic_basis_change_product_checks':144,'unit_and_grading':True,'scope':'Checks the normal form and explicit rescaling. Necessity and geometric hypotheses are proved in K2_YONEDA.md.'}
def dot(a,b):return sum((x*y for x,y in zip(a,b)),zero)
def local_check():
 w,x,y=var(2),var(3),var(4)
 dA1=[w,y];dA2=[-y,w];dB1=[w,x];dB2=[-x,w]
 f1=[zero,one];f2=[-one,zero];g1=[zero,one];g2=[-one,zero]
 assert dot(dA1,dA2)==zero and dot(dB1,dB2)==zero
 assert dot(dB1,f2)+dot(f1,dA2)==zero
 assert dot(dA1,g2)+dot(g1,dB2)==zero
 assert dot(g1,f2)==zero and dot(f1,g2)==zero
 return {'koszul_complexes_squared_to_zero':True,'degree_one_maps_closed':True,'both_degree_two_compositions_zero':True,'scope':'Affine model only; not a global Yoneda vanishing claim.'}
def matchings(points):
 if not points:return [()]
 a=points[0];out=[]
 for j in range(1,len(points),2):
  for l in matchings(points[1:j]):
   for r in matchings(points[j+1:]):out.append(((a,points[j]),)+l+r)
 return out
def partition(n,*ms):
 par=list(range(n))
 def f(i):
  while par[i]!=i:par[i]=par[par[i]];i=par[i]
  return i
 for m in ms:
  for a,b in m:par[f(a)]=f(b)
 roots={}
 for i in range(n):roots.setdefault(f(i),[]).append(i)
 return sorted(roots.values())
def rank(mat,ncols):
 a=[[Q(x) for x in row] for row in mat];r=0
 for c in range(ncols):
  piv=next((i for i in range(r,len(a)) if a[i][c]),None)
  if piv is None:continue
  a[r],a[piv]=a[piv],a[r];v=a[r][c];a[r]=[x/v for x in a[r]]
  for i in range(len(a)):
   if i!=r and a[i][c]:
    v=a[i][c];a[i]=[x-v*y for x,y in zip(a[i],a[r])]
  r+=1
 return r
def constraints(k,A,B,D):
 ac=partition(2*k,A,D);r=len(ac);s=len(partition(2*k,A,B,D))
 cab=len(partition(2*k,A,B));cbd=len(partition(2*k,B,D));qnum=k-cab-cbd+r
 assert qnum%2==0;m=qnum//2
 masks=[z for z in range(1<<r) if z.bit_count()==m];outm=[z for z in range(1<<r) if z.bit_count()==m+1]
 loc={i:j for j,b in enumerate(ac) for i in b};matrix=[]
 for i,j in B:
  u,v=loc[i],loc[j]
  if u==v:continue
  for z in outm:
   matrix.append([int(not(t>>u&1) and (t|1<<u)==z)-int(not(t>>v&1) and (t|1<<v)==z) for t in masks])
 dim=len(masks)-rank(matrix,len(masks));g=m-r+s
 predicted=comb(s,g) if 0<=g<=s else 0
 assert dim==predicted
 return {'pair_circle_counts':[cab,cbd,r],'triple_components':s,'target_polynomial_degree':m,'annihilator_dimension':dim,'degree_after_minimal_annihilator':g}
def balance_check():
 rows=[]
 for k in range(1,5):
  ms=matchings(tuple(range(2*k)));hist=Counter();count=0
  for A,B,D in product(ms,repeat=3):
   c=constraints(k,A,B,D);hist[c['annihilator_dimension']]+=1;count+=1
  rows.append({'k':k,'matchings':len(ms),'triples':count,'dimension_histogram':dict(sorted(hist.items()))})
 A=((0,1),(2,5),(3,4),(6,7));B=((0,3),(1,2),(4,5),(6,7));D=((0,5),(1,4),(2,3),(6,7))
 ex=constraints(4,A,B,D);assert ex['annihilator_dimension']==2 and ex['pair_circle_counts']==[2,2,2]
 return {'enumeration':rows,'explicit_k4_example':{'A':[[a+1,b+1] for a,b in A],'B':[[a+1,b+1] for a,b in B],'C':[[a+1,b+1] for a,b in D],**ex,'possible_outputs':'span(u,v) inside C[u,v]/(u^2,v^2)'},'scope':'Linear balance-and-degree constraints in the cohomological model, not full associativity or a counterexample to the Yoneda conjecture.'}
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path);a=ap.parse_args()
 result={'status':'PASS','k2_classification_normal_form':classify_check(),'local_koszul':local_check(),'higher_rank_linear_constraints':balance_check()}
 t=json.dumps(result,indent=2,sort_keys=True)+'\n'
 if a.output:a.output.write_text(t)
 print(t)
if __name__=='__main__':main()
