#!/usr/bin/env python3
"""Exact integer and free-word controls for AIM Conjecture 3.4.
Bounded experiments are not an atoroidality or quasi-isometry algorithm.
"""
import json
from itertools import permutations
from pathlib import Path
PHI={'a':'b','b':'c','c':'ab','d':'ea','e':'ed'}
PSI={'a':'cA','b':'a','c':'b','d':'cADe','e':'daC'}
def inv(w):return w.swapcase()[::-1]
def red(w):
 s=[]
 for a in w:
  if s and s[-1]==a.swapcase():s.pop()
  else:s.append(a)
 return ''.join(s)
def sub(w,m=PHI):return red(''.join(m[a] if a.islower() else inv(m[a.lower()]) for a in w))
def cyc(w):
 w=red(w)
 while len(w)>1 and w[0]==w[-1].swapcase():w=w[1:-1]
 return w

def conjugacy_key(w):
 w=cyc(w)
 return min(w[i:]+w[:i] for i in range(len(w))) if w else ''
def mat(m,letters):return [[m[a].count(b)-m[a].count(b.upper()) for a in letters] for b in letters]
def mul(a,b):return [[sum(x*y for x,y in zip(row,col)) for col in zip(*b)] for row in a]
def identity(n):return [[int(i==j) for j in range(n)] for i in range(n)]
def mpow(a,n):
 b=identity(len(a))
 while n:
  if n&1:b=mul(b,a)
  a=mul(a,a);n//=2
 return b

def det(a):
 n=len(a);s=0
 for p in permutations(range(n)):
  sign=(-1)**sum(p[i]>p[j] for i in range(n) for j in range(i+1,n));v=sign
  for i in range(n):v*=a[i][p[i]]
  s+=v
 return s

def torsion(a,n):
 b=mpow(a,n);return abs(det([[b[i][j]-int(i==j) for j in range(len(a))] for i in range(len(a))]))

def verify_t1():
 a=mat(PHI,'abc');m=mat(PHI,'abcde');b=[[0,1],[1,1]]
 assert all(sub(sub(x,PSI),PHI)==x==sub(sub(x,PHI),PSI) for x in PHI)
 assert det(a)==1 and det(m)==-1
 rows=[]
 for n in range(1,21):
  t,u,v=torsion(a,n),torsion(m,n),torsion(b,n)
  assert t>0 and u==t*v and v>0
  rows.append({'n':n,'Gamma_torsion_order':t,'G_torsion_order':u,'ratio':v})
 # Polynomial evaluations at seven points certify the characteristic polynomials.
 for x in range(-3,4):
  char=lambda c:det([[int(i==j)*x-c[i][j] for j in range(len(c))] for i in range(len(c))])
  assert char(a)==x**3-x-1
  assert char(m)==(x**3-x-1)*(x**2-x-1)
 return {'matrices':{'lower':a,'full':m,'quotient':b},'cyclic_cover_torsion':rows}
if __name__=='__main__':
 print(json.dumps({'turn1':verify_t1()},indent=2,sort_keys=True))
