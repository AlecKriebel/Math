"""Exact finite translation aid. Universal infinite assertions are proved in the corollary."""
from itertools import product
from pathlib import Path
import json,datetime
P=Path(__file__).resolve().parent
circleQ=lambda c,d:(c+d+2*c*d)%4
eps=lambda c:1 if c<2 else -1
counts={'circle_character_pairs':0,'binary_circle_pairs':0,'finite_family_pairs':0,'finite_base_associativity_triples':0}
for c,d in product(range(4),repeat=2):
 assert eps(circleQ(c,d))==eps(c)*eps(d)
 counts['circle_character_pairs']+=1
 assert circleQ(c,d)==(c^d)
 counts['binary_circle_pairs']+=1
for c,d,e in product(range(4),repeat=3):
 assert circleQ(circleQ(c,d),e)==circleQ(c,circleQ(d,e))
 counts['finite_base_associativity_triples']+=1
for q in (5,7):
 for c,a,d,b in product(range(4),range(q),range(4),range(q)):
  # Dietzel Theorem 5(iv), omega=-1, mu=+1; c written highbit lowbit.
  starQ=2*c*d%4
  starA=(((-1)**(c//2))*(1**(c%2))-1)*b%q
  old_circle=((c+d+starQ)%4,(a+b+starA)%q)
  candidate_swapped=((c+d+2*c*d)%4,(a+eps(c)*b)%q)
  assert old_circle==candidate_swapped
  counts['finite_family_pairs']+=1
assert eps(1)==1 and eps(2)==-1 and circleQ(1,1)==0
assert (1+1)%4==2
# Exact lambda witness: lambda_(0,1)(0,1)=(0,3).
assert (1+2*1)*1%4==3
result={'UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS','counts':counts,'scope':'Exhaustive finite-factor and finite-family translation checks; no numerical proof of infinite finiteness claims. Universal proof is CHECKABLE_OLD_COROLLARY_FINAL.md.','chosen_parameters':{'omega':-1,'mu':1,'q_tested':[5,7]}}
(P/'PRIORITY_TRANSLATION_CHECK_RESULT.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result))
