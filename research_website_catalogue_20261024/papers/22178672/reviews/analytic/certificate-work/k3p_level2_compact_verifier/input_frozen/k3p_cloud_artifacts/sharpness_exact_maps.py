#!/usr/bin/env python3
from __future__ import annotations
from fractions import Fraction as F
from itertools import product
import networkx as nx, json, sys, hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]

CHARS=tuple((a,b,a^b) for a in range(4) for b in range(4))

def make_graph(arcs,retics,labels):
 G=nx.DiGraph()
 nodes={x for e in arcs for x in e}
 for n in nodes:
  if n in labels:role='leaf'
  elif n=='r':role='root'
  elif n in retics:role='retic'
  else:role='tree'
  G.add_node(n,role=role,label=labels.get(n))
 G.add_edges_from(arcs)
 assert nx.is_directed_acyclic_graph(G)
 return G

def masks(G,kept):
 children={n:[] for n in G}
 for u,v in kept:children[u].append(v)
 H=nx.DiGraph();H.add_nodes_from(G);H.add_edges_from(kept)
 out={}
 for n in reversed(list(nx.topological_sort(H))):
  m=(1<<G.nodes[n]['label']) if G.nodes[n].get('label') is not None else 0
  for c in children[n]:m|=out[c]
  out[n]=m
 return {(u,v):out[v] for u,v in kept}

def sector(mask,chars):
 z=0;i=0
 while mask:
  if mask&1:z^=chars[i]
  i+=1;mask>>=1
 return z

class FullMap:
 def __init__(self,G,edge_order,retic_parent0):
  self.G=G;self.edges=tuple(edge_order);self.retics=tuple(retic_parent0);self.parent0=tuple(retic_parent0[r] for r in self.retics)
  self.parents=tuple(tuple(G.predecessors(r)) for r in self.retics);self.E=len(self.edges);self.R=len(self.retics)
  self.outputs=[]
  for chars in CHARS:
   terms=[]
   for bits in product((0,1),repeat=self.R):
    kept=[]
    for e in self.edges:
     keep=True
     for j,r in enumerate(self.retics):
      if e[1]==r:
       selected=self.parent0[j] if bits[j] else next(p for p in self.parents[j] if p!=self.parent0[j])
       if e[0]!=selected:keep=False
     if keep:kept.append(e)
    em=masks(G,kept);powers=[]
    for ei,e in enumerate(self.edges):
     if e in em:
      s=sector(em[e],chars)
      if s:powers.append((3*ei+s-1,1))
    # bit 1 means parent0 selected, weight lambda; 0 means 1-lambda expanded later
    terms.append((bits,tuple(powers)))
   self.outputs.append(tuple(terms))
 def eval_jac(self,edges,lams):
  n=3*self.E+self.R;q=[];J=[]
  flat=tuple(x for e in edges for x in e)
  for terms in self.outputs:
   val=F(0);gr=[F(0)]*n
   for bits,powers in terms:
    mv=F(1)
    for v,e in powers:mv*=flat[v]**e
    w=F(1)
    for j,b in enumerate(bits):w*=lams[j] if b else (1-lams[j])
    term=mv*w;val+=term
    for v,e in powers:gr[v]+=term*e/flat[v]
    for j,b in enumerate(bits):gr[3*self.E+j]+=term/lams[j] if b else -term/(1-lams[j])
   q.append(val);J.append(gr)
  return tuple(q),J

def rank_rref(A):
 A=[list(map(F,r)) for r in A];m=len(A);n=len(A[0]);r=0;pr=[];pc=[]
 for c in range(n):
  z=next((i for i in range(r,m) if A[i][c]),None)
  if z is None:continue
  A[r],A[z]=A[z],A[r];pv=A[r][c];A[r]=[x/pv for x in A[r]]
  for i in range(m):
   if i!=r and A[i][c]:
    a=A[i][c];A[i]=[x-a*y for x,y in zip(A[i],A[r])]
  pr.append(r);pc.append(c);r+=1
  if r==m:break
 return r,tuple(pc)

def det(A):
 A=[list(map(F,r)) for r in A];n=len(A);d=F(1)
 for c in range(n):
  z=next((i for i in range(c,n) if A[i][c]),None)
  if z is None:return F(0)
  if z!=c:A[c],A[z]=A[z],A[c];d=-d
  pv=A[c][c];d*=pv
  for i in range(c+1,n):
   if A[i][c]:
    a=A[i][c]/pv
    for j in range(c+1,n):A[i][j]-=a*A[c][j]
 return d

W_arcs=[('r','S'),('r','L0'),('S','U'),('S','V'),('U','X'),('V','Z'),('Z','X'),('U','V'),('Z','L1'),('X','L2')]
Wp_arcs=[('r','S'),('r','L0'),('S','U'),('S','X0'),('V','X0'),('U','X1'),('V','X1'),('U','V'),('X0','L1'),('X1','L2')]
W=make_graph(W_arcs,{'V','X'},{'L0':0,'L1':1,'L2':2});Wp=make_graph(Wp_arcs,{'X0','X1'},{'L0':0,'L1':1,'L2':2})
MW=FullMap(W,W_arcs,{'V':'S','X':'Z'});MP=FullMap(Wp,Wp_arcs,{'X0':'V','X1':'V'})
delta=F(1,2**30)
W_non={e for e in W_arcs if e not in [('r','L0'),('Z','L1'),('X','L2')]}
P_non={e for e in Wp_arcs if e not in [('r','L0'),('X0','L1'),('X1','L2')]}
wx={('r','L0'):F(86779,80)*delta,('Z','L1'):F(320,253)*delta,('X','L2'):F(114373,20240)*delta}
px={('r','L0'):F(16,3)*delta,('X0','L1'):F(32,9)*delta,('X1','L2'):F(96,5)*delta}
WE=tuple((F(1,7),)*3 if e in W_non else (wx[e],)*3 for e in W_arcs)
PE=tuple((F(1,4),)*3 if e in P_non else (px[e],)*3 for e in Wp_arcs)
WL=(F(1,8),F(15996,16339)) # V parent0 S; X parent0 Z
PL=(F(1,6),F(1,2)) # X0 parent0 V; X1 parent0 V
qW,JW=MW.eval_jac(WE,WL);qP,JP=MP.eval_jac(PE,PL)
assert qW==qP
rows=tuple(range(1,16))
print('common q',qW)
print('ranks',rank_rref([JW[i] for i in rows])[0],rank_rref([JP[i] for i in rows])[0])
FJ=[[JW[i][j] for j in range(len(JW[0]))]+[-JP[i][j] for j in range(len(JP[0]))] for i in rows]
r,cols=rank_rref(FJ);print('combined rank',r,'pivot cols',cols)
D=det([[FJ[i][j] for j in cols] for i in range(15)]) if r==15 else F(0)
print('combined det',D)
# Find rank14 pivot rows/cols for individual maps and then identify a nonzero first derivative direction along equality fibre.
rw,cw=rank_rref([JW[i] for i in rows]);rp,cp=rank_rref([JP[i] for i in rows])
print('individual pivot cols',cw,cp)
# Save base result now.
out={'schema':'k3p-weak-sharpness-ift-base-v1','output_order':[list(c) for c in CHARS],
 'W_edges':[list(e) for e in W_arcs],'Wprime_edges':[list(e) for e in Wp_arcs],
 'W_inheritance':[str(x) for x in WL],'Wprime_inheritance':[str(x) for x in PL],
 'common_tensor':[str(x) for x in qW],'W_rank':rw,'Wprime_rank':rp,'combined_equality_rank':r,
 'combined_pivot_columns':list(cols),'combined_pivot_determinant':str(D),'W_rank_columns':list(cw),'Wprime_rank_columns':list(cp)}
(ROOT/'software/certificates/k3p_sharpness_ift_base.json').write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
print('BASE_PASS')
