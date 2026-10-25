#!/usr/bin/env python3
"""Manuscript-only graph/Fourier controls; no published code imported."""
from fractions import Fraction as F
from itertools import product, permutations
import json
import sympy as sp
checks=[]
def ck(s,b):
 assert b,s;checks.append(s)
def topo(edges):
 nodes=set(sum(([a,b] for a,b in edges),[])); indeg={v:sum(b==v for a,b in edges) for v in nodes};ready=[v for v in nodes if indeg[v]==0];order=[]
 while ready:
  v=ready.pop();order.append(v)
  for a,b in edges:
   if a==v:
    indeg[b]-=1
    if indeg[b]==0:ready.append(b)
 assert len(order)==len(nodes)
 return order

def tensor_terms(edges,labels):
 order=topo(edges);ret=sorted(v for v in order if sum(b==v for a,b in edges)==2);incoming={v:[i for i,(a,b) in enumerate(edges) if b==v] for v in ret};terms=[]
 for bits in product([0,1],repeat=len(ret)):
  omit={incoming[v][1-bit] for v,bit in zip(ret,bits)};selected=[(i,e) for i,e in enumerate(edges) if i not in omit];desc={v:(1<<labels[v] if v in labels else 0) for v in order}
  for v in reversed(order):
   for i,(a,b) in selected:
    if a==v:desc[v]|=desc[b]
  terms.append((bits,[(i,desc[b]) for i,(a,b) in selected]))
 return ret,terms

def value_grad(terms,g,params,inherit):
 total=F(0);grad=[F(0)]*(len(params)+len(inherit))
 for bits,elist in terms:
  indicators=[]
  for i,mask in elist:
   h=0
   for j,c in enumerate(g):
    if mask>>j&1:h^=c
   if h:indicators.append(i)
  mono=F(1)
  for i in indicators:mono*=params[i]
  weight=F(1)
  for k,bit in enumerate(bits):weight*=inherit[k] if bit==0 else 1-inherit[k]
  term=mono*weight;total+=term
  for i in indicators:grad[i]+=term/params[i]
  for k,bit in enumerate(bits):grad[len(params)+k]+=term/(inherit[k] if bit==0 else 1-inherit[k])*(1 if bit==0 else -1)
 return total,grad

def mixed(edges,ret,root):
 E=[];children=[b for a,b in edges if a==root]
 for a,b in edges:
  if a!=root:E.append((a,b,tuple([b] if b in ret else [])))
 a,b=children;E.append((a,b,tuple(v for v in (a,b) if v in ret)))
 return E

def classify_rootings(E,labels,ret):
 nodes={x for a,b,h in E for x in [a,b]};rows=[]
 for rootidx,(a,b,heads) in enumerate(E):
  choices=[]
  for i,(u,v,H) in enumerate(E):
   if i==rootidx:continue
   if len(H)==1:choices.append([(v,u)] if H[0]==u else [(u,v)])
   elif not H:choices.append([(u,v),(v,u)])
   else:choices.append([])
  for orientations in product(*choices):
   arcs=list(orientations)+[('ROOT',a),('ROOT',b)]
   try:order=topo(arcs)
   except AssertionError:continue
   valid=True
   for v in nodes:
    bi=(sum(y==v for x,y in arcs),sum(x==v for x,y in arcs))
    if bi!=((1,0) if v in labels else (2,1) if v in ret else (1,2)):valid=False;break
   if not valid:continue
   dom={'ROOT':{'ROOT'}}
   for v in order:
    if v=='ROOT':continue
    parents=[u for u,w in arcs if w==v]
    if not parents or any(u not in dom for u in parents):valid=False;break
    dom[v]={v}|set.intersection(*(dom[u] for u in parents))
   if not valid or set.intersection(*(dom[v] for v in labels))!={'ROOT'}:continue
   if set(heads)!={v for v in (a,b) if v in ret}:continue
   tc=all(any(w not in ret for u,w in arcs if u==v) for v in order if any(u==v for u,w in arcs))
   rows.append({'edge_index':rootidx,'tree_child':tc,'arcs':arcs})
 return rows
