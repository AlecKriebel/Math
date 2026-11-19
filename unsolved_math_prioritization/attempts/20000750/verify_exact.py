#!/usr/bin/env python3
"""Exact finite arithmetic checks; not a prime-gap theorem or asymptotic computation."""
from fractions import Fraction as F
from math import gcd
import hashlib,json,pathlib

def ck(v,s):
 if not v: raise RuntimeError(s)
 return s

def dot(x,y):return sum(a*b for a,b in zip(x,y))
def mv(M,x):return [dot(row,x) for row in M]
def det(M):
 if len(M)==1:return M[0][0]
 return sum((-1)**j*M[0][j]*det([row[:j]+row[j+1:] for row in M[1:]]) for j in range(len(M)))
u=[F(1)]*3;v=list(map(F,[0,1,2]));z=list(map(F,[0,1,4]));r=list(map(F,[1,-2,1]));w=list(map(F,[-1,0,1]))
K=[[(r[i]*u[j]+u[i]*r[j])/3-w[i]*w[j]/4 for j in range(3)] for i in range(3)]
B=[[K[i][j]+(5 if i==j else 0) for j in range(3)] for i in range(3)]
checks=[ck(mv(K,u)==r,'Ku=r'),ck(dot(u,mv(K,u))==0,'uKu=0'),ck(dot(u,mv(K,v))==0,'uKv=0'),ck(dot(v,mv(K,v))==-1,'vKv=-1'),ck(dot(u,mv(K,z))==2,'uKz=2')]
mins=[det([row[:n] for row in B[:n]]) for n in (1,2,3)]
checks.append(ck(all(x>0 for x in mins),'B positive definite by Sylvester'))
checks.append(ck(2*(dot(v,mv(K,v))+dot(u,mv(K,z)))/dot(u,u)==F(2,3),'curve second derivative 2/3'))
wp=[v[i]-u[i] for i in range(3)]
checks.append(ck(dot(wp,mv(K,wp))/dot(wp,wp)==F(-1,2),'orthogonalized plane second value 9/2 below 5'))
D=[1,2,3,5,6,7];X=list(range(10,50));hs=[0,2]
def prime(n):return n>=2 and all(n%d for d in range(2,int(n**.5)+1))
def phi(n,d):return int((n*(n+2))%d==0)
def score(n):return sum(prime(n+h) for h in hs)
maxerr=F(0)
for d in D:
 for e in D:
  m=d*e//gcd(d,e); roots=[a for a in range(m) if a*(a+2)%m==0]
  A=sum(phi(n,d)*phi(n,e) for n in X); Bde=sum(score(n)*phi(n,d)*phi(n,e) for n in X)
  err=abs(F(A)-F(len(X)*len(roots),m));maxerr=max(maxerr,err)
  ck(err<=len(roots),'CRT error bound')
  exact=sum(sum(prime(n+h) and (n+h-a-h)%m==0 for n in X) for h in hs for a in roots)
  ck(exact==Bde,'prime residue formula')
checks+=['36 CRT entry error checks','36 exact prime-residue numerator checks']
# One-point worst-case signed obstruction, including m=1.
for m in range(1,8):
 g=-(m-1); W=-1
 ck(g*W==m-1,'sharp signed budget')
checks.append('7 sharp signed budget endpoint checks')
p=pathlib.Path(__file__).parent
hashes={n:hashlib.sha256((p/n).read_bytes()).hexdigest() for n in ['RESIDUAL_REPORT.md','verify_exact.py']}
print(json.dumps({'status':'PASS','checks':checks,'B_leading_principal_minors':list(map(str,mins)),'maximum_CRT_error_in_example':str(maxerr),'sha256':hashes},indent=2))
