"""Independent finite audit, with direct tuple actions and integer lattices.

Usage: python independent_check.py [attempt_directory]
Default is the parent of the published independent_review directory.
No author Python module is imported.
"""
from itertools import permutations,product
from collections import Counter,deque
from pathlib import Path
import json,sys
import sympy as S
C=Counter()
def ck(x,k):
 assert x,k
 C[k]+=1

def pair(table,x,y,m):return divmod(table[m*x+y],m)
def step(v,table,slot,m):
 w=list(v);w[slot],w[slot+1]=pair(table,w[slot],w[slot+1],m);return tuple(w)
def act(v,word,ops,m):
 for which,i in reversed(word):v=step(v,ops[which],i,m)
 return v
BRAID_L=[(0,0),(0,1),(0,0)];BRAID_R=[(0,1),(0,0),(0,1)]
MIX_L=[(1,0),(0,1),(1,0)];MIX_R=[(1,1),(0,0),(1,1)]
WELD_L=[(1,0),(0,1),(0,0)];WELD_R=[(0,1),(0,0),(1,1)]
def ybe(p,m):return all(act(v,BRAID_L,[p],m)==act(v,BRAID_R,[p],m) for v in product(range(m),repeat=3))
def nondeg(p,m):return all(len({pair(p,x,y,m)[0] for y in range(m)})==m for x in range(m)) and all(len({pair(p,x,y,m)[1] for x in range(m)})==m for y in range(m))
def compatible(r,q,m,kind=1):
 WL,WR=(WELD_L,WELD_R) if kind==1 else ([(0,0),(0,1),(1,0)],[(1,1),(0,0),(0,1)])
 return all(act(v,MIX_L,[r,q],m)==act(v,MIX_R,[r,q],m) and act(v,WL,[r,q],m)==act(v,WR,[r,q],m) for v in product(range(m),repeat=3))
all_solution_data={};invall=[];examined=0
for m in [2,3]:
 sols=[];invol_nd=[];invol_all=[]
 for p in permutations(range(m*m)):
  if m==3:examined+=1
  invol=all(p[p[j]]==j for j in range(m*m));nd=nondeg(p,m)
  if not(invol or nd):continue
  if not ybe(p,m):continue
  if invol:invol_all.append(p)
  if nd:
   sols.append(p)
   if invol:invol_nd.append(p)
 all_solution_data[m]=(sols,invol_nd)
 ck((len(sols),len(invol_nd))==({2:(4,2),3:(66,12)}[m]),'nondegenerate_census')
 if m==3:invall=invol_all
ck(examined==362880,'all_nine_factorial_bijections_covered');ck(len(invall)==19,'all_involutive_YBE_including_degenerate')
r=tuple(3*((y-x)%3)+(-x)%3 for x,y in product(range(3),repeat=2));ss=tuple(3*((-y)%3)+(-x)%3 for x,y in product(range(3),repeat=2));rp=tuple(3*y+(-x-y)%3 for x,y in product(range(3),repeat=2));R=tuple(3*((-x-y)%3)+x for x,y in product(range(3),repeat=2));tw=tuple(3*y+x for x,y in product(range(3),repeat=2))
partners=[q for q in invall if compatible(rp,q,3)];expected=[tuple(3*((c-y)%3)+(c-x)%3 for x,y in product(range(3),repeat=2)) for c in range(3)];ck(set(partners)==set(expected),'all_compatible_partners')
# Full finite census and guitar locality, independently represented as tuple maps.
def guitar(v,p,m):
 out=[]
 for i in range(len(v)):
  t=v[i]
  for j in range(i-1,-1,-1):t=pair(p,v[j],t,m)[0]
  out.append(t)
 return tuple(out)
sols,iqs=all_solution_data[3];census=Counter()
for rr in sols:
 P2=list(product(range(3),repeat=2));J2={v:guitar(v,rr,3) for v in P2};I2={w:v for v,w in J2.items()}
 P3=list(product(range(3),repeat=3));J3={v:guitar(v,rr,3) for v in P3};I3={w:v for v,w in J3.items()}
 ck(len(I2)==9 and len(I3)==27,'guitar_is_bijection')
 for qq in iqs:
  for kind in [1,2]:
   if not compatible(rr,qq,3,kind):continue
   census['welded_'+str(kind)]+=1
   target=tuple(3*J2[pair(qq,*I2[v],3)][0]+J2[pair(qq,*I2[v],3)][1] for v in P2)
   local=all(J3[step(I3[v],qq,i,3)]==step(v,target,i,3) for v in P3 for i in [0,1])
   census['local_'+str(kind)]+=local
ck(dict(census)=={'welded_1':228,'local_1':222,'welded_2':228,'local_2':222},'complete_three_color_locality_census')
# Integral matrices validate all-prime and all-strand Fourier mechanism.
M=S.Matrix([[2,1],[-1,0]]);Mp=S.Matrix([[0,1],[-1,2]]);T=S.Matrix([[0,-1],[-1,0]])
ck(M.inv().T==Mp and T.inv().T==T,'integral_inverse_transposes')
def emb(A,i):
 B=S.eye(3);B[i:i+2,i:i+2]=A;return B
for Q in [M,Mp]:
 a,b,c,d=emb(Q,0),emb(Q,1),emb(T,0),emb(T,1)
 for lhs,rhs in [(a*b*a,b*a*b),(c*d*c,d*c*d),(c*c,S.eye(3)),(c*b*c,d*a*d),(c*b*a,b*a*d)]:ck(lhs==rhs,'integral_welded_relations')
# Group-algebra norm: form each word by tuple action rather than color matrices.
u=[(0,1),(0,1),(1,0),(0,0),(1,1),(0,0)]
v=[(0,0),(0,1),(1,1),(1,0),(0,1),(0,1)]
P=list(product(range(3),repeat=3));index={x:i for i,x in enumerate(P)}
def rank3(A):
 A=[[int(x)%3 for x in row] for row in A];h=0
 for j in range(len(A[0])):
  k=next((k for k in range(h,len(A)) if A[k][j]),None)
  if k is None:continue
  A[k],A[h]=A[h],A[k];z=pow(A[h][j],-1,3);A[h]=[(z*x)%3 for x in A[h]]
  for k in range(len(A)):
   if k!=h:
    z=A[k][j];A[k]=[(a-z*b)%3 for a,b in zip(A[k],A[h])]
  h+=1
 return h
norm_ranks=[]
for k,q in enumerate([ss]+partners):
 ops=[r,q] if k==0 else [rp,q];U={x:act(x,u,ops,3) for x in P};V={x:act(x,v,ops,3) for x in P};N=[[0]*27 for _ in P]
 for x in P:
  for a in range(3):
   for b in range(3):
    y=x
    for _ in range(b):y=V[y]
    for _ in range(a):y=U[y]
    N[index[y]][index[x]]+=1
 norm_ranks.append(rank3(N))
 ck(norm_ranks[-1]==(0 if k==0 else 2),'group_algebra_norm_rank')
 # Fixed basis points are a different invariant from linear character.
 fixed=sum(all(step(x,ops[j],i,3)==x for j in [0,1] for i in [0,1]) for x in P)
 ck(fixed==(3 if k==0 else 1),'set_fixed_point_countercontrol')
# Direct integer relation matrices with RELATIONS OUTER, TRIPLES INNER order.
rels=[(BRAID_L,BRAID_R), ([(1,0),(1,1),(1,0)],[(1,1),(1,0),(1,1)]), ([(1,0),(1,0)],[]),(MIX_L,MIX_R),(WELD_L,WELD_R)]
def weighted_exponents(x,w,ops):
 state=list(x);c=Counter()
 for k,i in reversed(w):
  c[(k,state[i],state[i+1])]+=1;state[i],state[i+1]=pair(ops[k],state[i],state[i+1],3)
 return tuple(state),[c[(k,x,y)] for k,x,y in product(range(2),range(3),range(3))]
def relation_matrix(ops):
 rows=[]
 for L,H in rels:
  for x in P:
   a,b=weighted_exponents(x,L,ops);c,d=weighted_exponents(x,H,ops);ck(a==c,'weight_underlying_relation')
   rows.append([u-v for u,v in zip(b,d)])
 for k in range(2):
  for x,y in product(range(3),repeat=2):
   if pair(ops[k],x,y,3)==(x,y):
    row=[0]*18;row[9*k+3*x+y]=1;rows.append(row)
 return S.Matrix(rows)
root=Path(sys.argv[1]) if len(sys.argv)>1 else Path(__file__).resolve().parent.parent
certs=json.loads((root/'turn_4_lattice_certificate.json').read_text())
for name,ops,free,oldrows,lam in [('original',[r,ss],[3,10],[138,8,15,16,17,21,23,26,45,48,49,50,53,55,58,135],S.Matrix([[1,-1],[0,1],[0,0]])),('twist',[R,tw],[1,3],[138,8,15,17,19,20,23,24,25,29,30,45,48,49,55,135],S.Matrix([[0,1],[1,0],[0,0]]))]:
 A=relation_matrix(ops);ck(A.shape==(141,18),'complete_weight_matrix_shape')
 remap=lambda i:27*(i%5)+i//5 if i<135 else i
 cols=[j for j in range(18) if j not in free];B=A[[remap(i) for i in oldrows],cols]
 ck(B.det()==-1,'unimodular_weight_minor')
 # The gauge character matrix gives the expected full integer solutions.
 D=[]
 for k,x,y in product(range(2),range(3),range(3)):
  a,b=pair(ops[k],x,y,3);D.append([int(z==x)+int(z==y)-int(z==a)-int(z==b) for z in range(3)])
 E=S.Matrix(D)*lam;ck(A*E==S.zeros(141,2),'all_weight_equations_coboundary')
 ck(E[free,:]==S.eye(2),'free_weight_parameters_exact')
 solved=-B.inv()*A[[remap(i) for i in oldrows],free]
 ck(solved==E[cols,:] and all(x.q==1 for x in solved),'integral_unique_weight_solution')
 cert=next(x for x in certs if x['pair']==name)
 for i,row in enumerate(cert['relation_matrix']):
  for j,val in enumerate(row):ck(val==A[remap(i),j],'every_saved_lattice_entry')
 ck(cert['solution_exponents']==E.tolist(),'saved_monomial_exponents')
# Generic free-word calculation of the welded strand law (no commutation used).
def mulword(a,b,order2=False):
 w=list(a)
 for x in b:
  if w and (w[-1]==-x or (order2 and abs(x)==1 and w[-1]==x)):w.pop()
  else:w.append(x)
 return tuple(w)
def generic_lift(state,k,i,ops,f,g):
 st=list(state);x,label,u=st[i];y,label2,vv=st[i+1];a,b=pair(ops[k],x,y,3)
 if k==0:st[i]=(a,label2,vv);st[i+1]=(b,label,mulword(u,f(x,y)))
 else:st[i]=(a,label2,mulword(vv,g(x,y)));st[i+1]=(b,label,mulword(u,g(x,y)))
 return st
f=lambda x,y:(1+3*x+y,);g=lambda x,y:(10+3*x+y,)
for x,y,z in P:
 st=[(x,0,()),(y,1,()),(z,2,())];left=st;right=st
 for k,i in reversed(WELD_L):left=generic_lift(left,k,i,[r,ss],f,g)
 for k,i in reversed(WELD_R):right=generic_lift(right,k,i,[r,ss],f,g)
 a,b=pair(r,x,y,3);cc,dd=pair(r,b,z,3);h,j=pair(ss,y,z,3);a2,b2=pair(r,x,h,3)
 ck([x[1] for x in left]==[2,1,0] and [x[1] for x in right]==[2,1,0],'ordered_final_strands')
 ck(left[0][2]==g(a,cc) and left[1][2]==g(a,cc) and left[2][2]==f(x,y)+f(b,z),'generic_weld_left_products')
 ck(right[0][2]==g(y,z) and right[1][2]==g(y,z) and right[2][2]==f(x,h)+f(b2,j),'generic_weld_right_products')
# Source examples checked in Free(a,b) x Z(z), preserving noncommutation.
def coefficient_product(a,b,order2=False):return (mulword(a[0],b[0],order2),a[1]+b[1])
ONE=((),0)
def ex_ops(case,x,y):
 if case=='original':return [(y,x),(1-y,1-x)],((1,),0) if x!=y else ONE,ONE
 if case=='derived':return [(1-y,1-x),(y,x)],((1,),0) if x==y else ONE,ONE
 return [(y,x),(y,x)],(((1,) if x==0 else (2,)),0) if x!=y else ONE,((),1 if x==0 else -1) if x!=y else ONE

def ex_act(colors,w,case,order2=False):
 st=[(x,i,ONE) for i,x in enumerate(colors)]
 for k,i in reversed(w):
  x,j,a=st[i];y,l,b=st[i+1];op,ff,gg=ex_ops(case,x,y);u,v=op[k]
  st[i]=(u,l,coefficient_product(b,gg,order2) if k else b)
  st[i+1]=(v,j,coefficient_product(a,gg if k else ff,order2))
 return st
fails={}
for case in ['original','derived','nonabelian_twist']:
 for order2 in ([False,True] if case!='nonabelian_twist' else [False]):
  bad=0
  for xyz in product(range(2),repeat=3):
   for idx,(L,H) in enumerate(rels):
    same=ex_act(xyz,L,case,order2)==ex_act(xyz,H,case,order2)
    if idx==4 and case!='nonabelian_twist' and not order2:bad+=not same
    else:ck(same,'published_virtual_and_welded_examples')
  if case!='nonabelian_twist' and not order2:ck(bad>0,'infinite_cyclic_welded_failure');fails[case]=bad
ck(coefficient_product(((1,),0),((2,),0))!=coefficient_product(((2,),0),((1,),0)),'genuinely_noncommuting_control')
print(json.dumps({'status':'PASS','exact_assertions':sum(C.values()),'counts':dict(sorted(C.items())),'bijections_examined':examined,'involutive_YBE_count':len(invall),'compatible_partners':[list(q) for q in partners],'modular_norm_ranks':norm_ranks,'welded_census':dict(census),'source_virtual_weld_failures':fails,'scope':'Independent finite enumeration, modular ranks, full integer lattice and ordered nonabelian coefficient controls. Original general Q1/Q2 bundle remains unresolved.'},indent=2,sort_keys=True))
