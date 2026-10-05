#!/usr/bin/env python3
"""Exact, offline controls for authored partial results. Python 3.10+, stdlib only."""
from pathlib import Path
from itertools import combinations,permutations
from collections import Counter
from copy import deepcopy
import json,sys
ROOT=Path(__file__).resolve().parent

def graph(n,es):
 g=[set() for _ in range(n)]
 for a,b in es:
  assert 0<=a<n and 0<=b<n and a!=b
  g[a].add(b);g[b].add(a)
 return g

def edges(g):return sorted((a,b) for a in range(len(g)) for b in g[a] if a<b)

def product(m,n):
 return graph(m*n,[(i*n+j,((i+1)%m)*n+j) for i in range(m) for j in range(n)]+[(i*n+j,i*n+(j+1)%n) for i in range(m) for j in range(n)])

def product_facets(m,n):
 return [{i*n+j for i in range(m) for j in [k,(k+1)%n]} for k in range(n)]+[{i*n+j for i in [k,(k+1)%m] for j in range(n)} for k in range(m)]

def truncated_simplex():
 labels=list(permutations(range(5),2))
 return graph(20,[(a,b) for a in range(20) for b in range(a+1,20) if labels[a][0]==labels[b][0] or labels[a]==labels[b][::-1]])

def apply(g,op):
 h={i:set(g[i]) for i in range(len(g))}
 if op['op']=='delta_y':
  tri=op['triangle'];assert len(set(tri))==3
  assert all(b in h[a] for a,b in combinations(tri,2))
  z=len(h);h[z]=set(tri)
  for a,b in combinations(tri,2):h[a].remove(b);h[b].remove(a)
  for a in tri:h[a].add(z)
 else:
  assert op['op']=='y_delta'
  v=op['vertex'];assert len(h[v])==3
  ns=h.pop(v)
  for a in ns:h[a].remove(v)
  for a,b in combinations(ns,2):h[a].add(b);h[b].add(a)
 ks=sorted(h);mp={a:i for i,a in enumerate(ks)}
 return [set(mp[b] for b in h[a]) for a in ks]

def verify_family(records):
 for r in records:
  g=graph(6,combinations(range(6),2))
  for op in r['derivation']:g=apply(g,op)
  assert len(g)==r['n'] and edges(g)==sorted(map(tuple,r['edges']))
 return True

def connected(g,vs):
 if not vs:return False
 reached={min(vs)};todo=list(reached)
 while todo:
  u=todo.pop()
  for v in g[u]&vs-reached:reached.add(v);todo.append(v)
 return reached==vs

def verify_minor(g,r,family):
 bs=[set(b) for b in r['branch_sets']];f=family[r['family_index']]
 assert len(bs)==f['n']
 assert sorted(map(tuple,r['target_edges']))==sorted(map(tuple,f['edges']))
 assert all(b and b<=set(range(len(g))) for b in bs)
 assert sum(map(len,bs))==len(set.union(*bs))
 assert all(connected(g,b) for b in bs)
 for a,b in r['target_edges']:assert any(g[x]&bs[b] for x in bs[a])
 return True

def facial_cover(g,facets):
 """Enumerate ALL unoriented simple cycles of length <= n-3, exactly once.
 A disjoint pair can have no longer component. Mask compression is exact:
 containment in a facet and disjointness depend only on vertex sets.
 """
 n=len(g);fm=[sum(1<<v for v in f) for f in facets];counts=Counter();nf={};masks=set()
 for root in range(n):
  def dfs(path,mask):
   u=path[-1]
   if len(path)>=3 and root in g[u] and path[1]<u:
    counts[len(path)]+=1;masks.add(mask)
    if not any(mask&f==mask for f in fm):nf.setdefault(mask,path[:])
   if len(path)>=n-3:return
   for v in sorted(g[u]):
    if v>root and not (mask>>v&1):dfs(path+[v],mask|(1<<v))
  dfs([root],1<<root)
 full=(1<<n)-1;sub=[None]*(1<<n)
 for m in nf:sub[m]=m
 for i in range(n):
  for m in range(1<<n):
   if m>>i&1 and sub[m] is None:sub[m]=sub[m^(1<<i)]
 pair=None
 for m,p in nf.items():
  k=sub[full^m]
  if k is not None:pair=[p,nf[k]];break
 return {'n':n,'edges':len(edges(g)),'cycle_counts':dict(sorted(counts.items())), 'distinct_cycle_vertex_masks':len(masks),'nonfacial_cycle_vertex_masks':len(nf),'uncovered_pair':pair,'all_disjoint_pairs_facially_covered':pair is None}

def expect_reject(fn):
 try:fn()
 except AssertionError:return True
 return False

def main():
 family=json.loads((ROOT/'petersen_family_certificates.json').read_text());assert verify_family(family)
 certificates=json.loads((ROOT/'minor_certificates.json').read_text())
 gs={'Q4':product(4,4),'triangle_hexagon':product(3,6),'truncated_simplex':truncated_simplex()}
 out={'family_derivations_verified':len(family),'minor_models':{},'facial_covers':{},'negative_controls':{}}
 for name,r in certificates.items():out['minor_models'][name]=verify_minor(gs[name],r,family)
 for n in [3,4,5]:
  r=facial_cover(product(3,n),product_facets(3,n));assert r['all_disjoint_pairs_facially_covered'];out['facial_covers'][f'C3xC{n}']=r
 # An explicit intrinsic-link graph must not pass the sufficient facial test.
 r=facial_cover(product(4,4),product_facets(4,4));assert not r['all_disjoint_pairs_facially_covered'];out['negative_controls']['Q4_facial_test_rejects']=r
 bad=deepcopy(certificates['Q4']);bad['branch_sets'][0].append(bad['branch_sets'][1][0]);assert expect_reject(lambda:verify_minor(gs['Q4'],bad,family));out['negative_controls']['overlapping_branches_rejected']=True
 bad=deepcopy(certificates['Q4']);bad['branch_sets'][0]=[];assert expect_reject(lambda:verify_minor(gs['Q4'],bad,family));out['negative_controls']['empty_branch_rejected']=True
 bad=deepcopy(certificates['Q4']);g=graph(len(gs['Q4']),edges(gs['Q4']));a,b=bad['target_edges'][0]
 for u in bad['branch_sets'][a]:
  for v in bad['branch_sets'][b]:g[u].discard(v);g[v].discard(u)
 assert expect_reject(lambda:verify_minor(g,bad,family));out['negative_controls']['missing_target_edge_rejected']=True
 bad=deepcopy(family);bad[-1]['edges']=bad[-1]['edges'][:-1];assert expect_reject(lambda:verify_family(bad));out['negative_controls']['damaged_family_derivation_rejected']=True
 # Gale sign-count enumeration for six extreme points with no zero coefficient.
 out['six_vertex_sign_cases']={}
 for p in [2,3,4]:
  signs=[1]*p+[-1]*(6-p);es=[(a,b) for a,b in combinations(range(6),2) if {signs[i] for i in range(6) if i not in [a,b]}=={-1,1}]
  assert len(es)==(15 if p==3 else 14);out['six_vertex_sign_cases'][str(p)]=len(es)
 # Exact countercontrol: one-negative-eigenvalue well-signed matrices need not form a convex set.
 # Scale midpoint by 2 to avoid fractions: H=[[-9,-2],[-2,-9]].
 detA=(-10)*1-1;detB=1*(-10)-1;detH=81-4;traceH=-18
 assert detA==detB==-11 and detH==77 and traceH<0
 out['negative_controls']['well_signed_signature_not_convex']={'endpoint_determinants':[detA,detB],'twice_midpoint_determinant':detH,'twice_midpoint_trace':traceH}
 out['status']='PASS: partial results and controls only; exact existence question remains unresolved'
 print(json.dumps(out,indent=2,sort_keys=True))
 return out
if __name__=='__main__':main()
