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
E=[('U','V'),('U','P0'),('P0','P1'),('P1','V'),('S','U'),('S','X'),('V','P4'),('P4','X'),('P0','L0'),('P1','L1'),('P4','L2'),('X','L3')]
Ls={f'L{i}':i for i in range(4)};Lt={f'L{i}':j for i,j in enumerate([1,0,3,2])}
ret,Ts=tensor_terms(E,Ls);rt,Tt=tensor_terms(E,Lt);ck('Omega reticulations V,X',ret==rt==['V','X'])
src=list(map(F,['1/2','1/4','1/2','1/2','1/2','1/2','1/2','1/20','1/2','1/2','1/10','1/2']))
tgt=list(map(F,['7/12','1/7','1/2','41/48','28/41','1/2','1/2','12/205','1/2','1/2','3/40','1/2']))
ck('both exact Omega parameter points strict',all(0<x<1 for x in src+tgt));I=[F(1,2)]*2
coords=list(product(range(4),repeat=4));vals={}
for g in coords:
 h=0
 for a in g:h^=a
 if h:vs=vt=F(0)
 else:vs,_=value_grad(Ts,g,src,I);vt,_=value_grad(Tt,g,tgt,I)
 ck('Omega Fourier '+str(g),vs==vt);vals[g]=vs
rows=[(0,0,1,1),(0,1,0,1),(0,1,1,0),(0,1,2,3),(1,0,0,1),(1,0,1,0),(1,0,2,3),(1,1,0,0),(1,1,1,1),(1,1,2,2),(1,2,0,3),(1,2,1,2),(1,2,2,1),(1,2,3,0)]
ranks=[];dets=[]
for T,params in [(Ts,src),(Tt,tgt)]:
 J=sp.Matrix([[sp.Rational(x.numerator,x.denominator) for x in value_grad(T,g,params,I)[1]] for g in rows]);ranks.append(J.rank());rr=list(range(8))+[9];cc=[0,1,2,3,4,7,8,9,10];dets.append(str(J.extract(rr,cc).det()))
ck('complete Omega local Jacobian ranks9',ranks==[9,9]);ck('printed displayed rank minors',dets==['-171/2305843009213693952000000','-513/9223372036854775808000000'])
patterns=[]
for states in coords:
 total=F(0)
 for g,v in vals.items():
  parity=sum((a&b).bit_count() for a,b in zip(g,states))%2;total+=(-1 if parity else 1)*v
 patterns.append(total/256)
ck('all256 pattern probabilities positive and normalized',min(patterns)>0 and sum(patterns)==1)
ck('printed minimum pattern probability',min(patterns)==F(87763,26214400))
M=mixed(E,set(ret),'S');rootings=classify_rootings(M,Ls,set(ret));ck('all admissible Omega rootings seven',len(rootings)==7);ck('exactly two tree-child Omega rootings',sum(x['tree_child'] for x in rootings)==2)
internal=sorted(set(sum(([a,b] for a,b,h in M),[]))-set(Ls));isos=[]
def key(edges):return {tuple(sorted([a,b]))+(tuple(sorted(h)),) for a,b,h in edges}
for perm in permutations(internal):
 mp=dict(zip(internal,perm));mp.update({a:next(b for b in Lt if Lt[b]==lab) for a,lab in Ls.items()})
 if {mp[v] for v in ret}!=set(ret):continue
 if key([(mp[a],mp[b],tuple(mp[v] for v in h)) for a,b,h in M])==key(M):isos.append(mp)
ck('no label and arrowhead preserving Omega isomorphism',not isos)
out={'status':'PASS','source_pdf_sha256':'ae01c6beba01da624bba7060e9f3adfce74a5e568e5808f4db168300d7873084','checks':checks,'check_count':len(checks),'Omega_full_ranks':ranks,'Omega_displayed_minors':dets,'Omega_rootings':rootings,'minimum_probability':str(min(patterns)),'scope':'Independent manuscript-derived point/Fourier, rooted-class and rank controls. Does not yet prove global symbolic map, upper dimension, finite atlas or every-n theorem.'}
print(json.dumps(out,indent=2))
