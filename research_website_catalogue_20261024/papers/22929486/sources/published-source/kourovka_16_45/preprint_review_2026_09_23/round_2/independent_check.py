#!/usr/bin/env python3
"""Fresh round-2 checker. Written from the manuscript before reading supplied code.

No project modules, data files, certificates, or previous review results are read.
All groups are reconstructed from printed generators using exact modular arithmetic.
"""
from collections import Counter
from datetime import datetime, timezone
from functools import reduce
from itertools import combinations, product
from pathlib import Path
import hashlib
import json
import time

START = time.monotonic()
OUT = Path(__file__).resolve().parent
RESULT = {"started_utc": datetime.now(timezone.utc).isoformat(), "checks": []}

def require(condition, name):
    if not condition:
        raise RuntimeError(name)
    RESULT["checks"].append(name)

I = (1, 0, 0, 1)
def mul(x, y, p):
    a,b,c,d = x
    e,f,g,h = y
    return ((a*e+b*g)%p,(a*f+b*h)%p,(c*e+d*g)%p,(c*f+d*h)%p)

def closure(gens, identity, operation):
    seen = {identity}
    queue = [identity]
    for x in queue:
        for g in gens:
            y = operation(x, g)
            if y not in seen:
                seen.add(y)
                queue.append(y)
    return frozenset(seen)

def power(g,n,p):
    x = I
    for _ in range(n): x = mul(x,g,p)
    return x

def inv(g,p):
    a,b,c,d = g
    return (d,-b%p,-c%p,a)

def order(g,p):
    return len(closure((g,),I,lambda x,y:mul(x,y,p)))

p = 29
A, B = (0,28,1,0), (2,7,12,28)
H = closure((A,B),I,lambda x,y:mul(x,y,p))
Z = frozenset((I,(28,0,0,28)))
require(len(H)==120 and all((a*d-b*c)%29==1 for a,b,c,d in H),"H has 120 determinant-one matrices")
require(power(A,2,p)==power(B,3,p)==power(mul(A,B,p),5,p)==(28,0,0,28),"triangle relations")
require({x for x in H if x!=I and mul(x,x,p)==I}==Z-{I},"unique involution")

# A simultaneous word graph must yield one image per SL2(5) matrix.
a5,b5 = (0,4,1,0),(0,4,1,1)
graph = closure(((a5,A),(b5,B)),(I,I),lambda x,y:(mul(x[0],y[0],5),mul(x[1],y[1],29)))
all_sl5 = {x for x in product(range(5),repeat=4) if (x[0]*x[3]-x[1]*x[2])%5==1}
iso = dict(graph)
require(len(graph)==len(iso)==120 and set(iso)==all_sl5 and set(iso.values())==H,"explicit SL2(5) bijection from printed generators")
require(all(iso[mul(x,y,5)]==mul(iso[x],iso[y],29) for x in all_sl5 for y in all_sl5),"all SL2(5) homomorphism products")

ep = tuple(range(5))
ap,bp = (1,0,3,2,4),(2,1,4,3,0)
pc = lambda x,y:tuple(x[y[i]] for i in range(5))
qgraph=closure(((A,ap),(B,bp)),(I,ep),lambda x,y:(mul(x[0],y[0],29),pc(x[1],y[1])))
qmap=dict(qgraph)
require(len(qgraph)==len(qmap)==120 and len(set(qmap.values()))==60,"explicit quotient map to order-60 permutation group")
require({x for x in H if qmap[x]==ep}==Z and all(qmap[mul(x,y,29)]==pc(qmap[x],qmap[y]) for x in H for y in H),"quotient map multiplicativity and kernel Z")

R=(A,(12,24,0,17),(25,3,4,4))
require(R[1]==mul(mul(B,A,29),power(B,2,29),29) and R[2]==mul(mul(A,R[1],29),power(mul(A,B,29),2,29),29),"R2/R3 printed word identities")
require(all(x in H and mul(x,x,29)==(28,0,0,28) for x in R),"R witness membership and squares")
pairs=[closure(tuple(x for j,x in enumerate(R) if j!=i),I,lambda x,y:mul(x,y,29)) for i in range(3)]
require([len(x) for x in pairs]==[8,12,20],"pair subgroup orders 8,12,20")
require([order(mul(R[i],R[j],29),29) for i,j in [(1,2),(0,2),(0,1)]]==[4,3,10],"pair product orders 4,3,10")
require(reduce(frozenset.intersection,pairs)==Z and all(R[i] not in pairs[i] for i in range(3)),"H independence and exact Z intersection")

els=sorted(H)
ix={x:i for i,x in enumerate(els)}
unit=ix[I]
table=[[ix[mul(x,y,29)] for y in els] for x in els]
subgens={frozenset((unit,)):()}
queue=list(subgens)
for K in queue:
    for g in range(120):
        if g not in K:
            gens=subgens[K]+(g,)
            J=closure(gens,unit,lambda x,y:table[x][y])
            if J not in subgens:
                subgens[J]=gens
                queue.append(J)
require(len(queue)==76,"complete subgroup-adjoining search finds 76 subgroups")
full=(1<<120)-1
one=1<<unit
masks=[sum(1<<x for x in K) for K in queue if len(K)<120]
count4=0
bad4=0
for a,b,c,d in combinations(masks,4):
    count4+=1
    bottom=a&b&c&d
    if (a&b&c)!=bottom and (a&b&d)!=bottom and (a&c&d)!=bottom and (b&c&d)!=bottom: bad4+=1
count3=0
bad3=0
for a,b,c in combinations(masks,3):
    count3+=1
    if a&b&c==one and a&b!=one and a&c!=one and b&c!=one: bad3+=1
require((count4,bad4,count3,bad3)==(1215450,0,67525,0),"all four-family and faithful three-family exclusions")
normals=[]
for K in queue:
    actual={els[i] for i in K}
    if all(mul(mul(g,k,29),inv(g,29),29) in actual for g in (A,B) for k in actual): normals.append(actual)
require(sorted(map(len,normals))==[1,2,120],"normal subgroups of H have orders 1,2,120")
for K in pairs:
    core=set(K)
    for g in H: core.intersection_update(mul(mul(g,k,29),inv(g,29),29) for k in K)
    require(core==Z,"pair core equals Z")
lines=[(1,t) for t in range(29)]+[(0,1)]
stabilizers=[]
for x,y in lines:
    st={g for g in H if ((g[0]*x+g[1]*y)*y-(g[2]*x+g[3]*y)*x)%29==0}
    require(len(st)==4 and any(order(g,29)==4 for g in st),"line stabilizer cyclic order 4")
    stabilizers.append(st)
require(all(not all(g in st for g in K) for st in stabilizers for K in pairs),"all three pair groups irreducible")

def affine_mul(x,y,p):
    u,v,h=x
    a,b,k=y
    return ((u+h[0]*a+h[1]*b)%p,(v+h[2]*a+h[3]*b)%p,mul(h,k,p))
E=(0,0,I)
S=[(1,0,I)]+[(0,0,r) for r in R]
G=closure(S,E,lambda x,y:affine_mul(x,y,29))
require(len(G)==100920,"full affine group generation")
M=[closure(S[:i]+S[i+1:],E,lambda x,y:affine_mul(x,y,29)) for i in range(4)]
require(list(map(len,M))==[120,6728,10092,16820] and all(S[i] not in M[i] for i in range(4)),"affine independent four-set and omission orders")
Z0=frozenset(((0,0,I),(0,0,(28,0,0,28))))
require(reduce(frozenset.intersection,M)==Z0,"four omission intersection exactly Z0")
conj=affine_mul(affine_mul((1,0,I),(0,0,(28,0,0,28)),29),(28,0,I),29)
require(conj==(2,0,(28,0,0,28)) and conj not in Z0,"explicit nonnormality conjugate")
L=[closure(g,E,lambda x,y:affine_mul(x,y,29)) for g in [((1,0,I),(0,0,(28,0,0,28))),((0,1,I),(0,0,(28,0,0,28))),((1,1,I),(2,0,(28,0,0,28)))]]
require(list(map(len,L))==[58]*3 and reduce(frozenset.intersection,L)=={E},"faithful affine three-family orders and intersection")
require([L[0]&L[1],L[0]&L[2],L[1]&L[2]]==[frozenset((E,(0,0,(28,0,0,28)))),frozenset((E,(2,0,(28,0,0,28)))),frozenset((E,(0,27,(28,0,0,28))))],"exact pairwise affine intersections")

# Reconstruct the deliberately failing characteristic without using p=29 data.
A11,B11,C=(0,10,1,0),(0,2,5,1),(6,10,0,2)
H11=closure((A11,B11),I,lambda x,y:mul(x,y,11))
require(len(H11)==120 and C in H11 and order(C,11)==10,"characteristic-11 complement and C")
K11=[closure(g,E,lambda x,y:affine_mul(x,y,11)) for g in [((1,0,I),(0,0,C)),((1,4,I),(0,0,C)),((1,0,I),(0,1,I),(0,0,power(C,5,11))),((1,0,I),(0,1,I),(0,0,power(C,2,11)))]]
require(reduce(frozenset.intersection,K11)=={E},"characteristic-11 total intersection")
require([len(reduce(frozenset.intersection,K11[:i]+K11[i+1:])) for i in range(4)]==[11,11,5,2],"characteristic-11 deletion orders")

def reviewed_file(suffix):
    frozen=OUT/('input_proof.'+suffix)
    return frozen if frozen.exists() else OUT.parents[1]/('proof.'+suffix)

RESULT.update({"finished_utc":datetime.now(timezone.utc).isoformat(),"elapsed_seconds":round(time.monotonic()-START,3),"H_order":len(H),"subgroup_order_distribution":dict(sorted(Counter(map(len,queue)).items())),"four_families":count4,"irredundant_four_families":bad4,"three_families":count3,"faithful_irredundant_three_families":bad3,"affine_order":len(G),"omission_orders":list(map(len,M)),"source_sha256":hashlib.sha256(reviewed_file('tex').read_bytes()).hexdigest(),"pdf_sha256":hashlib.sha256(reviewed_file('pdf').read_bytes()).hexdigest(),"status":"PASS"})
(OUT/'independent_results.json').write_text(json.dumps(RESULT,indent=2)+'\n')
(OUT/'independent_subgroups.json').write_text(json.dumps(sorted([sorted(els[i] for i in K) for K in queue]),separators=(',',':'))+'\n')
print(json.dumps(RESULT,indent=2))
