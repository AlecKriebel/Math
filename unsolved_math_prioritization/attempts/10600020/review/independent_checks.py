#!/usr/bin/env python3
"""Independent exact diagnostics; none decides splitting or supporting genus."""
from pathlib import Path
import hashlib
import itertools
import json
import sympy as S

counts = {}
def ck(name, value):
    assert bool(value), name
    counts[name] = counts.get(name, 0)+1

# Matrix formulation independent of the submitted vector implementation.
for g in (1, 2, 3):
    J = S.zeros(2*g)
    for k in range(g):
        J[2*k,2*k+1]=1
        J[2*k+1,2*k]=-1
    I = S.eye(2*g)
    curves = [S.eye(2*g)[:,i] for i in range(2*g)]
    curves += [S.Matrix([(-1)**i*(i+1) for i in range(2*g)]),
               S.zeros(2*g,1)]  # Separating curves have zero homology.
    chain = I
    for c in curves:
        for n in (-4, -1, 0, 1, 5):
            T = I-n*c*c.T*J
            inverse = I+n*c*c.T*J
            ck("matrix_transvection_preserves_pairing", T.T*J*T == J)
            ck("matrix_transvection_inverse", T*inverse == I)
            ck("matrix_transvection_unimodular", T.det() == 1)
            ck("matrix_zero_preserved", T*S.zeros(2*g,1) == S.zeros(2*g,1))
            chain = T*chain
    ck("composed_mapping_class_zero", chain*S.zeros(2*g,1) == S.zeros(2*g,1))
    ck("composed_mapping_class_symplectic", chain.T*J*chain == J)

# Nondegenerate intersection-coordinate test, not a geometric intersection test.
J = S.Matrix([[0,1,0,0],[-1,0,0,0],[0,0,0,1],[0,0,-1,0]])
for coords in itertools.product((-1,0,1), repeat=4):
    v=S.Matrix(coords)
    ck("all_pairs_zero_iff_homology_zero", (v.T*J == S.zeros(1,4)) == (v == S.zeros(4,1)))

# Surgery torus markings: determinant-one map sends meridian to mu+n lambda.
for n in range(-12,13):
    A=S.Matrix([[1,0],[n,1]])
    mu,lam=S.Matrix([1,0]),S.Matrix([0,1])
    ck("surgery_marking_determinant", A.det()==1)
    ck("surgery_meridian_image", A*mu==mu+n*lam)
    ck("surgery_longitude_fixed", A*lam==lam)
    ck("nonmeridional_exactly_nonzero_n", (S.det(S.Matrix.hstack(mu,A*mu))!=0)==(n!=0))

# Product-annulus twist: its formula is independent of the thickening coordinate.
theta,u,r,n=S.symbols("theta u r n",real=True)
rho=10*u**3-15*u**4+6*u**5
F=S.Matrix([theta+n*rho,u,r])
ck("annular_product_orientation", F.jacobian([theta,u,r]).det()==1)
ck("thickening_coordinate_unchanged", F[2]==r and S.diff(F[0],r)==0)
ck("annular_twist_bottom",rho.subs(u,0)==0)
ck("annular_twist_top_integral_rotation",rho.subs(u,1)==1)
for order in (1,2):
    ck("annular_cutoff_endpoint_jets",S.diff(rho,u,order).subs(u,0)==0)
    ck("annular_cutoff_endpoint_jets",S.diff(rho,u,order).subs(u,1)==0)
ck("annular_twist_inverse",S.expand((F[0]-n*rho)-theta)==0)
# The polynomial only diagnoses the collar formula; a flat smooth cutoff
# supplies the standard smooth twist, and is part of the geometric argument.

# Integral surgery quotient: an explicit homomorphism and splitting.
for n,ell in itertools.product(range(-5,6),(-3,-1,0,2,4)):
    rel=S.Matrix([n*ell,1])
    quotient=S.Matrix([[1,-n*ell]])
    generator=S.Matrix([1,0])
    ck("filling_relation_in_kernel",(quotient*rel)[0]==0)
    ck("filling_generator_surjects",(quotient*generator)[0]==1)
    ck("filling_integral_basis",S.Matrix.hstack(generator,rel).det()==1)

# Independent trefoil polynomial from a Seifert matrix.
t=S.symbols("t")
V=S.Matrix([[1,0],[-1,1]])
delta=S.expand((V-t*V.T).det())
ck("trefoil_seifert_polynomial",delta==t*t-t+1)
ck("trefoil_nonunit_polynomial",S.degree(delta,t)==2 and delta.subs(t,-1)==3)
M=S.Matrix([[2,1],[3,2]])
ck("torus_curve_mapping",M.det()==1 and M*S.Matrix([1,0])==S.Matrix([2,3]))

root=Path(__file__).resolve().parent
result={
 "status":"PASS",
 "exact_assertions":sum(counts.values()),
 "checks":counts,
 "artifact_sha256":hashlib.sha256((root/"author_replay/OBSTRUCTION.md").read_bytes()).hexdigest(),
 "scope":"Independent matrix homology, surgery marking and quotient, local product-annulus "
         "twist, and Seifert-matrix diagnostics. No splitting, minimal-genus, disk-placement, "
         "or universal-realization certificate."
}
(root/"independent_results.json").write_text(json.dumps(result,indent=2)+"\n")
print(json.dumps(result,indent=2))
