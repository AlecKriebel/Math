"""New whole-package exact controls. Finite diagnostics, not universal proof."""
from pathlib import Path
from fractions import Fraction as Q
from collections import Counter,defaultdict
import json,random,sys
R=Path(__file__).resolve().parent
rng=random.Random(11410120261017)
counts=Counter()
def need(ok,msg):
 if not ok:raise RuntimeError(msg)
def mob(v):
 c=list(v);n=(len(v)-1).bit_length()
 for i in range(n):
  for x in range(len(v)):
   if x>>i&1:c[x]-=c[x^(1<<i)]
 return c
def deg(v):return max((i.bit_count() for i,a in enumerate(mob(v)) if a),default=-1)
def walsh(v):
 c=list(v);n=(len(v)-1).bit_length()
 for i in range(n):
  for x in range(len(v)):
   if not x>>i&1:
    a,b=c[x],c[x|(1<<i)];c[x],c[x|(1<<i)]=a+b,a-b
 return c
def rho(v,i):
 c=walsh(v);e=sum(a*a for a in c);need(e>0,'zero norm')
 return sum(a*a for s,a in enumerate(c) if s>>i&1)/e
def build(p,q,free):
 if not any(p):return 0
 if not any(q):return 1
 n=len(free);D=max(deg(p),deg(q));need(D>0,'disjoint constants')
 s=[a*a-b*b for a,b in zip(p,q)];z=max(range(len(s)),key=lambda x:abs(s[x]));need(s[z]!=0,'nonzero square difference')
 target=q if p[z] else p
 coeff=mob(target);k=deg(target);tops=[m for m,a in enumerate(coeff) if a and m.bit_count()==k]
 need(k>0,'opposite constant')
 family=[];union=0;blocks=[]
 for m in tops:
  if not union&m:
   family.append(m);union|=m
   witnesses=[e for e in range(1,1<<n) if e&m==e and target[z^e]]
   need(witnesses,'maximum coefficient flip witness');blocks.append(witnesses[0]);counts['block_witnesses']+=1
 need(all(m&union for m in tops),'maximal union hits')
 rv=[]
 for y in range(1<<len(blocks)):
  x=z
  for j,e in enumerate(blocks):
   if y>>j&1:x^=e
  rv.append(s[x]/s[z])
 need(rv[0]==1 and max(map(abs,rv))<=1 and all(rv[1<<j]<0 for j in range(len(blocks))),'block sign/max')
 need(deg(rv)<=2*D and len(blocks)<=8*D*D,'block degree or Markov count')
 counts['nonterminal_stages']+=1
 # Expand every answer to this query batch and independently check selected degree decrease.
 chosen=[j for j in range(n) if union>>j&1];remaining=[j for j in range(n) if not union>>j&1]
 def child(answers):
  base=sum(((answers>>t)&1)<<j for t,j in enumerate(chosen));pp=[];qq=[]
  for u in range(1<<len(remaining)):
   x=base|sum(((u>>t)&1)<<j for t,j in enumerate(remaining));pp.append(p[x]);qq.append(q[x])
  need(deg(qq if p[z] else pp)<k,'all-branch degree decrease');counts['answer_branches']+=1
  return build(pp,qq,[free[j] for j in remaining])
 children={a:child(a) for a in range(1<<len(chosen))}
 def expand(t,ans):
  if t==len(chosen):return children[ans]
  return (free[chosen[t]],expand(t+1,ans),expand(t+1,ans|(1<<t)))
 return expand(0,0)
def run(t,x):
 hist=[]
 while isinstance(t,tuple):
  i,l,h=t;need(i not in [j for j,_ in hist],'repeated query');b=x>>i&1;hist.append((i,b));t=h if b else l
 return t,tuple(hist)
def hybrid_laws(t,n):
 N=1<<n;pre=defaultdict(Counter);term=defaultdict(Counter);nxt={}
 for x in range(N):
  h,hist=run(t,x)
  for y in range(N):
   z=x
   for j,(i,b) in enumerate(hist):
    zz=(z&~(1<<i))|(y&(1<<i));pre[hist[:j]][(z,zz)]+=1;nxt[hist[:j]]=i;z=zz
   term[hist][z]+=1
 for hist,law in pre.items():
  i=nxt[hist];mult=1<<(n-len(hist)-1)
  need(law==Counter({(x,(x&~(1<<i))|(b<<i)):mult for x in range(N) for b in (0,1)}),'prequery pair law')
  counts['fresh_prequery_laws']+=1
 for hist,law in term.items():
  need(law==Counter({x:1<<(n-len(hist)) for x in range(N)}),'terminal uniform law');counts['fresh_terminal_laws']+=1
for n in range(1,7):
 N=1<<n
 for j in range(20):
  # Deliberately signed, highly unbalanced rational amplitudes with common zeros.
  p=[];q=[]
  ac=[Q(rng.randrange(-9,10),rng.randrange(1,7)) for _ in range(n+1)];bc=[Q(rng.randrange(-9,10),rng.randrange(1,7)) for _ in range(n+1)]
  ac[0]=bc[0]=Q(101)
  for x in range(N):
   label=rng.randrange(3);v=Q(rng.choice([-1,1])*rng.randrange(1,100),rng.randrange(1,23))
   if j%4==0:v*=Q(10**80) if label==1 else Q(1,10**80)
   if j>=10 and n>=2:
    signs=[1-2*((x>>k)&1) for k in range(n)];common=Q(1+signs[2]) if n>=3 and j%2 else Q(1)
    a=ac[0]+sum(ac[k+1]*signs[k] for k in range(3,n));b=bc[0]+sum(bc[k+1]*signs[k] for k in range(3,n))
    p.append((signs[0]+signs[1])*common*a);q.append((signs[0]-signs[1])*common*b)
   else:
    p.append(v if label==1 else Q(0));q.append(v if label==2 else Q(0))
  if not any(p) or not any(q):continue
  t=build(p,q,list(range(n)));hs=[run(t,x) for x in range(N)];T=max(len(hist) for h,hist in hs);d=max(deg(p),deg(q))
  need(T<=min(n,16*d**4),'depth');need(all((not p[x] or hs[x][0]==1) and (not q[x] or hs[x][0]==0) for x in range(N)),'support label')
  delta=max(rho(v,i) for v in [p,q] for i in range(n));need(delta>=Q(1,1024*d**8),'necessary bound')
  ep=sum(v*v for v in p)/N;eq=sum(v*v for v in q)/N
  mu=Q(sum(h for h,hist in hs),N);r=[Q(sum(i in [k for k,b in hist] for h,hist in hs),N) for i in range(n)]
  covsum=Q(0)
  for values,e in [(p,ep),(q,eq)]:
   u=[v*v/e for v in values];cov=abs(sum(Q(hs[x][0])*u[x] for x in range(N))/N-mu)
   A=[sum(abs(u[x]-u[x^(1<<i)]) for x in range(N))/(2*N) for i in range(n)]
   need(cov<=sum(r[i]*A[i] for i in range(n))/2,'covariance')
   for i in range(n):
    rr=rho(values,i);need(A[i]*A[i]<=4*rr*(1-rr),'square Fourier')
    counts['fresh_square_checks']+=1
   covsum+=cov
  need(covsum==1,'two densities covariance sum')
  counts['fresh_nonzero_disjoint_pairs']+=1
  counts['with_common_zeros']+=any(not p[x] and not q[x] for x in range(N))
  hybrid_laws(t,n)
result={'status':'PASS','seed':11410120261017,'arithmetic':'integer and Fraction only','counts':dict(counts),'scope':'120 generated candidate tables n=1..6 (including low-degree constructed pairs), omitting pairs with a zero member; actual source-style greedy construction checked recursively on every answer branch. Finite diagnostics, not a universal proof.','optimized':not __debug__}
print(json.dumps(result,indent=2));(R/('FRESH.optimized.json' if not __debug__ else 'FRESH.normal.json')).write_text(json.dumps(result,indent=2)+'\n')
