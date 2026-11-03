from itertools import combinations

def std(p):
 d={v:i for i,v in enumerate(sorted(p))};return tuple(d[v] for v in p)
def good(p):
 n=len(p)
 for j in range(1,n-2):
  lo=min(p[:j])
  for k in range(j+1,n-1):
   if lo<p[k]<p[j] and max(p[k+1:])>p[j]:return False
 e=n;s=-1
 for i,j,k in combinations(range(n),3):
  if p[i]<p[k]<p[j]:e=min(e,k)
  if p[k]<p[i]<p[j]:s=max(s,i)
 return s<e

def inv(p):return sum(a>b for i,a in enumerate(p) for b in p[i+1:])
def cuts(p):return [i for i in range(1,len(p)) if max(p[:i])==i-1]
def rc(p):return tuple(len(p)-1-x for x in p[::-1])
def inverse(p):return tuple(p.index(i) for i in range(len(p)))
def tilde(p):
 i=cuts(p)[0]
 return p[:i]+(i,)+tuple(x+1 for x in p[i:])
def almost(p):return cuts(p) or any(cuts(std(p[:i]+p[i+1:])) for i in {0,len(p)-1,p.index(0),p.index(len(p)-1)})
def f(p):
 if cuts(p):return tilde(p)
 s=std(p[1:])
 if cuts(s):
  s=tilde(s);e=p[0];return (e,)+tuple(x+(x>=e) for x in s)
 if cuts(std(tuple(x for x in p if x!=0))):return inverse(f(inverse(p)))
 return rc(f(rc(p)))
if __name__=='__main__':
 A=[()]
 for n in range(10):
  tested=0;bad=[]
  for p in A:
   if n>2 and almost(p):
    tested+=1;q=f(p)
    assert inv(q)==inv(p)
    if not good(q):bad.append((p,q,inv(p)))
  print(n,len(A),tested,len(bad),bad[:5],flush=True)
  if n<9:A=[p[:i]+(n,)+p[i:] for p in A for i in range(n+1) if good(p[:i]+(n,)+p[i:])]
