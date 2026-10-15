#!/usr/bin/env python3
"""Fresh tensor/word/matrix controls; no candidate code is imported."""
import hashlib,itertools,json,sys
from collections import defaultdict
import sympy as s

def need(c,m):
 if not c:raise ValueError(m)
checks=[]
def record(n,c):need(c,n);checks.append(n)
def add(a,b,sign=1):
 z=defaultdict(int,a)
 for m,c in b.items():z[m]+=sign*c
 return {m:c for m,c in z.items()if c}
def mul(a,b,cap=6):
 z=defaultdict(int)
 for u,c in a.items():
  for v,d in b.items():
   if len(u+v)<=cap:z[u+v]+=c*d
 return {m:c for m,c in z.items()if c}
def bracket(a,b):return add(mul(a,b),mul(b,a),-1)
X,Y,Z=[{(i,):1} for i in [1,2,3]];one={():1}
P=bracket(bracket(bracket(X,Y),bracket(X,Z)),X)
Q=bracket(bracket(bracket(X,Y),bracket(X,bracket(X,Y))),X)
record('P_integer_coefficient_11213_minus1',P.get((1,1,2,1,3))==-1)
record('Q_integer_coefficient_111212_plus1',Q.get((1,1,1,2,1,2))==1)
record('P_Q_homogeneous_degrees',all(len(x)==5 for x in P)and all(len(x)==6 for x in Q))
def red(w):
 z=[]
 for x in w:
  if z and z[-1]==-x:z.pop()
  else:z.append(x)
 return tuple(z)
def inv(w):return tuple(-x for x in reversed(w))
def comm(u,v):return red(u+v+inv(u)+inv(v))
a,b,c=(1,),(2,),(3,)
w=comm(comm(comm(a,b),comm(a,c)),a)
v=comm(comm(comm(a,b),comm(a,comm(a,b))),a)
def magnus(word,cap):
 out=one
 for t in word:
  f={():1,(abs(t),):1}if t>0 else{(abs(t),)*j:(-1)**j for j in range(cap+1)}
  out=mul(out,f,cap)
 return add(out,one,-1)
record('direct_Magnus_w_through5_exact_P',magnus(w,5)==P)
record('direct_Magnus_v_through6_exact_Q',magnus(v,6)==Q)
def subst(word,t,u):
 out=()
 for x in word:
  r=red((t,)+u)if abs(x)==t else(abs(x),)
  out+=r if x>0 else inv(r)
 return red(out)
for u,t,n in [(w,4,4),(v,3,3)]:
 record('spare_generator_%s_both_compositions'%t,all(subst(subst((i,),t,u),t,inv(u))==(i,) and subst(subst((i,),t,inv(u)),t,u)==(i,) for i in range(1,n+1)))
def mm(A,B):
 n=len(A);return tuple(tuple(sum(A[i][k]*B[k][j]for k in range(n))for j in range(n))for i in range(n))
def ma(A,B,sign=1):return tuple(tuple(x+sign*y for x,y in zip(a,b))for a,b in zip(A,B))
def eye(n):return tuple(tuple(int(i==j)for j in range(n))for i in range(n))
def mi(A):
 n=len(A);I=eye(n);N=ma(A,I,-1);term=I;out=I
 for d in range(1,n):term=mm(term,N);out=ma(out,term,(-1)**d)
 need(mm(out,A)==I,'inverse');return out
def ew(word, mats):
 out=eye(len(next(iter(mats.values()))))
 for x in word:out=mm(out,mats[x]if x>0 else mi(mats[-x]))
 return out
def pathmat(colors,j):
 d=len(colors)+1;I=eye(d);return tuple(tuple(I[r][c]+int(c==r+1 and colors[r]==j)for c in range(d))for r in range(d))
count=0
for word,alphabet,degree,poly in [(w,3,5,P),(v,2,6,Q)]:
 for d in range(1,degree+1):
  for colors in itertools.product(range(1,alphabet+1),repeat=d):
   M=ew(word,{j:pathmat(colors,j)for j in range(1,alphabet+1)})
   need(M[0][d]==poly.get(colors,0),'integral color coefficient '+str(colors));count+=1
record('489_all_colors_all_degrees_match_integer_polynomials',count==489)
def sparse(n,entries):
 z=[list(x)for x in eye(n)]
 for r,c in entries:z[r-1][c-1]+=1
 return tuple(tuple(x)for x in z)
M=ew(w,{1:sparse(6,[(1,2),(2,3),(4,5)]),2:sparse(6,[(3,4)]),3:sparse(6,[(5,6)])})
N=ew(v,{1:sparse(7,[(1,2),(2,3),(3,4),(5,6)]),2:sparse(7,[(4,5),(6,7)])})
record('paper_UT6_certificate_minus_E16',M==ma(eye(6),tuple(tuple(int(i==0 and j==5)for j in range(6))for i in range(6)),-1))
record('paper_UT7_certificate_plus_E17',N==sparse(7,[(1,7)]))
def B(A,C):return A*C-C*A
AA,BB,CC=[s.Matrix(2,2,s.symbols('%s0:4'%name))for name in ['a','b','c']]
record('generic_2x2_polynomial_P_zero',all(s.expand(t)==0 for t in B(B(B(AA,BB),B(AA,CC)),AA)))
record('generic_2x2_polynomial_Q_zero',all(s.expand(t)==0 for t in B(B(B(AA,BB),B(AA,B(AA,BB))),AA)))
# Detect the false extension to arbitrary 3x3 matrices.
E=lambda i,j:s.eye(3)[:,i]*s.eye(3)[j,:]
A=s.diag(0,1,2);C=E(0,1);D=E(1,2)
nonzero={'X':[[0,0,0],[0,1,0],[0,0,2]],'Y':'E12','Z':'E23','P':'2E13'} if B(B(B(A,C),B(A,D)),A)==2*E(0,2) else None
record('reject_unclaimed_3x3_extension',nonzero is not None)
# Cayley-Hamilton involves no division: exhaust all 2x2 matrices over F2.
matrices=[s.Matrix(2,2,x)for x in itertools.product(range(2),repeat=4)]
record('4096_characteristic2_specializations',all(all(int(z)%2==0 for z in B(B(B(A,C),B(A,D)),A))for A,C,D in itertools.product(matrices,repeat=3)))
record('pinned_sympy',s.__version__=='1.14.0')
print(json.dumps({'schema':'pr681-round3-independent-math-controls-v1','status':'PASS','check_count':len(checks),'checks':checks,'colored_path_count':count,'P_support':len(P),'Q_support':len(Q),'unclaimed_3x3_counterexample':nonzero,'candidate_code_imported':False,'sympy_version':s.__version__},indent=2,sort_keys=True))
