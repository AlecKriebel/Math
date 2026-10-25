"""Independent graph/rooting/Fourier controls transcribed from the 33+7 page paper.
No submitted verifier imports. Standard-library rational arithmetic for point/Jacobian checks.
"""
from fractions import Fraction as F
from itertools import product
from collections import defaultdict,deque
from functools import reduce
from pathlib import Path
from datetime import datetime,timezone
import json

omega=[('U','V'),('U','P0'),('P0','P1'),('P1','V'),('S','U'),('S','X'),('V','P4'),('P4','X'),('P0','L0'),('P1','L1'),('P4','L2'),('X','L3')]
theta=[('S','A'),('S','C'),('A','B'),('B','C'),('C','D'),('D','E'),('A','F'),('E','F'),('B','L0'),('D','L1'),('F','L2'),('E','L3')]
orbits=['0011','0101','0110','0123','1001','1010','1023','1100','1111','1122','1203','1212','1221','1230']

def topology(arcs):
 V=set(sum(([u,v] for u,v in arcs),[]));ins={v:[] for v in V};outs={v:[] for v in V}
 for i,(u,v) in enumerate(arcs):ins[v].append(i);outs[u].append(i)
 roots=[v for v in V if not ins[v]];assert len(roots)==1
 R={v for v in V if len(ins[v])==2}
 return V,ins,outs,roots[0],R

def configurations(arcs,labels):
 V,ins,outs,root,R=topology(arcs);retics=sorted(R);records=[]
 for choices in product(range(2),repeat=len(retics)):
  kept=[i for i,(u,v) in enumerate(arcs) if v not in R or i==ins[v][choices[retics.index(v)]]]
  children=defaultdict(list)
  for i in kept:children[arcs[i][0]].append(arcs[i][1])
  def descendants(v):
   if v in labels:return 1<<labels[v]
   return reduce(int.__or__,(descendants(w) for w in children[v]),0)
  masks={i:descendants(arcs[i][1]) for i in kept}
  records.append((choices,masks))
 return records

def terms(arcs,labels,g):
 if reduce(int.__xor__,g,0):return []
 result=[]
 for choices,masks in configurations(arcs,labels):
  active=[]
  for i,mask in masks.items():
   h=reduce(int.__xor__,(g[k] for k in range(len(g)) if mask>>k&1),0)
   if h:active.append(i)
  result.append((choices,active))
 return result

def coordinate(arcs,labels,g,x,lambdas):
 out=0
 for choices,active in terms(arcs,labels,g):
  w=1
  for c,a in zip(choices,lambdas):w*=a if c==0 else 1-a
  for i in active:w*=x[i]
  out+=w
 return out

def jacobian(arcs,labels,point,rows):
 x=point[:len(arcs)];ls=point[len(arcs):];out=[]
 for g in rows:
  row=[F(0)]*len(point)
  for choices,active in terms(arcs,labels,g):
   factors=[a if c==0 else 1-a for c,a in zip(choices,ls)];base=reduce(lambda a,b:a*b,factors,F(1))*reduce(lambda a,i:a*x[i],active,F(1))
   for i in active:row[i]+=base/x[i]
   for j,c in enumerate(choices):row[len(x)+j]+=base/factors[j]*(1 if c==0 else -1)
  out.append(row)
 return out

def det(A):
 A=[list(row) for row in A];answer=F(1)
 for j in range(len(A)):
  k=next((k for k in range(j,len(A)) if A[k][j]),None)
  if k is None:return F(0)
  if k!=j:A[k],A[j]=A[j],A[k];answer=-answer
  pivot=A[j][j];answer*=pivot
  for i in range(j+1,len(A)):
   ratio=A[i][j]/pivot
   for col in range(j+1,len(A)):A[i][col]-=ratio*A[j][col]
 return answer

def census(arcs):
 V,ins,outs,root,R=topology(arcs);ordinary=[];fixed=[]
 children=[arcs[i][1] for i in outs[root]];assert len(children)==2
 for u,v in arcs:
  if u==root:continue
  (fixed if v in R else ordinary).append((u,v))
 a,b=children
 if b in R:fixed.append((a,b))
 elif a in R:fixed.append((b,a))
 else:ordinary.append((a,b))
 edgepool=[(u,v,True) for u,v in fixed]+[(u,v,False) for u,v in ordinary]
 vertices=V-{root};leaves={v for v in vertices if v.startswith('L')};valid=[]
 for edgeidx,(a,b,directed) in enumerate(edgepool):
  remaining=[e for j,e in enumerate(edgepool) if j!=edgeidx]
  f=[(u,v) for u,v,d in remaining if d];und=[(u,v) for u,v,d in remaining if not d]
  for flips in product(range(2),repeat=len(und)):
   oriented=f+[(v,u) if bit else (u,v) for (u,v),bit in zip(und,flips)]+[('ROOT',a),('ROOT',b)]
   vs=vertices|{'ROOT'};parents={v:[] for v in vs};kids={v:[] for v in vs}
   for u,v in oriented:parents[v].append(u);kids[u].append(v)
   if any((len(parents[v]),len(kids[v])) != ((0,2) if v=='ROOT' else (1,0) if v in leaves else (2,1) if v in R else (1,2)) for v in vs):continue
   indeg={v:len(parents[v]) for v in vs};queue=['ROOT'];order=[]
   while queue:
    v=queue.pop();order.append(v)
    for w in kids[v]:
     indeg[w]-=1
     if indeg[w]==0:queue.append(w)
   if len(order)!=len(vs):continue
   # Lowest stable ancestor test: deleting any nonroot vertex must leave a leaf reachable.
   def reachable_without(block):
    reached={'ROOT'};todo=['ROOT']
    while todo:
     v=todo.pop()
     for w in kids[v]:
      if w!=block and w not in reached:reached.add(w);todo.append(w)
    return bool(leaves&reached)
   if any(not reachable_without(v) for v in vertices):continue
   tc=all(any(w not in R for w in kids[v]) for v in vs-leaves)
   valid.append({'root_edge':[a,b],'tree_child':tc,'arcs':oriented})
 # Simple cycle lengths by canonical unoriented vertex cycles.
 adj=defaultdict(set)
 for a,b,_ in edgepool:adj[a].add(b);adj[b].add(a)
 cycles=set()
 def visit(start,path):
  v=path[-1]
  for w in adj[v]:
   if w==start and len(path)>=3:
    seq=path;rots=[tuple(seq[i:]+seq[:i]) for i in range(len(seq))];rev=list(reversed(seq));rots += [tuple(rev[i:]+rev[:i]) for i in range(len(rev))];cycles.add(min(rots))
   elif w not in path and w>=start:visit(start,path+[w])
 for v in sorted(adj):visit(v,[v])
 def distances(leaf):
  ds={leaf:0};todo=deque([leaf])
  while todo:
   u=todo.popleft()
   for v in adj[u]:
    if v not in ds:ds[v]=ds[u]+1;todo.append(v)
  return sorted(ds[v] for v in R)
 return {'admissible':len(valid),'tree_child':sum(v['tree_child'] for v in valid),'rootings':valid,'cycle_lengths':sorted(len(c) for c in cycles),'leaf_reticulation_distances':{l:distances(l) for l in leaves}}

labels={f'L{i}':i for i in range(4)};permuted={f'L{i}':v for i,v in enumerate([1,0,3,2])}
src=list(map(F,['1/2','1/4','1/2','1/2','1/2','1/2','1/2','1/20','1/2','1/2','1/10','1/2','1/2','1/2']))
tgt=list(map(F,['7/12','1/7','1/2','41/48','28/41','1/2','1/2','12/205','1/2','1/2','3/40','1/2','1/2','1/2']))
assert all(0<x<1 for x in src+tgt)
cens=census(omega);assert (cens['admissible'],cens['tree_child'],cens['cycle_lengths'])==(7,2,[4,4,6])
assert cens['leaf_reticulation_distances']['L0']==[3,3] and cens['leaf_reticulation_distances']['L1']==[2,4]
allg=list(product(range(4),repeat=4));ps=[coordinate(omega,labels,g,src[:12],src[12:]) for g in allg];pt=[coordinate(omega,permuted,g,tgt[:12],tgt[12:]) for g in allg];assert ps==pt
J1=jacobian(omega,labels,src,[tuple(map(int,g)) for g in orbits]);J2=jacobian(omega,permuted,tgt,[tuple(map(int,g)) for g in orbits]);rows=[0,1,2,3,4,5,6,7,9];cols=[0,1,2,3,4,7,8,9,10]
d1=det([[J1[i][j] for j in cols] for i in rows]);d2=det([[J2[i][j] for j in cols] for i in rows]);assert d1==F(-171,2305843009213693952000000) and d2==F(-513,9223372036854775808000000)
probs=[]
for pattern in allg:
 total=F(0)
 for g,value in zip(allg,ps):
  parity=sum(((a&1)*(h&1)+((a>>1)&1)*((h>>1)&1)) for a,h in zip(pattern,g))%2
  total+=(-1 if parity else 1)*value
 probs.append(total/256)
assert min(probs)==F(87763,26214400) and sum(probs)==1
# Negative: unpermuted target and changed parameter must not accidentally pass.
assert ps!=[coordinate(omega,labels,g,tgt[:12],tgt[12:]) for g in allg]
changed=src[:];changed[0]=F(3,5);assert ps!=[coordinate(omega,labels,g,changed[:12],changed[12:]) for g in allg]
tcens=census(theta);assert tcens['tree_child']>0 and tcens['tree_child']<tcens['admissible'] and tcens['cycle_lengths']==[3,5,6]
result={'utc':datetime.now(timezone.utc).isoformat(),'status':'PASS','omega':{'census':cens,'all_256_fourier_equal':True,'all_pattern_probabilities_positive':True,'minimum_probability':str(min(probs)),'source_rank9_minor':str(d1),'target_rank9_minor':str(d2)},'theta_topology':tcens,'negative_controls':{'incorrect_leaf_map_rejected':True,'changed_edge_rejected':True},'scope':'Independent finite graph and exact sharpness controls; not the global classification proof'}
Path(__file__).with_name('fresh-graph-fourier.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'status':'PASS','omega_rootings':cens['admissible'],'omega_tree_child':cens['tree_child'],'theta_rootings':tcens['admissible'],'theta_tree_child':tcens['tree_child'],'Fourier_coordinates':256,'rank9_minors':2}))
