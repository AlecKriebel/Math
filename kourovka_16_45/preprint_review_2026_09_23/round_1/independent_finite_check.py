#!/usr/bin/env python3
"""Fresh exact referee check, written before reading the supplied verifiers.

Run from any directory. Only the Python standard library is required.
No tables, certificates, or project modules are imported.
"""
from collections import Counter
from functools import reduce
from itertools import combinations, product
from operator import and_
from pathlib import Path
import hashlib
import json
import time

started = time.time()
out = {}

def require(condition, detail):
    if not condition:
        raise ValueError(detail)

def mm(x, y, p):
    a,b,c,d = x
    e,f,g,h = y
    return ((a*e+b*g)%p,(a*f+b*h)%p,(c*e+d*g)%p,(c*f+d*h)%p)

I = (1,0,0,1)

def closure(gens, ident, mul):
    found, queue = {ident}, [ident]
    for x in queue:
        for g in gens:
            y = mul(x,g)
            if y not in found:
                found.add(y)
                queue.append(y)
    return frozenset(found)

def power(x, n, ident, mul):
    ans = ident
    for _ in range(n):
        ans = mul(ans,x)
    return ans

def order(x, ident, mul):
    ans = x
    k = 1
    while ans != ident:
        ans = mul(ans,x)
        k += 1
        require(k < 10000, 'order search cap')
    return k

p = 29
m = lambda x,y: mm(x,y,p)
A,B = (0,28,1,0),(2,7,12,28)
H = closure([A,B], I, m)
Z = frozenset([I,(28,0,0,28)])
require(len(H)==120, 'H order')
require(all((h[0]*h[3]-h[1]*h[2])%29==1 for h in H),'H determinants')
require(power(A,2,I,m)==power(B,3,I,m)==power(m(A,B),5,I,m)==(28,0,0,28), 'triangle relations')
out['H_order'] = len(H)
out['H_element_orders'] = dict(sorted(Counter(order(h,I,m) for h in H).items()))

# Paired closure proves each claimed generator mapping is consistent at every word.
slgens = [(0,4,1,0),(0,4,1,1)]
pairs = closure(list(zip(slgens,[A,B])), (I,I), lambda x,y:(mm(x[0],y[0],5),m(x[1],y[1])))
slall = {x for x in product(range(5),repeat=4) if (x[0]*x[3]-x[1]*x[2])%5==1}
require(len(pairs)==120 and {x for x,y in pairs}==slall and {y for x,y in pairs}==H, 'SL2(5) isomorphism')
out['SL2_5_generator_map'] = 'bijective homomorphism via 120 paired words'
permI = tuple(range(5))
pa,pb = (1,0,3,2,4),(2,1,4,3,0)
pm = lambda x,y: tuple(x[y[i]] for i in range(5))
apairs = closure([(A,pa),(B,pb)], (I,permI),lambda x,y:(m(x[0],y[0]),pm(x[1],y[1])))
require(len(apairs)==120 and len({y for x,y in apairs})==60,'A5 quotient sizes')
require({x for x,y in apairs if y==permI}==Z, 'A5 quotient kernel')
out['A5_quotient'] = {'order':60,'kernel':sorted(Z)}

R = [A,(12,24,0,17),(25,3,4,4)]
require(R[1]==m(m(B,A),power(B,2,I,m)), 'R2 word')
require(R[2]==m(m(A,R[1]),power(m(A,B),2,I,m)), 'R3 word')
require(all(r in H and m(r,r)==(28,0,0,28) for r in R), 'R squares')
omits = [closure(R[:i]+R[i+1:],I,m) for i in range(3)]
require([len(x) for x in omits]==[8,12,20], 'pair orders')
require(reduce(and_,omits)==Z,'pair-subgroup triple intersection')
require(len(closure(R,I,m))==120,'R generate H')
require([order(m(R[1],R[2]),I,m),order(m(R[0],R[2]),I,m),order(m(R[0],R[1]),I,m)]==[4,3,10],'product orders')
out['R_pair_orders'] = [len(x) for x in omits]
out['R_pair_intersection_orders'] = [len(x&y) for x,y in combinations(omits,2)]

# Completely enumerate H subgroups without any external group information.
Hlist=sorted(H)
ix={h:i for i,h in enumerate(Hlist)}
table=[[ix[m(x,y)] for y in Hlist] for x in Hlist]
identity=ix[I]
mulid=lambda x,y: table[x][y]
trivial=frozenset([identity])
subgroups={trivial:()}
todo=[trivial]
for K in todo:
    for x in range(120):
        if x not in K:
            gs=subgroups[K]+(x,)
            J=closure(gs,identity,mulid)
            if J not in subgroups:
                subgroups[J]=gs
                todo.append(J)
require(len(todo)==76,'subgroup count')
out['H_subgroup_order_counts']=dict(sorted(Counter(map(len,todo)).items()))
mask=lambda K: sum(1<<x for x in K)
proper=[mask(K) for K in todo if len(K)<120]
full=(1<<120)-1
def is_irredundant(family):
    total=reduce(and_,family,full)
    return all(reduce(and_,family[:i]+family[i+1:],full)!=total for i in range(len(family)))
four_count=0
for family in combinations(proper,4):
    four_count += 1
    require(not is_irredundant(family),'irredundant H four-family')
faithful_three=0
three_count=0
for family in combinations(proper,3):
    three_count += 1
    if reduce(and_,family)==1<<identity and is_irredundant(family):
        faithful_three += 1
require(four_count==1215450 and three_count==67525 and faithful_three==0,'H family counts')
out['exhaustive_H_family_counts']={'four':four_count,'three':three_count,'irredundant_four':0,'faithful_minimal_three':0}
linevecs=[(1,t) for t in range(p)]+[(0,1)]
line_counts=[]
for v in linevecs:
    stab=[h for h in H if ((h[0]*v[0]+h[1]*v[1])*v[1]-(h[2]*v[0]+h[3]*v[1])*v[0])%p==0]
    require(len(stab)==4 and any(order(h,I,m)==4 for h in stab),'cyclic line stabilizer')
    line_counts.append(len(stab))
out['line_stabilizer_orders']=dict(Counter(line_counts))

def am(x,y,p):
    u,v,a,b,c,d=x
    s,t,e,f,g,h=y
    return ((u+a*s+b*t)%p,(v+c*s+d*t)%p,*mm((a,b,c,d),(e,f,g,h),p))

affI=(0,0,*I)
affmul=lambda x,y:am(x,y,29)
S=[(1,0,*I)]+[(0,0,*r) for r in R]
G=closure(S,affI,affmul)
affomits=[closure(S[:i]+S[i+1:],affI,affmul) for i in range(4)]
require(len(G)==100920,'G order')
require([len(K) for K in affomits]==[120,6728,10092,16820],'affine omission orders')
require(all(S[i] not in affomits[i] for i in range(4)), 'affine independence')
Z0=frozenset((0,0,*h) for h in Z)
require(reduce(and_,affomits)==Z0,'affine total intersection')
conj=affmul(affmul((1,0,*I),(0,0,28,0,0,28)),(28,0,*I))
require(conj==(2,0,28,0,0,28) and conj not in Z0,'nonnormality')
out['G_order']=len(G)
out['affine_omission_orders']=[len(K) for K in affomits]
minus=(28,0,0,28)
L=[closure([(1,0,*I),(0,0,*minus)],affI,affmul),closure([(0,1,*I),(0,0,*minus)],affI,affmul),closure([(1,1,*I),(2,0,*minus)],affI,affmul)]
want=[{affI,(0,0,*minus)},{affI,(2,0,*minus)},{affI,(0,27,*minus)}]
require([len(K) for K in L]==[58]*3 and [x&y for x,y in combinations(L,2)]==want and reduce(and_,L)=={affI},'faithful three-family')
out['faithful_three_family']={'orders':[58]*3,'pair_intersections':[sorted(x&y) for x,y in combinations(L,2)],'total_order':1,'degree':5220}

A11,B11,C=(0,10,1,0),(0,2,5,1),(6,10,0,2)
m11=lambda x,y:mm(x,y,11)
H11=closure([A11,B11],I,m11)
require(len(H11)==120 and C in H11 and order(C,I,m11)==10,'char11 complement and C')
a11=lambda x,y:am(x,y,11)
boundarygens=[[(1,0,*I),(0,0,*C)],[(1,4,*I),(0,0,*C)],[(1,0,*I),(0,1,*I),(0,0,*power(C,5,I,m11))],[(1,0,*I),(0,1,*I),(0,0,*power(C,2,I,m11))]]
boundary=[closure(gs,affI,a11) for gs in boundarygens]
deletions=[len(reduce(and_,boundary[:i]+boundary[i+1:])) for i in range(4)]
require(reduce(and_,boundary)=={affI} and deletions==[11,11,5,2],'boundary family')
out['characteristic_11']={'complement_order':len(H11),'C_order':10,'family_orders':[len(K) for K in boundary],'deletion_orders':deletions,'total_order':1}
out['status']='all checks passed'
out['elapsed_seconds']=round(time.time()-started,3)
out['checker_sha256']=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
print(json.dumps(out,indent=2,sort_keys=True))
