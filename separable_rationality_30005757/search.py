import itertools,json,collections,time
from functools import lru_cache
from pathlib import Path
D=Path(__file__).parent
def std(p):return tuple(sorted(p).index(v)+1 for v in p)
def pats(p):return {std(q) for k in range(1,len(p)+1) for q in itertools.combinations(p,k)}
def contains(p,q):return q in pats(p)
def op(a,b,s):
 return a+tuple(x+len(a) for x in b) if s==1 else tuple(x+len(b) for x in a)+b
T=[p for p in itertools.permutations(range(1,5)) if p not in [(2,4,1,3),(3,1,4,2)] and contains(p,(2,3,1))]
def automaton(basis):
 P=sorted(set.union(*(pats(p) for p in basis)),key=lambda x:(len(x),x)); idx={p:i for i,p in enumerate(P)}; reject=sum(1<<idx[p] for p in basis)
 cuts={s:[] for s in (1,-1)}
 for p,i in idx.items():
  for k in range(1,len(p)):
   a,b=std(p[:k]),std(p[k:])
   for s in cuts:
    if op(a,b,s)==p:cuts[s].append((1<<idx[a],1<<idx[b],1<<i))
 @lru_cache(None)
 def join(a,b,s):
  z=a|b
  for u,v,w in cuts[s]:
   if a&u and b&v:z|=w
  return None if z&reject else z
 leaf=(1<<idx[(1,)],0); states={leaf}; trans=set()
 while 1:
  old=len(states)
  for a,sa in list(states):
   for b,sb in list(states):
    for s in (1,-1):
     if sa==s:continue
     z=join(a,b,s)
     if z is not None:states.add((z,s));trans.add(((a,sa),(b,sb),(z,s)))
  if len(states)==old:break
 S=sorted(states);ids={p:i for i,p in enumerate(S)}
 return S,[(ids[a],ids[b],ids[c]) for a,b,c in trans],ids[leaf]
def berlekamp(a,p=1000000007):
 C=[1];B=[1];L=0;m=1;b=1
 for n in range(len(a)):
  d=sum(C[i]*a[n-i] for i in range(L+1))%p
  if d==0:m+=1;continue
  T=C[:];coef=d*pow(b,p-2,p)%p
  C += [0]*max(0,len(B)+m-len(C))
  for j in range(len(B)):C[j+m]=(C[j+m]-coef*B[j])%p
  if 2*L<=n:L=n+1-L;B=T;b=d;m=1
  else:m+=1
 return L

def run(basis,N=50):
 S,T,l=automaton(basis);a=[[0]*(N+1) for _ in S];a[l][1]=1
 for n in range(2,N+1):
  for u,v,w in T:a[w][n]+=sum(a[u][k]*a[v][n-k] for k in range(1,n))
 seq=[1]+[sum(row[n] for row in a) for n in range(1,N+1)]
 return {'basis':[''.join(map(str,p)) for p in basis],'states':len(S),'transitions':len(T),'coefficients':seq,'modular_recurrence_order':berlekamp(seq)}
if __name__=='__main__':
 out=[]
 for k in [1,2]:
  for B in itertools.combinations(T,k):
   t=time.time();r=run(B);out.append(r);print(r['basis'],r['states'],r['modular_recurrence_order'],round(time.time()-t,2),flush=True);(D/'small_basis_results.json').write_text(json.dumps(out,indent=2))
