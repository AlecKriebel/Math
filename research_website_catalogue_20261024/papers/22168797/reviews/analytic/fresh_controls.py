"""Fresh exact controls from printed definitions; imports no submitted code."""
from pathlib import Path
from fractions import Fraction as F
from itertools import product
from math import comb
from datetime import datetime,timezone
import json
import sympy as s
import networkx as nx
P=Path(__file__).resolve().parent
O={'utc':datetime.now(timezone.utc).isoformat(),'boundary':'Independent finite controls, not exhaustive classification.'}
def xor(items):
 z=0
 for x in items:z^=x
 return z
def spec(pair,h):return 1 if h==0 else pair[1] if h==2 else pair[0]
def fourier(arcs,ret,weights,pairs,h):
 if xor(h):return 0
 total=0;incoming=[[a for a in arcs if a[1]==v] for v in ret]
 for selected in product(*incoming):
  keep=[a for a in arcs if a[1] not in ret or a in selected];g=nx.DiGraph(keep);term=1
  for a in selected:term*=weights[a]
  for a in keep:
   desc=nx.descendants(g,a[1])|{a[1]};term*=spec(pairs[a],xor(h[i] for i in range(3) if 'L'+str(i) in desc))
  total+=term
 return total
def census(arcs,ret):
 children=[b for a,b in arcs if a=='r'];heads={a for a in arcs if a[0]!='r' and a[1] in ret};ordinary={frozenset(a) for a in arcs if a[0]!='r' and a[1] not in ret};a,b=children
 if a in ret:heads.add((b,a))
 elif b in ret:heads.add((a,b))
 else:ordinary.add(frozenset(children))
 nodes=set(x for a in arcs for x in a)-{'r'};leaves={v for v in nodes if v.startswith('L')};valid=[]
 for edge,headed in [(tuple(e),False) for e in ordinary]+[(e,True) for e in heads]:
  a,b=edge;fixed=set(heads);und=set(ordinary)
  if headed:fixed.remove(edge)
  else:und.remove(frozenset(edge))
  fixed|={('r',a),('r',b)};und=[tuple(e) for e in und]
  for bits in product([0,1],repeat=len(und)):
   edges=list(fixed)+[(a,b) if bit==0 else (b,a) for (a,b),bit in zip(und,bits)];g=nx.DiGraph(edges)
   if not nx.is_directed_acyclic_graph(g) or nx.descendants(g,'r')!=nodes:continue
   if any((g.in_degree(v),g.out_degree(v))!=((2,1) if v in ret else (1,0) if v in leaves else (1,2)) for v in nodes):continue
   dominated=False
   for v in nodes-leaves:
    gg=g.copy();gg.remove_node(v)
    if not nx.descendants(gg,'r')&leaves:dominated=True;break
   if dominated:continue
   tc=all(any(w not in ret for w in g.successors(v)) for v in g if g.out_degree(v))
   valid.append({'root_edge':list(edge),'tree_child':tc,'arcs':sorted(edges)})
 return {'admissible':len(valid),'tree_child':sum(x['tree_child'] for x in valid),'non_tree_child':sum(not x['tree_child'] for x in valid),'rootings':valid}
names='a b c d e f'.split();pairs={n:s.symbols(n+'s '+n+'g') for n in names};lam=s.symbols('lam')
def sun(h):
 x,y,z=h;a,b,c,d,e,f=[pairs[n] for n in names]
 return spec(a,x)*spec(b,y)*spec(c,z)*(lam*spec(f,y)*spec(d,z)+(1-lam)*spec(f,x)*spec(e,z))
ti=s.factor(sun((1,3,2))**2*sun((2,2,0))-sun((1,1,0))**2*sun((2,0,2))*sun((0,2,2)))
want=-pairs['a'][0]**2*pairs['b'][0]**2*pairs['a'][1]*pairs['b'][1]*pairs['c'][1]**2*pairs['f'][0]**2*lam*(1-lam)*pairs['d'][1]*pairs['e'][1]*(1-pairs['f'][1])**2
assert s.expand(ti-want)==0
rows=[(0,1,1),(0,2,2),(1,0,1),(1,1,0),(1,2,3),(1,3,2),(2,0,2),(2,1,3),(2,2,0)]
pt={x:s.Rational(1,3) if name=='f' else s.Rational(1,2) for name,pair in pairs.items() for x in pair};pt[lam]=s.Rational(1,2)
q=[sun(h) for h in rows];J=s.Matrix(q).jacobian([x for p in pairs.values() for x in p]+[lam]).subs(pt);assert J.rank()==9
O['sunlet']={'Ti':str(ti),'common_coordinates':[str(x.subs(pt)) for x in q],'rank':9,'pivot_columns':list(J.rref()[1])}
W=[('r','S'),('r','L0'),('S','U'),('S','V'),('U','X'),('V','Z'),('Z','X'),('U','V'),('Z','L1'),('X','L2')]
WP=[('r','S'),('r','L0'),('S','U'),('S','X0'),('V','X0'),('U','X1'),('V','X1'),('U','V'),('X0','L1'),('X1','L2')]
delta=F(1,2**30);sharp=[]
cases=[('W',W,['V','X'],F(1,7),[F(86779,80)*delta,F(320,253)*delta,F(114373,20240)*delta],{('S','V'):F(1,8),('U','V'):F(7,8),('Z','X'):F(15996,16339),('U','X'):F(343,16339)},(5,2,3)),('Wprime',WP,['X0','X1'],F(1,4),[F(16,3)*delta,F(32,9)*delta,F(96,5)*delta],{('V','X1'):F(1,2),('U','X1'):F(1,2),('V','X0'):F(1,6),('S','X0'):F(5,6)},(7,2,5))]
for tag,arcs,ret,rate,leaf,weights,expected in cases:
 ps={a:(leaf[int(a[1][1:])],)*2 if a[1].startswith('L') else (rate,rate) for a in arcs}
 assert all(0<a<1 and a*a<b<1 for a,b in ps.values())
 for h in product(range(4),repeat=3):
  count=sum(x!=0 for x in h);want=0 if xor(h) else 1 if count==0 else delta**2 if count==2 else F(4,5)*delta**3
  assert fourier(arcs,ret,weights,ps,h)==want,(tag,h)
 cs=census(arcs,ret);assert tuple(cs[k] for k in ['admissible','tree_child','non_tree_child'])==expected,(tag,cs)
 sympairs={a:s.symbols(tag+'_'+a[0]+'_'+a[1]+'_s '+tag+'_'+a[0]+'_'+a[1]+'_g') if not a[1].startswith('L') else (1,1) for a in arcs}
 variables=[v for a,pair in sympairs.items() if not a[1].startswith('L') for v in pair]
 sq=[fourier(arcs,ret,weights,sympairs,h) for h in rows];sj=s.Matrix(sq).jacobian(variables).subs({v:s.Rational(rate.numerator,rate.denominator) for v in variables});assert sj.rank()==9
 piv=list(sj.rref()[1]);sharp.append({'name':tag,'all64_coordinates_exact':True,'strict_CT':True,'rooting_census':cs,'rank':9,'minor_columns':[str(variables[i]) for i in piv],'minor_determinant':str(sj[:,piv].det())})
O['weak_sharpness']=sharp
core=[(2,1,1),(5,1,2),(5,1,2),(6,2,4),(6,2,2)]
counts={str((k,e)):sum(r*sum(comb(q,j)*comb(k-e-j+m-1,m-1) for j in range(min(q,k-e)+1)) for m,q,r in core) for k,e in [(4,1),(4,0),(5,1),(5,0)]};assert list(counts.values())==[831,1983,1983,4155];O['completion_counts']=counts
us,vs,ug,vg=s.symbols('us vs ug vg');det=s.Matrix([us/vs,us*vs,ug/vg,ug*vg]).jacobian([us,vs,ug,vg]).det();assert s.simplify(det-4*us*ug/(vs*vg))==0;O['cherry_determinant']=str(s.factor(det))
O['all_controls_passed']=True;(P/'fresh_controls.json').write_text(json.dumps(O,indent=2)+'\n');print('PASS fresh Ti, triangle rank, both weak exact64-coordinate witnesses, rooting census, rank9, completion counts and cherry determinant')
