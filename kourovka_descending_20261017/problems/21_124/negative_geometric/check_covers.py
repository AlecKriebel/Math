#!/usr/bin/env python3
"""Exact cellular boundary/cocycle checks; standard library only."""
from fractions import Fraction as F
from itertools import product,permutations
from pathlib import Path
import json,datetime

GEN='abct'

def inv(p):
 q=[0]*len(p)
 for i,j in enumerate(p):q[j]=i
 return tuple(q)

def path(word,start,ps):
 n=len(ps['a']); vec=[0]*(4*n); v=start
 for ch in word:
  g=ch.lower();j=GEN.index(g)
  if ch.islower():vec[4*v+j]+=1;v=ps[g][v]
  else:v=inv(ps[g])[v];vec[4*v+j]-=1
 return v,vec

def rels(k):return ['taTA','tbT'+'A'*k+'B','tcTbaBAC']

def basis(rows):
 out={}
 for rr in rows:
  r=list(map(F,rr))
  for j,b in sorted(out.items()):
   if r[j]:
    c=r[j];r=[x-c*y for x,y in zip(r,b)]
  nz=next((j for j,x in enumerate(r) if x),None)
  if nz is not None:
   v=r[nz];out[nz]=[x/v for x in r]
 return out

def reduce(v,bb):
 r=list(map(F,v))
 for j,b in sorted(bb.items()):
  if r[j]:
   c=r[j];r=[x-c*y for x,y in zip(r,b)]
 return r

def cover(k,ps):
 n=len(ps['a']);rows=[]
 for v in range(n):
  for word in rels(k):
   end,r=path(word,v,ps);assert end==v,(word,v,end)
   rows.append(r)
 bb=basis(rows); visibility=[]
 for v in range(n):
  u=ps['a'][v];e=1
  while u!=v:u=ps['a'][u];e+=1
  end,vec=path('a'*e,v,ps);assert end==v
  if any(reduce(vec,bb)):visibility.append({'vertex':v,'a_power':e})
 return {'degree':n,'boundary_rank_Q':len(bb),'a_visible':visibility}

def affine(p,k):
 assert k%p
 pts=list(product(range(p),repeat=3));ix={v:i for i,v in enumerate(pts)};ki=pow(k,-1,p)
 fun={'a':lambda x,y,z:(x+ki*z,y,z),'b':lambda x,y,z:(x,y+z,z+1),'c':lambda x,y,z:(x,y+ki,z),'t':lambda x,y,z:(x+y,y,z)}
 # Cellular paths read words left to right: use the right action inverse
 # to the matrix left action used in the construction.
 return {g:inv(tuple(ix[tuple(t%p for t in fun[g](*v))] for v in pts)) for g in GEN}

def witness(k,d,cs,A,T):
 ps={'a':tuple(range(d)),'t':tuple(range(d)),'b':tuple((i+1)%d for i in range(d)),'c':tuple((i+cs)%d for i in range(d))}
 wt=[x for i in range(d) for x in (A[i],0,0,T[i])]
 vals=[]
 for i in range(d):
  for word in rels(k):
   end,r=path(word,i,ps);assert end==i
   val=sum(x*y for x,y in zip(r,wt));assert val==0,(k,i,word,val);vals.append(val)
 assert A[0]==1
 return {'k':k,'degree':d,'a_weights':A,'t_weights':T,'relator_evaluations':vals,'a_loop_evaluation_at_vertex_0':1,'exact_cover_homology':cover(k,ps)}

def main():
 out={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'method':'exact rational cellular boundary row spaces; no modular rank inference','sharp_witnesses':[witness(1,4,2,[1,0,-1,0],[0,0,1,1]),witness(2,2,1,[1,-1],[0,2])],'affine_nonabelian_covers':[]}
 for k,p in [(3,2),(3,5),(4,3),(5,2),(5,3),(6,5)]:
  if p**3>30:continue
  ps=affine(p,k);r=cover(k,ps);r.update(k=k,p=p,permutations={g:list(v) for g,v in ps.items()});out['affine_nonabelian_covers'].append(r)
 print(json.dumps(out,indent=2));Path(__file__).with_name('cover_results.json').write_text(json.dumps(out,indent=2)+'\n')
if __name__=='__main__':main()
