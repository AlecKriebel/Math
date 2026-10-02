"""Finite formulation checks for an already published theorem, not a new proof."""
from collections import Counter
from itertools import combinations,product
import json
N=0
def ck(b):
 global N
 N+=1
 assert b
def flat(T):return tuple(sorted(T[0]+T[1]))
def F(T):
 a=T[0]+T[1];values=tuple(sorted(set(a)));return values,tuple(a.count(v) for v in values)
def d(M):
 c=Counter(M);return tuple(sorted(tuple(c)+tuple(c.values())))
def period(T):
 seen={};i=0
 while T not in seen and i<200:
  seen[T]=i;T=F(T);i+=1
 ck(T in seen);return i-seen[T]
def main():
 arrays=0
 for n in range(1,5):
  for top in combinations(range(1,8),n):
   for bottom in product(range(1,8),repeat=n):
    T=(top,bottom);ck(flat(F(T))==d(flat(T)));arrays+=1
 expected=[((1,),(1,)),((1,),(2,)),((1,2),(1,1)),((1,2),(3,1)),((1,2,3),(2,1,1)),((1,2,3),(3,2,1)),((1,2,3),(2,2,2)),((1,2,3),(1,4,1)),((1,2,3,4),(3,1,1,1)),((1,2,3,4),(4,1,2,1)),((1,2,3,4),(3,2,1,2)),((1,2,3,4),(2,3,2,1))]
 for a,b in zip(expected,expected[1:]):ck(F(a)==b)
 ck(F(expected[-1])==expected[-1])
 examples=[]
 for T in [((1,),(1,)),((5,),(6,)),((6,),(7,))]:examples.append({'initial':T,'period':period(T)})
 ck([x['period'] for x in examples]==[1,2,3])
 periods=Counter();tested=0
 for n in (1,2):
  for top in combinations(range(1,7),n):
   for bottom in product(range(1,7),repeat=n):
    q=period((top,bottom));ck(q in (1,2,3));periods[q]+=1;tested+=1
 for z in (10,123,10**6,10**12):
  T=((z,),(z,));ck(F(T)==((z,),(2,)));ck(flat(F(T))==d(flat(T)))
 print(json.dumps({'problem_id':3048,'status':'PASS','proof_attempt_turns':0,'exact_assertions':N,'array_translation_cases':arrays,'source_orbit_transitions':len(expected),'cycle_examples':examples,'small_orbits_checked':tested,'observed_period_counts':dict(sorted(periods.items())),'scope':'Finite source-alignment controls only; universal periodicity and period bound are credited to published literature.'},indent=2))
if __name__=='__main__':main()
