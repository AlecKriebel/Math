"""Exact two-vertex-separator state controls; stdlib only."""
import itertools as it,json,random
from verify_turn1 import arb
from verify_turn2 import colored_trees
N=0
def check(x):
 global N
 N+=1
 assert x

def forest_state(V,es,u=0,v=1):
 parent={x:x for x in V};deg={x:0 for x in V}
 def f(x):
  while parent[x]!=x:x=parent[x]
  return x
 for a,b in es:
  deg[b]+=1
  if deg[b]>1:return None
  x,y=f(a),f(b)
  if x==y:return None
  parent[x]=y
 roots={f(x) for x in V}
 if not roots<={f(u),f(v)}:return None
 return len(roots),deg[u],deg[v]

def states(V,A,side):
 out={}
 for es in it.product(*[[None]+[e for e in T if set(e)<=V and not (side==2 and set(e)<={0,1})] for T in A]):
  picked=[e for e in es if e is not None];z=forest_state(V,picked)
  if z is not None:
   bits=sum(1<<j for j,e in enumerate(es) if e is not None);out[(bits,)+z]=tuple(picked)
 return out

def interface(V1,V2,A):
 s1=states(V1,A,1);s2=states(V2,A,2);full=(1<<len(A))-1
 for mask,c,x,y in s1:
  for z in range(2):
   for w in range(2):
    key=(full^mask,3-c,z,w)
    if x+z<=1 and y+w<=1 and key in s2:
     check(arb(V1|V2,s1[(mask,c,x,y)]+s2[key]));return True
 return False

def direct(V,A):return any(arb(V,es) for es in it.product(*A))

def main():
 V1={0,1,2};V2={0,1,3};V=V1|V2;H={(0,2),(1,2),(0,3),(1,3)};T=colored_trees(V,H);check(len(T)==16);small=0
 for ix in it.combinations_with_replacement(range(len(T)),3):
  A=[T[i] for i in ix];check(interface(V1,V2,A)==direct(V,A));small+=1
 theta=[[(2,0),(2,1),(0,3),(1,4)],[(3,0),(3,1),(1,2),(0,4)],[(4,0),(4,1),(0,2),(1,3)],[(0,2),(2,1),(0,3),(1,4)]]
 V={0,1,2,3,4};V1={0,1,2};V2={0,1,3,4}
 for T in theta:check(arb(V,T))
 check(forest_state(V1,[(2,0),(2,1)])==(1,1,1));check(forest_state(V2,[(0,3),(1,4)])==(2,0,0))
 check(interface(V1,V2,theta));check(direct(V,theta));check(forest_state({0,1},[(0,1),(1,0)]) is None)
 rng=random.Random(300040084);outcomes={True:0,False:0}
 arcs=[(u,v) for u in V for v in V if (u in [0,1]) != (v in [0,1])]+[(0,1),(1,0)]
 for rep in range(500):
  A=[tuple(rng.sample(arcs,rng.randrange(1,6))) for _ in range(4)]
  x=interface(V1,V2,A);y=direct(V,A);check(x==y);outcomes[x]+=1
 check(outcomes[True]>0 and outcomes[False]>0)
 # Explicit no-arc and singleton-color controls outside the original promise.
 check(not interface(V1,V2,[[]]*4));check(not direct(V,[[]]*4))
 print(json.dumps({'problem_id':30004008,'turn':4,'status':'PASS','exact_assertions':N,'exhaustive_four_cycle_color_multisets':small,'random_separated_graph_positive':outcomes[True],'random_separated_graph_negative':outcomes[False],'explicit_original_theta_fixture':True,'scope':'Finite verification of the exact separator characterization. No all-size theta theorem or full resolution claimed.'},indent=2))
if __name__=='__main__':main()
