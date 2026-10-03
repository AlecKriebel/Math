#!/usr/bin/env python3
"""New adversarial controls, standard library only; no candidate imports.

Finite controls are supplementary and do not settle Kourovka21.9.
"""
import itertools as it
import json
import math
from collections import deque

count = 0
def ck(b):
    global count
    assert b
    count += 1

def generated(gs, table):
    out = {0}; todo = [0]
    while todo:
        a = todo.pop()
        for g in gs:
            b = table[a][g]
            if b not in out: out.add(b); todo.append(b)
    return frozenset(out)

# Exhaustive additive subgroup classification over two rings, with full GL.
module_results = []
for p,e in [(2,2),(2,3),(3,2)]:
    q = p**e
    pts = list(it.product(range(q),repeat=2)); ix = {v:i for i,v in enumerate(pts)}
    table = [[ix[((a+c)%q,(b+d)%q)] for c,d in pts] for a,b in pts]
    subs={frozenset({0})}; todo=list(subs)
    while todo:
        H=todo.pop()
        for g in range(q*q):
            if g not in H:
                K=generated(tuple(H)+(g,),table)
                if K not in subs: subs.add(K); todo.append(K)
    gl=[(a,b,c,d) for a,b,c,d in it.product(range(q),repeat=4) if math.gcd(a*d-b*c,q)==1]
    invariant=[]
    for H in subs:
        stable=True
        for a,b,c,d in gl:
            moved={ix[((a*pts[g][0]+b*pts[g][1])%q,(c*pts[g][0]+d*pts[g][1])%q)] for g in H}
            if moved!=set(H): stable=False; break
        if stable: invariant.append(H)
    scalar={frozenset(ix[v] for v in pts if v[0]%p**a==0 and v[1]%p**a==0) for a in range(e+1)}
    ck(set(invariant)==scalar)
    module_results.append({'p':p,'e':e,'all_additive_subgroups':len(subs),'full_GL':len(gl),'invariant_subgroups':len(invariant)})

# Build the genuine F_2/Phi^2(F_2), p=2, using mod-2 homology of the
# four-vertex Schreier graph of Phi(F_2). Its 8 edges minus 3 tree edges
# give 5 homology coordinates, hence 4*2^5=128 elements.
vertices=list(it.product(range(2),repeat=2)); vid={q:i for i,q in enumerate(vertices)}
def nextq(q,g):
    v=list(q);v[g]^=1;return tuple(v)
tree={((0,0),0),((0,0),1),((1,0),1)}
chords=[(q,g) for q in vertices for g in range(2) if (q,g) not in tree]
vol={c:1<<i for i,c in enumerate(chords)}
states=[(q,z) for q in vertices for z in range(32)]; si={s:i for i,s in enumerate(states)}
def step(s,g):
    q,z=s; return nextq(q,g),z^vol.get((q,g),0)
adj=[[si[step(s,g)] for g in range(2)] for s in states]
words={0:()}; todo=deque([0])
while todo:
    a=todo.popleft()
    for g in range(2):
        b=adj[a][g]
        if b not in words:words[b]=words[a]+(g,);todo.append(b)
ck(len(words)==128)
def act(a,w):
    for g in w:a=adj[a][g]
    return a
table=[[act(a,words[b]) for b in range(128)] for a in range(128)]
ck(table[0]==list(range(128)))
ck(all(table[a][0]==a for a in range(128)))
ck(all(table[table[a][b]][c]==table[a][table[b][c]] for a,b,c in it.product(range(128),repeat=3)))
inverse=[next(b for b in range(128) if table[a][b]==0 and table[b][a]==0) for a in range(128)]
phi=frozenset(i for i,(q,z) in enumerate(states) if q==(0,0))
ck(len(phi)==32)
ck(all(table[a][b]==table[b][a] and table[a][a]==0 for a in phi for b in phi))
frattini_generators={table[a][a] for a in range(128)}
frattini_generators|={table[table[table[inverse[a]][inverse[b]]][a]][b] for a,b in it.product(range(128),repeat=2)}
ck(generated(frattini_generators,table)==phi)
gens=[adj[0][g] for g in range(2)]
ck(len(generated(gens,table))==128)
autos=0
for a,b in it.product(range(128),repeat=2):
    qa,qb=states[a][0],states[b][0]
    independent=(qa!=(0,0) and qb!=(0,0) and qa!=qb)
    if not independent:continue
    mapping={0:0};todo=[0];targets=(a,b)
    while todo:
        v=todo.pop()
        for g in range(2):
            w=adj[v][g];image=table[mapping[v]][targets[g]]
            if w in mapping:ck(mapping[w]==image)
            else:mapping[w]=image;todo.append(w)
    ck(len(mapping)==128 and len(set(mapping.values()))==128)
    autos+=1
ck(autos==6*32**2)

# Independent direct automorphism permutations, all subgroups and cyclic
# cores for ALL triples containing G in Q8 and D8, for all cyclic orders.
core_results=[]
def quaternion(a,b):
    # +/-1,+/-i,+/-j,+/-k encoded (basis,sign).
    u,s=a;v,t=b
    if u==0:return v,s^t
    if v==0:return u,s^t
    if u==v:return 0,s^t^1
    cyc={(1,2):3,(2,3):1,(3,1):2}
    return (cyc[(u,v)],s^t) if (u,v) in cyc else (cyc[(v,u)],s^t^1)
for name,pts,op in [('Q8',list(it.product(range(4),range(2))),quaternion),
                    ('D8',list(it.product(range(4),range(2))),lambda a,b:((a[0]+(-1)**a[1]*b[0])%4,(a[1]+b[1])%2))]:
    ix={v:i for i,v in enumerate(pts)}; M=[[ix[op(a,b)] for b in pts] for a in pts]
    G=frozenset(range(8));subs=[]
    for mask in range(1,256,2):
        H=frozenset(i for i in range(8) if mask>>i&1)
        if all(M[a][b] in H for a in H for b in H):subs.append(H)
    A={}
    for H in subs:
        h=sorted(H);maps=[]
        for perm in it.permutations(h[1:]):
            f=dict(zip(h,[0,*perm]))
            if all(f[M[a][b]]==M[f[a]][f[b]] for a in H for b in H):maps.append(f)
        A[H]=maps
    def characteristic(H,K):return all({f[x] for x in K}==set(K) for f in A[H])
    def core(H,V):
        K=set(V)
        for f in A[H]:K&={f[x] for x in V}
        return frozenset(K)
    families=0
    for U,V in it.product(subs,repeat=2):
        common=[K for K in subs if K<=U&V and all(characteristic(H,K) for H in [G,U,V])]
        target=frozenset().union(*common)
        ck(target in common)
        for family in it.permutations([G,U,V]):
            W=U&V
            for _ in range(9):
                old=W
                for H in family:W=core(H,W)
                if old==W:break
            ck(W==target)
        families+=1
    core_results.append({'group':name,'all_subgroups':len(subs),'all_family_pairs':families,'all_cyclic_orders':6})

# New integral control: companion ring Z[X]/(1+...+X^(p-1)), rather
# than the author's shift vectors or old review's binomial residue sums.
companion=[]
for p in [2,3,5,7,11,17,23]:
    rank=p-1
    def xmul(v):
        z=[0]+v[:-1];z=[z[i]-v[-1] for i in range(rank)];return z
    def tapply(v):return [x-y for x,y in zip(xmul(v),v)]
    v=[1]+[0]*(rank-1)
    for k in range(1,241):
        v=tapply(v)
        def val(x):
            if not x:return 10**9
            a=0
            while x%p==0:x//=p;a+=1
            return a
        # This primitive basis vector represents T e_0, so k steps
        # correspond to the original coefficient valuation at power k+1.
        ck(min(map(val,v))==k//rank)
    companion.append({'p':p,'augmentation_rank':rank,'powers':240})

# Finite-coordinate subgroups exhibit extra centers, unlike Z_p.
# Exhaust all horizontal pairs and test commutation with generators;
# c is free and contributes a factor q to the resulting center size.
centers=[]
for p,m in [(2,2),(2,3),(2,4),(3,2),(3,3),(5,2)]:
    q=p**m
    for r,s in it.product(range(m+1),repeat=2):
        horiz=[(a,b) for a in range(0,q,p**r) for b in range(0,q,p**s)]
        C=[(a,b) for a,b in horiz if a*p**s%q==0 and b*p**r%q==0]
        predicted=[(a,b) for a,b in horiz if a%p**max(r,m-s)==0 and b%p**max(s,m-r)==0]
        ck(C==predicted)
        ck(all((a*d-c*b)%q==0 for a,b in C for c,d in horiz))
        if len(C)>1:centers.append({'p':p,'modulus_exponent':m,'horizontal_exponents':[r,s],'extra_horizontal_center':len(C)})
ck(any(c['p']==2 for c in centers))
print(json.dumps({'result':'PASS','assertions':count,'scope':'new finite controls; original infinite claim unresolved',
 'module_classification':module_results,'actual_second_Frattini_quotient':{'p':2,'free_rank':2,'order':128,'Frattini_order':32,'all_basis_assignments_tested':autos},
 'all_triple_core_orders':core_results,'companion_ring_valuations':companion,'finite_extra_center_cases':len(centers),'extra_center_examples':centers[:8]},indent=2,sort_keys=True))
