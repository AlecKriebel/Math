"""Exact finite certificate for the characteristic-three rank obstruction."""
from search_small import *
from collections import Counter
C=Counter()
def ck(v,k):assert v,k;C[k]+=1
m=3;id9=tuple(range(9));r=tuple(3*((y-x)%3)+(-x)%3 for x in range(3) for y in range(3));ss=tuple(3*((-y)%3)+(-x)%3 for x in range(3) for y in range(3));rp=derived(r,3)
qs=[];iy=0
for q in permutations(range(9)):
 if comp(q,q)!=id9:continue
 a,b=lift(q,3,0),lift(q,3,1)
 if comp(a,comp(b,a))!=comp(b,comp(a,b)):continue
 iy+=1
 if welded(rp,q,3,1):qs.append(q)
expected=[tuple(3*((c-y)%3)+(c-x)%3 for x in range(3) for y in range(3)) for c in range(3)]
ck(iy==19,'all_involutive_YBE_bijections');ck(set(qs)==set(expected),'complete_partner_classification_without_nondegeneracy')
u=(1,1,2,0,3,0);v=(0,1,3,2,1,1)
def evalword(gs,w):
 out=tuple(range(27))
 for i in reversed(w):out=comp(gs[i],out)
 return out
ell=(1,2,1);phi=(1,1,0);psi=(0,1,1)
def dot(a,b):return sum(x*y for x,y in zip(a,b))%3
def enc(x):return 9*x[0]+3*x[1]+x[2]
def matrix_action(kind,form):
 out=[]
 for x in product(range(3),repeat=3):
  y=tuple((x[i]+ell[i]*dot(form,x))%3 for i in range(3)) if kind==0 else tuple((x[i]-form[i]*dot(ell,x))%3 for i in range(3))
  out.append(enc(y))
 return tuple(out)
old=[lift(p,3,i) for p in[r,ss] for i in[0,1]];new=[lift(p,3,i) for p in[rp,ss] for i in[0,1]]
for name,gs,kind in [('original',old,0),('target',new,1)]:
 U=evalword(gs,u);V=evalword(gs,v)
 ck(U==matrix_action(kind,phi),name+'_u_word');ck(V==matrix_action(kind,psi),name+'_v_word')
 ck(comp(U,V)==comp(V,U),name+'_commutes');ck(len(powers(U))==3 and len(powers(V))==3,name+'_order_three')
 ck(len({comp(a,b) for a in powers(U) for b in powers(V)})==9,name+'_nine_distinct_shears')
def norm_matrix(gs):
 U=evalword(gs,u);V=evalword(gs,v);N=[[0]*27 for _ in range(27)]
 for a in powers(U):
  for b in powers(V):
   p=comp(a,b)
   for i,j in enumerate(p):N[j][i]=(N[j][i]+1)%3
 return N

def rank_mod3(A):
 A=[r[:] for r in A];rank=0
 for col in range(len(A[0])):
  piv=next((j for j in range(rank,len(A)) if A[j][col]),None)
  if piv is None:continue
  A[rank],A[piv]=A[piv],A[rank];inv=pow(A[rank][col],-1,3);A[rank]=[(inv*x)%3 for x in A[rank]]
  for j in range(len(A)):
   if j!=rank:
    b=A[j][col];A[j]=[(x-b*y)%3 for x,y in zip(A[j],A[rank])]
  rank+=1
 return rank
ranks=[rank_mod3(norm_matrix(old))];ck(ranks[0]==0,'original_norm_zero')
for q in qs:
 gs=[lift(p,3,i) for p in[rp,q] for i in[0,1]];rank=rank_mod3(norm_matrix(gs));ck(rank==2,'target_norm_rank_two');ranks.append(rank)
print(json.dumps({'status':'PASS','exact_assertions':sum(C.values()),'families':dict(C),'all_involutive_YBE_bijections':iy,'compatible_qs':qs,'u_generator_indices':u,'v_generator_indices':v,'norm_ranks_original_then_targets':ranks,'scope':'A genuine K-linear inequivalence for n=3 over every field of characteristic three. It is not a characteristic-zero or cocycle-weighted counterexample.'},indent=2))
