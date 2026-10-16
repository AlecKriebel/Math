#!/usr/bin/env python3
from fractions import Fraction as Q
from itertools import product,combinations
from math import comb,prod,lcm
import json
C={}
def ck(x,s):
 assert x,s
 C[s]=C.get(s,0)+1
pairs=list(combinations(range(4),2))
matchings=[{(0,1),(2,3)},{(0,2),(1,3)},{(0,3),(1,2)}]

def c4(weights,A):
 n=len(weights);total=Q(0)
 for I in product(range(n),repeat=4):
  wt=prod(weights[i] for i in I)
  for M in matchings:
   z=wt
   for u,v in pairs:z*=1-A[I[u]][I[v]] if (u,v) in M else A[I[u]][I[v]]
   total+=z
 return total

def c4_integer(weights,A):
 D=lcm(*(a.denominator for a in weights));m=[int(a*D) for a in weights];total=0
 for I in product(range(len(m)),repeat=4):
  if all(sum(A[I[i]][I[j]] for j in range(4) if j!=i)==2 for i in range(4)):
   total+=prod(m[i] for i in I)
 return Q(total,D**4)

def edge(weights,A):return sum(weights[i]*weights[j]*A[i][j] for i,j in product(range(len(weights)),repeat=2))
def conditional(weights,A,i,j):
 z=Q(0)
 for k,l in product(range(len(weights)),repeat=2):
  I=[i,j,k,l];out=[]
  for edge01 in (0,1):
   deg=[0]*4
   for u,v in pairs:
    e=edge01 if (u,v)==(0,1) else A[I[u]][I[v]]
    deg[u]+=e;deg[v]+=e
   out.append(int(all(d==2 for d in deg)))
  z+=weights[k]*weights[l]*(out[1]-out[0])
 return z
ck(3*sum(comb(6,k) for k in range(2,7))==171,'remainder_term_count')
perturbations=0
for r in (2,3,4):
 for ratio in (Q(1,3),Q(1,2),Q(3,4)):
  a=1/(r+ratio);b=ratio*a;w=[a]*r+[b];m=len(w);q=sum(z*z for z in w)
  A=[[int(i!=j) for j in range(m)] for i in range(m)]
  K=[[conditional(w,A,i,j) for j in range(m)] for i in range(m)]
  for i,j in product(range(m),repeat=2):
   ck(K[i][j]==(-(q-w[i]*w[i]) if i==j else (w[i]+w[j])**2-q),'conditional_kernel_direct')
  gamma=b*(2*a+b)
  ck(max(K[i][i] for i in range(m))-min(K[i][j] for i in range(m) for j in range(i+1,m))==-gamma,'exact_slope_gap')
  c0=c4_integer(w,A);ck(c0==3*(q*q-sum(z**4 for z in w)),'baseline_count')
  for inside,uv in [(0,(0,r)),(r,(0,r)),(0,(0,1)),(r,(0,1))]:
   u,v=uv;plus=2*w[u]*w[v];minus=w[inside]**2
   tau=gamma/(228*max(plus,minus));H=[[Q(0)]*m for _ in range(m)]
   H[inside][inside]=tau*plus;H[u][v]=H[v][u]=-tau*minus
   B=[[A[i][j]+H[i][j] for j in range(m)] for i in range(m)]
   T=sum(w[i]*w[j]*abs(H[i][j]) for i,j in product(range(m),repeat=2))
   eta=max(abs(z) for row in H for z in row)
   D=6*sum(w[i]*w[j]*H[i][j]*K[i][j] for i,j in product(range(m),repeat=2))
   c1=c4(w,B);R=c1-c0-D
   ck(edge(w,B)==edge(w,A),'fractional_density_preservation')
   ck(all(0<=z<=1 for row in B for z in row),'fractional_admissibility')
   ck(eta<=gamma/114,'local_radius')
   ck(D<=-3*gamma*T,'linear_term_bound')
   ck(abs(R)<=171*eta*T,'exact_remainder_bound')
   ck(c1<=c0-Q(3,2)*gamma*T<c0,'strict_local_drop')
   perturbations+=1

paths=0
for r in (2,3,4):
 a=Q(2,2*r+1);b=Q(1,2*r+1);gamma=b*(2*a+b);q=r*a*a+b*b
 previous=None
 for den in (2,3,5,10,20):
  s=(a-b)/den;u=a-s;e=b*s/u;z=s-e
  # Remaining large parts, then U,E,Z,B. Original types U/E/Z all belong to A.
  w=[a]*(r-1)+[u,e,z,b];m=len(w);U,E,Z,B=r-1,r,r+1,r+2
  oldtypes=list(range(r-1))+[r-1]*3+[r]
  oldmass=[a]*r+[b]
  A0=[[int(oldtypes[i]!=oldtypes[j]) for j in range(m)] for i in range(m)]
  A1=[[int(i!=j and (i<r-1 or j<r-1 or (i==U and j in(E,B)) or (j==U and i in(E,B)))) for j in range(m)] for i in range(m)]
  H=[[A1[i][j]-A0[i][j] for j in range(m)] for i in range(m)]
  K=[[(-(q-oldmass[oldtypes[i]]**2) if oldtypes[i]==oldtypes[j] else (oldmass[oldtypes[i]]+oldmass[oldtypes[j]])**2-q) for j in range(m)] for i in range(m)]
  T=sum(w[i]*w[j]*abs(H[i][j]) for i,j in product(range(m),repeat=2))
  D=6*sum(w[i]*w[j]*H[i][j]*K[i][j] for i,j in product(range(m),repeat=2))
  delta=c4_integer(w,A1)-c4_integer(w,A0)
  ck(sum(w)==1 and min(w)>0,'tying_path_masses')
  ck(edge(w,A1)==edge(w,A0),'tying_path_edge_count')
  ck(delta==0,'tying_path_c4_direct_count')
  ck(T==4*b*s>0,'tying_path_L1')
  ck(max(abs(h) for row in H for h in row)==1,'tying_path_Linfinity')
  ck(D==-3*gamma*T==-12*b*b*s*(2*a+b),'tying_path_linear_term')
  ck(delta-D==3*gamma*T,'nonvanishing_L1_remainder_ratio')
  if previous is not None:ck(T<previous,'decreasing_edit_distance')
  previous=T;paths+=1
print(json.dumps({'assertions':sum(C.values()),'by_scope':C,
 'arithmetic':'exact fractions and integer weighted motif counts; no floating-point tests',
 'fractional_perturbations':perturbations,'exact_tying_paths':paths,
 'scope':'The local theorem is L-infinity small-amplitude only; exact L1 tying paths prevent an edit-distance uniqueness inference.'},indent=2)+'\n',end='')
