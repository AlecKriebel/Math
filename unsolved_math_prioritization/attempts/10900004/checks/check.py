#!/usr/bin/env python3
"""Exact supplementary checks. This does not solve any global holonomy problem."""
from fractions import Fraction as F
from itertools import permutations, product
import json
from pathlib import Path

counts = {}
def check(label, condition):
    if not condition:
        raise AssertionError(label)
    counts[label] = counts.get(label, 0) + 1

def mat(rows):
    return tuple(tuple(F(x) for x in row) for row in rows)

def mm(A, B):
    return tuple(tuple(sum(A[i][k]*B[k][j] for k in range(len(B)))
                       for j in range(len(B[0]))) for i in range(len(A)))

def tr(A): return tuple(zip(*A))
def det2(A): return A[0][0]*A[1][1]-A[0][1]*A[1][0]
def inv2(A):
    a,b=A[0]; c,d=A[1]; z=det2(A)
    return mat(((d/z,-b/z),(-c/z,a/z)))
def scale(c,A): return tuple(tuple(c*x for x in row) for row in A)
def sub(A,B): return tuple(tuple(a-b for a,b in zip(r,s)) for r,s in zip(A,B))
def perm(p,A): return tuple(A[i] for i in p)
def ident(n): return mat(tuple(tuple(int(i==j) for j in range(n)) for i in range(n)))
def mpow(A,n):
    R=ident(len(A))
    for _ in range(n): R=mm(R,A)
    return R

def enc(A): return [[int(x) if x.denominator==1 else str(x) for x in row] for row in A]
def zero(A): return all(x==0 for row in A for x in row)
def matches(X,Y,A):
    return [p for p in permutations(range(4)) if X==perm(p,mm(Y,A))]

I=ident(2)
W0=mat(((1,0),(0,1),(-1,-1),(0,0)))
W=mat(((3,0),(1,2),(-4,-2),(0,0)))
Wp=mat(((3,2),(1,0),(-4,-2),(0,0)))
P4=list(permutations(range(4)))

# Mayer--Vietoris relation matrix R=[(1,-a),(0,-b)] is row-equivalent
# to diag(1,-b): replace its second column by column2+a*column1.
# Exhaustively control all GL(2,Z) matrices in this bounded box.
As=[]
for a,b,c,d in product(range(-5,6), repeat=4):
    A=mat(((a,b),(c,d)))
    if abs(det2(A))!=1: continue
    As.append(A)
    R=mat(((1,-a),(0,-b)))
    S=mat(((1,a),(0,1)))
    check('homology_smith_column_operation', mm(R,S)==mat(((1,0),(0,-b))))
    check('inverse_gluing_matrix', mm(A,inv2(A))==I)

# Exact same-generator-spectrum example in base-two exponent form.
U=tuple(F(2)**int(row[0]) for row in W)
V=tuple(F(2)**int(row[1]) for row in W)
Up=tuple(F(2)**int(row[0]) for row in Wp)
Vp=tuple(F(2)**int(row[1]) for row in Wp)
from math import prod
check('sl4_determinants', all(prod(x)==1 for x in (U,V,Up,Vp)))
check('simple_meridian_spectrum', len(set(U))==4)
check('individual_spectra_match', sorted(U)==sorted(Up) and sorted(V)==sorted(Vp))
check('no_simultaneous_match', not matches(W,Wp,I))
for X, expected in ((W,F(18)),(Wp,F(-6))):
    L=mat((tuple(X[0][j]-X[2][j] for j in range(2)),
           tuple(X[1][j]-X[2][j] for j in range(2))))
    check('triangle_lattice_determinant', det2(L)==expected)
    check('transverse_centroid', X[3]==(0,0) and all(sum(X[i][j] for i in range(3))==0 for j in range(2)))
    for v in product(range(-8,9),repeat=2):
        if v==(0,0): continue
        vals=[sum(r[j]*v[j] for j in range(2)) for r in X[:3]]
        check('middle_eigenvalue_bounded_controls', min(vals)<0<max(vals))
check('gram_exact', mm(tr(W0),W0)==mat(((2,1),(1,2))))
check('gram_false_positive', mm(tr(W0),W0)==mm(tr(scale(-1,W0)),scale(-1,W0)) and not matches(W0,scale(-1,W0),I))

# W0 begins with I_2, so W0*A=P*W0 forces A=(P*W0)[:2].
# This computes the entire normalizer without a bounded search in A.
normal=[]
for p in P4:
    PW=perm(p,W0)
    A=PW[:2]
    if mm(W0,A)==PW:
        check('normalizer_integral_unimodular', abs(det2(A))==1)
        check('normalizer_fixes_transverse',p[3]==3)
        order=next(n for n in range(1,13) if mpow(A,n)==I)
        check('normalizer_order', order in (1,2,3))
        normal.append((A,order))
check('six_normalizer_matrices',len(normal)==6 and len(set(A for A,_ in normal))==6)
expected={mat(x) for x in [((1,0),(0,1)),((0,1),(1,0)),((-1,-1),(0,1)),((1,0),(-1,-1)),((0,1),(-1,-1)),((-1,-1),(1,0))]}
check('normalizer_list_complete',set(A for A,_ in normal)==expected)

# Ray comparisons over exact rational controls, with all GL(2,Z) in the box.
for A in As:
    for r in (F(-2),F(-1),F(-1,2),F(1,2),F(1),F(2)):
        found=any(mm(W0,A)==scale(r,perm(p,W0)) for p in P4)
        check('ray_scaling_controls', not found or abs(r)==1)
        if found: check('ray_finite_order_controls',mpow(A,12)==I)

# Shears, all exact: general infinite-order assertion is proved in prose.
for k in range(-20,21):
    A=mat(((1,k),(0,1)))
    check('shear_match_iff_identity', bool(matches(W0,W0,A))==(k==0))
    for n in range(1,13):
        check('shear_power_formula',mpow(A,n)==mat(((1,n*k),(0,1))))

# Cover relation A*B1=B2*D: choose B2=A*B1 and D=I, so the
# cover degrees agree. Multiplying mismatch by B1 never kills it.
Bs=[]
for a,b,c,d in product(range(-2,3),repeat=4):
    B=mat(((a,b),(c,d)))
    if det2(B)!=0: Bs.append(B)
for k in (-3,-1,0,1,3):
    A=mat(((1,k),(0,1)))
    for B1 in Bs:
        B2=mm(A,B1)
        check('cover_degree_compatibility',abs(det2(B2))==abs(det2(B1)))
        for p in P4:
            E=sub(W0,perm(p,mm(W0,A)))
            check('finite_cover_cancellation',zero(mm(E,B1))==zero(E))
            check('finite_cover_relation',mm(perm(p,W0),B2)==perm(p,mm(mm(W0,A),B1)))

# Non-extension to a semidirect product: its involution would exchange
# these normalized spectra, which are unequal.
S1=(F(2),F(1,2),F(1),F(1))
S2=(F(1),F(1),F(3),F(1,3))
check('descent_det_one',prod(S1)==prod(S2)==1)
check('descent_spectrum_obstruction',sorted(S1)!=sorted(S2))

out={
 'result':'PASS',
 'scope':'Supplementary exact matrix checks; no global figure-eight representations or complete solution are claimed.',
 'assertions':sum(counts.values()),
 'counts':counts,
 'bounded_gl2_matrices':len(As),
 'bounded_cover_matrices':len(Bs),
 'complete_W0_normalizer':[{'matrix':enc(A),'order':order} for A,order in normal],
 'peripheral_example':{'U':[str(x) for x in U],'V':[str(x) for x in V],'V_prime':[str(x) for x in Vp]},
}
text=json.dumps(out,indent=2)+'\n'
(Path(__file__).parent/'results.json').write_text(text)
print(text)
