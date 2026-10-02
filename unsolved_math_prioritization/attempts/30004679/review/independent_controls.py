#!/usr/bin/env python3
"""Independent finite prefix/representation controls; not proofs of jump degrees."""
from itertools import combinations,product
from collections import Counter
import json
C=Counter()
def ck(v,k):
 C[k]+=1
 if not v:raise AssertionError(k)
def pref(a,b):return len(a)<=len(b) and tuple(b[:len(a)])==tuple(a)
def compatible(a,b):return pref(a,b) or pref(b,a)
def member(basis,h):return any(pref(t,h) for t in basis)
def subseq(a,b):
 it=iter(b)
 return all(any(y==x for y in it) for x in a)
# Complete bounded shifted-name map and tail-decoding diagrams.
options=[(),((0,),),((1,2),),((2,4),),((0,1),(3,))]
for menu in product(options,repeat=3):
 Q=[]
 for i,basis in enumerate(menu):
  for t in basis:
   for alpha in combinations(range(t[0]),i):Q.append(alpha+t)
 for h in combinations(range(9),5):
  ck(member(Q,h)==any(member(b,h[i:]) for i,b in enumerate(menu)),'shifted_name_inverse_image')
  for i,basis in enumerate(menu):
   for f in combinations(h[i:],2):
    g=h[:i]+f
    ck(subseq(g,h) and g[i:]==f,'tail_prepend_decoding')
    ck(not member(basis,f) or member(Q,g),'all_output_prefix_implication')
# The unshifted union counterexample and its shifted simplification.
for h in combinations(range(11),5):
 ck(any(h[0]==i for i in range(11)),'ordinary_union_covers_test_prefixes')
 ck(any(h[i]==i for i in range(5))==(h[0]==0),'shifted_singleton_simplification')
# The easy uncountable menu example: finite restrictions recover every bit.
for bits in product((0,1),repeat=5):
 def belongs(pair):
  a,b=pair
  return a%2==0 and b==a+1 and a//2<len(bits) and bool(bits[a//2])
 for e in range(5):ck(belongs((2*e,2*e+1))==bool(bits[e]),'menu_parameter_recovery')
 for h in combinations(range(10),5):
  ck(not belongs((h[0],h[2])),'no_landing_prefix_witness')
  ck(not belongs((2*h[0],2*h[1])),'common_even_avoider')
# Finite-global-arity coloring recovered by compatible positive witnesses.
for arity in [1,2]:
 ts=list(combinations(range(5),arity))
 for bits in product((0,1),repeat=len(ts)):
  # Redundant deeper cylinders may arrive before the deciding parent cylinder.
  basis=[t+(7,) for t,b in zip(ts,bits) if b]+[t for t,b in zip(ts,bits) if b]
  for t,b in zip(ts,bits):ck(any(compatible(t,u) for u in basis)==bool(b),'arity_color_compatibility')
# First-value lookahead: explicit pairs defeat each proposed global bound.
for m in range(1,201):
 n=m+2;a=tuple(n+2*i for i in range(n+1));yes=a+(a[-1]+1,);no=a+(a[-1]+2,)
 ck(yes[:m]==no[:m],'unbounded_arity_same_prefix')
 ck(yes[yes[0]+1]==yes[yes[0]]+1,'lookahead_positive_extension')
 ck(no[no[0]+1]!=no[no[0]]+1,'lookahead_negative_extension')
 ck(all(x<y for x,y in zip(yes,yes[1:])) and all(x<y for x,y in zip(no,no[1:])),'lookahead_valid_sequences')
# Positive finite clopen unions: disjoint-cone complement enumeration.
words=[()]+[t for j in [1,2] for t in combinations(range(7),j)]
pool=[(0,),(1,3),(2,4),(3,),(4,6)]
for mask in range(1<<len(pool)):
 basis=[t for i,t in enumerate(pool) if mask>>i&1]
 negative=[s for s in words if not any(compatible(s,t) for t in basis)]
 redundant=basis+[t+(8,) for t in basis]
 ck(negative==[s for s in words if not any(compatible(s,t) for t in redundant)],'name_redundancy_invariance')
 for h in combinations(range(7),3):
  ck(member(basis,h)!=member(negative,h),'positive_complement_partition')
# Every-name dovetail logic with extra contained cones and arbitrary finite delays.
for bits in product((0,1),repeat=6):
 for offset in range(7):
  names=[[],[]]
  for e,b in enumerate(bits):
   names[b].append(((e*7+offset)%19+1,(e,e+2)))
   names[b].append(((e*11+offset)%23+20,(e,)))
  for e,b in enumerate(bits):
   h=(e,e+1,e+2);found=None
   for stage in range(45):
    hits=[side for side in [0,1] for when,t in names[side] if when==stage and pref(t,h)]
    if hits:found=hits[0];break
   ck(found==b,'delayed_redundant_name_decoding')
# Nonclopen singleton-complement failure: each prefix meets the open side.
for length in range(301):
 sigma=tuple(range(length));w=sigma+(length+1,)
 ck(compatible(sigma,w) and w!=tuple(range(length+1)),'singleton_complement_no_disjoint_cone')
print(json.dumps({'status':'PASS','assertions':sum(C.values()),'checks_by_kind':dict(sorted(C.items())),'scope':'Independent finite syntax and representation controls; infinite Ramsey, ordinal jumps and imported theorems are reviewed analytically'},indent=2,sort_keys=True))
