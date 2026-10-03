"""Independent signed-word lift + Artin free-word action + exact Fox3 controls.
Finite controls supplement the general proof, not a link-equivalence oracle.
"""
from collections import Counter
from itertools import product
from pathlib import Path
import datetime as dt, json, os, random
F=Path(__file__).absolute().parent;count=0;coverage=Counter();rng=random.Random(50010600042)
def check(x,n):
    global count
    if not x:raise ValueError(n)
    count+=1
def inv(w):return tuple(-i for i in reversed(w))
def valid(n,w):return type(n)is int and n>=1 and type(w)is tuple and all(type(i)is int and 1<=abs(i)<n for i in w)
def P(state):
    n,w=state;check(valid(n,w),'valid original');return state if n%2==0 else(n+1,w+(n,))
def template(name,N,a,b,sign=1):
    check(type(N)is int and N>=2 and N%2==0,'even state')
    k=N-1 if name in ('C','D')else N-2
    check(valid(k+1,a)and valid(k+1,b),'support');check(sign in (-1,1),'sign')
    if name=='C':return ((N,b),(N,a+b+inv(a)))
    if name=='BC':return ((N,b+(N-1,)),(N,a+b+inv(a)+(N-1,)))
    if name=='T':return ((N,b+(N-1,)),(N,b+(sign*(N-1),)))
    if name=='D':return ((N,b),(N+2,b+(sign*N,N+1)))
    raise ValueError(name)
def components(state):
    n,w=state;labels=list(range(n))
    for i in w:j=abs(i)-1;labels[j],labels[j+1]=labels[j+1],labels[j]
    seen=set();cycles=0
    for i in range(n):
        if i in seen:continue
        cycles+=1
        while i not in seen:seen.add(i);i=labels[i]
    return cycles
def fox_matrix(n,w):
    a=[[int(i==j)for j in range(n)]for i in range(n)]
    for i in w:
        k=abs(i)-1;u,v=a[k],a[k+1]
        if i>0:a[k],a[k+1]=v,[(2*y-x)%3 for x,y in zip(u,v)]
        else:a[k],a[k+1]=[(2*x-y)%3 for x,y in zip(u,v)],u
    return a
def rank3(a):
    a=[list(r)for r in a];rank=0
    for col in range(len(a[0])if a else 0):
        pivot=next((i for i in range(rank,len(a))if a[i][col]%3),None)
        if pivot is None:continue
        a[rank],a[pivot]=a[pivot],a[rank];scale=pow(a[rank][col]%3,-1,3);a[rank]=[(x*scale)%3 for x in a[rank]]
        for i in range(len(a)):
            if i!=rank:k=a[i][col]%3;a[i]=[(x-k*y)%3 for x,y in zip(a[i],a[rank])]
        rank+=1
    return rank
def fox(state):
    n,w=state;a=fox_matrix(n,w);return 3**(n-rank3([[(a[i][j]-int(i==j))%3 for j in range(n)]for i in range(n)]))
def reduce_word(w):
    s=[]
    for i in w:
        if s and s[-1]==-i:s.pop()
        else:s.append(i)
    return tuple(s)
def artin(n,w):
    images=[(i,)for i in range(1,n+1)]
    for letter in w:
        i=abs(letter);a=[(j,)for j in range(1,n+1)]
        if letter>0:a[i-1]=(i,i+1,-i);a[i]=(i,)
        else:a[i-1]=(i+1,);a[i]=(-(i+1),i,i+1)
        images=[reduce_word(tuple(k for j in u for k in (a[j-1]if j>0 else inv(a[-j-1]))))for u in images]
    return tuple(images)
def word(n,L):
    return tuple(rng.choice(tuple(range(1,n))+tuple(range(-n+1,0)))for _ in range(L))if n>1 else()
def test_edge(kind,n,a,b,sign=1):
    if kind=='conjugation':old=((n,b),(n,a+b+inv(a)));name='C'if n%2==0 else'BC'
    else:old=((n,b),(n+1,b+(sign*n,)));name='D'if n%2==0 else'T'
    new=tuple(P(s)for s in old);expected=template(name,n+n%2,a,b,sign)
    check(new==expected,'exact independent endpoint lift');check(new[::-1]==expected[::-1],'reverse lift')
    check(all(valid(*s)and s[0]%2==0 for s in new),'valid even endpoints')
    check(components(new[0])==components(new[1]),'component invariant')
    check(fox(new[0])==fox(new[1]),'Fox3 invariant')
    check(all(components(o)==components(p)and fox(o)==fox(p)for o,p in zip(old,new)),'padding invariants')
    check(max(s[0]for s in new)==2*((max(s[0]for s in old)+1)//2),'sharp height image')
    coverage[name]+=1
for n in range(1,11):
    for L in (0,1,3,8):
        for repeat in range(3):
            a=word(n,L);b=word(n,9-L);test_edge('conjugation',n,a,b)
            for sign in (-1,1):test_edge('stabilization',n,(),b,sign)
relations=0
for n in range(2,10):
    pairs=[]
    for i in range(1,n):pairs.extend([((i,-i),()),((-i,i),())])
    for i in range(1,n-1):
        for sign in (-1,1):pairs.append(((sign*i,sign*(i+1),sign*i),(sign*(i+1),sign*i,sign*(i+1))))
    for i in range(1,n):
        for j in range(i+2,n):
            for e in (-1,1):
                for f in (-1,1):pairs.append(((e*i,f*j),(f*j,e*i)))
    for left,right in pairs:
        pre=word(n,2);post=word(n,2);old=((n,pre+left+post),(n,pre+right+post));new=tuple(P(s)for s in old)
        tail=(n,)if n%2 else();N=n+n%2
        check(new==((N,pre+left+post+tail),(N,pre+right+post+tail)),'retained relation context')
        check(artin(N,new[0][1])==artin(N,new[1][1]),'Artin action relation and retained tail')
        check(fox(new[0])==fox(new[1])and components(new[0])==components(new[1]),'relation invariants');relations+=1
# Exhaustive field-specific local inverse/Yang-Baxter checks, distinct from lift code.
for colors in product(range(3),repeat=3):
    def act(w):
        a=list(colors)
        for i in w:
            k=abs(i)-1;x,y=a[k],a[k+1]
            a[k],a[k+1]=(y,(2*y-x)%3)if i>0 else((2*x-y)%3,x)
        return tuple(a)
    check(act((1,-1))==colors and act((-1,1))==colors,'exact Fox3 inverse')
    check(act((1,2,1))==act((2,1,2)),'exact Fox3 Yang-Baxter')
negative=[]
def reject(label,witness):negative.append(dict(label=label,witness=witness));check(True,'recorded actual mutant rejection')
check(components((2,(1,1,1)))==components((2,(1,)))==1,'same-component T counterexample')
check(fox((2,(1,1,1)))==9 and fox((2,(1,)))==3,'unsupported T changes nontrivial invariant')
reject('T lower-support omitted',dict(N=2,b=[1,1],left=[1,1,1],right=[1],Fox3_counts=[9,3],component_counts=[1,1]))
try:template('T',2,(),(1,1),-1)
except ValueError:reject('typed template refuses unsupported T',dict(N=2,b=[1,1]))
else:raise ValueError('bad support accepted')
left=(4,(3,3));right=(4,(2,3,-2,3));check(components(left)==4 and components(right)==2,'unsupported BC b changes components')
reject('BC b support omitted',dict(N=4,a=[2],b=[3],component_counts=[4,2]))
found=None
for L in range(1,4):
    for a in product((1,2,3,-1,-2,-3),repeat=L):
        left=(4,(2,3));right=(4,a+(2,)+inv(a)+(3,))
        if any(abs(i)==3 for i in a)and components(left)!=components(right):found=dict(N=4,a=list(a),b=[2],component_counts=[components(left),components(right)]);break
    if found:break
check(found is not None,'BC a support independent counterexample');reject('BC a support omitted',found)
check(components((2,()))!=components((4,())),'tags essential');reject('erase strand tag',dict(counts=[2,4],word=[]))
check(components((1,()))!=components((2,())),'idle strand is not padding');reject('pad odd with idle strand',dict(counts=[1,2]))
check(components((2,()))!=components((4,(2,))),'D second crossing necessary');reject('D terminal crossing omitted',dict(component_counts=[2,3]))
check(artin(4,(2,3,-2))!=artin(4,(3,)),'C versus BC distinct braid action')
reject('replace buffered odd conjugation lift by ordinary C literally',dict(m=3,a=[2],b=[],correct=[3],wrong=[2,3,-2],limits='Countercontrol of exact lift only; closures remain conjugate here.'))
check(P((1,()))==(2,(1,))and components(P((1,())))==1,'minimal unknot')
check(set(coverage)=={'C','BC','T','D'},'complete classical coverage')
result=dict(schema='pr50-independent-classical-controls/v1',status='PASS',actual_pid=os.getpid(),created_utc=dt.datetime.now(dt.timezone.utc).isoformat(),assertions=count,edge_cases=sum(coverage.values()),coverage=dict(coverage),relation_cases=relations,negative_controls=negative,Fox3_local_colors_cases=27,original_helper_imported=False,limits=['Finite controls supplement universal symbolic proof','Fox3/component invariants are incomplete','Artin action used to compare explicit relation/mutant examples only','No virtual certification or priority claim'])
with(F/'CONTROL_RESULT.json').open('xb')as h:h.write((json.dumps(result,indent=2,allow_nan=False)+'\n').encode())
print(json.dumps(result,indent=2))
