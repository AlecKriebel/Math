import itertools,json,hashlib
from pathlib import Path
N=0
def check(v):
 global N
 assert v;N+=1
def reduce(w):
 s=[]
 for a in w:
  if s and s[-1]+a==0:s.pop()
  else:s.append(a)
 return tuple(s)
def inverse(w):return tuple(-a for a in reversed(w))
def substitute(w,A):return reduce(itertools.chain.from_iterable(A[a-1] if a>0 else inverse(A[-a-1]) for a in w))
A=[((1,),(1,2),(1,3),(1,4)),((1,-2,1),(1,),(3,),(4,)),((1,),(2,-3,2),(2,),(4,)),((1,),(2,),(3,-4,3),(3,)),((1,),(2,),(3,),(3,-2,1,4))]
I=tuple((i,) for i in range(1,5))
def action(w):
 r=I
 for i in w:r=tuple(substitute(x,A[i-1]) for x in r)
 return r
h=(5,4,3,2,1,1,2,3,4,5);c=(1,2,3,4)*5
check(action(h)==action(c));target=action(h*2)
for i in range(1,6):
 for j in range(i+1,6):check(action((i,j,i))==action((j,i,j)) if j==i+1 else action((i,j))==action((j,i)))
# Iterative frontier with images carried along, independently of author's recursive word/action routine.
counts=[];survivors=set();total=0
for start in range(6):
 frontier=[(start,(0,)*5,(),I)]
 for depth in range(20):
  nxt=[]
  for pos,used,w,im in frontier:
   for delta in [-1,1]:
    q=pos+delta
    if not 0<=q<6:continue
    edge=min(pos,q)
    if used[edge]==4:continue
    v=list(used);v[edge]+=1
    nxt.append((q,tuple(v),w+(edge+1,),tuple(substitute(x,A[edge]) for x in im)))
  frontier=nxt
 retained=[r for r in frontier if r[0]==start]
 counts.append(len(retained));total+=len(retained)
 for pos,used,w,im in retained:
  check(used==(4,)*5)
  if im==target:survivors.add(w)
check(counts==[81,162,162,162,162,81]);check(total==810)
check(survivors=={(h*2)[i:]+(h*2)[:i] for i in range(20)})
# Stress all linking integer solutions in a box; analytic inequalities, not this box, prove exhaustiveness.
patterns={20:set(),30:set(),40:set()};pairs=list(itertools.combinations(range(6),2))
for m in [0,10,20,30,40]:
 T=m//10-4
 for t0 in itertools.product(range(-3,3),repeat=5):
  t=t0+(T-sum(t0),)
  L=tuple((2 if j<5 else 0)+T-2*(t[i]+t[j]) for i,j in pairs)
  if min(L)<0:continue
  check(m>=20)
  if m==20:check(L in {tuple(2 if k in (i,j) else 0 for i,j in pairs) for k in range(6)})
  if m==30:check(L==(1,)*15)
  if m==40:check(L in {tuple(0 if k in (i,j) else 2 for i,j in pairs) for k in range(6)})
  patterns[m].add(L)
check([len(patterns[m]) for m in [20,30,40]]==[6,1,6])
print(json.dumps({'status':'PASS','assertions':N,'twenty_letter_candidates':total,'twenty_letter_survivors':len(survivors),'candidate_counts':counts,'scope':'Independent iterative exhaustive twenty-letter action test and supplementary linking controls; full thirty-letter Python/C++ certificates separately replayed.'},indent=2))
