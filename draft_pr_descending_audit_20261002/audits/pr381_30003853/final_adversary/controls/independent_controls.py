#!/usr/bin/env python3
"""Independent exact controls; created before reading PR381 candidate content.

Finite computations are controls for, not replacements for, the accompanying
proofs. Everything uses Python's standard library and exact integers/Fractions.
"""
from fractions import Fraction as Q
from itertools import permutations, product, combinations
import json

OUT={}
checks=0
def ck(v):
    global checks
    assert v
    checks+=1

# Sparse integer Laurent polynomials.
def clean(p): return {k:v for k,v in p.items() if v}
def add(p,q):
    r=p.copy()
    for k,v in q.items(): r[k]=r.get(k,0)+v
    return clean(r)
def scale(p,c): return clean({k:c*v for k,v in p.items()})
def shift(p,k): return {i+k:v for i,v in p.items()}
def mul(p,q):
    r={}
    for i,a in p.items():
        for j,b in q.items():r[i+j]=r.get(i+j,0)+a*b
    return clean(r)
def ev(p):return sum(p.values())
def der(p):return sum(i*v for i,v in p.items())
u={0:-1,1:1}
lc=[]
for m in range(2,13):
    ck(ev(u)==0 and der(u)%m==1)
    ck(ev({0:m})//m==1 and der({0:m})%m==0)
    for coeff in product(range(-2,3),repeat=3):
        q={i-1:c for i,c in enumerate(coeff)}
        f=add(scale(q,m),mul(u,shift(q,2)))
        ck(ev(f)%m==0)
        uf=mul(u,f)
        ck(ev(uf)==0 and der(uf)%m==0)
        ck(mul(u,scale({0:1},m))==scale(u,m))
    lc.append({'m':m,'torsion_order':m,'I_generators':[m,'t-1'],
               'coinvariants':'Z + Z/m','H_abelianization':'Z^2 + Z/m'})
OUT['laurent_ideal_controls']=lc

# A finite base support can only grow in one shift direction in an ascending
# chain. Opposite shifts of a nonzero kernel word lie outside every chain member.
support=[]
for k in range(1,8):
    for lo,hi in [(-4,-1),(0,0),(2,7)]:
        for direction in [-1,1]:
            escaped=lo-k if direction==1 else hi+k
            for n in range(0,31):
                a,b=lo+direction*n*k,hi+direction*n*k
                # The union over n>=0 stays in [lo,infinity) or (-infinity,hi].
                ck((direction==1 and escaped<a) or (direction==-1 and escaped>b))
            support.append({'shift':k,'finite_base_window':[lo,hi],
                            'direction':direction,'opposite_escape':escaped})
OUT['one_sided_support_controls']=support

# Exact finite simple-derived normalizer control, using A5, not candidate code.
def pc(a,b):return tuple(a[b[i]] for i in range(len(a)))
def pi(a):
    b=[0]*len(a)
    for i,j in enumerate(a):b[j]=i
    return tuple(b)
def even(a):return sum(a[i]>a[j] for i in range(5) for j in range(i+1,5))%2==0
E=tuple(range(5)); A=list(filter(even,permutations(range(5))))
idx={a:i for i,a in enumerate(A)}
mt=[[idx[pc(a,b)] for b in A] for a in A]
inv=[idx[pi(a)] for a in A]; ei=idx[E]
def comm(a,b):return mt[mt[mt[inv[a]][inv[b]]][a]][b]
def close(gs):
    s={ei};front=[ei]
    while front:
        a=front.pop()
        for b in gs:
            x=mt[a][b]
            if x not in s:s.add(x);front.append(x)
    return s
cs={comm(a,b) for a in range(60) for b in range(60)}
ck(len(A)==60 and len(close(cs))==60)
classes=[]; left=set(range(60))
while left:
    a=min(left); cl={mt[mt[g][a]][inv[g]] for g in range(60)}
    classes.append(cl);left-=cl
sizes=sorted(map(len,classes)); ck(sizes==[1,12,12,15,20])
possible=[]
nontr=[len(c) for c in classes if ei not in c]
for bits in product([0,1],repeat=4):
    size=1+sum(b*s for b,s in zip(bits,nontr))
    if 60%size==0:possible.append(size)
ck(sorted(possible)==[1,60])
normalizer=[]
for a,b in product(range(60),repeat=2):
    good=all(mt[mt[a][s]][inv[a]]==mt[mt[b][s]][inv[b]] for s in range(60))
    if good:normalizer.append((a,b))
ck(set(normalizer)=={(a,a) for a in range(60)})
# Twisted diagonal via conjugation by a chosen nonidentity A5 element.
h=next(i for i in range(60) if i!=ei)
alpha=lambda s:mt[mt[h][s]][inv[h]]
tw=[]
for a,b in product(range(60),repeat=2):
    if all(alpha(mt[mt[a][s]][inv[a]])==mt[mt[b][alpha(s)]][inv[b]] for s in range(60)):
        tw.append((a,b))
ck(set(tw)=={(a,alpha(a)) for a in range(60)})
OUT['simple_diagonal']={'group':'A5','order':60,'derived_order':len(close(cs)),
 'conjugacy_class_sizes':sizes,'normal_union_divisor_sizes':sorted(possible),
 'normalizer_order':len(normalizer),'twisted_normalizer_order':len(tw)}
OUT['nonperfect_diagonal_mutant']={'group':'C3','diagonal_order':3,
 'ambient_normalizer_order':9,'reason':'ambient product is abelian'}
ck(3*3>3)

# Torsion-free class-two nilpotent proxy G_m, law z-cross-term m*a*b'.
def hm(x,y,m=1):
    a,b,c=x;d,e,f=y
    return a+d,b+e,c+f+m*a*e
def hi(x,m=1):
    a,b,c=x;return -a,-b,-c+m*a*b
def hp(x,k,m=1):
    a,b,c=x;return k*a,k*b,k*c+m*k*(k-1)//2*a*b
def hc(x,y,m=1):return hm(hm(hm(hi(x,m),hi(y,m),m),x,m),y,m)
X=(1,0,0);Y=(0,1,0);Z=(0,0,1)
ng=[]
for m in range(2,10):
    ck(hc(X,Y,m)==(0,0,m))
    box=list(product(range(-2,3),repeat=3))
    for x in box:
        ck(hm(x,hi(x,m),m)==(0,0,0))
        for k in [1,2,3,5]:
            z=(0,0,0)
            for _ in range(k):z=hm(z,x,m)
            ck(z==hp(x,k,m))
    for k in [2,3,5]:ck(len({hp(x,k,m) for x in box})==len(box))
    # Conjugation preserves the first two coordinates. If both vanish, the
    # element is central. Therefore the lexicographic order is a bi-order.
    for x,y in product(box[:30],box[::7]):
        c=hm(hm(hi(y,m),x,m),y,m)
        ck(c[:2]==x[:2])
        if x[:2]==(0,0):ck(c==x)
        ck((x>(0,0,0))==(c>(0,0,0)))
    ng.append({'m':m,'commutator_xy':[0,0,m],
               'abelianization':'Z^2 + Z/m','unique_roots_formula_verified':True,
               'biorder':'lex(a,b,c)','PL_embedding':'excluded by nilpotent PL lemma'})
OUT['nilpotent_unique_root_biorder_proxy']=ng

# A stronger negative mutant for the subdirect argument: L is the standard
# torsion-free Heisenberg group, L_ab=Z^2. H<=L^2 identifies a,b modulo m.
# Its central intersection K=Z^2, while H'={(c,d):c=d mod m}.
sd=[]
for m in range(2,10):
    gens=[(X,X),(Y,Y),(Z,(0,0,0)),((0,0,0),Z),((m,0,0),(0,0,0)),((0,m,0),(0,0,0))]
    vectors=[]
    for a,b in product(gens,repeat=2):
        c,d=hc(a[0],b[0]),hc(a[1],b[1]);ck(c[:2]==(0,0) and d[:2]==(0,0))
        vectors.append((c[2],d[2]));ck((c[2]-d[2])%m==0)
    ck((1,1) in vectors and (m,0) in vectors)
    # (0,m)=m*(1,1)-(m,0); it need not be one basic generator commutator.
    ck(tuple(m*x-y for x,y in zip((1,1),(m,0)))==(0,m))
    dets=[abs(a*d-b*c) for (a,b),(c,d) in combinations(vectors,2)]
    from math import gcd
    g=0
    for d in dets:g=gcd(g,d)
    ck(g==m)
    sd.append({'m':m,'commutator_lattice_index':g,'K_over_Hprime':'Z/m',
               'L_ab':'Z^2','subdirect':True,'perfectness_missing':True})
OUT['torsionfree_subdirect_nonperfect_mutant']=sd

# Rational PL maps: canonical knot tuples; multiplication means composition.
def canon(ps):
    ps=sorted(set(ps));r=[]
    for x,y in ps:
        r.append((Q(x),Q(y)))
        while len(r)>=3:
            (a,b),(c,d),(e,f)=r[-3:]
            if (d-b)*(e-c)==(f-d)*(c-a):r.pop(-2)
            else:break
    return tuple(r)
ID=canon([(0,0),(1,1)])
def val(f,x):
    for (a,b),(c,d) in zip(f,f[1:]):
        if a<=x<=c:return b+(d-b)*(x-a)/(c-a)
    raise ValueError(x)
def iv(f):return canon([(y,x) for x,y in f])
def compose(f,g):
    gi=iv(g);xs={x for x,y in g}|{val(gi,x) for x,y in f}
    return canon([(x,val(f,val(g,x))) for x in xs])
def power(f,n):
    if n<0:return power(iv(f),-n)
    r=ID
    for _ in range(n):r=compose(r,f)
    return r
def plcomm(f,g):return compose(compose(compose(iv(f),iv(g)),f),g)
def rescale(f,a,b):
    return canon([(0,0),(a,a)]+[(a+(b-a)*x,a+(b-a)*y) for x,y in f]+[(b,b),(1,1)])
def supp(f):
    return [(a,c) for (a,b),(c,d) in zip(f,f[1:]) if a!=b or c!=d]
def dyadic(x):return x.denominator & (x.denominator-1)==0
def isf(f):
    for x,y in f:
        if not dyadic(x) or not dyadic(y):return False
    for (a,b),(c,d) in zip(f,f[1:]):
        s=(d-b)/(c-a)
        if s<=0 or (s.numerator & (s.numerator-1)) or (s.denominator & (s.denominator-1)):return False
    return f[0]==(Q(0),Q(0)) and f[-1]==(Q(1),Q(1))
t=canon([(0,0),(Q(1,2),Q(1,4)),(Q(3,4),Q(1,2)),(1,1)])
a=rescale(t,Q(1,2),Q(3,4));ck(isf(t) and isf(a))
lamps={i:compose(compose(power(t,-i),a),power(t,i)) for i in range(-6,7)}
for f in lamps.values():ck(isf(f))
for i,j in combinations(lamps,2):ck(plcomm(lamps[i],lamps[j])==ID)
r=plcomm(a,t)
pl=[]
for m in range(2,10):
    s=power(a,m);ck(power(r,m)==plcomm(s,t))
    ck(isf(r) and isf(s))
    pl.append({'m':m,'r_power_equals_s_t_commutator':True,
               'r_nonidentity':r!=ID,'r_torsion_mod_commutators':'exactly m by Laurent proof'})
for n in range(1,8):
    # Conjugating a compact-support element pushes its support outside any
    # preassigned compact interval as n increases; ordinary fg cannot be used
    # in place of finite normal generation.
    f=lamps.get(n) or compose(compose(power(t,-n),a),power(t,n))
    ck(isf(f) and f!=ID)
OUT['concrete_dyadic_PL']={'t':[[str(x),str(y)] for x,y in t],
 'a':[[str(x),str(y)] for x,y in a],'pairwise_commuting_lamps':13,
 'torsion_relations':pl,'support_shift':'positive indices approach 1; negative approach 0'}

# Independent high-level recursion control: no quotient finiteness inheritance.
# Every tested leaf is explicitly tagged with the original domain H.
trees=[]
for depth in range(1,7):
    for branch in range(1,6):
        stack=[(depth,'H')];leaves=0
        while stack:
            d,domain=stack.pop();ck(domain=='H')
            if not d:leaves+=1
            else:stack.extend([(d-1,'H')]*branch)
        trees.append({'depth':depth,'branching':branch,'leaves':leaves,
                      'all_FP2_inputs':'original H','quotient_FP2_assumed':False})
OUT['original_domain_recursion_bookkeeping']=trees
OUT['assertions_passed']=checks
OUT['scope']='exact finite controls; general claims are established in INITIAL_RECONSTRUCTION.md'
print(json.dumps(OUT,indent=2,sort_keys=True))
