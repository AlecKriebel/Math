#!/usr/bin/env python3
"""Independent standard-library replay of the fourteen K3P orbit certificates.
It does not import the primary graph canonicalizer, switching compiler, Fourier
compiler, rank selector, or polynomial selector.
"""
from __future__ import annotations
from dataclasses import dataclass
from itertools import product,permutations
from fractions import Fraction as Q
from collections import defaultdict,Counter
from pathlib import Path
import json,hashlib
ROOT=Path(__file__).resolve().parents[1]
LOCK=json.load(open(ROOT/'K3P_14_ORBIT_LOCK.json'));REC={r['orbit_id']:r for r in LOCK['records']}
CH4=tuple(p+(p[0]^p[1]^p[2],) for p in product(range(4),repeat=3));CH3=tuple(p+(p[0]^p[1],) for p in product(range(4),repeat=2))

@dataclass(frozen=True)
class MapDescriptor:
 k:int;retic_count:int;edge_class_count:int;outputs:tuple;edge_signatures:tuple
class Graph:
 def __init__(self,j):
  self.node={x['id']:dict(x) for x in j['nodes']};self.arcs=tuple(sorted((x['tail'],x['head']) for x in j['arcs']))
  self.out=defaultdict(list);self.inc=defaultdict(list)
  for u,v in self.arcs:self.out[u].append(v);self.inc[v].append(u)
 def relabel(self,p):
  j={'nodes':[],'arcs':[{'tail':u,'head':v} for u,v in self.arcs]}
  for n,d in self.node.items():
   e=dict(d);e['id']=n
   if isinstance(e.get('label'),int):e['label']=p[e['label']]
   j['nodes'].append(e)
  return Graph(j)

def masks(G,kept):
 out=defaultdict(list)
 for u,v in kept:out[u].append(v)
 memo={}
 def dfs(n):
  if n in memo:return memo[n]
  d=G.node[n];m=(1<<d['label']) if isinstance(d.get('label'),int) else 0
  for v in out[n]:m|=dfs(v)
  memo[n]=m;return m
 for n in G.node:dfs(n)
 return {(u,v):memo[v] for u,v in kept}
def sector(mask,c):
 z=0;i=0
 while mask:
  if mask&1:z^=c[i]
  i+=1;mask>>=1
 return z
def wpoly(bits):
 p={0:1}
 for j,b in enumerate(bits):
  q=defaultdict(int)
  for m,c in p.items():
   if b:q[m|1<<j]+=c
   else:q[m]+=c;q[m|1<<j]-=c
  p={m:c for m,c in q.items() if c}
 return tuple(sorted(p.items()))
def descriptor_variant(G,ret,parent_orders):
 chars=CH4;k=4;arms={e for e in G.arcs if G.node[e[1]]['role']=='leaf' and isinstance(G.node[e[1]].get('label'),int)}
 sw=[]
 for bits in product((0,1),repeat=len(ret)):
  removed=set()
  for j,r in enumerate(ret):
   kp=parent_orders[j][bits[j]]
   for p in G.inc[r]:
    if p!=kp:removed.add((p,r))
  kept=tuple(e for e in G.arcs if e not in removed);sw.append((bits,kept,masks(G,kept)))
 sigs=[];iedges=[]
 for e in G.arcs:
  if e in arms:continue
  s=[]
  for bits,kept,em in sw:
   if e not in em:s.extend((0,)*64)
   else:s.extend(sector(em[e],c) for c in chars)
  if any(s):iedges.append(e);sigs.append(tuple(s))
 active=tuple(sorted(set(sigs)));cl={s:i for i,s in enumerate(active)};ec={e:cl[s] for e,s in zip(iedges,sigs)};outs=[]
 for c in chars:
  grouped=defaultdict(lambda:defaultdict(int))
  for bits,kept,em in sw:
   fac=Counter()
   for e in kept:
    ci=ec.get(e)
    if ci is None:continue
    h=sector(em[e],c)
    if h:fac[(ci,h)]+=1
   mon=tuple(sorted((ci,h,x) for (ci,h),x in fac.items()))
   for m,a in wpoly(bits):grouped[mon][m]+=a
  expr=[]
  for mon,p in grouped.items():
   pp=tuple(sorted((m,a) for m,a in p.items() if a))
   if pp:expr.append((mon,pp))
  outs.append(tuple(sorted(expr)))
 return MapDescriptor(k,len(ret),len(active),tuple(outs),active)
def compile_map(G):
 ret=tuple(sorted((n for n,d in G.node.items() if d['role']=='retic')));V=[]
 for order in permutations(ret):
  pp=[tuple(sorted(G.inc[r])) for r in order]
  for flips in product((0,1),repeat=len(order)):
   po=tuple((p[f],p[1-f]) for p,f in zip(pp,flips));V.append(descriptor_variant(G,order,po))
 return min(V,key=lambda d:(d.retic_count,d.edge_class_count,d.outputs,d.edge_signatures))

def sparse_outputs(d):
 n=3*d.edge_class_count+d.retic_count;out=[]
 for expr in d.outputs:
  P=defaultdict(int)
  for mon,lp in expr:
   b=[0]*n
   for ci,h,e in mon:b[3*ci+h-1]+=e
   for mask,a in lp:
    x=list(b)
    for j in range(d.retic_count):
     if mask>>j&1:x[3*d.edge_class_count+j]+=1
    P[tuple(x)]+=a
  out.append({e:a for e,a in P.items() if a})
 return tuple(out)
def pmul(a,b):
 z=defaultdict(Q)
 for e,c in a.items():
  for f,d in b.items():z[tuple(x+y for x,y in zip(e,f))]+=c*d
 return {e:c for e,c in z.items() if c}
def pprod(ps):
 if not ps:return {():Q(1)}
 z=ps[0]
 for p in ps[1:]:z=pmul(z,p)
 return z
def plin(terms):
 z=defaultdict(Q)
 for a,p in terms:
  for e,c in p.items():z[e]+=Q(a)*c
 return {e:c for e,c in z.items() if c}
def phash(p):return hashlib.sha256(json.dumps([(list(e),str(c)) for e,c in sorted(p.items())],separators=(',',':')).encode()).hexdigest()
def point(r,side):
 d=r[side+'_exact_rank_point'];return tuple(tuple(Q(x) for x in e) for e in d['edges']),tuple(Q(x) for x in d['inheritance'])
def eval_map(d,E,L):
 out=[]
 for expr in d.outputs:
  z=Q(0)
  for mon,lp in expr:
   m=Q(1)
   for ci,h,e in mon:m*=E[ci][h-1]**e
   p=Q(0)
   for mask,a in lp:
    t=Q(a)
    for j,x in enumerate(L):
     if mask>>j&1:t*=x
    p+=t
   z+=m*p
  out.append(z)
 return tuple(out)
def jac(d,E,L):
 n=3*d.edge_class_count+d.retic_count;flat=tuple(x for e in E for x in e);J=[]
 for expr in d.outputs:
  row=[Q(0)]*n
  for mon,lp in expr:
   m=Q(1)
   for ci,h,e in mon:m*=E[ci][h-1]**e
   p=Q(0);dp=[Q(0)]*d.retic_count
   for mask,a in lp:
    t=Q(a)
    for j,x in enumerate(L):
     if mask>>j&1:t*=x
    p+=t
    for j,x in enumerate(L):
     if mask>>j&1:dp[j]+=t/x
   for ci,h,e in mon:row[3*ci+h-1]+=m*p*e/E[ci][h-1]
   for j in range(d.retic_count):row[3*d.edge_class_count+j]+=m*dp[j]
  J.append(row)
 return J
def det(A):
 A=[list(map(Q,r)) for r in A];n=len(A);s=Q(1)
 for c in range(n):
  p=next((i for i in range(c,n) if A[i][c]),None)
  if p is None:return Q(0)
  if p!=c:A[c],A[p]=A[p],A[c];s=-s
  v=A[c][c];s*=v
  for i in range(c+1,n):
   if A[i][c]:
    a=A[i][c]/v
    for j in range(c+1,n):A[i][j]-=a*A[c][j]
 return s

def pull(d,terms):
 op=sparse_outputs(d);return plin((t['coefficient'],pprod([op[i] for i in t['coordinate_indices']])) for t in terms)
def evalpoly(q,terms):
 z=Q(0)
 for t in terms:
  m=Q(t['coefficient'])
  for i in t['coordinate_indices']:m*=q[i]
  z+=m
 return z

def iso(A,B):
 # independent color-refinement/backtracking isomorphism, ignoring construction edge names
 def refine(G):
  col={n:(G.node[n]['role'],G.node[n].get('label'),len(G.inc[n]),len(G.out[n])) for n in G.node}
  for _ in range(len(G.node)):
   raw={n:(col[n],tuple(sorted(col[x] for x in G.inc[n])),tuple(sorted(col[x] for x in G.out[n]))) for n in G.node};vals={x:i for i,x in enumerate(sorted(set(raw.values()),key=repr))};new={n:vals[raw[n]] for n in G.node}
   if all(new[n]==col[n] for n in G.node):break
   col=new
  return col
 ca,cb=refine(A),refine(B);ga=defaultdict(list);gb=defaultdict(list)
 for n,c in ca.items():ga[c].append(n)
 for n,c in cb.items():gb[c].append(n)
 if sorted((c,len(v)) for c,v in ga.items())!=sorted((c,len(v)) for c,v in gb.items()):return False
 groups=[]
 for c in sorted(ga,key=repr):groups.append((sorted(ga[c]),sorted(gb[c])))
 amap={}
 def rec(j):
  if j==len(groups):
   return all((amap[u],amap[v]) in set(B.arcs) for u,v in A.arcs)
  aa,bb=groups[j]
  for p in permutations(bb):
   amap.update(zip(aa,p))
   if rec(j+1):return True
   for x in aa:amap.pop(x,None)
  return False
 return rec(0)

def verify():
 assert len(REC)==14 and sum(len(r['raw_members']) for r in REC.values())==38 and len(LOCK['prelock_exact_separations'])==2
 maps={}
 for oid,r in REC.items():
  sg=Graph(r['source_literal_graph']);tg=Graph(r['target_literal_graph']);sd=compile_map(sg);td=compile_map(tg);maps[oid]=(sd,td)
  assert hashlib.sha256(repr(sd).encode()).hexdigest()==r['source_map_hash'];assert hashlib.sha256(repr(td).encode()).hexdigest()==r['target_map_hash'];assert not iso(sg,tg)
  for w in r['raw_member_transports']:
   if not iso(sg,sg.relabel(tuple(w['source_automorphism']))):
    raise AssertionError(('source automorphism',oid,w))
   if not iso(tg,tg.relabel(tuple(w['target_automorphism']))):
    raise AssertionError(('target automorphism',oid,w))
 print('CLEANROOM PASS literal graphs, 14 descriptors, 38 orbit transports')
 # Independently reconstruct and verify the two exact pre-lock sink-swap separations.
 PC=json.load(open(ROOT/'software/certificates/k3p_prelock_source5_quartic.json'))
 assert len(PC['records'])==2
 for c,lk in zip(PC['records'],LOCK['prelock_exact_separations']):
  sg=Graph(lk['source_literal_graph']);tg=Graph(lk['target_literal_graph']);sd=compile_map(sg);td=compile_map(tg)
  assert hashlib.sha256(repr(sd).encode()).hexdigest()==lk['source_map_hash'];assert hashlib.sha256(repr(td).encode()).hexdigest()==lk['target_map_hash'];assert not iso(sg,tg)
  assert not pull(td,c['terms']);sp=pull(sd,c['terms']);assert phash(sp)==c['source_pullback_sha256']
  ep=c['source_exact_point'];pt=(tuple(tuple(Q(x) for x in row) for row in ep['edges']),tuple(Q(x) for x in ep['inheritance']))
  assert evalpoly(eval_map(sd,*pt),c['terms'])==Q(c['source_evaluation'])!=0
 print('CLEANROOM PASS two pre-lock source-5 quartic separations')
 for fn in ['k3p_h14_marginal_orbit_certificates.json','k3p_remaining_quartic_separators.json']:
  C=json.load(open(ROOT/'software/certificates'/fn))
  for c in C['records']:
   sd,td=maps[c['orbit_id']];assert not pull(td,c['terms']);sp=pull(sd,c['terms']);assert phash(sp)==c['source_pullback_sha256'];r=REC[c['orbit_id']];q=eval_map(sd,*point(r,'source'));assert evalpoly(q,c['terms'])==Q(c['source_evaluation'])!=0
   print('CLEANROOM PASS',c['orbit_id'],'quartic')
 C=json.load(open(ROOT/'software/certificates/k3p_directed_rank_obstructions.json'))
 for c in C['records']:
  sd,td=maps[c['orbit_id']];r=REC[c['orbit_id']]
  for side,d,cc in [('source',sd,c['source_rank_certificate']),('target',td,c['target_rank_certificate'])]:
   J=jac(d,*point(r,side));D=det([[J[i][j] for j in cc['parameter_columns']] for i in cc['output_rows']]);assert str(D)==cc['determinant'] and D
  assert c['source_rank_certificate']['rank']>c['target_dimension_upper_bound']==c['target_rank_certificate']['rank']
  print('CLEANROOM PASS',c['orbit_id'],'rank minors')
 cov=set()
 for fn in ['k3p_h14_marginal_orbit_certificates.json','k3p_remaining_quartic_separators.json','k3p_directed_rank_obstructions.json']:
  cov|={x['orbit_id'] for x in json.load(open(ROOT/'software/certificates'/fn))['records']}
 assert cov==set(REC)
 print('CLEANROOM_K3P_FOURTEEN_ORBITS_ZERO_UNRESOLVED')
if __name__=='__main__':verify()
