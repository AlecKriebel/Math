"""Finite convention checks; not a computational proof of Baire or root theory."""
from fractions import Fraction as Q
from collections import Counter
import json
C=Counter()
def ck(b,k):
 assert b,k
 C[k]+=1
def zeros(n):return [[Q(0) for j in range(n)] for i in range(n)]
def unit(n,i,j):
 a=zeros(n);a[i][j]=Q(1);return a
def add(a,b):return [[x+y for x,y in zip(r,s)] for r,s in zip(a,b)]
def scale(a,c):return [[x*c for x in r] for r in a]
def mul(a,b):
 n=len(a);return [[sum(a[i][k]*b[k][j] for k in range(n)) for j in range(n)] for i in range(n)]
def bracket(a,b):return add(mul(a,b),scale(mul(b,a),-1))
for n in range(2,9):
 lam=[Q(1,2**i) for i in range(1,n+1)];mean=sum(lam)/n;lam=[v-mean for v in lam]
 D=zeros(n)
 for i in range(n):D[i][i]=lam[i]
 ck(sum(lam)==0,'trace_zero_model')
 for i in range(n):
  for j in range(n):
   E=unit(n,i,j);ck(bracket(D,E)==scale(E,lam[i]-lam[j]),'adjoint_root_eigenvalue')
   ck((lam[i]==lam[j])==(i==j),'regular_diagonal_separation')
 A=[[Q((i+2)*(j+3)+i-j,7) for j in range(n)] for i in range(n)]
 for i in range(n):
  for j in range(n):
   if i==j:continue
   Pi=unit(n,i,i);Pj=unit(n,j,j);B=bracket(Pi,bracket(A,Pj))
   ck(scale(add(B,bracket(Pi,B)),Q(1,2))==scale(unit(n,i,j),A[i][j]),'ideal_matrix_unit_extraction')
   ck(bracket(unit(n,i,j),unit(n,j,i))==add(Pi,scale(Pj,-1)),'ideal_diagonal_difference')
for n in range(1,501):
 ck(n*Q(1,n)**2==Q(1,n),'trace_zero_approximation_HS_error_squared')
for rank in range(1,31):
 lam=[Q(1,2**i) for i in range(1,rank+1)]
 for i in range(rank):
  ck(lam[i]!=0 and 2*lam[i]!=0,'B_C_single_roots_nonzero')
  for j in range(i+1,rank):
   ck(lam[i]-lam[j]!=0 and lam[i]+lam[j]!=0,'B_C_D_pair_roots_nonzero')
print(json.dumps({'status':'PASS','exact_assertions':sum(C.values()),'counts':dict(sorted(C.items())),'scope':'Finite adjoint/root and matrix-ideal identities plus norm arithmetic. Infinite-dimensional root decomposition and Baire arguments are analytic proofs in PROOF.md, not conclusions of these finite tests.'},indent=2,sort_keys=True))
