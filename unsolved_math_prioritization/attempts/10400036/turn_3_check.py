#!/usr/bin/env python3
"""Exact finite controls of the all-order unipotent/cochain construction."""
from itertools import product,combinations
from collections import Counter
import json
C=Counter()
def ck(x,key):
 assert x,key
 C[key]+=1

def ident(n):return tuple(tuple(int(i==j) for j in range(n)) for i in range(n))
def mm(A,B):
 n=len(A)
 return tuple(tuple(sum(A[i][k]*B[k][j] for k in range(i,j+1)) if i<=j else 0 for j in range(n)) for i in range(n))
def inv(A):
 n=len(A);B=[list(row) for row in ident(n)]
 for d in range(1,n):
  for i in range(n-d):
   j=i+d;B[i][j]=-sum(A[i][k]*B[k][j] for k in range(i+1,j+1))
 return tuple(map(tuple,B))
def gen(n,i,sign=1):
 A=[list(row) for row in ident(n)];A[i-1][i]=sign;return tuple(map(tuple,A))
def word_matrix(w,r):
 A=ident(r+1)
 for x in w:A=mm(A,gen(r+1,abs(x),1 if x>0 else -1))
 return A

def magnus(w,r):
 # Independent sparse expansion in the ring with repeated variables zero.
 out={():1}
 for x in w:
  new=Counter(out)
  for u,c in out.items():
   if len(u)<r and abs(x) not in u:new[u+(abs(x),)]+=c*(1 if x>0 else -1)
  out={u:c for u,c in new.items() if c}
 return out

def sample(n,seed):
 A=[list(row) for row in ident(n)]
 for i in range(n):
  for j in range(i+1,n):A[i][j]=((seed*(i+2)*(j+3)+7*i-5*j)%9)-4
 return tuple(map(tuple,A))

word_count=0
for r in range(1,5):
 letters=tuple(x for i in range(1,r+1) for x in (i,-i))
 for length in range(5):
  for w in product(letters,repeat=length):
   word_count+=1;A=word_matrix(w,r);E=magnus(w,r)
   for p,q in combinations(range(r+1),2):
    ck(A[p][q]==E.get(tuple(range(p+1,q+1)),0),'every_contiguous_coefficient')
   ck(mm(A,inv(A))==ident(r+1),'integral_inverse')

for n in range(2,7):
 for seed in range(60):
  U=[sample(n,seed+31*v) for v in range(4)]
  G={(v,w):mm(inv(U[v]),U[w]) for v,w in combinations(range(4),2)}
  for u,v,w in combinations(range(4),3):
   ck(G[u,w]==mm(G[u,v],G[v,w]),'triangle_flatness')
   for p,q in combinations(range(n),2):
    delta=G[v,w][p][q]-G[u,w][p][q]+G[u,v][p][q]
    cup=sum(G[u,v][p][s]*G[v,w][s][q] for s in range(p+1,q))
    ck(delta==-cup,'integer_maurer_cartan')
  # Delta b over the tetrahedron, with all signs from the ordered cup formula.
  def b(u,v,w,p,q):return -sum(G[u,v][p][s]*G[v,w][s][q] for s in range(p+1,q))
  for p,q in combinations(range(n),2):
   ck(b(1,2,3,p,q)-b(0,2,3,p,q)+b(0,1,3,p,q)-b(0,1,2,p,q)==0,'relative_obstruction_cocycle')
  # Triangle relative to edge01: any two extensions differ by a gauge at2.
  B=sample(n,seed+100);H=sample(n,seed+200);Hp=sample(n,seed+300)
  gauge=mm(inv(H),Hp)
  ck(mm(H,gauge)==Hp and mm(mm(B,H),gauge)==mm(B,Hp),'relative_vertex_gauge')

# Cancellation of all triple split terms is formal and noncommutative.
for n in range(2,30):
 for p,q in combinations(range(n),2):
  first=Counter();second=Counter()
  for k in range(p+1,q):
   for j in range(p+1,k):first[((p,j),(j,k),(k,q))]+=1
   for j in range(k+1,q):second[((p,k),(k,j),(j,q))]+=1
  ck(first==second,'formal_all_split_cancellation')

# Based circle gauge preserves full holonomy. The prefix gauge makes every
# edge except the last identity and leaves the last equal to the original holonomy.
for n in range(2,7):
 for seed in range(120):
  edges=[sample(n,seed+17*i) for i in range(1,6)]
  prefixes=[ident(n)]
  for G in edges:prefixes.append(mm(prefixes[-1],G))
  hol=prefixes[-1]
  gauge=[ident(n)]+[inv(P) for P in prefixes[1:-1]]+[ident(n)]
  transformed=[mm(mm(inv(gauge[i]),edges[i]),gauge[i+1]) for i in range(len(edges))]
  ck(all(G==ident(n) for G in transformed[:-1]),'circle_gauge')
  ck(transformed[-1]==hol,'circle_gauge')
  hol2=ident(n)
  for G in transformed:hol2=mm(hol2,G)
  ck(hol2==hol,'based_holonomy_invariance')
  central=lambda A:all(A[i][j]==0 for i,j in combinations(range(n),2) if (i,j)!=(0,n-1))
  ck(all(central(G) for G in transformed)==central(hol),'central_reduction_criterion')

# Concrete lower-holonomy and path-reversal controls.
A=word_matrix((1,2),2)
ck(A[0][2]==1 and A[0][1]==A[1][2]==1,'noncentral_lower_data_control')
ck(inv(A)[0][2]==0 and inv(A)[0][2]!=-A[0][2],'higher_entry_orientation_control')
B=word_matrix((1,2,-1,-2),2)
ck(B[0][1]==B[1][2]==0 and B[0][2]==1,'central_vanishing_lower_control')
print(json.dumps({'status':'PASS','exact_assertions':sum(C.values()),'groups':dict(sorted(C.items())),'exhaustive_words':word_count,'arithmetic':'exact integer matrices, cochains and sparse coefficients only','scope':'Finite matrix/cochain/Milnor-extraction controls. The relative acyclicity, integral existence/uniqueness and arbitrary triangulated-exterior arguments are written proofs. No embedded derived-link realization or full Polyak solution is certified.'},indent=2,sort_keys=True))
