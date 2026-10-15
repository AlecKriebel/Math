"""Exact controls of Fourier equivalence and a distinct set-action obstruction."""
from search_small import *
import sympy as sp
from collections import Counter,deque
C=Counter()
def ck(v,k):assert v,k;C[k]+=1
M=sp.Matrix([[2,1],[-1,0]]);Mp=sp.Matrix([[0,1],[-1,2]]);S=sp.Matrix([[0,-1],[-1,0]])
ck(M.inv().T==Mp,'inverse_transpose_r');ck(S.inv().T==S,'inverse_transpose_s')
def emb(A,i):
 B=sp.eye(3)
 for x in range(2):
  for y in range(2):B[x+i,y+i]=A[x,y]
 return B
for R in [M,Mp]:
 a,b,c,d=emb(R,0),emb(R,1),emb(S,0),emb(S,1)
 for lhs,rhs,k in [(a*b*a,b*a*b,'integral_YBE_r'),(c*d*c,d*c*d,'integral_YBE_s'),(c*c,sp.eye(3),'integral_s_square'),(c*b*c,d*a*d,'integral_virtual'),(c*b*a,b*a*d,'integral_welded')]:ck(lhs==rhs,k)
J=sp.Matrix([[1,0,0],[2,1,0],[2,2,1]]);T=J*emb(S,0)*J.inv();ck(T[2,0]==4 and T[2,1]==-4 and T[2,2]==1,'guitar_nonlocal_row')
# Complete size-three finite partner classification.
m=3;sols=enumerate_solutions(m);ck(len(sols)==66,'finite_nondegenerate_YBE_count');invol=[x for x in sols if comp(x,x)==tuple(range(9))];ck(len(invol)==12,'finite_involutive_count')
r=tuple((m*((2*x+y)%m)+(-x)%m) for x in range(m) for y in range(m));ss=tuple(m*((-y)%m)+(-x)%m for x in range(m) for y in range(m));rp=derived(r,m)
qs=[q for q in invol if welded(rp,q,m,1)];expected=[tuple(m*((c-y)%m)+(c-x)%m for x in range(m) for y in range(m)) for c in range(m)]
ck(set(qs)==set(expected),'complete_local_partner_classification')
oldgens=[lift(p,m,i) for p in [r,ss] for i in [0,1]]
fixed=lambda gs:sum(all(g[i]==i for g in gs) for i in range(27))
ck(fixed(oldgens)==3,'original_common_fixed_points')
charcounts=[]
for q in qs:
 newgens=[lift(p,m,i) for p in [rp,q] for i in [0,1]];ck(fixed(newgens)==1,'target_common_fixed_points')
 identity=tuple(range(27));seen={(identity,identity)};todo=[(identity,identity)]
 while todo:
  old,new=todo.pop();ck(sum(i==x for i,x in enumerate(old))==sum(i==x for i,x in enumerate(new)),'all_joint_image_characters')
  for a,b in zip(oldgens,newgens):
   e=(comp(a,old),comp(b,new))
   if e not in seen:seen.add(e);todo.append(e)
 ck(len(seen)==432,'joint_image_order');charcounts.append(len(seen))
print(json.dumps({'status':'PASS','exact_assertions':sum(C.values()),'families':dict(C),'joint_image_sizes':charcounts,'scope':'All-n complex linear equivalence is proved by finite Fourier duality in TURN_2. The set-action obstruction is different and is not a linear counterexample. General Q1/Q2 unresolved.'},indent=2))
