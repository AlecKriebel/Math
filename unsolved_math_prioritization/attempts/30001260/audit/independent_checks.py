#!/usr/bin/env python3
"""Independent exact audit checks. Does not import or execute author mathematics.
Uses Murnaghan-Nakayama characters and complete subgroup closure enumeration.
No check here proves Smith theory, Borel's formula, or smooth realizability.
"""
from itertools import permutations, combinations
from functools import lru_cache
from fractions import Fraction
from collections import Counter
import json

def require(condition, label):
    if not condition:
        raise RuntimeError(label)

perms = tuple(permutations(range(5)))
index = {p: i for i, p in enumerate(perms)}
identity = index[tuple(range(5))]
product = [[index[tuple(a[b[j]] for j in range(5))] for b in perms] for a in perms]
inverse = [next(j for j in range(120) if product[i][j] == identity) for i in range(120)]

def cycle_type(i):
    remaining = set(range(5)); lengths=[]
    while remaining:
        x=min(remaining); y=x; k=0
        while y in remaining:
            remaining.remove(y); k+=1; y=perms[i][y]
        lengths.append(k)
    return tuple(sorted(lengths, reverse=True))

types=[cycle_type(i) for i in range(120)]
classes=sorted(set(types), reverse=True)

def generate(generators):
    found={identity}; pending=[identity]
    while pending:
        h=pending.pop()
        for g in generators:
            v=product[g][h]
            if v not in found: found.add(v); pending.append(v)
    return frozenset(found)

def from_cycles(*cycles):
    p=list(range(5))
    for cyc in cycles:
        for a,b in zip(cyc,cyc[1:]+cyc[:1]): p[a-1]=b-1
    return index[tuple(p)]

orders=[]
for i in range(120): orders.append(len(generate([i])))
allgroups={frozenset([identity]): ()}; todo=list(allgroups)
while todo:
    h=todo.pop(); gens=allgroups[h]
    for g in range(120):
        if g in h: continue
        k=generate(gens+(g,))
        if k not in allgroups:
            allgroups[k]=gens+(g,);todo.append(k)
require(len(allgroups)==156,'complete S5 subgroup count')
V4=[h for h in allgroups if len(h)==4 and all(orders[g]<=2 for g in h)]
require(len(V4)==20,'twenty Klein four groups')
EA=generate([from_cycles((1,2),(3,4)),from_cycles((1,3),(2,4))])
EB=generate([from_cycles((1,2)),from_cycles((3,4))])
c=from_cycles((1,2,3,4)); s=from_cycles((1,3)); P2=generate([c,s]);Z=generate([product[c][c]])

def conjugate(h,g): return frozenset(product[product[g][v]][inverse[g]] for v in h)
orbits=[{conjugate(h,g) for g in range(120)} for h in [EA,EB]]
require(len(orbits[0])==5 and len(orbits[1])==15 and orbits[0]|orbits[1]==set(V4),'V4 conjugacy orbits')
require(not any(len(h)==8 and all(orders[g]<=2 for g in h) for h in allgroups),'no elementary abelian subgroup of order eight')
rankone=[h for h in allgroups if not any(e<=h for e in V4)]

@lru_cache(None)
def partitions(n, maximum=None):
    if n==0: return ((),)
    maximum=n if maximum is None else min(maximum,n)
    return tuple((a,)+b for a in range(maximum,0,-1) for b in partitions(n-a,a))

def boxes(part): return frozenset((r,c) for r,n in enumerate(part) for c in range(n))
@lru_cache(None)
def mn(part, cycles):
    if not cycles: return int(not part)
    cells=boxes(part); total=0
    for sub in partitions(sum(part)-cycles[0]):
        small=boxes(sub)
        if not small<=cells: continue
        strip=cells-small
        if not strip: continue
        reached={next(iter(strip))}; pending=list(reached)
        while pending:
            r,c0=pending.pop()
            for n in ((r+1,c0),(r-1,c0),(r,c0+1),(r,c0-1)):
                if n in strip and n not in reached: reached.add(n);pending.append(n)
        if reached!=strip: continue
        if any({(r,c0),(r+1,c0),(r,c0+1),(r+1,c0+1)}<=strip for r,c0 in strip):continue
        height=len({r for r,c0 in strip})-1
        total+=(-1)**height*mn(sub,cycles[1:])
    return total

parts=partitions(5)
rows=[[mn(p,t) for t in types] for p in parts]
for i,a in enumerate(rows):
    for j,b in enumerate(rows): require(sum(x*y for x,y in zip(a,b))==120*int(i==j),'MN character orthogonality')
require(sum(row[identity]**2 for row in rows)==120,'complete MN dimensions')

def fixed(row,h): return sum(Fraction(row[g],len(h)) for g in h)
fixed_table=[]
for p,row in zip(parts,rows):
    fixed_table.append({'partition':p,'dimension':row[identity],'EA':int(fixed(row,EA)),'EB':int(fixed(row,EB)),'classes':[row[types.index(t)] for t in classes]})
require([(r['dimension'],r['EA'],r['EB']) for r in fixed_table]==[(1,1,1),(4,1,2),(5,2,2),(6,0,1),(5,2,1),(4,1,0),(1,1,0)],'independent fixed table')
require(all(r['EA']+r['EB']>0 for r in fixed_table),'each irrep fails some forbidden subgroup')
# Compare independent MN table against the author's explicitly constructed character formulas.
def sign(i):return (-1)**(5-len(types[i]))
def fp(i):return types[i].count(1)
pairs=tuple(combinations(range(5),2))
def pairfix(i):return sum({perms[i][a],perms[i][b]}=={a,b} for a,b in pairs)
constructed=[tuple(f(i) for i in range(120)) for f in [lambda i:1,sign,lambda i:fp(i)-1,lambda i:sign(i)*(fp(i)-1),lambda i:pairfix(i)-fp(i),lambda i:sign(i)*(pairfix(i)-fp(i)),lambda i:((fp(i)-1)**2-(fp(product[i][i])-1))//2]]
require(set(constructed)==set(map(tuple,rows)),'all 120 values of all seven characters')
# Full fusion and restriction checks using all conjugators, not representative class samples.
H4=frozenset(i for i,p in enumerate(perms) if p[4]==4)
W={i:sign(i)*(fp(i)-2) for i in H4}
locals_=[(P2,{i:4*W[i] for i in P2}),(generate([from_cycles((1,2,3))]),None),(generate([from_cycles((1,2,3,4,5))]),None)]
locals_[1]=(locals_[1][0],{i:(12 if i==identity else -6) for i in locals_[1][0]})
locals_[2]=(locals_[2][0],{i:(12 if i==identity else -3) for i in locals_[2][0]})
fusion_tests=0
for P,chi in locals_:
    require(chi[identity]==12,'common complex dimension twelve')
    for x in P:
        for g in range(120):
            y=product[product[g][x]][inverse[g]]
            if y in P:require(chi[x]==chi[y],'fusion stable for every conjugator');fusion_tests+=1
    for E in V4:
        if E<=P:require(sum(chi[x] for x in E)==0,'rank two fixed subspace vanishes')
for P,chi in locals_[1:]:require(sum(chi.values())==0,'odd Sylow free sphere')
# Explicit real matrices for D8 local rotation model, including complex normal action.
C=((0,-1,0),(1,0,0),(0,0,1));S=((1,0,0),(0,-1,0),(0,0,-1));I=((1,0,0),(0,1,0),(0,0,1))
def matmul(a,b):return tuple(tuple(sum(a[i][k]*b[k][j] for k in range(3)) for j in range(3)) for i in range(3))
def matpow(a,n):
    out=I
    for unused in range(n):out=matmul(out,a)
    return out
require(matpow(C,4)==I and matpow(S,2)==I and matmul(matmul(S,C),S)==matpow(C,3),'D8 matrix relations')
matrices={}
for a in range(4):
    for b in range(2):
        g=identity
        for unused in range(a):g=product[g][c]
        if b:g=product[g][s]
        m=matmul(matpow(C,a),matpow(S,b));matrices[g]=m
        require(sum(m[j][j] for j in range(3))==W[g],'explicit rotation matrix character')
require(len(matrices)==8,'faithful local D8 representation')
require(matpow(C,2)==((-1,0,0),(0,-1,0),(0,0,1)),'C4 normal plane squares to negative identity')
# Induction decomposition computed by Frobenius reciprocity and then all 120 traces.
multiplicities=[sum(Fraction(row[h]*W[h],24) for h in H4) for row in rows]
require(list(map(int,multiplicities))==[0,0,0,1,1,1,0],'induction is L + sign D + sign U')
induced=[sum(mult*row[g] for mult,row in zip(multiplicities,rows)) for g in range(120)]
require(all(induced[g]==sign(g)*fp(g)*(fp(g)-2) for g in range(120)),'induction full character')
require(induced[identity]==15 and fixed(induced,EA)==3 and fixed(induced,EB)==2,'induced forbidden invariants')
# Check all elementary-abelian quotient sections within all p-subgroups.
def ispgroup(h,p):
    n=len(h)
    while n%p==0:n//=p
    return n==1

def normal(h,k):return all(conjugate(h,g)==h for g in k)
def d(h):return 23 if len(h)==1 else (7 if ispgroup(h,2) and max(orders[g] for g in h)==len(h) else -1)
section_count=0; c4_section_count=0; odd_parity_count=0; quaternion_section_count=0
for p in (2,3,5):
    psub=[h for h in allgroups if ispgroup(h,p)]
    for K in psub:
        for H in psub:
            if not H<=K or not normal(H,K):continue
            if len(K)==len(H)*p*p and all(generate([g])<=H or product[g][g] in H for g in K) and p==2:
                middles=[L for L in psub if H<L<K and len(L)==2*len(H)]
                require(len(middles)==3,'three quotient lines')
                require(d(H)-d(K)==sum(d(L)-d(K) for L in middles),'Borel equation for local dimension function')
                section_count+=1
            if p in (3,5) and len(K)==p*len(H):
                require((d(H)-d(K))%2==0,'odd prime Smith parity');odd_parity_count+=1
            if p==2 and len(K)==4*len(H) and any(product[g][g] not in H for g in K):
                middles=[L for L in psub if H<L<K and len(L)==2*len(H)]
                require(len(middles)==1,'unique index two subgroup in cyclic four quotient')
                require((d(H)-d(middles[0]))%2==0,'cyclic-four Borel-Smith parity');c4_section_count+=1
            if p==2 and len(K)==8*len(H):
                # A quaternion-eight quotient has exactly one order-two subgroup.
                middles=[L for L in psub if H<L<K and len(L)==2*len(H)]
                if len(middles)==1:quaternion_section_count+=1
require(quaternion_section_count==0,'no quaternion-eight sections among p-subgroups')
# Rational row reduction for universal Borel equations, with columns n,a,b,constant.
A=[[Fraction(v) for v in row] for row in [[1,-3,0,2],[1,-1,-2,2]]]
A[1]=[b-a for a,b in zip(A[0],A[1])]
A[1]=[x/2 for x in A[1]]
A[0]=[a+3*b for a,b in zip(A[0],A[1])]
require(A==[[1,0,-3,2],[0,1,-1,0]],'universal solution n=3b+2 and a=b')
negative=[]
for label,condition in [('false subgroup count',len(V4)==19),('false invariant table',all(r['EA']==0 for r in fixed_table)),('false local dimension',locals_[0][1][identity]==24),('false induced free sphere',fixed(induced,EA)==0)]:
    try:require(condition,label)
    except RuntimeError:negative.append(label)
    else:raise RuntimeError('negative control passed')
output={'status':'PASS','scope':'independent finite group, character, matrix, fusion, induction, and local dimension diagnostics; no smooth existence or nonexistence certificate','group_order':120,'complete_subgroup_count':len(allgroups),'subgroup_order_counts':dict(sorted(Counter(map(len,allgroups)).items())),'rank_at_most_one_subgroup_order_counts':dict(sorted(Counter(map(len,rankone)).items())),'klein_four_count':len(V4),'klein_four_conjugacy_orbit_sizes':[len(o) for o in orbits],'cycle_classes':classes,'independent_Murnaghan_Nakayama_character_table':fixed_table,'fusion_comparisons':fusion_tests,'local_complex_dimensions':[12,12,12],'explicit_D8_matrices_verified':True,'induction_irrep_multiplicities':list(map(int,multiplicities)),'induced_EA_EB_invariant_dimensions':[int(fixed(induced,EA)),int(fixed(induced,EB))],'all_p_subgroup_V4_quotient_sections_checked':section_count,'cyclic_four_parity_sections_checked':c4_section_count,'odd_prime_parity_sections_checked':odd_parity_count,'quaternion_eight_sections':quaternion_section_count,'universal_Borel_solution':'n=3r+2, a=b=r; n>=0 and integer r imply r>=0','negative_controls_rejected':negative}
print(json.dumps(output,indent=2,sort_keys=True))
