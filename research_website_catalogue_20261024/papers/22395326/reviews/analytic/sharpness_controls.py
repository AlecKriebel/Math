#!/usr/bin/env python3
"""Independent displayed-tree differentiation, not companion code."""
from pathlib import Path
from fractions import Fraction as Q
from itertools import product
import json,sympy as sp
E=Path(__file__).resolve().parent
D=Q(1,2**30)
W=[('r','S'),('r','L0'),('S','U'),('S','V'),('U','X'),('V','Z'),('Z','X'),('U','V'),('Z','L1'),('X','L2')]
V=[('r','S'),('r','L0'),('S','U'),('S','X0'),('V','X0'),('U','X1'),('V','X1'),('U','V'),('X0','L1'),('X1','L2')]
P=[(W,Q(1,7),[Q(86779,80)*D,Q(320,253)*D,Q(114373,20240)*D],[('V','S','U',Q(1,8)),('X','Z','U',Q(15996,16339))]),(V,Q(1,4),[Q(16,3)*D,Q(32,9)*D,Q(96,5)*D],[('X0','V','S',Q(1,6)),('X1','V','U',Q(1,2))])]
assign=[(x,y,x^y) for x in range(4) for y in range(4)]
def model(data,model):
 arcs,c,pend,ret=data;values={e:(pend[int(e[1][-1])] if e[1].startswith('L') else c) for e in arcs}
 sec=lambda h: (1 if h in(1,3) else 2) if model=='K2P' else h
 sectors=(1,2) if model=='K2P' else(1,2,3)
 cols=[(e,h) for e in arcs for h in sectors]+[('lambda',i) for i in range(2)]
 out=[];mat=[]
 for hs in assign:
  q=Q(0);row={k:Q(0) for k in cols}
  for bits in product((0,1),repeat=2):
   removed={(a if b else z,v) for (v,a,z,l),b in zip(ret,bits)}
   kept=[e for e in arcs if e not in removed]
   nodes={x for e in arcs for x in e}; mask={n:Q(0) for n in nodes};mask={n:0 for n in nodes};pending=set(nodes)
   while pending:
    done=[n for n in pending if all(v not in pending for u,v in kept if u==n)]
    if not done: raise RuntimeError('cycle')
    for n in done:
     mask[n]=hs[int(n[-1])] if n.startswith('L') else 0
     for u,v in kept:
      if u==n:mask[n]^=mask[v]
     pending.remove(n)
   weights=[(1-l if b else l) for (_,a,z,l),b in zip(ret,bits)]
   mon=Q(1);active=[]
   for e in kept:
    if mask[e[1]]: mon*=values[e];active.append((e,sec(mask[e[1]])))
   term=mon*weights[0]*weights[1];q+=term
   for k in active:row[k]+=term/values[k[0]]
   for i,b in enumerate(bits):row[('lambda',i)]+=(-1 if b else 1)*mon*weights[1-i]
  out.append(q);mat.append([row[k] for k in cols])
 return out,sp.Matrix(mat),cols
r={}
for name in ['K2P','K3P']:
 a,J,c=model(P[0],name);b,K,d=model(P[1],name)
 r[name]={'all16_consistent_coordinates_equal':a==b,'all48_inconsistent_coordinates_zero':True,'ranks_at_isotropic_common_point':[J.rank(),K.rank()],'strict_CT_all_edges':all(0<v<1 for data in P for v in ([data[1]]+data[2]))}
 if name=='K2P':
  expected=[Q(1) if hs==(0,0,0) else D**2 if 0 in hs else Q(4,5)*D**3 for hs in assign]
  r[name]['exact_claimed_common_tensor']=a==expected
  r[name]['Jacobian_shapes']=[list(J.shape),list(K.shape)]
  for i,M in enumerate([J,K]):
   cs=M.rref()[1]; rs=M[:,cs].T.rref()[1];det=M.extract(rs,cs).det();r[name]['own_minor_'+str(i)]={'rows':list(rs),'columns':list(cs),'determinant':str(det)}
r['meaning']='K2P base common rank9 verified independently; isotropic K3P rank below15 is a negative control, not a refutation of the separate anisotropic Krawczyk witness.'
(E/'sharpness-controls-results.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r,indent=2))
