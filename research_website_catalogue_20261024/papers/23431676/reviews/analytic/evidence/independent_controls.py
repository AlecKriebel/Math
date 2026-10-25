#!/usr/bin/env python3
"""Fresh analytic controls; written from the paper's definitions before reading helpers.
Exact integers/Fractions only. Finite checks supplement, not replace, universal proof.
"""
from itertools import product
from collections import deque
from fractions import Fraction
from math import gcd, prod
from functools import reduce
from datetime import datetime, timezone
import json, hashlib
from pathlib import Path
HERE=Path(__file__).resolve().parent
stats={}; examples={}
def check(ok,msg):
    if not ok: raise RuntimeError(msg)
def sc(A):
    for s in range(len(A)):
        seen={s}; q=[s]
        for u in q:
            for v in range(len(A)):
                if A[u][v] and v not in seen: seen.add(v);q.append(v)
        if len(seen)!=len(A):return False
    return True
def enabled(A,x): return [i for i in range(len(A)) if x[i]>=sum(A[i])]
def fire(A,x,v):
    y=list(x)
    for j,a in enumerate(A[v]): y[j]+=a
    y[v]-=sum(A[v]); return tuple(y)
def stategraph(A,x):
    todo=deque([x]); edges={x:None}
    while todo:
        z=todo.popleft(); targets=[fire(A,z,v) for v in enabled(A,z)];edges[z]=targets
        for y in targets:
            if y not in edges: edges[y]=None;todo.append(y)
    # A finite reachable digraph has an infinite path iff deleting sinks leaves vertices.
    rev={z:[] for z in edges};out={z:len(es) for z,es in edges.items()}
    for z,es in edges.items():
        for y in es:rev[y].append(z)
    q=deque(z for z,c in out.items() if not c)
    removed=0
    while q:
        y=q.popleft();removed+=1
        for z in rev[y]:
            out[z]-=1
            if out[z]==0:q.append(z)
    return edges,removed<len(edges)
def comps(c,n):
    if n==1:yield (c,);return
    for a in range(c+1):
        for b in comps(c-a,n-1):yield (a,)+b
def Lmatrix(A):
    n=len(A);return [[A[j][i]-(sum(A[j]) if i==j else 0) for j in range(n)] for i in range(n)]
def endpoint(A,x,f):
    L=Lmatrix(A);return tuple(x[i]+sum(L[i][j]*f[j] for j in range(len(A))) for i in range(len(A)))
def gadget(A,x,override=None):
    n=len(A); C=sum(x);D=max(map(sum,A));N=(C+1)**n;M=N+1;B=N*(M*D+1)
    if override:
        M=override.get('M',M);B=override.get('B',B)
    H=[[0]*(n+2) for _ in range(n+2)]
    for i in range(n):
        for j in range(n):H[i][j]=M*A[i][j]
        H[i][n]=1;H[n][i]=B
    H[n][n+1]=H[n+1][n]=1
    X=tuple(M*v+N for v in x)+(n*B+1-N,0)
    Y=tuple(M*x[v]+M*N*(sum(A[u][v] for u in range(n))-sum(A[v]))+B for v in range(n))+((n-1)*N,1)
    return H,X,Y,N,M,B
models=[]
for a,b in product(range(1,4),repeat=2):models.append([[0,a],[b,0]])
for es in product(range(2),repeat=6):
    A=[[0]*3 for _ in range(3)];k=0
    for i in range(3):
        for j in range(3):
            if i!=j:A[i][j]=es[k];k+=1
    if sc(A):models.append(A)
stats['models']=len(models)
prefixnodes=0; fullprefixes=0; cleanupwords=0; instances=0
for A in models:
    n=len(A)
    for c in range(3):
      for x in comps(c,n):
        instances+=1; SG,nonhalt=stategraph(A,x)
        check(not(nonhalt and any(not e for e in SG.values())),'halting dichotomy finite check')
        H,X,Y,N,M,B=gadget(A,x)
        check(sc(H) and all(H[i][i]==0 for i in range(n+2)),'graph domain')
        check(min(X)>=0 and min(Y)>=0 and sum(X)==sum(Y) and X!=Y,'configs')
        check(endpoint(H,X,(N,)*n+(1,0))==Y,'target formula')
        layer={(x,(0,)*n,X)}
        for t in range(N+1):
            if t==N: fullprefixes+=len(layer);break
            nxt=set()
            for z,counts,h in layer:
                prefixnodes+=1
                check(enabled(A,z)==[v for v in enabled(H,h) if v<n],'exact old legality')
                check(n not in enabled(H,h) and n+1 not in enabled(H,h),'early gate/marker')
                for v in enabled(A,z):
                    cc=list(counts);cc[v]+=1;cc=tuple(cc); zz=fire(A,z,v);hh=fire(H,h,v)
                    check(hh==tuple(M*zz[j]+N-cc[j] for j in range(n))+(n*B+1-N+t+1,0),'prefix invariant')
                    nxt.add((zz,cc,hh))
            layer=nxt
            if not layer:break
        check(bool(layer)==nonhalt,'cutoff iff nonhalting')
        for z,counts,h in layer:
            check(n in enabled(H,h),'gate at N')
            after=fire(H,h,n)
            for order in [list(range(n)),list(reversed(range(n)))]:
                k=after
                for v in order:
                    for _ in range(N-counts[v]):
                        check(v in enabled(H,k),'cleanup legality');k=fire(H,k,v)
                check(k==Y,'cleanup endpoint');cleanupwords+=1
stats.update(prefix_instances=instances,prefix_nodes=prefixnodes,full_prefix_count_states=fullprefixes,cleanup_words=cleanupwords)
# Whole target reachability independently explores every reachable gadget state,
# including arbitrary later gate/marker/old firings, rather than canonical counts.
full=[]
for A,x in [([[0,1],[1,0]],(0,0)),([[0,1],[1,0]],(1,0)),([[0,2],[1,0]],(1,0)),([[0,2],[1,0]],(0,1))]:
    SG,nonhalt=stategraph(A,x);H,X,Y,N,M,B=gadget(A,x);HG,hn=stategraph(H,X)
    check((Y in HG)==nonhalt,'whole gadget arbitrary-word equivalence')
    full.append(dict(A=A,x=x,source_nonhalting=nonhalt,gadget_reachable=Y in HG,gadget_states=len(HG),N=N))
examples['whole_gadget']=full
# Independent exact reduced-count solver uses anchored rational elimination,
# not the submitted helper or a symbolic linear-algebra package.
def det(M):
    if not M:return 1
    if len(M)==1:return M[0][0]
    return sum((-1)**j*M[0][j]*det([r[:j]+r[j+1:] for r in M[1:]]) for j in range(len(M)))
def solve(M,b):
    n=len(M);Q=[[Fraction(z) for z in M[i]]+[Fraction(b[i])] for i in range(n)]
    for i in range(n):
        j=next(j for j in range(i,n) if Q[j][i]);Q[i],Q[j]=Q[j],Q[i]
        f=Q[i][i];Q[i]=[a/f for a in Q[i]]
        for j in range(n):
            if j!=i:
                f=Q[j][i];Q[j]=[a-f*b for a,b in zip(Q[j],Q[i])]
    return [r[-1] for r in Q]
def period(A):
    L=Lmatrix(A);cs=[abs(det([r[:w]+r[w+1:] for i,r in enumerate(L) if i!=w])) for w in range(len(A))];d=reduce(gcd,cs)
    return tuple(c//d for c in cs)
def reduced(A,x,y):
    p=period(A);L=Lmatrix(A);n=len(A);delta=[y[i]-x[i] for i in range(n)]
    if sum(delta):return None
    for a in range(p[0]):
        z=[Fraction(a)]+solve([r[1:] for r in L[1:]],[delta[i]-a*L[i][0] for i in range(1,n)])
        if all(q.denominator==1 for q in z):
            h=[int(q) for q in z];k=min(h[i]//p[i] for i in range(n));g=tuple(h[i]-k*p[i] for i in range(n))
            check(endpoint(A,x,g)==y,'integer equation');return g
    return None
certpairs=0; boxes=0;nonrealizablecert=0;periodwords=0
for A in models:
    n=len(A);p=period(A)
    check(min(p)>0 and endpoint(A,(0,)*n,p)==(0,)*n,'period')
    for c in range(4):
      cs=list(comps(c,n))
      for x in cs:
        SG,_=stategraph(A,x)
        for y in cs:
            certpairs+=1;g=reduced(A,x,y)
            if g is None:check(y not in SG,'no integer image');continue
            found=False
            for u in product(*(range(v+1) for v in g)):
                boxes+=1
                if u==g:continue
                z=endpoint(A,x,u)
                if all(u[v]==g[v] or z[v]<sum(A[v]) for v in range(n)):
                    found=True
                    if min(z)<0:nonrealizablecert+=1
            check(found==(y not in SG),'negative certificate biconditional')
        # exhaustive legal words to length six for period deletion
        layer=[(x,())]
        for depth in range(7):
            nextlayer=[]
            for z,word in layer:
                counts=tuple(word.count(v) for v in range(n))
                if all(counts[v]>=p[v] for v in range(n)):
                    deleted=[0]*n;new=[]
                    for v in word:
                        if deleted[v]<p[v]:deleted[v]+=1
                        else:new.append(v)
                    state=x
                    for v in new:check(v in enabled(A,state),'period deletion legality');state=fire(A,state,v)
                    check(state==z,'period deletion endpoint');periodwords+=1
                if depth<6:
                    for v in enabled(A,z):nextlayer.append((fire(A,z,v),word+(v,)))
            layer=nextlayer
stats.update(certificate_pairs=certpairs,certificate_boxes=boxes,certificates_with_negative_coordinates=nonrealizablecert,period_deletion_words=periodwords)
# Exact loop-relay full-state classifications including arbitrary delayed returns.
loopcases=0
for a,b,l0,l1 in product(range(1,3),range(1,3),range(3),range(3)):
    A=[[l0,a],[b,l1]];parents=[v for v,l in enumerate([l0,l1]) if l]
    H=[[0]*(2+len(parents)) for _ in range(2+len(parents))]
    for i in range(2):
        for j in range(2):
            if i!=j:H[i][j]=A[i][j]
    for r,v in enumerate(parents,2):H[v][r]=H[r][v]=A[v][v]
    for c in range(4):
      for x in comps(c,2):
        loopcases+=1;SG,nh=stategraph(A,x);HG,nhh=stategraph(H,x+(0,)*len(parents));check(nh==nhh,'loop halting classification')
        check(sc(H),'loop relay SC')
        # all expanded legal words depth six, track pending relay returns
        layer=[(x+(0,)*len(parents),(0,)*len(H),(0,)*2)]
        for depth in range(7):
          nxt=[]
          for h,counts,oldcounts in layer:
            z=endpoint(A,x,oldcounts)
            for r,v in enumerate(parents,2):check(h[r]==A[v][v]*(counts[v]-counts[r]) and counts[r]<=counts[v] and z[v]-h[v]==h[r],'relay invariant')
            if depth<6:
              for v in enabled(H,h):
                cc=list(counts);cc[v]+=1;oo=list(oldcounts)
                if v<2:check(v in enabled(A,z),'projection legality');oo[v]+=1
                nxt.append((fire(H,h,v),tuple(cc),tuple(oo)))
          layer=nxt
stats['loop_relay_instances']=loopcases
signedwords=0
for a,b in product(range(1,3),repeat=2):
  A=[[0,a],[b,0]]
  for x in product(range(-2,3),repeat=2):
    shift=tuple(max(0,-v) for v in x);H=[r[:] for r in A]
    for v in range(2):H[v][v]+=shift[v]
    Y=tuple(x[v]+shift[v] for v in range(2));layer=[(x,Y)]
    for depth in range(7):
      nxt=[]
      for z,h in layer:
        signedwords+=1;check(enabled(A,z)==enabled(H,h),'signed/loop legality');check(h==tuple(z[v]+shift[v] for v in range(2)),'signed invariant')
        if depth<6:
          for v in enabled(A,z):nxt.append((fire(A,z,v),fire(H,h,v)))
      layer=nxt
stats['signed_word_prefixes']=signedwords
for ell in range(4):
    for x in range(5):
        SG,nh=stategraph([[ell]],(x,));check(nh==(x>=ell),'singleton loop halt');check(set(SG)=={(x,)},'singleton reach identity')
# Deliberate faulty variants must be rejected by a distinct witness.
A=[[0,1],[1,0]];x=(1,0);H,X,Y,N,M,B=gadget(A,x,{'M':1})
check(1 not in enabled(A,x) and 1 in enabled(H,X),'fault sensitivity small M');examples['fault_small_M']={'source':x,'source_enabled':enabled(A,x),'fault_gadget_enabled':enabled(H,X)}
A=[[0,1],[1,0]];x=(0,0);H,X,Y,N,M,B=gadget(A,x);bad=list(X);bad[2]+=1
check(2 in enabled(H,tuple(bad)) and not enabled(A,x),'fault early gate');examples['fault_early_gate']={'N':N,'source':x,'X':X,'wrong_X':bad}
A=[[0,1],[1,0]];x=(1,0);H,X,Y,N,M,B=gadget(A,x,{'B':3})
h=X;counts=[0,0]
for _ in range(N):
    v=next(v for v in enabled(H,h) if v<2);h=fire(H,h,v);counts[v]+=1
h=fire(H,h,2);failed=False
for v in range(2):
  for _ in range(N-counts[v]):
    if v not in enabled(H,h):failed=True;break
    h=fire(H,h,v)
  if failed:break
check(failed,'fault cleanup reserve sensitivity');examples['fault_small_B']={'B':3,'failure_state':h,'requested_vertex':v}
# Replacing strict < by <= would incorrectly certify a one-step reachable target.
x=(1,0);y=(0,1);u=(0,0);g=(1,0);check(y in stategraph(A,x)[0] and x[0]==sum(A[0]),'fault certificate boundary');examples['fault_nonstrict_certificate']={'x':x,'y':y,'g':g,'u':u}
# Huge binary values only construct the output, never enumerate its trajectory.
A=[[0,2**1000],[2**999+3,0]];x=(2**2048,2**1024);H,X,Y,N,M,B=gadget(A,x)
check(endpoint(H,X,(N,N,1,0))==Y and min(Y)>=0,'large binary exact output')
examples['binary_size']={'input_max_bits':max(v.bit_length() for r in A for v in r)+max(v.bit_length() for v in x),'N_bits':N.bit_length(),'output_max_bits':max(v.bit_length() for r in H for v in r)+max(v.bit_length() for v in X+Y)}
result={'completed_utc':datetime.now(timezone.utc).isoformat(),'status':'PASS finite controls only','independence':'Implemented before reading any submitted helper; no sibling/historical opinions consulted.','stats':stats,'examples':examples}
(HERE/'independent_results.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
