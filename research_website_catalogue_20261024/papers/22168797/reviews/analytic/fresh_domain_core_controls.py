"""Further exact local controls, independently constructed from printed graphs."""
from pathlib import Path
from itertools import product
from fractions import Fraction as F
import sympy as s
import networkx as nx
import json
P=Path(__file__).resolve().parent;out={}
p=s.symbols('p0:4');si,gi=s.symbols('si gi')
def xor(h):
 v=0
 for x in h:v^=x
 return v
def qt(h,split):return s.prod(p[i] for i in range(4))*([1,si,gi,si][xor(h[i] for i in split)])
table={}
for name,split in [('A',(0,1)),('B',(0,2)),('C',(0,3))]:
 f=s.factor(qt((1,1,1,1),split)-qt((1,1,3,3),split));g=s.factor(qt((1,1,1,1),split)-qt((1,1,3,3),split)-qt((1,3,3,1),split)+qt((1,3,1,3),split))
 assert s.expand(f-(0 if name=='A' else s.prod(p)*(1-gi)))==0
 assert s.expand(g-(2*s.prod(p)*(1-gi) if name=='B' else 0))==0
 table[name]={'F':str(f),'G':str(g)}
out['quartet_identities']=table
templates={'cycle': [('S','X'),('S','X')], 'theta0':[('S','U'),('S','V'),('U','X'),('V','X'),('U','V')], 'theta1':[('S','U'),('S','X'),('V','X'),('U','V'),('U','V')], 'theta2':[('S','U'),('S','V'),('U','X0'),('V','X0'),('U','X1'),('V','X1')], 'theta3':[('S','U'),('S','X0'),('V','X0'),('U','X1'),('V','X1'),('U','V')]}
expect={'cycle':[[0],[1]],'theta0':[[2,3],[3,4]],'theta1':[[2,3],[2,4]],'theta2':[[2,3],[2,5],[3,4],[4,5]],'theta3':[[2],[4]]}
checks={}
for name,arcs in templates.items():
 valid=[]
 for bits in product([0,1],repeat=len(arcs)):
  ed=[('r','S'),('r','L0')]
  for i,((a,b),occupied) in enumerate(zip(arcs,bits)):
   if occupied:ed.extend([(a,f'P{i}'),(f'P{i}',b),(f'P{i}',f'L{i+1}')])
   else:ed.append((a,b))
  sinks={b for a,b in arcs}-{a for a,b in arcs}
  for sink in sinks:ed.append((sink,'L_'+sink))
  g=nx.DiGraph(ed)
  if len(ed)!=len(g.edges) or not nx.is_directed_acyclic_graph(g):continue
  ret={v for v in g if g.in_degree(v)==2}
  if any((g.in_degree(v),g.out_degree(v)) not in [(0,2),(1,2),(2,1),(1,0)] for v in g):continue
  # No-omnian property computed from reconstructed directed incidences, not clauses.
  if any(a in ret or sum(v in ret for v in g.successors(a))>1 for a,b in g.edges if b in ret):continue
  valid.append(frozenset(i for i,x in enumerate(bits) if x))
 minimal=sorted([sorted(A) for A in valid if not any(B<A for B in valid)])
 assert minimal==expect[name],(name,minimal)
 checks[name]={'minimum_valid_occupancies':minimal,'valid_occupancy_count':len(valid)}
out['core_repair_incidence_controls']=checks
def physical(x):a,b=x;return 0<a<1 and 0<b<1 and b>2*a-1
def ct(x):a,b=x;return 0<a<1 and a*a<b<1
grid=[(F(i,12),F(j,12)) for i in range(1,12) for j in range(1,12) if physical((F(i,12),F(j,12)))]
for a,b in product(grid,repeat=2):assert physical((a[0]*b[0],a[1]*b[1]))
# Exact gluing values for deliberately unequal two-sector incidence products.
gluing=[]
for A1,B1,A2,B2 in [(F(3,7),F(7,2),F(11,3),F(2,13)),(F(1,17),F(1,19),F(23),F(29))]:
 L=max(F(1),B1/A1**2,B2/A2**2);U=min(F(1),B1,B2);a=min(F(1,2),A1/2,A2/2,U/(2*(L+1)));b=(L*a*a+U)/2
 assert ct((a,b)) and ct((a/A1,b/B1)) and ct((a/A2,b/B2))
 gluing.append([str(x) for x in [A1,B1,A2,B2,a,b]])
out['physical_serial_product_grid_pairs']=len(grid)**2;out['strict_CT_gluing_examples']=gluing;out['all_controls_passed']=True
(P/'fresh_domain_core_controls.json').write_text(json.dumps(out,indent=2)+'\n');print('PASS quartet identities, independently reconstructed primitive repairs, serial product grid, strict CT gluing')
