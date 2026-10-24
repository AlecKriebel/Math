#!/usr/bin/env python3
"""Exact symbolic no-rainbow search over arbitrary odd abelian groups.
Relations are integer lattices, saturated at 2. Every surviving quotient
embeds its distinct marked vertices into some finite odd abelian quotient.
"""
import itertools,collections,json,time,sys
from pathlib import Path

def row_hnf(rows,d):
 A=[list(row) for row in rows if any(row)];r=0
 for c in range(d):
  if r==len(A):break
  while True:
   choices=[i for i in range(r,len(A)) if A[i][c]]
   if not choices:break
   i=min(choices,key=lambda i:abs(A[i][c]));A[r],A[i]=A[i],A[r]
   if A[r][c]<0:A[r]=[-x for x in A[r]]
   p=A[r][c]
   changed=False
   for i in range(r+1,len(A)):
    if A[i][c]:
     q=A[i][c]//p;A[i]=[x-q*y for x,y in zip(A[i],A[r])]
     if A[i][c]:changed=True
   if not changed:break
  if A[r][c]==0:continue
  p=A[r][c]
  for i in range(r):
   q=A[i][c]//p;A[i]=[x-q*y for x,y in zip(A[i],A[r])]
  r+=1
 return tuple(tuple(row) for row in A[:r])

def mod2_dependence(rows):
 basis={}
 for j,row in enumerate(rows):
  v=sum((x&1)<<i for i,x in enumerate(row));comb=1<<j
  while v:
   p=v.bit_length()-1
   if p not in basis:basis[p]=(v,comb);break
   z,b=basis[p];v^=z;comb^=b
  if not v:return comb
 return None

def canonical(rows,d):
 H=row_hnf(rows,d)
 while True:
  comb=mod2_dependence(H)
  if comb is None:return H
  half=tuple(sum(row[i] for j,row in enumerate(H) if comb>>j&1)//2 for i in range(d))
  H=row_hnf(H+(half,),d)

def contains(H,v):
 v=list(v)
 for row in H:
  p=next(i for i,x in enumerate(row) if x)
  if v[p]%row[p]:return False
  q=v[p]//row[p];v=[x-q*y for x,y in zip(v,row)]
 return not any(v)

def search(n,limit=500000):
 d=n-1;V=tuple(range(n));cycles=[(0,)+p for p in itertools.permutations(range(1,n)) if p[0]<p[-1]]
 E=[{tuple(sorted((a[i],a[(i+1)%n]))) for i in range(n)} for a in cycles]
 events=[];cycle_events=[[] for _ in cycles]
 for Q in itertools.combinations(V,4):
  a,b,c,e=Q
  for L,R in [((a,b),(c,e)),((a,c),(b,e)),((a,e),(b,c))]:
   row=tuple(int(k in L)-int(k in R) for k in range(1,n))
   cover=sum(1<<i for i,F in enumerate(E) if L in F and R in F)
   j=len(events);events.append((row,cover,(L,R)))
   for i,F in enumerate(E):
    if L in F and R in F:cycle_events[i].append(j)
 diffs=[tuple(int(k==i)-int(k==j) for k in range(1,n)) for i,j in itertools.combinations(V,2)]
 full=(1<<len(cycles))-1;seen=set();counts=collections.Counter();started=time.time();witness=None
 def visit(H,depth):
  nonlocal witness
  if H in seen:return False
  seen.add(H);counts['states']+=1;counts['max_depth']=max(counts['max_depth'],depth)
  if counts['states']%10000==0:print(dict(counts),'seconds',time.time()-started,flush=True)
  if counts['states']>limit:raise RuntimeError('state limit')
  if any(contains(H,v) for v in diffs):counts['vertex_collision']+=1;return False
  mask=0;implied=[]
  for j,(row,cover,_) in enumerate(events):
   if contains(H,row):mask|=cover;implied.append(j)
  if mask==full:witness={'H':H,'implied':implied};return True
  # Arbitrary uncovered cycle. Fewest still-possible child quotients is a valid heuristic.
  uncovered=[i for i in range(len(cycles)) if not mask>>i&1]
  best=None
  for i in uncovered:
   children={canonical(H+(events[j][0],),d) for j in cycle_events[i]}
   children={Q for Q in children if Q not in seen and not any(contains(Q,v) for v in diffs)}
   if not children:counts['dead_cycle']+=1;return False
   if best is None or len(children)<len(best):best=children
   if len(best)==1:break
  for Q in sorted(best):
   if visit(Q,depth+1):return True
  return False
 try:found=visit(tuple(),0);status='counterexample_relations' if found else 'exhausted_no_counterexample'
 except RuntimeError as e:status=str(e)
 result={'n':n,'status':status,'counts':dict(counts),'seconds':time.time()-started,'witness':witness}
 Path(f'universal_{n}_result.json').write_text(json.dumps(result,indent=2)+'\n')
 print(json.dumps(result,indent=2),flush=True)
 return result
if __name__=='__main__':search(int(sys.argv[1]) if len(sys.argv)>1 else 6)
