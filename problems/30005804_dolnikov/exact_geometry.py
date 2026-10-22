from fractions import Fraction as F
from itertools import combinations

def pt(x):return tuple(map(F,x))
def cross(a,b):return a[0]*b[1]-a[1]*b[0]
def sub(a,b):return(a[0]-b[0],a[1]-b[1])
def inside(p,P):return all(cross(sub(P[(i+1)%len(P)],P[i]),sub(p,P[i]))>=0 for i in range(len(P)))
def segment_cross(a,b,c,d):
 u=sub(b,a);v=sub(d,c);den=cross(u,v)
 if not den:return None
 t=cross(sub(c,a),v)/den;s=cross(sub(c,a),u)/den
 if 0<=t<=1 and 0<=s<=1:return(a[0]+t*u[0],a[1]+t*u[1])
 return None
def candidates(polys):
 V=set(p for P in polys for p in P);E=[(P[i],P[(i+1)%len(P)]) for P in polys for i in range(len(P))]
 for (a,b),(c,d) in combinations(E,2):
  p=segment_cross(a,b,c,d)
  if p is not None:V.add(p)
 return sorted(V)
def masks(polys):
 out={}
 for p in candidates(polys):
  m=sum(1<<i for i,P in enumerate(polys) if inside(p,P))
  if m:out.setdefault(m,p)
 return out
def min_cover(S,coverage):
 if not S:return 0
 ms=sorted({m&S for m in coverage if m&S},key=int.bit_count,reverse=True)
 dp={0:0}
 for m in ms:
  for a,n in list(dp.items()):
   b=a|m
   if n+1<dp.get(b,100):dp[b]=n+1
 return dp[S]
def hypergraph_chromatic(S,coverage):
 ids=[i for i in range(S.bit_length()) if S>>i&1]
 if not ids:return 0
 bad=[]
 for n in (2,3):
  for I in combinations(ids,n):
   e=sum(1<<i for i in I)
   if not any(m&e==e for m in coverage):bad.append(e)
 def possible(q):
  classes=[]
  def rec(j):
   if j==len(ids):return True
   bit=1<<ids[j]
   for k in range(min(q,len(classes)+1)):
    new=k==len(classes)
    if new:classes.append(0)
    old=classes[k];v=old|bit
    if not any(v&e==e for e in bad):
     classes[k]=v
     if rec(j+1):return True
    classes[k]=old
    if new:classes.pop()
   return False
  return rec(0)
 return next(q for q in range(1,len(ids)+1) if possible(q))
