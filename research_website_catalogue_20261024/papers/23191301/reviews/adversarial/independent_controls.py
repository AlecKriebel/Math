#!/usr/bin/env python3
"""Fresh controls derived from published manuscript; does not import supplied helper/certificate."""
from fractions import Fraction as F
from itertools import product
from math import factorial
from pathlib import Path
import json,hashlib,time
checks=[]
def ck(label, value):
    assert value,label
    checks.append(label)
def poly(terms): return {tuple(a):F(c) for a,c in terms if c}
def add(*ps):
    r={}
    for p in ps:
        for a,c in p.items():r[a]=r.get(a,F(0))+c
    return {a:c for a,c in r.items() if c}
def mul(p,q):
    r={}
    for a,c in p.items():
        for b,d in q.items():
            k=tuple(x+y for x,y in zip(a,b));r[k]=r.get(k,F(0))+c*d
    return {a:c for a,c in r.items() if c}
def scale(p,c):return {a:b*c for a,b in p.items() if b*c}
def powp(p,n):
    r={(0,0,0):F(1)}
    for _ in range(n):r=mul(r,p)
    return r
def square_diff(a,b,k=1):return powp(poly([(a,1),(b,-k)]),2)
p=poly([((4,2,0),1),((2,4,0),1),((0,0,6),1),((2,2,2),-1)])
hpairs=[((5,4,0),(3,4,2)),((4,5,0),(4,3,2)),((4,2,3),(2,2,5)),((2,4,3),(2,2,5)),((1,2,6),(3,4,2)),((2,1,6),(4,3,2)),((2,4,3),(4,2,3)),((4,5,0),(2,1,6)),((5,4,0),(1,2,6))]
rest=[((0,0,9),(2,2,5)),((1,1,7),(3,3,3)),((3,6,0),(3,4,2)),((3,5,1),(3,3,3)),((6,3,0),(4,3,2)),((5,3,1),(3,3,3))]
rhs=add(*(scale(square_diff(a,b),F(3,2)) for a,b in hpairs),*(square_diff(a,b,2) for a,b in rest),{(6,6,6):F(2)})
ck('complete credited SOS identity exact polynomial equality',rhs==powp(p,3))
ck('all displayed square factors homogeneous of degree9',all(sum(a)==sum(b)==9 for a,b in hpairs+rest))
p_original=add(p,{(2,2,2):F(-2)})
ck('negative control: coefficient3 Motzkin cannot use this identity',powp(p_original,3)!=rhs)
for q in [3,5,7]:
    ck(f'odd power q={q} exact multiplied-square identity',mul(rhs,powp(p,q-3))==powp(p,q))
def gaussian(a):
    out=1
    for k in a:
        if k%2:return 0
        for j in range(1,k,2):out*=j
    return out
six={(3,0,0):2**24,(0,3,0):2**24,(2,1,0):1,(1,2,0):1,(0,0,3):1,(1,1,1):4,(1,0,2):32,(0,1,2):32,(2,0,1):4096,(0,2,1):4096}
T={4:10**16,5:10**34,6:10**53,7:10**73,8:10**94,9:10**116}
def moment(a):
    assert sum(a)<=18
    if any(k%2 for k in a):return F(0)
    r=sum(a)//2
    if r==0:return F(1)
    if r<=2:return F(gaussian(a),1024)
    if r==3:return F(six[tuple(k//2 for k in a)])
    return F(T[r]*gaussian(a))
def expect(p):return sum((c*moment(a) for a,c in p.items()),F(0))
a=[expect(powp(p,j)) for j in range(4)]
ck('seed moments exact from independent sparse expansion',a==[1,-1,11292*10**53,35039520*10**116])
ck('no measure interpretation: nonnegative seed has negative functional value',a[1]<0)
mon=[(i,j,k) for i in range(10) for j in range(10-i) for k in range(10-i-j)]
ck('local monomial count220',len(mon)==220)
blocks={s:[v for v in mon if tuple(k%2 for k in v)==s] for s in product(range(2),repeat=3)}
ck('largest parity block35',max(map(len,blocks.values()))==35)
ck('cross parity entries vanish',all(moment(tuple(x+y for x,y in zip(u,v)))==0 for s,U in blocks.items() for t,V in blocks.items() if s!=t for u in U for v in V))
def matrix(mons):return [[moment(tuple(x+y for x,y in zip(u,v))) for v in mons] for u in mons]
def ldl(M):
    n=len(M); L=[[F(int(i==j)) for j in range(n)] for i in range(n)]; D=[]
    for j in range(n):
        d=M[j][j]-sum((L[j][k]**2*D[k] for k in range(j)),F(0))
        assert d>0,('nonpositive pivot',j,d)
        D.append(d)
        for i in range(j+1,n):L[i][j]=(M[i][j]-sum((L[i][k]*L[j][k]*D[k] for k in range(j)),F(0)))/d
    assert all(M[i][j]==sum((L[i][k]*D[k]*L[j][k] for k in range(n)),F(0)) for i in range(n) for j in range(n))
    return L,D
start=time.monotonic(); block_evidence=[]
for s,U in blocks.items():
    L,D=ldl(matrix(U));ck('positive pivots and exact reconstruction parity'+''.join(map(str,s)),len(D)==len(U))
    block_evidence.append({'parity':list(s),'dimension':len(U),'positive_pivots':len(D),'pivot_sha256':hashlib.sha256(json.dumps([str(x) for x in D]).encode()).hexdigest()})
initial_expected={'000':['1','3071/1048576','2047/268435456','5117/274877906944'],'001':['1/1024','1015/1048576','3109055/1048576','1056109395/131072'],'010':['1/1024','32767/1048576','16642474743/32768','257328824345/1048576'],'100':['1/1024','32767/1048576','16359/1048576','257328824345/1048576'],'011':['1/1024'],'101':['1/1024'],'110':['1/1024'],'111':['4']}
for s,U in blocks.items():
    U=[u for u in U if sum(u)<=3];_,D=ldl(matrix(U));det=F(1);mins=[]
    for d in D:det*=d;mins.append(str(det))
    ck('printed initial minors '+''.join(map(str,s)),mins==initial_expected[''.join(map(str,s))])
N=10**62
cubic=N*a[3]+3*N*(N-1)*a[2]*a[1]+N*(N-1)*(N-2)*a[1]**3
ck('finite N cubic exact negative',cubic<0)
ck('printed cubic upper bound',cubic<=N*(a[3]-(N*N-1))<0)
ck('finite N displayed numerical inequality',35039520*10**116<10**124-1)
# Independent occupancy expansion compared with labelled-factor direct assignments.
# These synthetic moments test the combinatorics; they are not a PSD certificate above degree18.
def partitions(seq):
    if not seq:yield [];return
    x,*xs=seq
    for p0 in partitions(xs):
        yield [(x,)]+p0
        for i in range(len(p0)):yield p0[:i]+[(x,)+p0[i]]+p0[i+1:]
def falling(s,r):
    out=1
    for j in range(r):out*=s-j
    return out
for q in range(1,7):
    aj=[1,-1]+[j*j+1 for j in range(2,q+1)]
    for s in [1,2,3]:
        direct=0
        for assign in product(range(s),repeat=q):
            v=1
            for i in range(s):v*=aj[assign.count(i)]
            direct+=v
        parted=0
        for part in partitions(list(range(q))):
            v=falling(s,len(part))
            for b in part:v*=aj[len(b)]
            parted+=v
        ck(f'partition expansion q{q}s{s}',direct==parted)
    ck(f'leading sign control q{q}',((-1)**q<0)==(q%2==1))
# Tensor positivity checked on a concrete truncation; universal proof remains analytic.
U=[u for u in mon if sum(u)<=1];M=matrix(U);K=[[M[i][j]*M[k][l] for j,l in product(range(len(U)),repeat=2)] for i,k in product(range(len(U)),repeat=2)]
ldl(K);ck('two-block local tensor matrix exact PD',True)
out={'status':'PASS','source_pdf_sha256':'78930bbd8e727df2de0ca64ac3b5994a7e3392a289bd9058a4fc8dce02fd9e66','checks':checks,'check_count':len(checks),'full_local_positive_pivots':sum(x['positive_pivots'] for x in block_evidence),'parity_blocks':block_evidence,'moments':[str(x) for x in a],'N':str(N),'cubic_negative':True,'cubic_sha256':hashlib.sha256(str(cubic).encode()).hexdigest(),'elapsed_seconds':time.monotonic()-start,'limits':'Fresh exact local and combinatorial controls. No giant tensor matrix constructed; arbitrary block count and all odd q require the analytic proof. No supplied helper or certificate imported.'}
print(json.dumps(out,indent=2))
