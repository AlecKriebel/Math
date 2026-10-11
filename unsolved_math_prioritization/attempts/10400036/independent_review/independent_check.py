#!/usr/bin/env python3
"""Independent exact controls, with no imports from the author packet."""
from itertools import product,permutations
from collections import Counter
from pathlib import Path
import json,hashlib
C=Counter()
def ok(x,name):
 assert x,name
 C[name]+=1

def eye(n):return [[int(i==j) for j in range(n)] for i in range(n)]
def mm(a,b):return [[sum(x*y for x,y in zip(row,col)) for col in zip(*b)] for row in a]
def add(a,b):return [[x+y for x,y in zip(u,v)] for u,v in zip(a,b)]
def scale(a,k):return [[k*x for x in row] for row in a]
def invert(a):
 n=len(a);T=add(a,scale(eye(n),-1));out=eye(n);power=eye(n)
 for j in range(1,n):power=mm(power,T);out=add(out,scale(power,(-1)**j))
 return out

def tr(n,i,j,x=1):
 a=eye(n);a[i][j]=x;return a

def matrix_word(w,target):
 n=len(target)+1;out=eye(n)
 for x in w:
  if abs(x) in target:
   i=target.index(abs(x));out=mm(out,tr(n,i,i+1,1 if x>0 else -1))
 return out

def series(w,d):
 out={():1}
 for x in w:
  fac={():1}
  if x>0:fac[(x,)]=1
  else:
   for k in range(1,d+1):fac[(abs(x),)*k]=(-1)**k
  new=Counter()
  for u,a in out.items():
   for v,b in fac.items():
    if len(u)+len(v)<=d:new[u+v]+=a*b
  out={u:a for u,a in new.items() if a}
 return out

def iw(w):return tuple(-x for x in reversed(w))
def cword(u,v):return tuple(u)+tuple(v)+iw(u)+iw(v)

def sample(n,t):
 a=eye(n)
 for i in range(n):
  for j in range(i+1,n):a[i][j]=((t+3)*(i+1)+t*t*(j+1)+3*i*j)%5-2
 return a

def section(a):
 b=[r[:] for r in a];b[0][-1]=0;return b

def residue(q,g):
 end=section(mm(q,g));res=mm(mm(q,g),invert(end))
 ok(res==tr(len(q),0,len(q)-1,res[0][-1]),'central_residual_exact')
 return end,res[0][-1]

# Distinct targets in arbitrary order; repeated variables retained in the independent series.
targets=[x for k in range(1,4) for x in permutations((1,2,3),k)]
for size in range(5):
 for w in product((1,-1,2,-2,3,-3),repeat=size):
  E=series(w,3)
  for t in targets:ok(matrix_word(w,t)[0][-1]==E.get(t,0),'arbitrary_order_magnus_extraction')
  ok(E.get((1,2),0)+E.get((2,1),0)==E.get((1,),0)*E.get((2,),0),'shuffle_with_negative_powers')
  ok(series(w+iw(w),3)=={():1},'free_word_inverse')

# Degree-two transported meridians and the closure ambiguity, directly as expansions.
for size in range(4):
 for h in product((1,-1,2,-2,3,-3),repeat=size):
  A=[sum(1 if x>0 else -1 for x in h if abs(x)==i) for i in (1,2,3)]
  for i,j in permutations((1,2,3),2):
   for mer in (1,2,3):
    for eps in (-1,1):
     E=series(h+(eps*mer,)+iw(h),2)
     ok(E.get((i,j),0)==eps*(A[i-1]*(mer==j)-(mer==i)*A[j-1]),'transport_formula')
for power in range(-20,21):
 w=cword((1,),(2,));ww=(w*power if power>=0 else iw(w)*(-power))
 ok(series(ww,2).get((1,2),0)==power,'closed_hopf_relator_lift_ambiguity')

# Integral acyclicity certificate for a graph cylinder relative to its bottom graph.
def det_bareiss(A):
 A=[row[:] for row in A];n=len(A);last=1;sgn=1
 for k in range(n-1):
  if A[k][k]==0:
   j=next(i for i in range(k+1,n) if A[i][k]);A[k],A[j]=A[j],A[k];sgn=-sgn
  pivot=A[k][k]
  for i in range(k+1,n):
   for j in range(k+1,n):A[i][j]=(A[i][j]*pivot-A[i][k]*A[k][j])//last
  for i in range(k+1,n):A[i][k]=0
  last=pivot
 return sgn*A[-1][-1]
for r in range(1,7):
 V=2*r+1;edges=[e for i in range(r) for e in [(0,2*i+1),(2*i+1,2*i+2),(0,2*i+2)]];E=len(edges);N=V+2*E
 basis=[[int(i==j) for j in range(V)] for i in range(N)]
 B=[]
 for e,(u,v) in enumerate(edges):
  a=[0]*N;a[v]=1;a[V+e]=-1
  b=[0]*N;b[u]=1;b[V+e]=-1;b[V+E+e]=1
  B.extend([a,b])
 for row in range(N):basis[row].extend(col[row] for col in B)
 ok(abs(det_bareiss(basis))==1,'relative_integral_unimodular_basis')
 boundary=[[0]*N for _ in range(V)]
 for v in range(V):boundary[v][v]=1
 for e,(u,v) in enumerate(edges):boundary[v][V+e]=1;boundary[v][V+E+e]=1;boundary[u][V+E+e]=-1
 ok(mm(boundary,basis)==[[int(i==j) for j in range(N)] for i in range(V)],'relative_integral_chain_contraction')
 # Nontrivial U holonomy on each meridian survives a boundary-fixed cylinder gauge.
 n=r+1;H=[sample(n,23+i) for i in range(V)]
 for e,(u,v) in enumerate(edges):
  bottom=tr(n,e//3,e//3+1,-1) if e%3==2 else eye(n)
  top=mm(mm(invert(H[u]),bottom),H[v]);diagonal=mm(bottom,H[v])
  ok(mm(bottom,H[v])==diagonal and mm(H[u],top)==diagonal,'nontrivial_cylinder_flat_extension')
  for i in range(n):
   for j in range(i+1,n):
    # Triangle(u0,u1,v1) uses H[u],top,diagonal.
    lhs=top[i][j]-diagonal[i][j]+H[u][i][j]
    rhs=-sum(H[u][i][k]*top[k][j] for k in range(i+1,j))
    ok(lhs==rhs,'integral_ordered_cup_equation')

# Independent Gaussian elimination returns a word in adjacent meridians.
def transvection_word(i,j,a):
 w=tuple([i+1 if a>=0 else -(i+1)]*abs(a))
 for t in range(i+1,j):w=cword(w,(t+1,))
 return w
for n in range(2,7):
 for t in range(25):
  G=sample(n,t);q=section(G);target=invert(q);A=[row[:] for row in target];ops=[]
  for distance in range(1,n):
   for i in range(n-distance):
    j=i+distance;a=A[i][j];ops.append((i,j,-a));A=mm(A,tr(n,i,j,-a))
  ok(A==eye(n),'independent_right_elimination')
  eta=()
  for i,j,a in reversed(ops):eta+=transvection_word(i,j,-a)
  M=matrix_word(eta,tuple(range(1,n)))
  ok(M==target,'lower_only_return_word_full_matrix')
  closed=mm(G,M);ok(closed==tr(n,0,n-1,G[0][-1]),'target_retained_by_correction')
  # Telescoping on the explicitly generated lifted corrected path.
  start=eye(n);value=0
  for edge in [G]+[tr(n,abs(x)-1,abs(x),1 if x>0 else -1) for x in eta]:start,c=residue(start,edge);value+=c
  ok(start==eye(n) and value==G[0][-1],'closed_cover_geometric_pairing')
  H=sample(n,t+10);end,c1=residue(q,G);end2,c2=residue(end,H);end3,c3=residue(q,mm(G,H))
  ok(end2==end3 and c1+c2==c3,'cover_cocycle_concatenation')
  _,reverse=residue(end,invert(G));ok(reverse==-c1,'cover_edge_orientation')

# Closed-grid area by the shoelace formula, independently of matrix multiplication.
for length in range(8):
 for w in product((1,-1,2,-2),repeat=length):
  vertices=[(0,0)]
  for x in w:
   a,b=vertices[-1];vertices.append((a+(1 if x==1 else -1 if x==-1 else 0),b+(1 if x==2 else -1 if x==-2 else 0)))
  a,b=vertices[-1];vertices.extend([(0,b),(0,0)])
  twice=sum(x*v-y*u for (x,y),(u,v) in zip(vertices,vertices[1:]))
  ok(twice==2*matrix_word(w,(1,2))[0][-1],'proper_grid_surface_shoelace_pairing')
  ok(twice%2==0,'integral_grid_pairing')
for n in range(3,9):
 A=tr(n,0,1);B=tr(n,1,n-1)
 for a,b in product(range(-2,3),repeat=2):
  X=mm(A,tr(n,0,n-1,a));Y=mm(B,tr(n,0,n-1,b));comm=mm(mm(mm(X,Y),invert(X)),invert(Y))
  ok(comm==tr(n,0,n-1),'central_extension_nonsplitting')
for r in range(2,10):
 target=tuple(range(1,r+1));u=target[:-1];v=target[-1:]
 ok(matrix_word(u,target)[0][-1]==matrix_word(v,target)[0][-1]==0 and matrix_word(u+v,target)[0][-1]==1,'fixed_cycle_additivity_obstruction')
print(json.dumps({'problem_id':10400036,'status':'PASS','exact_controls':sum(C.values()),'groups':dict(sorted(C.items())),'arithmetic':'integers only; dense matrices, full truncated series, Artin-free transport, integral relative chain basis and shoelace geometry','scope':'Independent finite controls support the reviewed proofs. They do not establish the missing adaptive downstairs derived-link comparison or a universal impossibility claim.','checker_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()},indent=2,sort_keys=True))
