from itertools import product
import json
P=20; S={0}; sums=[S]
for m in range(1,7):
 S={(a+b)%P for a in S for b in range(7,14)}; sums.append(S)
def shift(S,a):return {(x+a)%20 for x in S}
def triple_universal(lens):
 for b,c in product(range(20), repeat=2):
  if not (sums[lens[0]] & shift(sums[lens[1]],b) & shift(sums[lens[2]],c)):
   return False,[0,b,c]
 return True,None
def double_universal(lens):
 # four arms, with centers joined by one edge
 for b,c,d in product(range(20), repeat=3):
  A=sums[lens[0]] & shift(sums[lens[1]],b)
  B=shift(sums[lens[2]],c)&shift(sums[lens[3]],d)
  if not any((y-x)%20 in sums[1] for x in A for y in B):return False,[0,b,c,d]
 return True,None
r={'path_sumsets':[sorted(s) for s in sums], 'tripods':{},'double_stars':{}}
for ls in product(range(1,4),repeat=3):
 if tuple(sorted(ls))==ls:r['tripods'][str(ls)]=triple_universal(ls)
for ls in [(1,2,2,2),(2,2,2,2),(1,3,1,3),(1,2,2,3),(1,1,3,3),(1,3,2,2)]:r['double_stars'][str(ls)]=double_universal(ls)
print(json.dumps(r,indent=2))
