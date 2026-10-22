"""Independent formal polynomial expansion and unipotent/torus controls.
No candidate imports, network, or writes. Exact modular arithmetic.
"""
from math import comb
from itertools import product
from collections import deque
import json

def need(x,m):
 if not x:raise ValueError(m)
def rank(rows,p):
 piv={}
 for row in rows:
  v=[x%p for x in row]
  for j,b in sorted(piv.items()):
   if v[j]:
    c=v[j];v=[(x-c*y)%p for x,y in zip(v,b)]
  lead=next((j for j,x in enumerate(v) if x),None)
  if lead is not None:
   z=pow(v[lead],-1,p);piv[lead]=[(z*x)%p for x in v]
 return len(piv)
def flatten(A):return sum(A,[])
def polys(m,k,p):
 # Expand each input monomial by repeated multiplication of linear forms.
 # Keys are (exponents of a,b,c,d, output y exponent); no binomial formula used.
 mats={};d=m+1
 for col in range(d):
  f={(0,0,0,0,0):1}
  factors=[[(0,0,1),(2,1,1)]]*(m-col)+[[(1,0,1),(3,1,1)]]*col
  for factor in factors:
   g={}
   for ex,v in f.items():
    for variable,dy,c in factor:
     yy=list(ex);yy[variable]+=1;yy[4]+=dy;yy=tuple(yy);g[yy]=(g.get(yy,0)+v*c)%p
   f={ex:v for ex,v in g.items() if v}
  for repeat in range(k):
   g={}
   for ex,v in f.items():
    for add,c in [((1,0,0,1,0),1),((0,1,1,0,0),-1)]:
     yy=tuple(x+y for x,y in zip(ex,add));g[yy]=(g.get(yy,0)+c*v)%p
   f={ex:v for ex,v in g.items() if v}
  for ex,v in f.items():
   A=mats.setdefault(ex[:4],[[0]*d for _ in range(d)]);A[ex[4]][col]=v
 return mats
def section_ranks(mats,W,Q,p):
 s=len(W);equations=[];aug=[]
 for A in mats.values():
  need(all(A[i][j]==0 for i in Q for j in W),'W formal-coefficient invariance')
  for wi,i in enumerate(W):
   for j in range(len(Q)):
    row=[0]*(s*len(Q))
    for u,h in enumerate(W):row[u*len(Q)+j]+=A[i][h]
    for v,h in enumerate(Q):row[wi*len(Q)+v]-=A[h][Q[j]]
    equations.append(row);aug.append(row+[-A[i][Q[j]]])
 return rank(equations,p),rank(aug,p)
def centralizer(mats,p):
 d=len(next(iter(mats.values())));rows=[]
 for A in mats.values():
  for i in range(d):
   for j in range(d):
    row=[0]*(d*d)
    for h in range(d):
     row[h*d+j]+=A[i][h];row[i*d+h]-=A[h][j]
    rows.append(row)
 return d*d-rank(rows,p)
def submat(mats,I,J):return {ex:[[A[i][j] for j in J] for i in I] for ex,A in mats.items()}
def evalmat(mats,g,p):
 d=len(next(iter(mats.values())));R=[[0]*d for _ in range(d)]
 for ex,A in mats.items():
  c=1
  for x,e in zip(g,ex):c=c*pow(x,e,p)%p
  for i in range(d):
   for j in range(d):R[i][j]=(R[i][j]+c*A[i][j])%p
 return R
def graph(m,p):
 E={i:set() for i in range(m+1)}
 for i in E:
  for j in range(i+1):
   if comb(i,j)%p:E[i].add(j)
  for j in range(i,m+1):
   if comb(m-i,j-i)%p:E[i].add(j)
 def reach(i):
  R={i};q=[i]
  for v in q:
   for u in E[v]:
    if u not in R:R.add(u);q.append(u)
  return R
 reaches={i:reach(i) for i in E};remaining=set(E);classes=[]
 while remaining:
  i=min(remaining);C={j for j in remaining if j in reaches[i] and i in reaches[j]};classes.append(sorted(C));remaining-=C
 return E,classes
def mm(A,B,p):
 d=len(A);return [[sum(A[i][h]*B[h][j] for h in range(d))%p for j in range(d)] for i in range(d)]
def augmentation_algebra(r,p):
 d=r-1;gen=[]
 for h in range(r-1):
  perm=list(range(r));perm[h],perm[h+1]=perm[h+1],perm[h]
  A=[[0]*d for _ in range(d)]
  for j in range(d):
   for i in range(d):A[i][j]=((i==perm[j])-(i==perm[-1]))%p
  gen.append(A)
 piv={};basis=[];todo=deque()
 def add(A):
  v=flatten(A)
  for j,b in sorted(piv.items()):
   c=v[j]
   if c:v=[(x-c*y)%p for x,y in zip(v,b)]
  lead=next((j for j,x in enumerate(v) if x),None)
  if lead is None:return
  z=pow(v[lead],-1,p);v=[x*z%p for x in v];piv[lead]=v;B=[v[i*d:(i+1)*d] for i in range(d)];basis.append(B);todo.append(B)
 add([[int(i==j) for j in range(d)] for i in range(d)])
 while todo and len(basis)<d*d:
  A=todo.popleft()
  for B in gen:add(mm(A,B,p))
 return len(basis)
def main():
 graph_results=[]
 primes=[3,5,7,11,13,17,19,23,29,31,37,41,43,47]
 for p in primes:
  m=2*p-3;E,C=graph(m,p);W=list(range(p-2))+list(range(p,m+1));Q=[p-2,p-1]
  need(sorted(C,key=lambda x:x[0])==sorted([W,Q],key=lambda x:x[0]),'two exact unipotent SCCs')
  need(all(E[i]<=set(W) for i in W),'closed socle SCC')
  need(0 in E[p-2] and comb(p-2,0)%p==1,'non-splitting coefficient')
  _,D=graph(2*p-1,p);need(len(D)==1,'row costandard strong connectivity')
  graph_results.append({'p':p,'symmetric_degree':m,'socle_indices':W,'quotient_indices':Q,'socle_dimension':len(W),'quotient_dimension':2,'SCCs':C,'row_symmetric_degree':2*p-1,'row_SCC_count':len(D),'socle_label':[2*p-2,1],'head_label':[p,p-1],'distinct_labels':True})
 formal=[]
 for p in (3,5):
  r=2*p-1;M=polys(r,0,p);B=polys(r-2,1,p);W=list(range(p-2))+list(range(p,r-1));Q=[p-2,p-1]
  full=rank([flatten(A) for A in M.values()],p);need(full==(r+1)**2,'row full formal coefficient span')
  sw=rank([flatten(A) for A in submat(B,W,W).values()],p);sq=rank([flatten(A) for A in submat(B,Q,Q).values()],p)
  need(sw==len(W)**2 and sq==4,'absolute simplicity of socle and quotient')
  a,b=section_ranks(B,W,Q,p);need(b>a,'formal lift equations inconsistent')
  end=centralizer(B,p);need(end==1,'scalar endomorphism algebra')
  ar=augmentation_algebra(r,p);need(ar==(r-1)**2,'augmentation full matrix algebra')
  rec={'p':p,'lambda':[r-1,1],'Sym_r_formal_span_rank':full,'I2_formal_span_rank':rank([flatten(A) for A in B.values()],p),'socle_span_rank':sw,'quotient_span_rank':sq,'section_rank':a,'section_augmented_rank':b,'I2_endomorphism_dimension':end,'augmentation_generated_algebra_rank':ar,'augmentation_dimension':r-1}
  if p==3:
   values=[g for g in product(range(p),repeat=4) if (g[0]*g[3]-g[1]*g[2])%p]
   erank=rank([flatten(evalmat(M,g,p)) for g in values],p);need(erank<full,'finite-group sampling danger control')
   rec.update({'GL2_F3_matrices':len(values),'Sym5_finite_evaluation_span_rank':erank,'formal_vs_finite_differ':True})
  formal.append(rec)
 # Out-of-scope mutation controls.
 _,p2=graph(1,2);need(len(p2)==1,'p2 no proposed nonsplit extension')
 neg=augmentation_algebra(3,3);need(neg<4,'divisible-degree augmentation not simple')
 # Numerics recorded from reciprocity are derived, not independent certificates.
 D=[[1,0,0],[0,1,1],[0,0,1]];nabla=[6,4,2];dims=[sum(nabla[i]*D[i][j] for i in range(3)) for j in range(3)];need(dims==[6,4,6],'reciprocity dimension arithmetic')
 print(json.dumps({'result':'PASS','formal_coefficient_cases':formal,'all_prime_graph_controls':graph_results,'negative_controls':{'p2_Sym1_SCCs':p2,'p3_degree3_augmentation_algebra_rank':neg},'derived_not_independent_decomposition_matrix':D,'derived_injective_dimensions':dims,'scope':'Exact finite formal actions and graph controls support, but do not replace, the analytic all-odd-prime/all-rank argument. Algebraic-group invariance is not finite GL(Fp) sampling.'},indent=2,sort_keys=True))
if __name__=='__main__':main()
