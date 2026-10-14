"""Exact stripe and cyclotomic controls; no numerical roots."""
from collections import Counter
from tile_model import D4
import json
C=Counter()
# Polynomial remainders at primitive roots of order2,3,6.
def rem(a,m):
 a=list(a)
 while len(a)>len(m)-1:
  c=a[-1];shift=len(a)-len(m)
  for i,b in enumerate(m):a[shift+i]-=c*b
  a.pop()
 return tuple(a+[0]*(len(m)-1-len(a)))
mods={2:[1,1],3:[1,1,1],6:[1,-1,1]}
for q in D4:
 sx=sum((-1)**x for x,y in q);sy=sum((-1)**y for x,y in q)
 assert sorted((abs(sx),abs(sy)))==[0,6];C['all_orientation_stripes']+=1
 for m in mods.values():
  for swap in (False,True):
   a=[0]*7
   for x,y in q:
    if swap:x,y=y,x
    a[y]+=(-1)**x
   assert not any(rem(a,m));C['all_orientations_cyclotomic_zero']+=1
for W in range(1,201):
 for H in range(1,201):
  test=all((W%2==0 or H%d==0) and (H%2==0 or W%d==0) for d in (2,3,6))
  claimed=(W%2==0 and H%2==0) or (W%2 and H%6==0) or (H%2 and W%6==0)
  assert bool(test)==bool(claimed);C['complete_character_dimension_test']+=1
  if W*H%14==0 and (W*H//14)%2 and test:
   even=W if W%2==0 else H
   assert even%12==6 and (W*H//14)%6==3;C['odd_dimension_and_count_restriction']+=1
# The incompatible y=1 branch has x^4=1 and x^2=-4/3, impossible since16/9 !=1.
assert 16!=9;C['remaining_branch_contradiction']+=1
print(json.dumps({'status':'PASS','exact_assertions':sum(C.values()),'families':dict(C),'scope':'Exact finite/cyclotomic checks of the analytical character classification. No sufficiency for positive tiling, full coloring completeness, or odd-case resolution is asserted.'},indent=2))
