#!/usr/bin/env python3
"""Exact small-frame controls for universally valid last-induction premises.
The universal semantic identities are proved in TURN_5.md; these checks
are neither completeness nor cut-free derivability certificates.
"""
import importlib.util,json
from pathlib import Path
from itertools import product
spec=importlib.util.spec_from_file_location('t1',Path(__file__).parents[1]/'turn1/proof_certificate.py');t=importlib.util.module_from_spec(spec);spec.loader.exec_module(t)
U,W,A,B=t.U,t.W,t.A,t.B
checks=0;models=0
def check(b):
 global checks
 assert b;checks+=1
def ev(a,R,lab,env=None):
 env={} if env is None else env;worlds=set(range(len(R)));tag=a[0]
 if tag=='lit':return set(lab) if a[2] else worlds-set(lab)
 if tag=='var':return env[a[1]]
 if tag=='and':return ev(a[1],R,lab,env)&ev(a[2],R,lab,env)
 if tag=='or':return ev(a[1],R,lab,env)|ev(a[2],R,lab,env)
 if tag=='box':
  z=ev(a[1],R,lab,env);return{u for u in worlds if set(R[u])<=z}
 if tag=='dia':
  z=ev(a[1],R,lab,env);return{u for u in worlds if set(R[u])&z}
 z=worlds if tag=='nu' else set()
 for _ in range(len(R)+1):
  zz=ev(a[2],R,lab,{**env,a[1]:z})
  if zz==z:return z
  z=zz
 raise AssertionError('positive fixed point not reached')
VA=t.V(A);FA=t.subst(U[2],U[1],A);GB=t.subst(W[2],W[1],B)
premises=[]
for f,C in [(U,{W}),(W,{U}),(U,{U,W}),(W,{U,W})]:premises.append(C|{t.subst(f[2],f[1],t.dual_context(C))})
for n in (1,2):
 edges=list(product(range(n),repeat=2))
 for mask in range(1<<len(edges)):
  R=[[] for _ in range(n)]
  for i,(u,v) in enumerate(edges):
   if mask>>i&1:R[u].append(v)
  for valuation in range(1<<n):
   lab={i for i in range(n) if valuation>>i&1};a=ev(A,R,lab);b=ev(B,R,lab)
   check(a|b==set(range(n)) and not a&b)
   check(ev(VA,R,lab)==b);check(ev(FA,R,lab)==a);check(ev(GB,R,lab)==b)
   check(ev(U,R,lab)==a);check(ev(W,R,lab)==b)
   for G in premises:
    truth=set()
    for f in G:truth|=ev(f,R,lab)
    check(truth==set(range(n)))
   models+=1
print(json.dumps({'status':'PASS','models':models,'exact_assertions':checks,'premises_checked_per_model':4,'scope':'Small-frame controls only. Universal standard-semantic identities are proved in TURN_5.md; no cut-free proof claim follows from validity.'},indent=2))
