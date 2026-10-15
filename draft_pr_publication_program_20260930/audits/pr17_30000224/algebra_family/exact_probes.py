#!/usr/bin/env python3
"""Distinct exact algebra probes. Pure Python; no CAS or external packages.

Universal proofs are in REPORT.md. Finite degree slices are regression evidence,
not substitutes for those proofs. This file imports no author arithmetic code.
"""
from pathlib import Path
from datetime import datetime, timezone
from fractions import Fraction as Q
from itertools import combinations
from math import comb, gcd
import hashlib
import json

HERE = Path(__file__).resolve().parent
records = []
checks = 0

def require(condition):
    global checks
    assert condition
    checks += 1

def record(name, **values):
    records.append({'name': name, **values})

def monomials(degree, n=4):
    if n == 1:
        return [(degree,)]
    return [(i,) + tail for i in range(degree + 1) for tail in monomials(degree-i, n-1)]

def add(a, b):
    return tuple(x+y for x,y in zip(a,b))

def sub(a, b):
    return tuple(x-y for x,y in zip(a,b))

def divides(a, b):
    return all(x <= y for x,y in zip(a,b))

def rref(rows, ncols=None):
    a = [[Q(v) for v in row] for row in rows]
    if ncols is None:
        ncols = len(a[0]) if a else 0
    pivots = []
    for col in range(ncols):
        pivot = next((i for i in range(len(pivots), len(a)) if a[i][col]), None)
        if pivot is None:
            continue
        pos = len(pivots)
        a[pos], a[pivot] = a[pivot], a[pos]
        scale = a[pos][col]
        a[pos] = [v/scale for v in a[pos]]
        for i in range(len(a)):
            if i != pos:
                scale = a[i][col]
                a[i] = [x-scale*y for x,y in zip(a[i], a[pos])]
        pivots.append(col)
        if len(pivots) == len(a):
            break
    return a, pivots

def rank(rows, ncols=None):
    return len(rref(rows, ncols)[1])

def nullspace(rows, ncols):
    reduced, pivots = rref(rows, ncols)
    vectors = []
    for free in range(ncols):
        if free in pivots:
            continue
        vector = [Q(0)]*ncols
        vector[free] = Q(1)
        for i,pivot in enumerate(pivots):
            vector[pivot] = -reduced[i][free]
        vectors.append(vector)
    return vectors

def columns_to_rows(columns, nrows):
    return [[col[i] for col in columns] for i in range(nrows)]

def matvec(rows, vec):
    return [sum(a*b for a,b in zip(row,vec)) for row in rows]

# The parameter lattice and T-basis, independently of polynomial parsing.
exponents = [(4,0), (3,1), (1,3), (0,4)]
u = (2,2)
require(add(u,u) == add(exponents[0],exponents[3]))
require(add(add(u,u),u) == add(add(exponents[1],exponents[1]),exponents[3]))
kernel_basis = [(2,-3,1,0),(3,-4,0,1)]
for v in kernel_basis:
    require(tuple(sum(exponents[i][j]*v[i] for i in range(4)) for j in range(2)) == (0,0))
minors = [exponents[i][0]*exponents[j][1]-exponents[j][0]*exponents[i][1]
          for i,j in combinations(range(4),2)]
require(gcd(*minors) == 4)
record('parameter_lattice', kernel_basis=kernel_basis, minor_gcd=4,
       universal_description='image={(a,b): a+b divisible by 4}; kernel parametrized by v3,v4')

residues = [(0,0),(3,1),(2,2),(1,3)]
semigroup = {(0,0)}
defect_slices = []
for d in range(0,33):
    if d:
        semigroup = {add(a,b) for a in semigroup for b in exponents}
    veronese = {(4*d-j,j) for j in range(4*d+1)}
    missing = veronese-semigroup
    require(missing == ({u} if d == 1 else set()))
    for a,b in veronese:
        matches = [(a0,b0) for a0,b0 in residues if a%4 == a0 and b%4 == b0]
        require(len(matches) == 1)
        a0,b0 = matches[0]
        # T module A = T + Tx + Ty + (w,z)Tu.
        in_A_by_T = (a0,b0) != u or ((a-a0)//4 + (b-b0)//4) > 0
        require(((a,b) in semigroup) == in_A_by_T)
    defect_slices.append({'degree':d,'A_dimension':len(semigroup),'B_dimension':len(veronese),
                          'missing':sorted(missing)})
# Parameter radical identities x^4=w^3z and y^4=wz^3.
require(tuple(4*j for j in exponents[1]) == add(tuple(3*j for j in exponents[0]), exponents[3]))
require(tuple(4*j for j in exponents[2]) == add(exponents[0], tuple(3*j for j in exponents[3])))
require(u not in set(exponents))
require((add(u,exponents[0]) in {add(a,b) for a in exponents for b in exponents})
        and (add(u,exponents[3]) in {add(a,b) for a in exponents for b in exponents}))
record('unique_hole_and_T_module', degree_slices=defect_slices,
       T_module='T + Tx + Ty + (w,z)Tu',
       T_resolution_degrees={'F0':[0,1,1,2,2],'F1':[3]},
       hilbert_numerator=[1,2,2,-1])

# A_w consists of all lattice monomials with b>=0; A_z those with a>=0.
# Their intersection has a,b>=0 and equals B. Test signed slices too.
cech_holes = []
for d in range(-8,17):
    for b in range(-40, 4*d+41):
        a=4*d-b
        in_Aw=b>=0
        in_Az=a>=0
        in_intersection=in_Aw and in_Az
        in_A=(d==0 and a==0 and b==0) or (d==1 and (a,b) in exponents) or (d>=2 and a>=0 and b>=0)
        require(not in_A or in_intersection)
        if in_intersection and not in_A:
            cech_holes.append({'degree':d,'exponent':[a,b]})
require(cech_holes == [{'degree':1,'exponent':[2,2]}])
record('signed_Cech_slices', observed_H1_basis=cech_holes,
       universal_proof='A_w intersection A_z = full fourth Veronese; no negative-degree H1')

# Laurent finite-group step: Q[C_n] reduced versus F_p[C_p] nonreduced.
# Polynomial Euclidean gcd here does not assume roots lie in the ground field.
def trim(p):
    p = [Q(a) for a in p]
    while len(p)>1 and not p[-1]:
        p.pop()
    return p

def remainder(p,q):
    p,q=trim(p),trim(q)
    while p != [0] and len(p)>=len(q):
        shift=len(p)-len(q)
        coeff=p[-1]/q[-1]
        for i,a in enumerate(q):
            p[i+shift]-=coeff*a
        p=trim(p)
    return p

def poly_gcd(p,q):
    p,q=trim(p),trim(q)
    while q!=[0]:
        p,q=q,remainder(p,q)
    return [a/p[-1] for a in p]

for n in range(1,25):
    p=[-1]+[0]*(n-1)+[1]
    derivative=[0]*(n-1)+[n]
    require(poly_gcd(p,derivative)==[1])
require(poly_gcd([1,1,1],[1,2])==[1])
require(all(comb(3,i)%3==0 for i in (1,2)))
require([comb(3,i)*(-1)**(3-i)%3 for i in range(4)] == [2,0,0,1])
record('Laurent_reducedness_controls', rational_cyclic_orders_tested=list(range(1,25)),
       nonsplit_field_control='Q[C3] = Q times Q(root of T^2+T+1), both separable',
       characteristic_3_negative_control='(g-1)^3=0 in F3[C3], but g-1 !=0')

# Radical/generic length alone cannot replace primaryness.
J_generators=[(2,0),(1,1)]
in_J=lambda e:any(divides(g,e) for g in J_generators)
require(not in_J((1,0)) and in_J((1,1)))
require(in_J((2,0)))
record('primaryness_negative_control', ring='K[u,v]', ideal='(u^2,uv)', radical='(u)',
       generic_length=1, localization_at_v='(u)', strict_contraction=True,
       reason='u not in J but vu in J, so v outside radical is a zerodivisor')

# Powers of one binomial are generally not binomial in characteristic zero.
for n in range(2,13):
    require(len([i for i in range(n+1) if comb(n,i)*(-1)**i])==n+1)
record('binomial_boundary_control', q_power_term_counts={str(n):n+1 for n in range(2,13)},
       consequence='excluding binomial ideals does not exclude ideals generated by q^N')

# Multigraded Koszul slices, using only exponent divisibility and signs.
f=[(1,0,1,0),(1,0,0,1),(0,1,1,0),(0,1,0,1)]
unit=[tuple(int(i==j) for i in range(4)) for j in range(4)]
def subsets(alpha,k, generators=f):
    out=[]
    for S in combinations(range(len(generators)),k):
        shift=(0,)*4
        for i in S:
            shift=add(shift,generators[i])
        if divides(shift,alpha):
            out.append(S)
    return out

def differential(alpha,k, generators=f):
    source=subsets(alpha,k,generators)
    target=subsets(alpha,k-1,generators)
    # d(e_ij)=f_i e_j-f_j e_i as in the stated convention.
    rows=[[0]*len(source) for _ in target]
    for j,S in enumerate(source):
        for pos in range(k):
            T=S[:pos]+S[pos+1:]
            rows[target.index(T)][j]=(-1)**pos
    return rows

def boundary_columns(alpha,generators=f):
    rows=differential(alpha,2,generators)
    return [[row[i] for row in rows] for i in range(len(subsets(alpha,2,generators)))]

def embed(vec,small,large):
    return [vec[small.index(s)] if s in small else Q(0) for s in large]

def socle_dimension(alpha):
    vertices=subsets(alpha,1)
    if not vertices:
        return 0
    cycles=nullspace(differential(alpha,1),len(vertices))
    constraints=[]
    for e in unit:
        beta=add(alpha,e)
        target_vertices=subsets(beta,1)
        Bcols=boundary_columns(beta)
        annihilators=nullspace(Bcols,len(target_vertices))
        for row in annihilators:
            constraints.append([sum(a*b for a,b in zip(row,embed(v,vertices,target_vertices))) for v in cycles])
    kernel_dimension=len(cycles)-rank(constraints,len(cycles))
    B=boundary_columns(alpha)
    return kernel_dimension-rank(columns_to_rows(B,len(vertices)),len(B))

koszul_slices=[]
all_socles=[]
for degree in range(2,11):
    total={'degree':degree,'K1_dimension':0,'Z1_dimension':0,'B1_dimension':0,'H1_dimension':0,
           'socle_dimension':0}
    for alpha in monomials(degree):
        K1=len(subsets(alpha,1))
        d1=differential(alpha,1)
        d2=differential(alpha,2)
        d3=differential(alpha,3)
        # Check d1 d2 and d2 d3 exactly, with explicit dimensions.
        for column in boundary_columns(alpha):
            require(matvec(d1,column)==[0])
        for col in range(len(subsets(alpha,3))):
            vector=[row[col] for row in d3]
            require(all(v==0 for v in matvec(d2,vector)))
        Z1=K1-rank(d1,K1)
        B1=rank(d2,len(subsets(alpha,2)))
        H1=Z1-B1
        require(H1>=0)
        sd=socle_dimension(alpha)
        require(sd>=0)
        if sd:
            all_socles.append({'degree':degree,'multidegree':list(alpha),'dimension':sd})
        for key,value in [('K1_dimension',K1),('Z1_dimension',Z1),('B1_dimension',B1),
                          ('H1_dimension',H1),('socle_dimension',sd)]:
            total[key]+=value
    koszul_slices.append(total)
require(all_socles == [{'degree':4,'multidegree':[1,1,1,1],'dimension':1}])
require(koszul_slices[1]['H1_dimension']==4 and koszul_slices[2]['H1_dimension']==9)
for slice in koszul_slices:
    d=slice['degree']
    choose3=lambda k:comb(k,3) if k>=3 else 0
    # Independently predicted by the tensor-product minimal resolution of I.
    require(slice['Z1_dimension']==4*choose3(d)-choose3(d-1))
alpha=(1,1,1,1)
vertices=subsets(alpha,1)
c=[-1,1,0,0]
mutated=[-1,-1,0,0]
boundary=[-1,0,0,1]  # d14, a positive control for membership.
Bcols=boundary_columns(alpha)
Bmatrix=columns_to_rows(Bcols,len(vertices))
base=rank(Bmatrix,len(Bcols))
require(matvec(differential(alpha,1),c)==[0])
require(matvec(differential(alpha,1),mutated)==[-2])
require(rank(columns_to_rows(Bcols+[c],len(vertices)),len(Bcols)+1)==base+1)
require(rank(columns_to_rows(Bcols+[boundary],len(vertices)),len(Bcols)+1)==base)
for e in unit:
    beta=add(alpha,e)
    Bnext=boundary_columns(beta)
    mapped=embed(c,vertices,subsets(beta,1))
    require(rank(columns_to_rows(Bnext+[mapped],len(mapped)),len(Bnext)+1)
            == rank(columns_to_rows(Bnext,len(mapped)),len(Bnext)))
# Deleting f4 preserves c being a cycle but destroys annihilation by x.
f_deleted=f[:3]
beta=add(alpha,unit[1])
Bdeleted=boundary_columns(beta,f_deleted)
c_deleted=[-1,1,0]
require(matvec(differential(alpha,1,f_deleted),c_deleted)==[0])
require(rank(columns_to_rows(Bdeleted+[c_deleted],3),len(Bdeleted)+1)
        > rank(columns_to_rows(Bdeleted,3),len(Bdeleted)))
record('multigraded_Koszul_and_mutations', slices=koszul_slices, observed_socles=all_socles,
       alpha_1111_boundary_rank=base, alpha_1111_with_c_rank=base+1,
       sign_mutation_detected=True, actual_boundary_positive_control=True,
       deleted_f4_mutation_detected=True,
       method='entire multigraded complex by monomial divisibility, not author supplied identities')

# A separate minimal I-resolution gives the depth-Z1 input by tensor product.
record('minimal_I_resolution_certificate',
       syzygy_columns=[['-z','y','0','0'],['-x','0','w','0'],['0','-x','0','w'],['0','0','-z','y']],
       relation_column=['x','-z','y','-w'],
       free_resolution='0 -> R(-4) -> R(-3)^4 -> R(-2)^4 -> I -> 0',
       exactness_mechanism='tensor product over K of two parameter-ideal resolutions in disjoint variables',
       depths={'R/I':1,'I':2,'Z1':3,'H1':0,'B1':1,'Z2':2},
       pdim_Z2_at_m=2, required_bound_r4_i2=1,
       redundant_generator_invariance='with k padded zero generators, Z_(k+2) has Z2 as a direct summand; same bound 1 fails')

out={'status':'passed','checked_at_utc':datetime.now(timezone.utc).isoformat(),
     'arithmetic':'integer exponent arithmetic and fractions.Fraction linear algebra',
     'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
     'assertions':checks,'records':records,
     'scope':'validation only; universal deductions in REPORT.md; remaining arbitrary ideal class unresolved'}
(HERE/'evidence'/'exact_probe_results.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({'status':out['status'],'assertions':checks,'groups':len(records),
                  'Koszul_H1_dimensions':[x['H1_dimension'] for x in koszul_slices],
                  'socles':all_socles},indent=2))
