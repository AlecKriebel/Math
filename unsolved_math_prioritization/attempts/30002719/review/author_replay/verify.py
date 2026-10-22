#!/usr/bin/env python3
"""Exact finite controls only; the proof supplies all infinite quantifiers."""
from fractions import Fraction as Q
from math import comb, factorial
from pathlib import Path
import hashlib, json

checks=0
def check(condition):
 global checks
 assert condition
 checks+=1

def mul(a,b,limit=None):
 size=len(a)+len(b)-1
 if limit is not None:size=min(size,limit+1)
 c=[Q(0)]*size
 for i,x in enumerate(a):
  for j,y in enumerate(b):
   if i+j<size:c[i+j]+=x*y
 return c

def power(a,n,limit):
 out=[Q(1)]
 for _ in range(n):out=mul(out,a,limit)
 return out+[Q(0)]*(limit+1-len(out))

def fracpower(a,s,limit):
 b=[Q(1)]
 for j in range(1,limit+1):
  b.append(sum(((s+1)*i-j)*a[i]*b[j-i]
               for i in range(1,min(j,len(a)-1)+1))/j)
 return b

C=[[],[1]];A=[[],[Q(1)]];Gs={};screen={}
for n in range(2,17):
 degree=n*(n-1)//2
 p=[0]*(degree+1);p[degree]=1
 for k in range(1,n):
  shift=(n-k)*(n-k-1)//2
  for i,v in enumerate(C[k]):p[i+shift]-=comb(n-1,k-1)*v
 C.append(p)
 a=[Q((-1)**(n-1)*v,factorial(n-1)) for v in p];A.append(a)
 check(a[0]==1);check(sum(a)==0)
 # Independent Newton power-sum recurrence, with e_j=y^(j choose 2)/j!.
 newton=[Q(0)]*(degree+1);newton[degree]=Q((-1)**(n-1)*n,factorial(n))
 for k in range(1,n):
  shift=k*(k-1)//2
  for i,v in enumerate(A[n-k]):newton[i+shift]+=Q((-1)**(k-1),factorial(k))*v
 check(a==newton)
 b=fracpower(a,Q(1,n),160);g=fracpower(a,Q(-1,n),8);Gs[n]=g
 for value in b[1:]:check(value<0)
 screen[str(n)]={'degrees':160,'strictly_positive_F_coefficients':160}
 check(power(b,n,8)==(a+[Q(0)]*9)[:9])
 check(mul(b[:9],g,8)==[Q(1)]+[Q(0)]*8)
 # The exact unit-root order follows from the connected-graph factor.
 t=p[:]
 for _ in range(n-1):
  quotient=[0]*(len(t)-1);quotient[-1]=t[-1]
  for j in range(len(quotient)-2,-1,-1):quotient[j]=t[j+1]+quotient[j+1]
  check(t[0]==-quotient[0]);t=quotient
 check(sum(t)==n**(n-2))

# Independent exhaustive graph counts, at most 1024 graphs for one n.
graphs_checked=0
for n in range(2,6):
 edges=[(i,j) for i in range(n) for j in range(i+1,n)]
 counts=[0]*(len(edges)+1)
 for mask in range(1<<len(edges)):
  graphs_checked+=1;adj=[set() for _ in range(n)]
  for k,(i,j) in enumerate(edges):
   if mask>>k&1:adj[i].add(j);adj[j].add(i)
  reached={0};front=[0]
  while front:
   i=front.pop()
   for j in adj[i]-reached:reached.add(j);front.append(j)
  if len(reached)==n:counts[mask.bit_count()]+=1
 shifted=[sum(counts[j]*comb(j,k)*(-1)**(j-k) for j in range(k,len(counts))) for k in range(len(counts))]
 check(shifted==C[n]);check(counts[n-1]==n**(n-2))
 for k in range(n-1):check(counts[k]==0)

stable=list(map(Q,['1','1/2','1/2','11/24','11/24','7/16','7/16','493/1152','163/384']))
U=stable
res=[Q(1)-U[0]]+[-u for u in U[1:]]
for j in (2,3,4):
 shift=j*(j-1)//2
 for k,v in enumerate(power(U,j,8-shift)):res[k+shift]+=Q((-1)**j,factorial(j))*v
check(res==[Q(0)]*9)
for n in range(9,17):check(Gs[n]==stable)

q=[-1,132,-108,-264,240]
expected={4:Q(-25059,32),5:Q(-1016,5),6:Q(-153,2),7:Q(-2070,7),8:Q(-2265,8),9:Q(-255)}
certificate={}
for n,value in expected.items():
 g=Gs[n];form=sum(Q(q[i]*q[j])*g[i+j] for i in range(5) for j in range(5))
 check(form==value);check(form<0)
 certificate[str(n) if n<9 else 'n>=9']={'g_0_to_8':[str(x) for x in g],'quadratic_form':str(form)}
check(Gs[3][1]*Gs[3][3]-Gs[3][2]**2==Q(-1,24))
for n in range(4,17):check(Gs[n][1]*Gs[n][3]-Gs[n][2]**2==Q(-1,48))
# n=2 Sibuya coefficient formula and a finite-state-return positive control.
b=fracpower(A[2],Q(1,2),64)
for k in range(1,65):check(-b[k]==Q(comb(2*k,k),(2*k-1)*4**k))
# Two-state reversible flip: return PGF y^2, moments 1,0,1,0,...
g=[Q(int(k%2==0)) for k in range(9)]
check(sum(Q(q[i]*q[j])*g[i+j] for i in range(5) for j in range(5))==Q(sum(q[::2])**2+sum(q[1::2])**2))

receipt={'problem_id':30002719,'status':'PASS_FINITE_EXACT_CONTROLS','assertions':checks,
 'graphs_enumerated':graphs_checked,'coefficient_screen':screen,'return_obstruction':certificate,
 'scope':'Finite algebra only; infinite n uses credited coefficient stabilization and the formal root identity.',
 'original_target':'unsolved','proof_sha256':hashlib.sha256(Path(__file__).with_name('OBSTRUCTION.md').read_bytes()).hexdigest(),
 'verifier_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
print(json.dumps(receipt,indent=2,sort_keys=True))
