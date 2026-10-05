#!/usr/bin/env python3
"""Exact rational certificates for Kourovka 21.90; no graph-existence inference."""
from fractions import Fraction as F
from itertools import permutations,product
from math import comb,ceil
import json,pathlib

def inv(A):
 n=len(A);B=[[F(x)for x in r]+[F(i==j)for j in range(n)]for i,r in enumerate(A)]
 for i in range(n):
  p=next(j for j in range(i,n)if B[j][i]);B[i],B[p]=B[p],B[i]
  d=B[i][i];B[i]=[x/d for x in B[i]]
  for j in range(n):
   if j!=i:
    d=B[j][i];B[j]=[x-d*y for x,y in zip(B[j],B[i])]
 return [r[n:]for r in B]

def data(t,c,a):
 t,c,a=map(F,(t,c,a));k=t*(c+1)+a
 P=[[1,k,t*k,k*(a+1)/(c+1)],[1,a+t,-t,-a-1],[1,-1,-t,t],[1,-c-1,a+c+1,-a-1]]
 P=[[F(x)for x in r]for r in P];v=sum(P[0]);Q=[[v*x for x in r]for r in inv(P)]
 p=[[[sum(P[l][i]*P[l][j]*Q[h][l]for l in range(4))/v for h in range(4)]for j in range(4)]for i in range(4)]
 q=[[[sum(Q[l][i]*Q[l][j]*P[h][l]for l in range(4))/v for h in range(4)]for j in range(4)]for i in range(4)]
 return P,Q,p,q,v

def q_orders(q):
 result=[]
 for order in permutations((1,2,3)):
  o=(0,)+order;g=o[1]
  if all((q[g][o[j]][o[h]]==0 if abs(j-h)>1 else q[g][o[j]][o[h]]>0 if abs(j-h)==1 else True)for j in range(4)for h in range(4)):
   result.append(o)
 return result

def integral_nonnegative(xs):return all(x.denominator==1 and x>=0 for x in xs)

def enumerate_parameters(T):
 rows=[]
 for t in range(2,T+1):
  for a in range(1,t*t-1):
   z=F(a*(a+1),t*t-a-1)
   if z.denominator!=1 or z<=1:continue
   c=int(z)-1;k=t*(c+1)+a
   P,Q,p,q,v=data(t,c,a)
   reasons=[]
   if not integral_nonnegative(P[0]+Q[0]):reasons.append('nonintegral_valency_or_multiplicity')
   if not integral_nonnegative([x for r in p for s in r for x in s]):reasons.append('intersection_number')
   if any(x<0 for r in q for s in r for x in s):reasons.append('negative_Krein')
   if not q_orders(q):reasons.append('not_Q_polynomial')
   if not (k>=t*c>=a+1 and 1<=c<=t*(c+1)):reasons.append('intersection_array_monotonicity')
   if any((P[0][i]*p[i][h][i]).denominator==1 and int(P[0][i]*p[i][h][i])%2 for i in range(1,4) for h in range(1,4)):reasons.append('shell_edge_parity')
   alpha=(k+(a+t)-1)//(a+t)
   if k<alpha*(a+t)-comb(alpha,2)*(c-1):reasons.append('local_claw_bound')
   # Primitive SRG absolute bound in each of the two nonprincipal eigenspaces.
   for i in (2,3):
    vals={P[j][i]for j in (1,2,3)}
    assert len(vals)==2
    for lam in vals:
     m=sum(Q[0][j]for j in (1,2,3)if P[j][i]==lam)
     if v>m*(m+3)/2:reasons.append('SRG_absolute_bound_distance_'+str(i))
   rows.append(dict(t=t,c=c,a=a,array=[k,t*c,a+1,1,c,t*(c+1)],v=int(v)if v.denominator==1 else str(v),rejections=sorted(set(reasons))))
 return rows

def crown_check(n):
 # Vertices (side,label). Exact distance, distance-regularity and SRG checks.
 N=2*n;V=list(product(range(2),range(n)))
 A=[[int(s!=t and i!=j)for t,j in V]for s,i in V]
 D=[[0 if u==v else 1 if A[u][v] else 2 if V[u][0]==V[v][0] else 3 for v in range(N)]for u in range(N)]
 # Independently verify the displayed distance rule by breadth-first search.
 for u in range(N):
  dist=[None]*N;dist[u]=0;queue=[u]
  for v in queue:
   for w in range(N):
    if A[v][w] and dist[w] is None:dist[w]=dist[v]+1;queue.append(w)
  assert D[u]==dist
 assert max(max(r)for r in D)==3
 arr=[[],[]]
 for d in range(4):
  stats=set()
  for u in range(N):
   for v in range(N):
    if D[u][v]==d:
     stats.add(tuple(sum(A[v][w]and D[u][w]==e for w in range(N))for e in (d-1,d,d+1)))
  assert len(stats)==1
  cc,aa,bb=next(iter(stats))
  if d<3:arr[0].append(bb)
  if d>0:arr[1].append(cc)
 assert arr==[[n-1,n-2,1],[1,n-2,n-1]]
 srg=[]
 for d in (2,3):
  B=[[int(D[u][v]==d)for v in range(N)]for u in range(N)]
  deg=set(map(sum,B));adj=set();non=set()
  for u in range(N):
   for v in range(u):
    (adj if B[u][v] else non).add(sum(B[u][w]*B[v][w]for w in range(N)))
  assert len(deg)==len(adj)==len(non)==1
  srg.append([N,next(iter(deg)),next(iter(adj)),next(iter(non))])
 assert srg==[[2*n,n-1,n-2,0],[2*n,1,0,0]]
 P,Q,p,q,v=data(1,n-2,0)
 assert (0,1,2,3)in q_orders(q)
 assert all(x>=0 for r in q for s in r for x in s)
 return {'n':n,'array':arr,'SRGs':srg,'Q_orders':q_orders(q)}

def main():
 rows=enumerate_parameters(30)
 small=[r for r in rows if r['t']<=6 and not r['rejections']]
 assert len(small)==10
 assert all(r['t']>=3 for r in small)
 controls={}
 P,Q,p,q,v=data(2,5,2);controls['array_14_rejected_absolute']=v>Q[0][3]*(Q[0][3]+3)/2
 P,Q,p,q,v=data(3,5,3);controls['wrong_relation_rejected_Q']=not q_orders(q)
 controls['mutated_crown_parameter_rejected']=([6,2,1,1] != crown_check(3)['SRGs'][0])
 assert all(controls.values())
 result={'scope':'Exact necessary-parameter search for 2 <= t <= 30; no graph construction or global nonexistence claim.','crown_checks':[crown_check(n)for n in range(3,11)],'negative_controls':controls,'parameter_count':len(rows),'survivors_t_le_6':small,'survivors_t_le_30':[r for r in rows if not r['rejections']],'all_parameter_rows':rows}
 out=pathlib.Path(__file__).with_name('CHECK_RESULTS.json');out.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items()if k not in ('all_parameter_rows','survivors_t_le_30')},indent=2));print('Survivors through 30:',len(result['survivors_t_le_30']))
if __name__=='__main__':main()
