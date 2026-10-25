"""Independent three-lineage no-merger CTMC, forced merger operators and recovery.
No published code imports. Rates are integer multiples of 4 log(2); quarter-grid
integration gives exact rational state probabilities and log(2)-scaled densities.
"""
from pathlib import Path
from fractions import Fraction as F
from collections import defaultdict,Counter
from itertools import product
import random,json,networkx as nx
base=Path(__file__).parent;graphs=json.loads((base/'generated-graphs.json').read_text());rng=random.Random(2272954503);count=Counter()
for rec in graphs:
 g=nx.DiGraph(rec['edges']);samples=[(int(x),j) for x,m in rec['sample_multiplicities'].items() for j in range(m)]
 iv=[v for v in nx.topological_sort(g) if g.out_degree(v)];age={v:F(len(iv)-j) for j,v in enumerate(iv)}
 ev={t:v for v,t in age.items()};rr=[v for v in g if g.in_degree(v)==2];gamma={v:rng.choice([F(1,2),F(2,5)]) for v in rr}
 rates={e:4*rng.randint(1,3) for e in g.edges};rates[(None,0)]=4
 maxage=max(age.values());bounds=sorted(set(age.values())|{F(j,2) for j in range(1,int(2*maxage))})
 def rate(e,t):return rates[e]*(1+(int(2*t)%2)) # one unequal demographic change in each half-epoch
 def decay(states,lo,hi):
  out={}
  for es,p in states.items():
   mult=Counter(es);r=sum(n*(n-1)//2*rate(e,(lo+hi)/2) for e,n in mult.items());expo=r*(hi-lo);assert expo.denominator==1
   out[es]=p*F(1,2**int(expo))
  return out
 def at_event(states,v):
  def choices(e):
   if e[0]!=v:return [(e,F(1))]
   ps=list(g.predecessors(v))
   if len(ps)==0:return [((None,v),F(1))]
   if len(ps)==1:return [((ps[0],v),F(1))]
   return [((ps[0],v),gamma[v]),((ps[1],v),1-gamma[v])]
  out=defaultdict(F)
  for es,p in states.items():
   for opts in product(*(choices(e) for e in es)):
    w=p
    for e,x in opts:w*=x
    out[tuple(e for e,x in opts)]+=w
  return out
 def prop(states,lo,hi,before=False):
  for t in [x for x in bounds if lo<x<hi]+[hi]:
   states=decay(states,lo,t)
   if t in ev and not (t==hi and before):states=at_event(states,ev[t])
   lo=t
  return states
 def initial(labels):return {tuple((next(g.predecessors(x)),x) for x,j in labels):F(1)}
 def witness(v):
  while g.out_degree(v):v=next(c for c in g.successors(v) if g.in_degree(c)==1)
  return (v,0)
 def survival(e,lo,hi):
  val=F(1)
  for t in [x for x in bounds if lo<x<hi]+[hi]:
   exponent=rate(e,(lo+t)/2)*(t-lo);assert exponent.denominator==1
   val*=F(1,2**int(exponent));lo=t
  return val
 for v in rr:
  descendants=nx.descendants(g,v);labels=[s for s in samples if s[0] in descendants]
  if len(labels)<2:continue
  a=witness(v);b=rng.choice([s for s in labels if s!=a]);ps=list(g.predecessors(v));p1=min(ps,key=age.get);p2=max(ps,key=age.get)
  z=witness(next(c for c in g.successors(p1) if c!=v));h=age[v];a1=age[p1];a2=age[p2];gam=gamma[v] if ps[0]==p1 else 1-gamma[v]
  pre=prop(initial([a,b,z]),F(0),h,True);q3=sum(p for es,p in pre.items() if es[0]==es[1] and es[0]!=es[2]);assert q3>0
  pairpre=prop(initial([a,b]),F(0),h,True);q=sum(p for es,p in pairpre.items() if es[0]==es[1]);assert q>0
  for t in (h+F(1,4),a1-F(1,4)):
   one=prop(initial([a,b,z]),F(0),t);merged=defaultdict(F)
   for es,p in one.items():
    if es[0]==es[1]:merged[(es[0],es[2])]+=p*rate(es[0],t)
   u=F(1,4);later=prop(merged,t,a1+u);D=sum(p*rate(es[0],a1+u) for es,p in later.items() if es[0]==es[1])
   ordinary=(next(g.predecessors(p1)),p1) if g.in_degree(p1) else (None,p1)
   A1=survival((p1,v),h,t);lam1=rate((p1,v),t);lamo=rate(ordinary,a1+u)
   expected=q3*gam**2*lam1*A1*lamo*survival(ordinary,a1,a1+u)
   assert D==expected,(v,t,D,expected)
   g1scaled=D/(q3*gam**2*lamo*survival(ordinary,a1,a1+u));assert g1scaled/A1==lam1
   pair=prop(initial([a,b]),F(0),t);f=sum(p*rate(es[0],t) for es,p in pair.items() if es[0]==es[1])
   g2=(f/q-gam**2*g1scaled)/(1-gam)**2
   assert g2/survival((p2,v),h,t)==rate((p2,v),t)
   count['exact_density_and_two_arm_recoveries']+=1
  count['exposed_reticulations']+=1
  if q3!=q:count['nontrivial_triple_vs_pair_normalization']+=1
  # Independently exercise longer-arm subtraction, including bypass and upper reticulation.
  blob=next(bb for bb in nx.biconnected_components(g.to_undirected()) if v in bb and len(bb)>2)
  ancestors=[r for r in rr if r!=v and r in blob and nx.has_path(g,r,v)]
  current=prop(initial([a,b]),F(0),a1)
  observed=sum(p for es,p in current.items() if es[0]==es[1])
  q2start=q*(1-gam)**2*survival((p2,v),h,a1)
  path=(next(g.predecessors(p1)),p1) if g.in_degree(p1) else (None,p1)
  if ancestors:
   known={(path,path):q*gam**2*survival((p1,v),h,a1)}
  else:scalar=observed-q2start
  last=a1
  # Fine quarter grid contains every biological/demographic boundary and interior cut.
  for jj in range(int(4*a1)+1,int(4*a2)):
   end=F(jj,4);before=decay(current,last,end)
   if ancestors:
    assert all((p2,v) not in es for es in known)
    known=decay(known,last,end)
   else:
    exponent=rate(path,(last+end)/2)*(end-last);assert exponent.denominator==1
    scalar*=F(1,2**int(exponent))
   beforeq=sum(p for es,p in before.items() if es[0]==es[1])
   current=at_event(before,ev[end]) if end in ev else before
   afterq=sum(p for es,p in current.items() if es[0]==es[1])
   if ancestors:
    if end in ev:known=at_event(known,ev[end])
    kq=sum(p for es,p in known.items() if es[0]==es[1])
    kf=sum(p*rate(es[0],end) for es,p in known.items() if es[0]==es[1])
   else:
    if end in ev:
     e=ev[end]
     if path[0]==e:
      assert g.in_degree(e)<2
      scalar+=afterq-beforeq
      path=(next(g.predecessors(e)),e) if g.in_degree(e) else (None,e)
     else:assert afterq==beforeq
    kq=scalar;kf=scalar*rate(path,end)
   observedf=sum(p*rate(es[0],end) for es,p in current.items() if es[0]==es[1])
   remainder=afterq-kq
   assert remainder==q2start*survival((p2,v),a1,end)>0
   assert (observedf-kf)/remainder==rate((p2,v),end)
   count['longer_arm_exact_subtractions']+=1
   last=end
  count['longer_arm_with_upper_reticulation' if ancestors else 'longer_arm_with_bypass_allowed']+=1
  # A deterministic anchor independently checks the oriented inheritance formula.
  az=prop(initial([a,z]),F(0),a1);qa=sum(p for es,p in az.items() if es[0]==es[1]);assert qa==gam
  count['oriented_anchor_weights']+=1
out={'status':'PASS','seed':2272954503,'counts':dict(count),'scope':'Fresh exact three-lineage forward survival, route enumeration and forced ordered mergers on all exposed reticulations in the 160 generated networks. Full finite demographic words change at every half integer. Two early-arm test times per reticulation; longer arms recovered on every quarter-grid cut, including bypass and known ancestor-reticulation propagation. This is bounded corroboration, not universal proof.'}
(base/'triple-controls.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
