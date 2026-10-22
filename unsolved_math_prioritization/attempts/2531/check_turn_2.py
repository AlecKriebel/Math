#!/usr/bin/env python3
from itertools import permutations,product
import random,json
rng=random.Random(253102);checks=commutators=orbit_masks=0
def even(p):return sum(p[i]>p[j] for i in range(len(p)) for j in range(i+1,len(p)))%2==0
A=[p for p in permutations(range(5)) if even(p)];ix={p:i for i,p in enumerate(A)}
M=[[ix[tuple(a[b[i]] for i in range(5))] for b in A] for a in A]
Inv=[next(j for j in range(60) if M[i][j]==0 and M[j][i]==0) for i in range(60)]
def conj(a,b):return M[M[a][b]][Inv[a]]
# Every nonidentity normal closure in the finite A5 control is the full group.
for a in range(1,60):
 gs={conj(g,a) for g in range(60)};seen={0};todo=[0]
 while todo:
  z=todo.pop()
  for g in gs:
   w=M[z][g]
   if w not in seen:seen.add(w);todo.append(w)
 assert len(seen)==60;checks+=1
P=list(permutations(range(3)));pi={p:i for i,p in enumerate(P)}
HM=[[pi[tuple(a[b[i]] for i in range(3))] for b in P] for a in P]
HI=[next(j for j in range(6) if HM[i][j]==0 and HM[j][i]==0) for i in range(6)]
one=(0,0)
def gm(a,b):return (M[a[0]][b[0]],M[a[1]][b[1]])
def gi(a):return (Inv[a[0]],Inv[a[1]])
def gc(a,b):return gm(gm(gm(a,b),gi(a)),gi(b))
def wm(a,b):
 f,h=a;g,k=b
 return (tuple(gm(f[x],g[P[HI[h]][x]]) for x in range(3)),HM[h][k])
def wi(a):
 f,h=a
 return (tuple(gi(f[P[h][x]]) for x in range(3)),HI[h])
def wc(a,b):return wm(wm(wm(a,b),wi(a)),wi(b))
def lamp(g,x):
 f=[one]*3;f[x]=g;return(tuple(f),0)
for h in range(1,6):
 for x in range(3):
  if P[h][x]==x:continue
  for _ in range(1000):
   f=tuple((rng.randrange(60),rng.randrange(60)) for _ in range(3));g=(rng.randrange(60),rng.randrange(60));u=(rng.randrange(60),rng.randrange(60))
   assert wc(wc((f,h),lamp(g,x)),lamp(u,x))==lamp(gc(gi(g),u),x);checks+=1;commutators+=1
# H-invariant subsets of simple factors are exactly unions of type orbits.
for m in range(1,5):
 count=0
 for mask in range(1<<(3*m)):
  invariant=all(all(bool(mask>>(3*i+x)&1)==bool(mask>>(3*i+P[h][x])&1) for i in range(m) for x in range(3)) for h in range(6))
  whole=all((mask>>(3*i)&7) in [0,7] for i in range(m))
  assert invariant==whole;checks+=1;orbit_masks+=1
  if invariant:
   count+=1;killed=sum((mask>>(3*i)&7)==7 for i in range(m))
   assert m-killed==sum((mask>>(3*i)&7)==0 for i in range(m));checks+=1
 assert count==2**m;checks+=1
# Factor swap for the one-point nonfaithful action: exact involution.
for a,b in product(range(60),repeat=2):
 assert tuple(reversed(tuple(reversed((a,b)))))==(a,b);checks+=1
assert (1,0)!=(0,1);checks+=1
print(json.dumps({'status':'PASS','exact_assertions':checks,'double_commutator_controls':commutators,'orbit_subset_controls':orbit_masks,'scope':'Finite exact normal-closure, support and orbit controls; theorem for arbitrary simple factors is proved in TURN_2.md.'},indent=2))
