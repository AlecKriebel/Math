from functools import lru_cache
from itertools import permutations
import json,sys,time

def length(w):return sum(a>b for i,a in enumerate(w) for b in w[i+1:])
def add(out,m,c):
 out[m]=out.get(m,0)+c
 if not out[m]:del out[m]
def dd(f,i):
 out={}
 for m,c in f.items():
  a,b=m[i:i+2]
  if a>b:
   for j in range(a-b):
    q=list(m);q[i]=a-1-j;q[i+1]=b+j;add(out,tuple(q),c)
  elif b>a:
   for j in range(b-a):
    q=list(m);q[i]=a+j;q[i+1]=b-1-j;add(out,tuple(q),-c)
 return out
@lru_cache(None)
def poly(w,g=False):
 n=len(w)
 for i in range(n-1):
  if w[i]<w[i+1]:
   v=list(w);v[i],v[i+1]=v[i+1],v[i];f=poly(tuple(v),g)
   if g:
    h=dict(f)
    for m,c in f.items():
     q=list(m);q[i+1]+=1;add(h,tuple(q),-c)
    f=h
   return dd(f,i)
 return {tuple(range(n-1,-1,-1)):1}
def code(w):return tuple(sum(b<a for b in w[i+1:]) for i,a in enumerate(w))
def left(w,k):return tuple(k+1 if a==k else k if a==k+1 else a for a in w)
def expand(f,bycode):
 f=dict(f);out={}
 while f:
  m=min(f);c=f[m];w=bycode[m];out[w]=c
  for q,d in poly(w).items():add(f,q,-c*d)
 return out

def main(n):
 start=time.time();W=list(permutations(range(1,n+1)));bycode={code(w):w for w in W}
 stats={'n':n,'permutations':len(W),'support_pairs':0,'non_top_pairs':0,'failures':[],'sign_failures':[],'max_support':0,'unique_ascent_examples':[],'right_growth_failures':[],'coefficient_growth_failures':[],'no_common_ascent_examples':[]}
 supports={}
 for idx,w in enumerate(W):
  a=expand(poly(w,True),bycode);supports[w]=a;top=max(map(length,a));stats['support_pairs']+=len(a);stats['max_support']=max(stats['max_support'],len(a))
  for u,c in a.items():
   if c*(-1)**(length(u)-length(w))<=0:stats['sign_failures'].append((w,u,c))
   if length(u)==top:continue
   stats['non_top_pairs']+=1
   asc=[left(u,k) for k in range(1,n) if u.index(k)<u.index(k+1) and left(u,k) in a]
   if not asc:stats['failures'].append((w,u,c))
   if asc and max(abs(a[v]) for v in asc)<abs(c) and len(stats['coefficient_growth_failures'])<5:stats['coefficient_growth_failures'].append((w,u,c,[(v,a[v]) for v in asc]))
   if len(asc)==1 and len(stats['unique_ascent_examples'])<5:stats['unique_ascent_examples'].append((w,u,asc[0]))
   rightasc=[]
   for k in range(n-1):
    v=list(u);v[k],v[k+1]=v[k+1],v[k]
    if u[k]<u[k+1] and tuple(v) in a:rightasc.append(v)
   if not rightasc and len(stats['right_growth_failures'])<5:stats['right_growth_failures'].append((w,u))
  if idx%100==0:print(n,idx,'elapsed',time.time()-start,flush=True)
 stats['seconds']=time.time()-start
 path=f'exact_n{n}.json';json.dump(stats,open(path,'w'),indent=2)
 import pickle
 pickle.dump(supports,open(f'groth_supports{n}.pickle','wb'))
 print(json.dumps(stats,indent=2))
if __name__=='__main__':main(int(sys.argv[1]))
