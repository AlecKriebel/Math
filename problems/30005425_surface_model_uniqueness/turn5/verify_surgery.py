#!/usr/bin/env python3
import itertools,json

def complete(n,arrows,rel):
 a=list(arrows);r=set(rel);matches=[];nextv=n
 for v in range(n):
  inc=[i for i,(s,t) in enumerate(a) if t==v];out=[i for i,(s,t) in enumerate(a) if s==v];oi=inc.copy();oo=out.copy()
  while len(inc)<2:inc.append(len(a));a.append((nextv,v));nextv+=1
  while len(out)<2:out.append(len(a));a.append((v,nextv));nextv+=1
  choices=[{(inc[0],out[j]),(inc[1],out[1-j])} for j in (0,1)]
  opts=[x for x in choices if all(((i,j) in x)==((i,j) in r) for i in oi for j in oo)]
  assert opts
  x=opts[0];r|=x
  seams=set()
  for i,j in itertools.product(inc,out):seams.add((i,2,j,3) if (i,j) in x else (i,1,j,0))
  matches.append(seams)
 return a,r,matches

def all_covers(n,a):
 options=[]
 for v in range(n):
  inc=[i for i,(s,t) in enumerate(a) if t==v];out=[i for i,(s,t) in enumerate(a) if s==v]
  if len(inc)>2 or len(out)>2:return []
  pairs=list(itertools.product(inc,out));opts=[]
  for bits in itertools.product((0,1),repeat=len(pairs)):
   r={p for p,b in zip(pairs,bits) if b}
   if all(sum((i,j) in r for j in out)<=1 and sum((i,j) not in r for j in out)<=1 for i in inc) and all(sum((i,j) in r for i in inc)<=1 and sum((i,j) not in r for i in inc)<=1 for j in out):opts.append(r)
  options.append(opts)
 return [set().union(*rs) for rs in itertools.product(*options)]
checks=0;quivers=pairs_checked=0;finite_pair_examples=[]
def ck(x):
 global checks
 assert x;checks+=1
for n in range(1,4):
 possible=list(itertools.product(range(n),repeat=2))
 for mask in range(1<<len(possible)):
  a=[e for i,e in enumerate(possible) if mask>>i&1];covers=all_covers(n,a)
  if not covers:continue
  quivers+=1;completed=[complete(n,a,r) for r in covers]
  for aa,rr,ss in completed:
   ck(len(aa)==4*n-len(a));ck(sum(map(len,ss))==4*n)
   sides=[x for seam in set().union(*ss) for x in [(seam[0],seam[1]),(seam[2],seam[3])]];ck(len(sides)==len(set(sides)))
  for first,second in itertools.product(completed,repeat=2):
   aa,r0,s0=first;bb,r1,s1=second;ck(aa==bb);pairs_checked+=1
   changed=[i for i in range(n) if s0[i]!=s1[i]]
   old=set().union(*(s0[i] for i in changed));new=set().union(*(s1[i] for i in changed));full0=set().union(*s0);full1=set().union(*s1)
   ck(len(old)==len(new)==4*len(changed));ck((full0-old)|new==full1)
   for i in changed:
    ck(s0[i].isdisjoint(s1[i]));ck({(x[0],x[1]) for x in s0[i]}=={(x[0],x[1]) for x in s1[i]});ck({(x[2],x[3]) for x in s0[i]}=={(x[2],x[3]) for x in s1[i]})
# Parallel-arrow finite-locus example, changed at both vertices simultaneously.
a=[(0,1),(0,1),(1,0)];x=complete(2,a,{(0,2),(2,1)});y=complete(2,a,{(1,2),(2,0)})
ck(len([i for i in range(2) if x[2][i]!=y[2][i]])==2)
print(json.dumps({'assertions':checks,'quivers':quivers,'ordered_cover_pairs':pairs_checked,'parallel_arrow_simultaneous_example':{'arrows':a,'old_seams':[sorted(s) for s in x[2]],'new_seams':[sorted(s) for s in y[2]]},'scope':'Checks cover loops, nonsaturated tables and infinite intermediate possibilities; no identification with the source tile-rotation move.'},indent=2))
