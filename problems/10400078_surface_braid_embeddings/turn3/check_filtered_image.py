#!/usr/bin/env python3
import json,sys,itertools,contextlib,io
from pathlib import Path
from fractions import Fraction
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'turn2'))
with contextlib.redirect_stdout(io.StringIO()):
 from check_lattice_embedding import path
# Imported turn2 controls replay silently; they are not counted again.
checks=0
def ck(x):
 global checks
 assert x;checks+=1

def red(w):
 z=[]
 for a in w:
  if z and z[-1]==-a:z.pop()
  else:z.append(a)
 return z
def pw(a,n):return [a if n>=0 else -a]*abs(n)
def inv(w):return [-a for a in w[::-1]]
def r(i,j):return red(pw(2,j)+pw(1,i)+[2]+pw(1,-i)+pw(2,-j-1))
def q(i,j):return red(pw(2,j)+pw(1,i)+[1,2,-1,-2]+pw(1,-i)+pw(2,-j))
for i,j in itertools.product(range(-4,5),repeat=2):
 ck(q(i,j)==red(r(i+1,j)+inv(r(i,j))))
 l,h=path(q(i,j));v={}
 for g,s in l:v[g]=v.get(g,0)+s
 v={g:s for g,s in v.items() if s};ck(h==(0,0));ck(v=={(-i-1,-j):1,(-i,-j):-1})
 # Explicit finite inverse basis transformation, for positive and negative columns.
 rr=[]
 if i>0:
  for a in range(i-1,-1,-1):rr+=q(a,j)
 elif i<0:
  for a in range(i,0):rr+=inv(q(a,j))
 ck(red(rr)==r(i,j))

def rank(M):
 M=[list(map(Fraction,r)) for r in M];rr=0
 for c in range(len(M[0]) if M else 0):
  piv=next((i for i in range(rr,len(M)) if M[i][c]),None)
  if piv is None:continue
  M[rr],M[piv]=M[piv],M[rr];z=M[rr][c];M[rr]=[x/z for x in M[rr]]
  for i in range(len(M)):
   if i!=rr and M[i][c]:z=M[i][c];M[i]=[x-z*y for x,y in zip(M[i],M[rr])]
  rr+=1
 return rr
ranks=[]
for width in range(1,7):
 for rows in range(1,4):
  M=[[0]*(width*rows) for _ in range((width+1)*rows)]
  for j in range(rows):
   for i in range(width):M[j*(width+1)+i][j*width+i]=-1;M[j*(width+1)+i+1][j*width+i]=1
  rk=rank(M);ck(rk==width*rows);ck(all(sum(M[j*(width+1)+i][c] for i in range(width+1))==0 for j in range(rows) for c in range(width*rows)));ranks.append([width,rows,rk])
print(json.dumps({'assertions':checks,'grid_face_indices':81,'difference_rank_checks':ranks,'scope':'Finite checks of exact free-word basis transformations and first-order differences; the all-degree tensor proof is analytic.'},indent=2))
