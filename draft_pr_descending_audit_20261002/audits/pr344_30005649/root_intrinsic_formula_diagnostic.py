#!/usr/bin/env python3
"""Read-only independent root falsification of the sealed generic formula.

Own polynomial arithmetic and elimination; no author or reviewer imports.
An optional original control path enables a separate comparison only after all
independent quantities have been computed. No writes or network.
"""
import json, random, runpy, sys
p=5; q=125
Z=(0,0,0); ONE=(1,0,0)
def add(a,b):return tuple((x+y)%p for x,y in zip(a,b))
def neg(a):return tuple(-x%p for x in a)
def mul(a,b):
    c=[0]*5
    for i,x in enumerate(a):
        for j,y in enumerate(b):c[i+j]+=x*y
    for i in (4,3):
        c[i-3]-=c[i];c[i-2]-=c[i]
    return tuple(x%p for x in c[:3])
def power(a,n):
    r=ONE
    while n:
        if n%2:r=mul(r,a)
        a=mul(a,a);n//=2
    return r
def sumf(xs):
    r=Z
    for x in xs:r=add(r,x)
    return r
def mm(a,b):return [[sumf(mul(x,y) for x,y in zip(row,col)) for col in zip(*b)] for row in a]
def trans(a):return [list(row) for row in zip(*a)]
def twist(a,e):return [[power(x,e) for x in row] for row in a]
def eye(n):return [[ONE if i==j else Z for j in range(n)] for i in range(n)]
def join(a,b):return [x+y for x,y in zip(a,b)]
def rref(a):
    a=[r[:] for r in a];pivots=[]
    for j in range(len(a[0])):
        r=next((i for i in range(len(pivots),len(a)) if a[i][j]!=Z),None)
        if r is None:continue
        d=len(pivots);a[r],a[d]=a[d],a[r];s=power(a[d][j],q-2)
        a[d]=[mul(s,x) for x in a[d]]
        for i in range(len(a)):
            if i!=d:
                s=a[i][j];a[i]=[add(x,neg(mul(s,y))) for x,y in zip(a[i],a[d])]
        pivots.append(j)
        if len(pivots)==len(a):break
    return a,pivots
rank=lambda a:len(rref(a)[1])
def kernel(a):
    r,pv=rref(a);free=[j for j in range(len(a[0])) if j not in pv];cols=[]
    for j in free:
        v=[Z]*len(a[0]);v[j]=ONE
        for i,c in enumerate(pv):v[c]=neg(r[i][j])
        cols.append(v)
    return trans(cols) if cols else [[] for _ in range(len(a[0]))]
def inverse(a):
    r,pv=rref(join(a,eye(len(a))));assert pv==list(range(len(a)))
    return [row[len(a):] for row in r]
def encoded(a):return [[x[0]+5*x[1]+25*x[2] for x in row] for row in a]
def invariant(A,B):
    C=mm(A,twist(A,5));D=mm(B,twist(B,25))
    AD=trans(twist(B,5));BD=trans(twist(A,25))
    CD=mm(AD,twist(AD,5));DD=mm(BD,twist(BD,25))
    assert CD==trans(twist(D,25)) and DD==trans(twist(C,5))
    Kf=twist(kernel(C),5);Kv=twist(kernel(D),25)
    for M,K,e in ((C,Kf,25),(D,Kv,5)):
        assert all(x==Z for row in mm(M,twist(K,e)) for x in row)
    actual=rank(CD)+rank(DD)-rank(join(CD,DD))
    semantic=len(A)-rank(join(Kf,Kv))
    corrected=rank(C)+rank(D)-rank(join(trans(twist(D,25)),trans(twist(C,5))))
    bare=rank(C)+rank(D)-rank(join(trans(C),trans(D)))
    assert actual==semantic==corrected
    return dict(delta=rank(C)+rank(D)-rank(join(C,D)),dual_delta=actual,semantic_kernel_codimension=semantic,corrected=corrected,bare=bare,C=C,D=D)
assert all((x**3+x+1)%5 for x in range(5))
for x in range(1,125):
    a=(x%5,x//5%5,x//25);assert mul(a,power(a,123))==ONE
F=[[Z]*6 for _ in range(6)];V=[[Z]*6 for _ in range(6)]
for i,j in ((0,1),(1,2),(3,4)):F[j][i]=ONE
for i,j in ((0,5),(3,2),(5,4)):V[j][i]=ONE
rows=[]
for name in ('minimal','dense'):
    P=eye(6)
    if name=='minimal':P[0][1]=(0,1,0)
    else:
        rng=random.Random(34002)
        for i in range(6):
            for j in range(i+1,6):P[i][j]=(rng.randrange(5),rng.randrange(1,5),rng.randrange(5))
    Pi=inverse(P);assert mm(P,Pi)==eye(6)==mm(Pi,P)
    A=mm(mm(Pi,F),twist(P,5));B=mm(mm(Pi,V),twist(P,25));iv=invariant(A,B)
    assert iv['delta']==0 and iv['dual_delta']==iv['corrected']==1 and iv['bare']==0
    row=dict(name=name,P=encoded(P),F=encoded(A),V=encoded(B),F2=encoded(iv.pop('C')),V2=encoded(iv.pop('D')),**iv)
    if len(sys.argv)==2:
        original=runpy.run_path(sys.argv[1]);k=original['Field'](5,[1,1,0,1])
        old=original['invariants'](encoded(A),encoded(B),k)
        assert old['dual_kernel_formula']==0 and old['dual_delta2']==1
        row['original_helper']=old
    rows.append(row)
print(json.dumps(dict(status='INDEPENDENT_FORMULA_COUNTEREXAMPLES_REPRODUCED',field='F5[t]/(t^3+t+1)',witnesses=rows,main_theorem_implication='none: its correctly twisted dual calculation is unchanged',repair_required=True),indent=2))
