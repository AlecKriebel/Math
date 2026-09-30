#!/usr/bin/env python3
"""Finite exact monoid controls. No knot diagrams or isotopy tests are claimed."""
from itertools import product
from pathlib import Path
import hashlib,json
checks=0

def ck(condition):
 global checks
 assert condition
 checks+=1

def words(n):return [''.join(x) for x in product('ab',repeat=n)]

def common_root(u,v):
 if not u:return v,0,1
 if not v:return u,1,0
 if len(u)>len(v):
  w,n,m=common_root(v,u);return w,m,n
 assert v.startswith(u)
 w,m,k=common_root(u,v[len(u):]);return w,m,m+k

def all_common_roots(u,v):
 if not u and not v:return [('',0,0)]
 seed=u or v;out=[]
 for k in range(1,len(seed)+1):
  w=seed[:k]
  if len(u)%k==0 and len(v)%k==0 and w*(len(u)//k)==u and w*(len(v)//k)==v:
   out.append((w,len(u)//k,len(v)//k))
 return out

W=sum((words(n) for n in range(5)),[]);commuting=0
for u in W:
 for v in W:
  same=(u+v==v+u);roots=all_common_roots(u,v)
  ck(same==bool(roots))
  if same:
   commuting+=1;w,m,n=common_root(u,v)
   ck(w*m==u);ck(w*n==v);ck(m>=0 and n>=0)
   # Central classical coordinates do not affect a free-word commutator.
   for c,d in [(0,0),(0,2),(1,3)]:
    ck((c+d,u+v)==(d+c,v+u))

# Exact finite rewrite components for the homogeneous monoid presentation.
def neighbors(w):
 for i in range(len(w)-3):
  b=w[i:i+4]
  if b=='abba':yield w[:i]+'baab'+w[i+4:]
  if b=='baab':yield w[:i]+'abba'+w[i+4:]

def component(w):
 todo=[w];seen={w}
 while todo:
  x=todo.pop()
  for y in neighbors(x):
   ck(len(y)==len(w))
   if y not in seen:seen.add(y);todo.append(y)
 return seen

components={};total_words=0
for n in range(7):
 for w in words(n):
  total_words+=1;comp=component(w);components[w]=comp
  ck(w in comp)
  if n<4:ck(comp=={w})
  for x in comp:
   ck(x.count('a')==w.count('a'));ck(x.count('b')==w.count('b'))
ck(components['ab']=={'ab'});ck(components['ba']=={'ba'})
ck('baab' in components['abba']);ck('abba' in components['baab'])
# All ordered pairs of nonclassical atoms have distinct products.
for u in words(2):
 for v in words(2):ck((v in components[u])==(u==v))
# Any possible common root for X=ab and Y=ba has positive length dividing2.
# First coordinates of a proposed factorization must be zero by positivity.
for c in range(4):
 for qa in range(4):
  for qb in range(4):
   for w in words(1)+words(2):
    m=2//len(w);n=m
    if m*c+qa==0 and n*c+qb==0:
     ck(c==qa==qb==0)
     ck(not ('ab' in components[w*m] and 'ba' in components[w*n]))

r={'problem_id':10600021,'status':'PASS_FINITE_ALGEBRA_CONTROLS','assertions':checks,
 'free_word_pairs':len(W)**2,'commuting_word_pairs':commuting,'presentation_words_checked':total_words,
 'artifact_sha256':hashlib.sha256(Path(__file__).with_name('OBSTRUCTION.md').read_bytes()).hexdigest(),
 'verifier_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
 'scope':'Commuting free words and an abstract monoid countermodel only; no virtual-knot realization or complete geometric normal form is certified.'}
print(json.dumps(r,indent=2,sort_keys=True))
