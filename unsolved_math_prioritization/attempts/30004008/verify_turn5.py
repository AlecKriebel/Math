"""Exact determinant and polynomial route controls. Stdlib only."""
import itertools as it,json,random
from verify_turn1 import arb,trees
N=0
def check(x):
 global N
 N+=1
 assert x

def det(M):
 n=len(M)
 if n==0:return 1
 A=[row[:] for row in M];sgn=1;prev=1
 for k in range(n-1):
  if A[k][k]==0:
   j=next((j for j in range(k+1,n) if A[j][k]),None)
   if j is None:return 0
   A[k],A[j]=A[j],A[k];sgn=-sgn
  pivot=A[k][k]
  for i in range(k+1,n):
   for j in range(k+1,n):
    z=A[i][j]*pivot-A[i][k]*A[k][j];check(z%prev==0);A[i][j]=z//prev
  for i in range(k+1,n):A[i][k]=0
  prev=pivot
 return sgn*A[-1][-1]

def count(n,A,S):
 L=[[0]*n for _ in range(n)]
 for c in S:
  for u,v in A[c]:L[v][v]+=1;L[v][u]-=1
 return sum(det([[L[u][v] for v in range(n) if v!=r] for u in range(n) if u!=r]) for r in range(n))

def ie(n,A):
 q=len(A);ans=0
 for bits in range(1<<q):
  S=[j for j in range(q) if bits>>j&1];x=count(n,A,S);check(x>=0);ans+=(-1)**(q-len(S))*x
 return ans

def direct(n,A):return sum(arb(set(range(n)),E) for E in it.product(*A))

def random_tree(n,rng):
 order=list(range(n));rng.shuffle(order);return tuple((order[rng.randrange(j)],order[j]) for j in range(1,n))

def mul(z,w):return(z[0]*w[0]-z[1]*w[1],z[0]*w[1]+z[1]*w[0])
def add(*zs):return tuple(sum(z[j] for z in zs) for j in range(2))

def main():
 small=0;randoms=0
 for n in [2,3]:
  ts=trees(n)
  for ix in it.combinations_with_replacement(range(len(ts)),n-1):
   A=[ts[j] for j in ix];x=ie(n,A);check(x==direct(n,A));check(x>0);small+=1
 rng=random.Random(300040085)
 for n in range(4,7):
  for rep in range(80):
   A=[random_tree(n,rng) for _ in range(n-1)];check(all(arb(set(range(n)),T) for T in A));x=ie(n,A);check(x==direct(n,A));check(x>0);randoms+=1
 A=[[(0,1),(1,2)],[(2,1),(1,0)]];arcs=[(0,1),(1,2),(2,1),(1,0)];basis=[ij for ij in it.combinations(range(4),2) if arb({0,1,2},[arcs[i] for i in ij])]
 check(basis==[(0,1),(1,3),(2,3)]);check(ie(3,A)==1)
 check(not arb({0,1,2},[arcs[0],arcs[2]]));check(not arb({0,1,2},[arcs[0],arcs[3]]))
 z=[(2,1),(1,1),(-2,1),(-1,1)];check(all(y>0 for x,y in z));check(add(*(mul(z[i],z[j]) for i,j in basis))==(0,0))
 # Coarsened polynomial x²+xy+y² verified as an exact exponent dictionary.
 co={}
 for i,j in basis:
  a=int(i<2)+int(j<2);co[(a,2-a)]=co.get((a,2-a),0)+1
 check(co=={(2,0):1,(1,1):1,(0,2):1})
 # For x=sqrt(3)+i, y=-sqrt(3)+i: xy=-4 and (x+y)^2=-4.
 check(-3-1==-4);check(mul((0,2),(0,2))==(-4,0))
 # Determinant controls include zero and nonzero minors, row pivot swaps and n=0.
 check(ie(1,[])==1);check(direct(1,[])==1);check(det([])==1);check(det([[0,1],[1,0]])==-1);check(det([[1,2],[2,4]])==0)
 print(json.dumps({'problem_id':30004008,'turn':5,'status':'PASS','exact_assertions':N,'exhaustive_small_color_multisets':small,'random_original_instances_n4_to_n6':randoms,'integer_matrix_tree_IE_equals_direct_counts':True,'explicit_upper_half_plane_zero':True,'basis_exchange_failure':True,'coarsened_polynomial':'x^2+x*y+y^2','scope':'Exact finite algebraic controls and explicit obstruction to the stability/matroid shortcut; original all-n conjecture unresolved.'},indent=2))
if __name__=='__main__':main()
