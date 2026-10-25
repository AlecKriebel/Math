"""Independent literal graph and exact full-map check. No submitted imports."""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
from datetime import datetime,timezone
import json,networkx as nx
P=Path(__file__).resolve().parent
S=[('r','S'),('r','L0'),('S','U'),('S','X'),('V','A'),('A','X'),('A','L1'),('U','B'),('B','V'),('B','L2'),('U','V'),('X','L3')]
T=[('r','S'),('r','L2'),('S','U'),('S','V'),('U','A'),('A','X'),('A','L0'),('V','B'),('B','X'),('B','L1'),('U','V'),('X','L3')]
ret=['V','X']
def xor(xs):
 z=0
 for x in xs:z^=x
 return z
def physical(arcs):
 g=nx.Graph();g.add_nodes_from((v,{'label':int(v[1:]) if v.startswith('L') else None}) for v in set(sum(([a,b] for a,b in arcs),[]))-{'r'})
 for a,b in arcs:
  if a!='r':g.add_edge(a,b,heads={b} if b in ret else set())
 children=[b for a,b in arcs if a=='r'];g.add_edge(*children,heads=set(children)&set(ret));return g
def expand(g):
 h=nx.Graph()
 for v,d in g.nodes(data=True):h.add_node(('v',v),kind='vertex',label=d['label'])
 for i,(a,b,d) in enumerate(g.edges(data=True)):
  h.add_node(('e',i),kind='edge',label=None)
  for v in (a,b):h.add_edge(('e',i),('v',v),head=v in d['heads'])
 return h
sg,tg=physical(S),physical(T);gm=nx.algorithms.isomorphism.GraphMatcher(expand(sg),expand(tg),node_match=lambda a,b:(a['kind'],a['label'])==(b['kind'],b['label']),edge_match=lambda a,b:a['head']==b['head']);assert gm.is_isomorphic()
mp={a[1]:b[1] for a,b in gm.mapping.items() if a[0]=='v'}
for a,b,d in sg.edges(data=True):assert tg.has_edge(mp[a],mp[b]) and {mp[v] for v in d['heads']}==tg.edges[mp[a],mp[b]]['heads']
# Physical parameters on the common mixed graph. Use CT equal-sector pairs,
# with rational perfect squares to split the two different root edges.
physical_pairs={frozenset((a,b)):(F(i+2,4*i+13)**2,)*2 for i,(a,b) in enumerate(sg.edges())}
def rooted_pairs(arcs,backmap):
 rootchildren=[b for a,b in arcs if a=='r'];out={}
 for a,b in arcs:
  edge=frozenset(backmap[v] for v in (rootchildren if a=='r' else (a,b)));x,y=physical_pairs[edge]
  if a=='r':
   import math
   x=F(math.isqrt(x.numerator),math.isqrt(x.denominator));y=F(math.isqrt(y.numerator),math.isqrt(y.denominator))
  out[a,b]=(x,y)
 return out
sp=rooted_pairs(S,{v:v for v in sg});tp=rooted_pairs(T,{v:k for k,v in mp.items()})
# Reticulation weights transported by headed physical edges, not root direction.
sw={('B','V'):F(2,7),('U','V'):F(5,7),('S','X'):F(3,8),('A','X'):F(5,8)}
tw={(mp[a],mp[b]):w for (a,b),w in sw.items()}
assert all(a in T for a in tw)
def q(arcs,pairs,weights,h):
 ans=F(0)
 for chosen in product(*[[a for a in arcs if a[1]==v] for v in ret]):
  keep=[a for a in arcs if a[1] not in ret or a in chosen];g=nx.DiGraph(keep);term=F(1)
  for a in chosen:term*=weights[a]
  for a in keep:
   desc=nx.descendants(g,a[1])|{a[1]};c=xor(h[i] for i in range(4) if 'L'+str(i) in desc)
   if c:term*=pairs[a][int(c==2)]
  ans+=term
 return ans
chars=[h for h in product(range(4),repeat=4) if xor(h)==0 and h<=tuple(3 if x==1 else 1 if x==3 else x for x in h)]
for h in product(range(4),repeat=4):
 if xor(h):continue
 assert q(S,sp,sw,h)==q(T,tp,tw,h),(h,q(S,sp,sw,h),q(T,tp,tw,h))
# Exact Jacobians of the independently evaluated four-switch polynomial maps.
def jac(arcs,omit_arms):
 ep={a:(F(2*i+3,8*i+17),F(3*i+5,11*i+23)) for i,a in enumerate(arcs)}
 for a in ep:
  if omit_arms and a[1].startswith('L'):ep[a]=(F(1),F(1))
 parents=[sorted([a for a in arcs if a[1]==v]) for v in ret];ls=[F(2,5),F(3,7)];vars=[(a,c) for a in arcs if not(omit_arms and a[1].startswith('L')) for c in range(2)];vi={v:i for i,v in enumerate(vars)};ans=[];vals=[]
 for h in chars:
  row=[F(0)]*(len(vars)+2);total=F(0)
  for bits in product([0,1],repeat=2):
   chosen=[parents[j][bits[j]] for j in range(2)];keep=[a for a in arcs if a[1] not in ret or a in chosen];g=nx.DiGraph(keep);factors=[];term=F(1)
   for j,b in enumerate(bits):term*=ls[j] if b else 1-ls[j]
   for a in keep:
    desc=nx.descendants(g,a[1])|{a[1]};c=xor(h[i] for i in range(4) if 'L'+str(i) in desc)
    if c:
     v=(a,int(c==2));term*=ep[a][v[1]];factors.append(v)
   total+=term
   for v in factors:
    if v in vi:row[vi[v]]+=term/ep[v[0]][v[1]]
   for j,b in enumerate(bits):row[len(vars)+j]+=term/ls[j] if b else -term/(1-ls[j])
  ans.append(row);vals.append(total)
 return ans,vals,[str(x) for x in vars]+['lambda_V','lambda_X']
def pivots(matrix):
 a=[list(r) for r in matrix];ids=list(range(len(a)));rs=[];cs=[];r=0
 for c in range(len(a[0])):
  p=next((i for i in range(r,len(a)) if a[i][c]),None)
  if p is None:continue
  a[p],a[r]=a[r],a[p];ids[p],ids[r]=ids[r],ids[p];v=a[r][c];a[r]=[x/v for x in a[r]]
  for i in range(r+1,len(a)):
   v=a[i][c]
   if v:a[i]=[x-v*y for x,y in zip(a[i],a[r])]
  rs.append(ids[r]);cs.append(c);r+=1
 return r,rs,cs
out={'utc':datetime.now(timezone.utc).isoformat(),'independence':'Literal arcs from manuscript Table 1 and target tuple; no submitted code imported. Specific ledger target received from root after independent raw-rank/quotient concern.','source_arcs':S,'target_arcs':T,'physical_mixed_isomorphism':mp,'all64_supported_Fourier_coordinates_equal':True,'transported_source_weights':{str(k):str(v) for k,v in sw.items()},'transported_target_weights':{str(k):str(v) for k,v in tw.items()},'common_physical_pairs':{str(sorted(k)):list(map(str,v)) for k,v in physical_pairs.items()},'rooted_parameters_in_strict_CT':all(0<a<1 and a*a<b<1 for a,b in list(sp.values())+list(tp.values())),'ranks':[]}
for name,arcs in [('source',S),('target',T)]:
 for omit in [True,False]:
  J,vals,vs=jac(arcs,omit);rank,rows,cols=pivots(J);torus=[[v*int(h[p] in (1,3)) if c==0 else v*int(h[p]==2) for p in range(4) for c in range(2)] for h,v in zip(chars,vals)];tr=pivots(torus)[0];fr=pivots([a+b for a,b in zip(J,torus)])[0]
  out['ranks'].append({'graph':name,'omit_selected_pendant_parameters':omit,'rank':rank,'torus_rank':tr,'rank_with_torus':fr,'quotient_rank':fr-tr,'pivot_rows':[list(chars[i]) for i in rows],'pivot_parameters':[vs[i] for i in cols]})
  print(name,omit,rank,tr,fr,fr-tr,flush=True)
assert out['rooted_parameters_in_strict_CT']
assert [r['rank'] for r in out['ranks']]==[14,17,13,17]
assert all(r['quotient_rank']==9 for r in out['ranks'])
(P/'fresh_false_exclusion.json').write_text(json.dumps(out,indent=2)+'\n');print('CONFIRMED: isomorphic physical maps; false rank exclusion caused by omitted arms')
# Exact polynomial identity: compare switching monomials after physical edge
# relabelling; each root half contributes half the root-edge exponent, so the
# pair represents its serial product. The two halves have the same sector.
from collections import Counter
import hashlib
def switching_monomials(arcs,backmap,h):
 rootchildren=[b for a,b in arcs if a=='r'];out=Counter()
 for chosen in product(*[[a for a in arcs if a[1]==v] for v in ret]):
  keep=[a for a in arcs if a[1] not in ret or a in chosen];g=nx.DiGraph(keep);ex=Counter()
  for a in keep:
   desc=nx.descendants(g,a[1])|{a[1]};c=xor(h[i] for i in range(4) if 'L'+str(i) in desc)
   if c:
    edge=tuple(sorted(backmap[v] for v in (rootchildren if a[0]=='r' else a)));ex[(edge,int(c==2))]+=F(1,2) if a[0]=='r' else 1
  assert all(v.denominator==1 if isinstance(v,F) else True for v in ex.values())
  wt=tuple(sorted((backmap[a],backmap[b]) for a,b in chosen))
  key=(wt,tuple(sorted((edge,c,int(e)) for (edge,c),e in ex.items())))
  out[key]+=1
 return sorted((str(k),v) for k,v in out.items())
mon=[]
for h in product(range(4),repeat=4):
 if xor(h):continue
 x=switching_monomials(S,{v:v for v in sg},h);y=switching_monomials(T,{v:k for k,v in mp.items()},h);assert x==y,h;mon.append({'characters':h,'monomials':x})
out['polynomial_identity']={'coordinates':len(mon),'all_switching_monomials_identical':True,'monomial_rows_sha256':hashlib.sha256(json.dumps(mon,sort_keys=True).encode()).hexdigest(),'scope':'All physical mixed-edge parameters and transported inheritance weights, not only the displayed rational point. The other 192 coordinates vanish by uniform-root conservation.'}
def all_rootings(arcs):
 g=physical(arcs);ns=set(g);leaves={v for v in ns if v.startswith('L')};ans=[]
 for e in g.edges():
  h=g.copy();heads=h.edges[e]['heads'];h.remove_edge(*e);ordinary=[];fixed=[('r',v) for v in e]
  for a,b,d in h.edges(data=True):
   if d['heads']:
    bhead=next(iter(d['heads']));fixed.append((b if bhead==a else a,bhead))
   else:ordinary.append((a,b))
  for bits in product([0,1],repeat=len(ordinary)):
   es=fixed+[(b,a) if bit else (a,b) for (a,b),bit in zip(ordinary,bits)];d=nx.DiGraph(es)
   if not nx.is_directed_acyclic_graph(d) or nx.descendants(d,'r')!=ns:continue
   if any((d.in_degree(v),d.out_degree(v))!=((2,1) if v in ret else (1,0) if v in leaves else (1,2)) for v in ns):continue
   if any(not (nx.descendants(nx.subgraph_view(d,filter_node=lambda w:w!=v),'r')&leaves) for v in ns-leaves):continue
   tc=all(any(w not in ret for w in d.successors(v)) for v in d if d.out_degree(v));ans.append(tc)
 return {'admissible_rootings':len(ans),'tree_child':sum(ans),'all_tree_child':bool(ans) and all(ans)}
out['strong_class_checks']={'source':all_rootings(S),'target':all_rootings(T)}
assert all(v['all_tree_child'] for v in out['strong_class_checks'].values())
(P/'fresh_false_exclusion.json').write_text(json.dumps(out,indent=2)+'\n');print('Exact switching-polynomial identity and all admissible rootings independently checked')
