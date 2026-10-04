#!/usr/bin/env python3
"""Fresh audit checks. No import of the frozen implementation.
Permutations act on the right: product a*b applies a first, then b.
The A6 lattice search closes conjugacy classes, not the original left-coset BFS.
"""
from itertools import permutations, product
from collections import Counter, deque
from math import factorial
from fractions import Fraction
from pathlib import Path
import json, time

START = time.monotonic()

def parity(p):
    return (len(p) - len(cycles(p))) % 2

def cycles(p):
    pending = set(range(len(p))); ans = []
    while pending:
        a = next(iter(pending)); orbit = []; b = a
        while b in pending:
            orbit.append(b); pending.remove(b); b = p[b]
        ans.append(orbit)
    return ans

class Group:
    def __init__(self, elements, operation):
        self.elements = elements
        lookup = {x:i for i,x in enumerate(elements)}
        self.mul = [[lookup[operation(a,b)] for b in elements] for a in elements]
        self.n = len(elements)
        self.one = next(i for i in range(self.n) if self.mul[i] == list(range(self.n)))
        self.inv = [next(j for j in range(self.n) if self.mul[i][j] == self.one) for i in range(self.n)]
    def generated(self, generators):
        steps = set(generators) | {self.inv[g] for g in generators}
        found = {self.one}; pending = deque(found)
        while pending:
            a = pending.popleft()
            for b in steps:
                ab = self.mul[a][b]
                if ab not in found:
                    found.add(ab); pending.append(ab)
        return frozenset(found)
    def conjugate(self, subgroup, g):
        return frozenset(self.mul[self.mul[self.inv[g]][h]][g] for h in subgroup)
    def all_subgroups(self):
        # Store all conjugates immediately, but expand just one per conjugacy class.
        trivial = frozenset([self.one]); seen = {trivial}; todo = [(trivial, ())]
        classes = []; pos = 0
        while pos < len(todo):
            H, gens = todo[pos]; pos += 1
            classes.append({"order":len(H), "class_size":len({self.conjugate(H,g) for g in range(self.n)})})
            for g in range(self.n):
                if g in H: continue
                K = self.generated(gens + (g,))
                if K in seen: continue
                conjugates = {self.conjugate(K,a) for a in range(self.n)}
                seen.update(conjugates); todo.append((K, gens + (g,)))
            if time.monotonic()-START > 120: raise RuntimeError('Audit runtime bound exceeded')
        # Every subgroup extends via one generator, so conjugacy closure makes this exhaustive.
        assert sum(x['class_size'] for x in classes) == len(seen)
        return seen, classes

def symmetric(n, alternating=False):
    elts = [p for p in permutations(range(n)) if not alternating or parity(p)==0]
    return Group(elts, lambda a,b: tuple(b[a[i]] for i in range(n)))

P = symmetric(6,True); Q = frozenset(i for i,p in enumerate(P.elements) if p[5]==5)
subgroups, classes = P.all_subgroups()
centralizers = {t:frozenset(q for q in Q if P.mul[q][t]==P.mul[t][q]) for t in Q if t!=P.one}
allowed = {R for R in subgroups if any(R & Q <= C for C in centralizers.values())}
t5 = next(t for t in Q if sorted(map(len,cycles(P.elements[t])))==[1,5])
shortest_allowed = {R for R in subgroups if R & Q <= centralizers[t5]}
max_allowed = max(map(len,allowed)); max_shortest = max(map(len,shortest_allowed))
assert len(subgroups)==501 and len(allowed)==432 and max_allowed==24 and max_shortest==5

# Work with only six coordinate values. Independently derive the induced right action.
transversal=[]; decomposition={}
for a in range(P.n):
    if a in decomposition: continue
    j=len(transversal); transversal.append(a)
    for q in Q: decomposition[P.mul[a][q]]=(j,q)

def conjugate_value(t,q):
    return P.mul[P.mul[P.inv[q]][t]][q]

def transform(f,g):
    out=[]
    for x in transversal:
        j,q=decomposition[P.mul[g][x]]
        out.append(conjugate_value(f[j],q))
    return tuple(out)

pairs={frozenset([0,2]),frozenset([1,3]),frozenset([4,5])}
R=frozenset(i for i,p in enumerate(P.elements) if {frozenset(p[x] for x in pair) for pair in pairs}==pairs)
t = P.elements.index((2,3,0,1,4,5))
assert len(R)==24 and R & Q <= centralizers[t]
f=[]
for x in transversal:
    values={conjugate_value(t,q) for r in R for q in Q if P.mul[r][q]==x}
    assert len(values)<=1
    f.append(next(iter(values)) if values else P.one)
f=tuple(f)
stabilizer=frozenset(g for g in range(P.n) if transform(f,g)==f)
assert stabilizer==R
orbit={transform(f,g) for g in range(P.n)}
assert len(orbit)==15
# Test the action law on the full 15-orbit, all g, and a generating pair of A6.
gens=next((a,b) for a in range(1,P.n) for b in range(a+1,P.n) if len(P.generated((a,b)))==360)
assert all(transform(transform(v,g),h)==transform(v,P.mul[g][h]) for v in orbit for g in range(P.n) for h in gens)

# Count fixed coordinate-tuples by following coordinate cycles and their twisting maps,
# without using the double-coset formula in the frozen implementation.
fixed_type={}; fixed_total=0
for g,p in enumerate(P.elements):
    links=[decomposition[P.mul[g][x]] for x in transversal]
    pending=set(range(6)); count=1
    while pending:
        start=next(iter(pending)); c=start; qs=[]
        while c in pending:
            pending.remove(c); nxt,q=links[c]; qs.append(q); c=nxt
        assert c==start
        possible=0
        for seed in Q:
            v=seed
            for q in reversed(qs): v=conjugate_value(v,q)
            possible += (v==seed)
        count*=possible
    typ=','.join(map(str,sorted(map(len,cycles(p)))))
    record=fixed_type.setdefault(typ,{'elements':0,'fixed':count})
    assert record['fixed']==count
    record['elements']+=1; fixed_total+=count
assert fixed_total//360==129607960 and fixed_total%360==0

# Direct A8 conjugacy enumeration: no partition centralizer formula.
A8=[p for p in permutations(range(8)) if parity(p)==0]
reps={}
for p in A8: reps.setdefault(tuple(sorted(map(len,cycles(p)))),p)
a8=[]
for typ,p in sorted(reps.items()):
    if len(typ)==8: continue
    centralizer=sum(all(q[p[i]]==p[q[i]] for i in range(8)) for q in A8)
    a8.append({'type':list(typ),'centralizer':centralizer,'class_size':len(A8)//centralizer})
assert min(x['class_size'] for x in a8)==105

# Independent exhaustive toy induced action, including a nonfaithful twisting map.
# P=S3 x C2, Q=<transposition> x C2, T=C3, phi inverts according to first factor.
S3=symmetric(3)
K=Group(list(product(range(6),range(2))), lambda a,b:(S3.mul[a[0]][b[0]],(a[1]+b[1])%2))
tr=next(i for i,p in enumerate(S3.elements) if sorted(map(len,cycles(p)))==[1,2])
L=frozenset(i for i,(a,b) in enumerate(K.elements) if a in (S3.one,tr))
reps=[]; decomp={}
for x in range(K.n):
    if x in decomp: continue
    i=len(reps); reps.append(x)
    for q in L: decomp[K.mul[x][q]]=(i,q)
def toy_action(f,g):
    return tuple((f[i] if K.elements[q][0]==S3.one else -f[i])%3 for i,q in (decomp[K.mul[g][x]] for x in reps))
toy_subgroups,_=K.all_subgroups()
toy_admissible=[R for R in toy_subgroups if all(K.elements[q][0]==S3.one for q in R & L)]
toy_M=max(map(len,toy_admissible))
all_functions=set(product(range(3),repeat=3)); pending=set(all_functions); sizes=[]
for f0 in all_functions:
    for g in range(K.n):
        for h in range(K.n): assert toy_action(toy_action(f0,g),h)==toy_action(f0,K.mul[g][h])
while pending:
    f0=next(iter(pending)); orb={toy_action(f0,g) for g in range(K.n)}; pending-=orb
    if any(f0): sizes.append(len(orb))
assert min(sizes)==K.n//toy_M

# Exhaustive nonabelian toy: P=S4, Q=T=S3 fixing the fourth letter.
# This is not a primitive simple-socle datum; it is an orientation/formula control only.
U=symmetric(4); V=frozenset(i for i,p in enumerate(U.elements) if p[3]==3)
usubs,_=U.all_subgroups(); urep=[]; udec={}
for x in range(U.n):
    if x in udec: continue
    i=len(urep); urep.append(x)
    for q in V: udec[U.mul[x][q]]=(i,q)
def uc(t,q): return U.mul[U.mul[U.inv[q]][t]][q]
def ua(f,g): return tuple(uc(f[i],q) for i,q in (udec[U.mul[g][x]] for x in urep))
uvalues=list(product(sorted(V),repeat=4)); orbit_remaining=set(uvalues); u_orbit_sizes=[]
while orbit_remaining:
    v=next(iter(orbit_remaining)); o={ua(v,g) for g in range(U.n)}; orbit_remaining-=o
    if any(t!=U.one for t in v): u_orbit_sizes.append(len(o))
uadmissible=[R for R in usubs if any(t!=U.one and all(uc(t,q)==t for q in R & V) for t in V)]
uM=max(map(len,uadmissible)); assert min(u_orbit_sizes)==U.n//uM
# Compare every subgroup's direct fixed points with the exact double-coset product.
for R in usubs:
    direct=sum(all(ua(v,g)==v for g in R) for v in uvalues)
    left=set(range(U.n)); predicted=1
    while left:
        s=min(left)
        left-={U.mul[U.mul[r][s]][q] for r in R for q in V}
        D=U.conjugate(R,s)&V
        predicted*=sum(all(uc(t,q)==t for q in D) for t in V)
    assert direct==predicted

report={
 'method':'Fresh opposite-composition implementation, conjugacy-closed subgroup search, six-coordinate action, and direct A8 commutator counts',
 'A6_subgroups':len(subgroups),'A6_conjugacy_classes_of_subgroups':len(classes),'A6_subgroups_by_order':dict(sorted(Counter(map(len,subgroups)).items())),
 'A6_admissible':len(allowed),'maximum_admissible_order':max_allowed,'minimum_subdegree':360//max_allowed,
 'maximum_order_for_fixed_5_cycle':max_shortest,'shortest_component_only_index':360//max_shortest,
 'witness_coordinate_orbit':len(orbit),'witness_stabilizer_order':len(stabilizer),'action_law_checks':len(orbit)*360*len(gens),
 'fixed_functions_by_cycle_type':fixed_type,'burnside_orbits':fixed_total//360,
 'average_nonidentity_orbit':str(Fraction(60**6-1,fixed_total//360-1)),
 'A8_direct_class_counts':a8,'A8_minimum':min(x['class_size'] for x in a8),
 'nonfaithful_toy':{'P_order':K.n,'Q_order':len(L),'phi_kernel_order':2,'functions':len(all_functions),'admissible_maximum':toy_M,'minimum_nonidentity_orbit':min(sizes)},
 'nonabelian_toy':{'P_order':U.n,'Q_order':len(V),'functions':len(uvalues),'subgroups_checked':len(usubs),'all_fixed_point_products_verified':True,'admissible_maximum':uM,'minimum_nonidentity_orbit':min(u_orbit_sizes),'not_a_primitive_simple_socle_datum':True},
 'all_assertions_passed':True,'universal_claim_resolved':False}
Path(__file__).with_name('independent_results.json').write_text(json.dumps(report,indent=2,sort_keys=True)+'\n')
print(json.dumps({'all_assertions_passed':True,'elapsed_seconds':round(time.monotonic()-START,3),'subgroups':len(subgroups),'subgroup_classes':len(classes),'minimum':360//max_allowed}))
