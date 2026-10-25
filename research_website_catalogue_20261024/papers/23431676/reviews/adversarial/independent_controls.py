"""Fresh state-space/certificate controls derived from the manuscript before helper reading."""
from collections import deque,Counter
from fractions import Fraction as F
from itertools import product
from math import gcd
from functools import reduce
from pathlib import Path
from datetime import datetime,timezone
import json
OWN=Path(__file__).resolve().parent
counts=Counter();details={}
def req(ok,msg):
 if not ok:raise RuntimeError(msg)
def degrees(A):return tuple(map(sum,A))
def fire(A,x,v):
 d=degrees(A);req(x[v]>=d[v],'illegal test firing')
 return tuple(x[w]+A[v][w]-(d[v] if w==v else 0) for w in range(len(A)))
def legal(A,x):return [v for v,d in enumerate(degrees(A)) if x[v]>=d]
def endpoint(A,x,f):
 d=degrees(A)
 return tuple(x[w]+sum(A[v][w]*f[v] for v in range(len(A)))-d[w]*f[w] for w in range(len(A)))
def closure(A,x):
 seen={x};todo=deque([x]);adj={};parent={x:None}
 while todo:
  state=todo.popleft();nexts={}
  for v in legal(A,state):
   nxt=fire(A,state,v);nexts[nxt]=v
   if nxt not in seen:seen.add(nxt);todo.append(nxt);parent[nxt]=(state,v)
  adj[state]=nexts
  if len(seen)>500000:raise RuntimeError('declared finite-control budget exceeded')
 return adj,parent
def cyclic(adj):
 deg={x:0 for x in adj}
 for ys in adj.values():
  for y in ys:deg[y]+=1
 q=deque(x for x,d in deg.items() if d==0);n=0
 while q:
  x=q.popleft();n+=1
  for y in adj[x]:
   deg[y]-=1
   if deg[y]==0:q.append(y)
 return n!=len(adj)
def strong(A):
 n=len(A)
 for start in range(n):
  seen={start};todo=[start]
  while todo:
   u=todo.pop()
   for v in range(n):
    if A[u][v] and v not in seen:seen.add(v);todo.append(v)
  if len(seen)<n:return False
 return True
def configs(n,C):return [z for z in product(range(C+1),repeat=n) if sum(z)==C]
def gadget(A,x,overrideN=None,overrideM=None,early=False):
 n=len(A);C=sum(x);D=max(degrees(A));N=(C+1)**n if overrideN is None else overrideN;M=N+1 if overrideM is None else overrideM;B=N*(M*D+1)
 H=[[0]*(n+2) for _ in range(n+2)]
 for v in range(n):
  for w in range(n):H[v][w]=M*A[v][w]
  H[v][n]=1;H[n][v]=B
 H[n][n+1]=H[n+1][n]=1
 H=tuple(map(tuple,H));X=tuple(M*z+N for z in x)+(n*B+1-(0 if early else N),0);f=(N,)*n+(1,0);Y=endpoint(H,X,f)
 req(min(X)>=0 and min(Y)>=0 and sum(X)==sum(Y),'gadget domain')
 return H,X,Y,N,M,B
# All 2-vertex positive multiplicities 1..3 and all simple SC 3-vertex graphs.
graphs=[((0,a),(b,0)) for a in range(1,4) for b in range(1,4)]
for bits in product(range(2),repeat=6):
 A=[[0]*3 for _ in range(3)];k=0
 for u in range(3):
  for v in range(3):
   if u!=v:A[u][v]=bits[k];k+=1
 A=tuple(map(tuple,A))
 if strong(A):graphs.append(A)
# Exhaustive count-DAG explores every possible prefix ordering up to N (merged only at identical counts).
for A in graphs:
 n=len(A)
 for C in range(3 if n==2 else 2):
  for x in configs(n,C):
   adj,_=closure(A,x);nonhalt=cyclic(adj);H,X,Y,N,M,B=gadget(A,x);req(strong(H),'output disconnected')
   req(all(H[v][v]==0 for v in range(n+2)),'output loops')
   req(Y[:n]==tuple(M*x[v]+M*N*(sum(A[u][v] for u in range(n))-sum(A[v]))+B for v in range(n)),'Y formula')
   req(Y[n:]==((n-1)*N,1),'gate/marker endpoint')
   prefixes={(0,)*n};todo=deque(prefixes);atN=[]
   while todo:
    f=todo.popleft();t=sum(f);z=endpoint(A,x,f);h=endpoint(H,X,f+(0,0))
    req(h[:n]==tuple(M*z[v]+N-f[v] for v in range(n)),'prefix invariant')
    req(h[n:]==(n*B+1-N+t,0),'gate invariant')
    req((h[n]>=degrees(H)[n])==(t>=N),'gate timing')
    if t==N:atN.append(f);continue
    req(set(legal(A,z))==set(v for v in legal(H,h) if v<n),'prefix legal set differs')
    req(n not in legal(H,h) and n+1 not in legal(H,h),'early gate/marker')
    counts['prefix_count_states']+=1
    for v in legal(A,z):
     nf=list(f);nf[v]+=1;nf=tuple(nf)
     if nf not in prefixes:prefixes.add(nf);todo.append(nf)
   req(bool(atN)==nonhalt,'finite-state cutoff mismatch')
   # All cleanup count states after each possible horizon count, with gate fixed at1 and marker0.
   for f in atN:
    h=fire(H,endpoint(H,X,f+(0,0)),n);req(min(h[:n])>=B,'reserve not delivered')
    for cf in product(*(range(f[v],N+1) for v in range(n))):
     state=endpoint(H,X,cf+(1,0))
     for v in range(n):
      if cf[v]<N:req(state[v]>=degrees(H)[v],'cleanup ordering illegal')
     counts['cleanup_count_states']+=1
    req(endpoint(H,X,(N,)*n+(1,0))==Y,'cleanup target')
   counts['source_instances']+=1
# Uncapped (within explicit emergency budget) COMPLETE gadget state spaces for smallest genuine cases.
full=[]
for a,b in product(range(1,3),repeat=2):
 A=((0,a),(b,0))
 for x in [(0,0),(1,0),(0,1)]:
  H,X,Y,N,M,B=gadget(A,x);src,_=closure(A,x);hgraph,parents=closure(H,X)
  req((Y in hgraph)==cyclic(src),'full gadget reachability mismatch')
  full.append({'arcs':[a,b],'x':x,'N':N,'gadget_states':len(hgraph),'reachable':Y in hgraph})
  # Every explored target-reaching word has marker balance by endpoint; all immediate incoming edges audited.
  for state,nxts in hgraph.items():
   for nxt,v in nxts.items():req(nxt[-1]-state[-1]==(1 if v==2 else -1 if v==3 else 0),'marker balance transition')
  counts['complete_gadget_states']+=len(hgraph)
details['complete_gadget_closures']=full
# Signed normalization and loop-relay preservation via COMPLETE small state graphs.
for a,b,l0,l1 in product(range(1,3),range(1,3),range(2),range(2)):
 A=((l0,a),(b,l1))
 for x in product(range(-2,3),repeat=2):
  k=tuple(max(0,-z) for z in x);Ap=[list(row) for row in A]
  for v in range(2):Ap[v][v]+=k[v]
  Ap=tuple(map(tuple,Ap));xp=tuple(x[v]+k[v] for v in range(2));old,_=closure(A,x);new,_=closure(Ap,xp)
  req({tuple(z[v]+k[v] for v in range(2)) for z in old}==set(new),'signed state graphs differ')
  for z in old:
   zz=tuple(z[v]+k[v] for v in range(2));req(legal(A,z)==legal(Ap,zz),'signed legality differs')
  counts['signed_normalization_instances']+=1
for a,b,l0,l1 in product(range(1,3),range(1,3),range(3),range(3)):
 A=((l0,a),(b,l1));loops=[v for v in range(2) if A[v][v]];n=2+len(loops);Ar=[[0]*n for _ in range(n)]
 for u in range(2):
  for v in range(2):
   if u!=v:Ar[u][v]=A[u][v]
 for r,v in enumerate(loops,2):Ar[v][r]=Ar[r][v]=A[v][v]
 Ar=tuple(map(tuple,Ar));req(strong(Ar),'relay graph disconnected')
 for C in range(3):
  for x in configs(2,C):
   old,_=closure(A,x);new,_=closure(Ar,x+(0,)*len(loops));req(cyclic(old)==cyclic(new),'relay nonhalting differs');counts['relay_instances']+=1
# Exact reduced-count and blocking-vector certificate independently checked against full reachability.
def det(A):
 if not A:return 1
 if len(A)==1:return A[0][0]
 return sum((-1)**j*A[0][j]*det([row[:j]+row[j+1:] for row in A[1:]]) for j in range(len(A)))
def period(A):
 n=len(A);d=degrees(A);L=[[A[v][w]-(d[v] if v==w else 0) for v in range(n)] for w in range(n)]
 co=[abs(det([[L[u][v] for v in range(n) if v!=w] for u in range(n) if u!=w])) for w in range(n)];g=reduce(gcd,co)
 p=tuple(z//g for z in co);req(min(p)>0 and endpoint(A,(0,)*n,p)==(0,)*n,'period');return p,L
def solve(A,b):
 n=len(A);R=[[F(z) for z in A[i]]+[F(b[i])] for i in range(n)]
 for j in range(n):
  k=next(k for k in range(j,n) if R[k][j]);R[j],R[k]=R[k],R[j];q=R[j][j];R[j]=[z/q for z in R[j]]
  for i in range(n):
   if i!=j:
    q=R[i][j];R[i]=[R[i][k]-q*R[j][k] for k in range(n+1)]
 return [row[-1] for row in R]
def reduced(A,x,y):
 p,L=period(A);n=len(A);solutions=set()
 for w in range(n):
  idx=[v for v in range(n) if v!=w];Q=[[L[u][v] for v in idx] for u in idx]
  for gw in range(p[w]):
   ans=solve(Q,[y[u]-x[u]-gw*L[u][w] for u in idx]);g=[0]*n;g[w]=gw
   if any(z.denominator!=1 or z<0 for z in ans):continue
   for v,z in zip(idx,ans):g[v]=int(z)
   if endpoint(A,x,g)==y:solutions.add(tuple(g))
 req(len(solutions)<=1,'multiple reduced solutions');return next(iter(solutions)) if solutions else None,p
unrealizable_certificate=None
for A in graphs:
 n=len(A)
 for C in range(3):
  states=configs(n,C)
  for x in states:
   adj,_=closure(A,x)
   for y in states:
    g,p=reduced(A,x,y);reach=y in adj
    if g is None:req(not reach,'reach without lattice solution');counts['integer_image_no_cases']+=1;continue
    witnesses=[]
    for u in product(*(range(z+1) for z in g)):
     st=endpoint(A,x,u)
     cert=u!=g and all(u[v]==g[v] or st[v]<degrees(A)[v] for v in range(n))
     if cert:witnesses.append(u)
     counts['blocking_vectors_checked']+=1
    req(bool(witnesses)==(not reach),'blocking certificate mismatch')
    counts['reduced_target_pairs']+=1
# Direct period-deletion on explicit legal words, with order retained.
for A in [((0,1),(1,0)),((0,2),(1,0)),((0,1,0),(0,0,1),(1,0,0)),((0,1,1),(1,0,0),(1,0,0))]:
 n=len(A);p,_=period(A)
 for x in configs(n,3):
  stack=[(x,())]
  while stack:
   st,word=stack.pop();f=Counter(word)
   if all(f[v]>=p[v] for v in range(n)):
    deleted=Counter();kept=[]
    for v in word:
     if deleted[v]<p[v]:deleted[v]+=1
     else:kept.append(v)
    state=x
    for v in kept:req(v in legal(A,state),'period deletion illegal');state=fire(A,state,v)
    req(state==st,'period deletion endpoint');counts['explicit_period_deletions']+=1
   if len(word)<9:
    for v in legal(A,st):stack.append((fire(A,st,v),word+(v,)))
# Fault controls: too-short cutoff, early gate, insufficient scaling and raw loop removal.
A=((0,1),(2,0));x=(1,0);req(not cyclic(closure(A,x)[0]),'chosen halting witness')
H,X,Y,N,M,B=gadget(A,x,overrideN=1);graph,parents=closure(H,X);req(Y in graph,'cutoff mutant not caught')
path=[];cur=Y
while parents[cur] is not None:cur,v=parents[cur];path.append(v)
path.reverse();details['too_short_cutoff_false_yes']={'source':A,'x':x,'mutant_N':1,'legal_gadget_word':path}
A=((0,1),(1,0));x=(0,0);H,X,Y,N,M,B=gadget(A,x,early=True);state=fire(H,X,2)
for v in range(2):state=fire(H,state,v)
req(state==Y and not cyclic(closure(A,x)[0]),'early gate mutant not caught')
H,X,Y,N,M,B=gadget(A,(0,1),overrideM=1);req(0 in legal(H,X) and 0 not in legal(A,(0,1)),'small scaling mutant')
loop=((1,1),(1,0));raw=((0,1),(1,0));req(0 not in legal(loop,(1,0)) and 0 in legal(raw,(1,0)),'raw loop removal mutant')
for ell in range(4):
 for x in range(5):req(cyclic(closure(((ell,),),(x,))[0])==(x>=ell),'singleton cutoff');counts['singletons']+=1
# Large integer output formation is never a long trajectory simulation.
big=[]
for n in [2,5,12]:
 A=tuple(tuple((2**80+3) if w==(v+1)%n else 0 for w in range(n)) for v in range(n));x=(2**256+1,)+(0,)*(n-1)
 H,X,Y,N,M,B=gadget(A,x);req(N.bit_length()<=1+n*(sum(x)+1).bit_length(),'N bit bound')
 big.append({'n':n,'C_bits':sum(x).bit_length(),'N_bits':N.bit_length(),'M_bits':M.bit_length(),'B_bits':B.bit_length(),'max_output_bits':max(z.bit_length() for row in H for z in row)})
details['large_binary_outputs']=big
result={'completed_utc':datetime.now(timezone.utc).isoformat(),'status':'pass','graph_count':len(graphs),'counts':dict(counts),'details':details,'negative_controls':['too-short cutoff false YES','gate initially legal false YES','small scale permits illegal source move','raw loop removal changes legality'],'scope':'Independent exact finite state/certificate controls; universal reduction and polynomial-bit bounds proved separately. No published helper read before this control was authored/executed.'}
(OWN/'evidence/independent-controls.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'status':'pass','counts':dict(counts)}))
