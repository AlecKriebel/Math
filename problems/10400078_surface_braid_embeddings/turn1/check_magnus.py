#!/usr/bin/env python3
from itertools import product
import json,math
checks=0
def ck(x):
 global checks
 assert x;checks+=1

def mul(a,b,N):
 c={}
 for u,x in a.items():
  for v,y in b.items():
   w=u+v
   if len(w)<=N:c[w]=c.get(w,0)+x*y
 return {w:x for w,x in c.items() if x}
def binom(a,j):
 z=1
 for i in range(j):z=z*(a-i)//(i+1)
 return z
def power(i,a,N):return {(i,)*j:binom(a,j) for j in range(N+1) if binom(a,j)}
def expand(word,N):
 z={():1}
 for v in word:z=mul(z,power(abs(v)-1,1 if v>0 else -1,N),N)
 return z
words=0
for n in range(1,7):
 for w in product((1,-1,2,-2),repeat=n):
  if any(w[i]==-w[i-1] for i in range(1,n)):continue
  x=expand(w,n);ck(x!={():1});words+=1
  inv=tuple(-v for v in w[::-1]);ck(mul(x,expand(inv,n),n)=={():1})
syllables=0
for k in range(1,5):
 for first in (0,1):
  for exps in product((-2,-1,1,2),repeat=k):
   pat=tuple((first+i)%2 for i in range(k));z={():1}
   for i,a in zip(pat,exps):z=mul(z,power(i,a,k),k)
   ck(z.get(pat)==math.prod(exps));syllables+=1
# Torus group action: (u,v) shifts a chord label gamma by u-v.
vec=list(product(range(-1,2),repeat=2));actions=0
for u in vec:
 for v in vec:
  for gamma in vec:
   shifted=tuple(gamma[i]+u[i]-v[i] for i in range(2))
   restored=tuple(shifted[i]-u[i]+v[i] for i in range(2));ck(restored==gamma);actions+=1
   if u==v:ck(shifted==gamma)
print(json.dumps({'assertions':checks,'reduced_words_through_length6':words,'syllable_coefficients':syllables,'translation_actions':actions,'scope':'Finite controls for the classical Magnus coefficient proof and diagonal bead action; no full source resolution.'},indent=2))
