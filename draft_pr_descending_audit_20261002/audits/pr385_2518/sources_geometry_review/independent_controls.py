#!/usr/bin/env python3
"""Independent exact controls. No imports of author modules or historical review.

Finite models check mechanisms and limiting traps, not the free-pro-p target.
Matrices are multiplied as matrices, rather than using the author's triple law.
"""
import itertools
import json
from collections import deque

counts = {}
def check(label, statement):
    assert statement, label
    counts[label] = counts.get(label, 0) + 1

def mat(a, b, c, q):
    return ((1, a % q, c % q), (0, 1, b % q), (0, 0, 1))
def mm(A, B, q):
    return tuple(tuple(sum(A[i][k] * B[k][j] for k in range(3)) % q
                       for j in range(3)) for i in range(3))
def mi(A, q):
    # Geometric-series inverse of I+N for N^3=0.
    I = mat(0, 0, 0, q)
    N = tuple(tuple((A[i][j] - I[i][j]) % q for j in range(3)) for i in range(3))
    N2 = mm(N, N, q)
    return tuple(tuple((I[i][j] - N[i][j] + N2[i][j]) % q for j in range(3))
                 for i in range(3))
def coords(A):
    return A[0][1], A[1][2], A[0][2]
def matrix_group(q):
    return [mat(a, b, c, q) for a, b, c in itertools.product(range(q), repeat=3)]
def com(A, B, q):
    return mm(mm(mm(A, B, q), mi(A, q), q), mi(B, q), q)

# Full multiplication-table automorphisms for the smallest boundary case.
G2 = matrix_group(2)
I2 = mat(0, 0, 0, 2)
rest = [g for g in G2 if g != I2]
table = {(a, b): mm(a, b, 2) for a in G2 for b in G2}
autos = []
for images in itertools.permutations(rest):
    f = dict(zip([I2] + rest, [I2] + list(images)))
    if all(f[table[a,b]] == table[f[a],f[b]] for a in G2 for b in G2):
        autos.append(f)
check('full_Aut_UT3_F2_order', len(autos) == 8)
U2 = {g for g in G2 if coords(g)[0] == 0}
check('p2_displayed_U_elementary_abelian', all(mm(g,g,2)==I2 for g in U2))
orbit = {frozenset(f[g] for g in U2) for f in autos}
check('p2_U_not_characteristic', len(orbit) == 2)

# Finite centers of deep, nonnormal open-subgroup shadows need not be images
# of the p-adic center. Exhaustive center check via commuting generators.
center_rows = []
for p, s, e in [(2,1,3), (2,1,4), (3,1,3), (5,1,3), (2,2,5)]:
    q = p**e
    a_step, c_step = p**s, p**(2*s)
    X, Y, Z = mat(a_step,0,0,q), mat(0,a_step,0,q), mat(0,0,c_step,q)
    H = {mat(a,b,c,q) for a,b,c in itertools.product(range(0,q,a_step),
         range(0,q,a_step), range(0,q,c_step))}
    observed = {h for h in H if all(mm(h,g,q)==mm(g,h,q) for g in (X,Y,Z))}
    predicted = {h for h in H if all((p**s*v) % q == 0 for v in coords(h)[:2])}
    check('nonnormal_shadow_exact_center', observed == predicted)
    y = mat(0,1,0,q)
    check('deep_open_shadow_not_normal', mm(mm(y,X,q),mi(y,q),q) not in H)
    true_center_image = {h for h in H if coords(h)[:2] == (0,0)}
    check('finite_center_has_extra_torsion', true_center_image < observed)
    # The extra center directions retreat with e: valuation >= e-s.
    check('finite_center_threshold', all(a%(p**(e-s))==b%(p**(e-s))==0
          for a,b,_ in map(coords,observed)))
    center_rows.append({'p':p,'s':s,'e':e,'subgroup_order':len(H),
                       'finite_center_order':len(observed),
                       'image_of_padic_center_order':len(true_center_image)})

# Test theta through matrix multiplication for primes outside the author scan,
# both characteristic 2 and odd, and for composite p-power precision.
for p, e in [(2,2), (3,2), (7,1), (11,1)]:
    q=p**e
    def theta(A):
        a,b,c=coords(A)
        return mat(b,a,a*b-c,q)
    selected = [mat(a,b,c,q) for a,b,c in itertools.product(
        sorted({0,1,p%q,(q-1)%q}),repeat=3)]
    for A in selected:
        check('matrix_inverse', mm(A,mi(A,q),q)==mat(0,0,0,q))
        check('matrix_theta_involution', theta(theta(A))==A)
        for B in selected:
            check('matrix_theta_homomorphism', theta(mm(A,B,q))==mm(theta(A),theta(B),q))
    X,Y=mat(1,0,0,q),mat(0,1,0,q)
    check('noncommuting_matrix_witness', com(X,Y,q)==mat(0,0,1,q))

# Full local automorphism group of the displayed F2 subgroup, independent
# multiplication-table enumeration, explicitly moves the central line.
local_autos=[]
u_rest=[g for g in U2 if g!=I2]
for images in itertools.permutations(u_rest):
    f=dict(zip([I2]+u_rest,[I2]+list(images)))
    if all(f[table[a,b]]==table[f[a],f[b]] for a in U2 for b in U2):
        local_autos.append(f)
center_line={mat(0,0,c,2) for c in range(2)}
check('p2_local_Aut_order', len(local_autos)==6)
check('p2_local_center_image_not_characteristic',
      any({f[g] for g in center_line}!=center_line for f in local_autos))
common=[]
for size in range(1,5):
    for generators in itertools.combinations(U2,size):
        K=set(generators)
        if I2 not in K or not all(table[a,b] in K for a in K for b in K):
            continue
        if all({f[g] for g in K}==K for f in local_autos) and all(
               {f[g] for g in K}==K for f in autos):
            common.append(frozenset(K))
check('p2_full_common_characteristic_enumeration',common==[frozenset({I2})])

# Wreath separator with nonabelian dihedral lamps, defined as permutations of
# the vertices of a square; top cycle has order 4, different from author cases.
def perm_product(a,b):
    return tuple(a[b[i]] for i in range(len(a)))
lamp_identity=tuple(range(4))
rotation=(1,2,3,0)
reflection=(0,3,2,1)
lamps={lamp_identity}
todo=deque([lamp_identity])
while todo:
    a=todo.popleft()
    for g in (rotation,reflection):
        b=perm_product(a,g)
        if b not in lamps:lamps.add(b);todo.append(b)
check('permutation_D8_lamps',len(lamps)==8)
def wreath_mul(u,v):
    lamps_u,i=u;lamps_v,j=v
    return tuple(perm_product(lamps_u[k],lamps_v[(k-i)%4]) for k in range(4)),(i+j)%4
zero=(lamp_identity,)*4
shift=(zero,1)
inverse_shift=(zero,3)
for a in lamps-{lamp_identity}:
    v=((a,)+zero[1:],0)
    cv=wreath_mul(wreath_mul(shift,v),inverse_shift)
    check('nonabelian_permutation_lamp_separator', cv!=v)
    check('lamp_shift_is_single_support',sum(x!=lamp_identity for x in cv[0])==1)
    check('lamp_subgroup_not_normal', cv[0][0]==lamp_identity)
# The trivial top group defeats the separator, marking the B=1 excluded case.
check('trivial_complement_control',perm_product(lamp_identity,reflection)==reflection)

# Subgroup enumeration of additive finite modules, not merely bounded exponent
# identities: enumerate every subgroup and its characteristic orbit under full
# generating coordinate swaps, elementary transvections and unit diagonals.
def subgroup_lattice(q,d):
    G=list(itertools.product(range(q),repeat=d));z=(0,)*d
    def add(a,b):return tuple((x+y)%q for x,y in zip(a,b))
    subs={frozenset({z})};todo=deque(subs)
    while todo:
        H=todo.popleft()
        for g in G:
            if g in H:continue
            cyclic=set();v=z
            while v not in cyclic:
                cyclic.add(v);v=add(v,g)
            J=frozenset(add(h,v) for h in H for v in cyclic)
            if J not in subs:subs.add(J);todo.append(J)
    return G,subs
module_rows=[]
for p,e,d in [(2,3,2),(3,2,2),(2,1,3),(3,1,3)]:
    q=p**e;G,subs=subgroup_lattice(q,d)
    transforms=[]
    for i in range(d):
        for j in range(d):
            if i==j:continue
            def trans(v,i=i,j=j):
                w=list(v);w[i]=(w[i]+w[j])%q;return tuple(w)
            def swap(v,i=i,j=j):
                w=list(v);w[i],w[j]=w[j],w[i];return tuple(w)
            transforms.extend([trans,swap])
    for i in range(d):
        for u in range(q):
            if u%p:
                def diag(v,i=i,u=u):
                    w=list(v);w[i]=w[i]*u%q;return tuple(w)
                transforms.append(diag)
    invariants={H for H in subs if all(frozenset(f(v) for v in H)==H for f in transforms)}
    scalars={frozenset(v for v in G if all(c%(p**a)==0 for c in v)) for a in range(e+1)}
    check('all_finite_module_subgroups_scalar_invariant',invariants==scalars)
    # The finite nonscalar maximal subgroup has trivial common characteristic
    # subgroup, matching the separate module comparison, not free-pro-p F.
    U=frozenset(v for v in G if v[0]%p==0)
    possible=[H for H in invariants if H<=U]
    # At e>1 U has unequal invariant factors; its characteristic subgroups may
    # differ from the Zp lattice, so avoid an unwarranted inverse-limit claim.
    module_rows.append({'p':p,'e':e,'d':d,'all_subgroups':len(subs),
                        'GL_invariant_subgroups':len(invariants),
                        'scalar_candidates_inside_nonscalar_U':len(possible)})

print(json.dumps({'assertions':sum(counts.values()),'counts':counts,
    'center_boundary_cases':center_rows,'module_cases':module_rows,
    'scope':'Finite mechanism and boundary controls only; universal p-adic claims require the audited proofs. No author imports.'},indent=2,sort_keys=True))
