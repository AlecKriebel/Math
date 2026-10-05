# Scoped proofs and obstruction controls

Throughout, k is perfect of characteristic different from 2. Schemes are
smooth separated and of finite type over k. B_q is the integral BLRS complex
specified in REPORT.md. R denotes the ordinary Rost–Schmid complex. None of
the statements below is asserted to be a new theorem in the literature.

## 1. Weight zero has descent

**Proposition.** B_0(-,M) is naturally homotopy equivalent to R(-,M) for a
strictly A¹-invariant sheaf M. In particular the requested comparison holds
for q=0 and M=K_0^MW.

**Proof.** Every support is 0-good, and the full space is a final support.
For i>0 the term in degree -i is therefore H^0(X×Δ^i,M)=M(X×Δ^i).
Strict A¹ invariance, and Δ^i≅A^i, identify this with A=M(X) by projection
pullback. Under these identifications every face map is the identity of A.
Thus the negative differential from degree -i to -i+1 is multiplication
by the alternating sum of i+1 copies of 1. For i>1 it is the identity
when i is even and zero when i is odd, up to the uniform convention for
alternating face signs. At i=1 the splice is the difference of the two
endpoint maps and is zero. Degrees >=0 are exactly R.

Consequently B_0 is the direct sum of R and the negative complex formed by
copies of A, paired by identity differentials -2j -> -(2j-1), j>=1.
Contract each such pair by the inverse identity from -(2j-1) to -2j.
This defines h with dh+hd=1 on the negative summand. The identification
and contraction commute with open restriction. The ordinary R is a
flasque resolution of M and hence computes RΓ_Zar(X,M). Applying the
natural homotopy equivalence proves the assertion. ∎

This proof also fixes the edge case q=0 without claiming that the lower
terms literally vanish before normalization.

## 2. A lower BLRS term is not flasque

**Proposition.** For k=Q and q=2, the restriction

    B_2^0(A¹_x) -> B_2^0(Gm_x)

is not surjective.

**Proof.** Write Δ² with coordinates t_1,t_2 and t_0=1-t_1-t_2. In
Y_U=Gm_x×Δ² take the closed curve

    Γ_U: t_1=x, t_2=x.

It is smooth and isomorphic to Gm. The two displayed equations form a
regular sequence and trivialize its conormal determinant, and therefore
also its normal determinant. Purity for the ordinary Rost–Schmid
complex identifies H^2_{Γ_U}(Y_U,K_2^MW) with the sections of K_0^MW
on Γ_U twisted by that determinant. The chosen equations give a section
α corresponding to the constant rank-one form <1>.

We check admissibility in the ambient face, not in the full ambient space
only. Γ_U has codimension 2 in Y_U. It misses the faces t_1=0 and t_2=0.
Its intersection with t_0=0 is the point x=1/2,t_1=t_2=1/2. A face here
has dimension 2, so this intersection has codimension 2. All vertices
are missed: a vertex with t_1=0 or t_2=0 would require x=0, which is
excluded; no vertex has t_1=t_2=1/2. These exhaust all nonempty proper
faces. Hence Γ_U is 2-good and α defines an element of B_2^0(U).

The residue-kernel description makes this group a subgroup of the direct
sum over the codimension-2 points of Y_U: supports of codimension >=2
have no degree-1 Rost–Schmid terms. In particular α has nonzero
coefficient, of rank 1, at the generic point of Γ_U.

Suppose β∈B_2^0(A¹) restricts to α. Choose a closed 2-good support Z for β.
The coefficient of β at that same generic point must be nonzero. Thus Z
contains the closure

    Γ: t_1=x, t_2=x

in A¹×Δ². This closure meets the face F given by t_1=t_2=0 at x=0.
The ambient A¹×F has dimension 1, so that intersection has codimension 1,
not at least 2. Since Z contains Γ, the same forbidden point lies in
Z∩(A¹×F). This contradicts 2-goodness. Adding further components cannot
remove a point from a closed support. Therefore β cannot exist. ∎

This is a statement about a **single term**, not the cohomology of the
total complex. The ambient A¹ has trivial canonical bundle and is affine,
so Bachmann–Yakerson's theorem already gives descent for B_2 there. The
proposition is fully consistent with that theorem. The same support
obstruction also appears for ordinary Bloch cycles; it is not evidence
peculiar to a failure of Milnor–Witt descent.

## 3. Quadratic ramification obstructs coefficientwise closure

**Proposition.** Fix a∈Q\{0,1}. On the smooth divisor
Z_U={t=a}⊂Gm_x×Δ¹, the coefficient <x> defines a degree-1 supported
Milnor–Witt cocycle. On its closure Z={t=a}⊂A¹_x×Δ¹, keeping that
generic coefficient and adding no other component does not define a
cocycle.

**Proof.** Trivialize the normal line by the equation t-a. The form <x>
is nondegenerate over Q[x,x^(-1)], so defines an unramified GW section on
Z_U. The support misses both faces t=0,1 and is 1-good. Purity gives the
asserted supported class.

At the discrete valuation x=0 on Q(x), the second Witt residue is

    ∂_x(<x>) = <1> ∈ W(Q).

Indeed the usual second residue of a diagonal form <u x^m>, with u a
unit, is zero for even m and <ū> for odd m. Apply this to u=1,m=1.
The rank modulo 2 of <1> is nonzero, so the residue is nonzero. In the
chosen determinant frames this is precisely the local component of the
Rost–Schmid differential GW(Q(x))->K_{-1}^MW(Q)=W(Q). A possible global
sign from alternative residue conventions leaves it nonzero.

Consequently the proposed degree-1 chain on Z has a nonzero boundary at
(x,t)=(0,a), and fails the cocycle condition. ∎

No claim that all extensions are impossible follows: a new component on
the deleted divisor x=0 may contribute a cancelling residue. This is why
the proposition invalidates only closure *without correction*. It also
shows why a rational orientation cannot be treated as a everywhere
unramified unit.

## 4. The terms are Zariski sheaves; the tail has exact Čech rows

**Lemma.** Each degree of B_q on X_Zar is a sheaf.

**Proof.** For p>=q the assertion holds for the usual direct sum of
point-supported coefficient sheaves. For p=q-i<q, supported cohomology
has the concrete description

    colim_{Z q-good} ker(R_Z^q(V×Δ^i,M)->R_Z^(q+1)(V×Δ^i,M))

on an open V⊂X, since R_Z^(q-1)=0. Thus its sections are finite
codimension-q point chains with q-good closed support and zero residue.

Given compatible sections on an open cover of V, choose a finite subcover,
possible because V is noetherian. The finite point chains glue uniquely
by the canonical identifications of their residue fields and determinant
lines on overlaps. The resulting chain is finite because only finitely
many finite chains were used. Its residue is zero since that condition
holds on the cover. Take the union of the closures of its nonzero point
terms. Admissibility is local on the base V: after restriction to each
member of the cover, this closed support is contained in the given
q-good support. Thus on every face its codimension is at least q locally,
hence globally. The glued chain is the required section. Uniqueness is
immediate from its pointwise coefficients. ∎

**Lemma.** For a finite open cover (U_j) of X and every p>=q, the augmented
Čech complex of the sheaf B_q^p=R^p is exact.

**Proof.** For a point x∈X^(p), put I_x={j:x∈U_j}, a nonempty finite set,
and let A_x be its twisted coefficient group. The summands indexed by x
form the augmented cochain complex of the full simplex on I_x with
constant coefficients A_x. Choose its least vertex b. On alternating
cochains define (hc)(j_0,...,j_{r-1})=c(b,j_0,...,j_{r-1}), interpreting
repeated indices as zero and reordering with the permutation sign. In
degree zero h is evaluation at b, landing in the augmentation group.
Expanding the alternating differential gives δh+hδ=1, including the
augmentation. This is the familiar insertion-of-a-vertex contraction,
and the formula proves the identity directly by pairwise cancellation.

Because the cover is finite, the finite products in each Čech degree
commute with the direct sums over x. Taking the direct sum of these
contractions proves exactness. ∎

Notice that extension by zero works for each **term** R^p but need not
commute with the vertical residue differential. Nothing here asserts it
does.

## 5. Exact finite Čech formulation of the unresolved defect

Let U_1,...,U_r be a finite affine open cover trivializing ω_X. Since X is
separated, every nonempty finite intersection U_I is affine; restricting
a trivialization from any member shows ω_{U_I} is trivial. Use normalized
Čech cochains indexed by strictly increasing, nonempty subsets I. For a
complex of presheaves F write

    Č(F)^a = ∏_{|I|=a+1} F(U_I),  0<=a<=r-1,
    D_U(F) = Cone(F(X) -> Tot Č(F)).

Total degree in the Čech double complex is a+b, where b is the degree
inside F; one may use d_tot=δ+(-1)^a d_F. Empty intersections contribute
zero. Finite horizontal width makes every total-degree sum finite, even
though B_q is unbounded below.

**Proposition.** In the source regime:

1. Tot Č(B_q) is naturally quasi-isomorphic to RΓ_Zar(X,B_q).
2. The desired comparison for X holds if and only if D_U(B_q) is acyclic.
3. Put T_q^b=B_q^b for b>=q and T_q^b=0 for b<q, with inherited
   differential. Put L_q=B_q/T_q (the brutal quotient, including zero
   differential out of degree q-1). Then the induced map

       D_U(B_q) -> D_U(L_q)

   is a quasi-isomorphism.

**Proof.** Let E=(K_q^MW)^(q) be the homotopy-coniveau presheaf in
Bachmann–Yakerson. Their comparison α:B_q->E is natural for open
immersions; E has Zariski descent; and the induced localization map is
an equivalence. On every U_I the affine/trivial-canonical-bundle theorem
says α(U_I) is a quasi-isomorphism. Finite Čech totalization therefore
gives Tot Č(B_q)≃Tot Č(E)≃E(X)≃RΓ_Zar(X,B_q), compatibly with the
augmentation. This proves (1) and (2).

There is a degreewise split short exact sequence of complexes
0->T_q->B_q->L_q->0. Finite products, totalization and formation of the
augmentation cone give a short exact sequence of complexes

    0 -> D_U(T_q) -> D_U(B_q) -> D_U(L_q) -> 0.

Each augmented horizontal row of T_q is exact by §4, because its
nonzero rows are ordinary Rost–Schmid terms. These rows are also zero
for b>dim X. Thus this particular augmented bicomplex is bounded in
both directions, and its row-exact total complex D_U(T_q) is acyclic
(filter by its finitely many vertical degrees and use successive exact
rows, or the elementary finite-double-complex spectral sequence).
The long exact sequence in cohomology proves (3). ∎

This proposition does not prove acyclicity of D_U(L_q). The fact that
L_q has only degrees below q is insufficient: nonzero Čech degrees can
carry nonzero total cohomology. Nor does the affine comparison apply to
the global augmentation just because it applies on every U_I. That
augmentation is exactly what is being tested.

The construction is independent of the chosen good affine cover in the
derived sense: (1) identifies its cone with the cone of the canonical
global comparison. This independence does not make the cone zero.

## 6. Square twists and the remaining orientation issue

**Lemma.** Let N be a sheaf with the usual GW-module action, and let L be
a line bundle. There is a canonical isomorphism N(L⊗²)≅N, natural in
open restriction. More generally N(D⊗L⊗²)≅N(D).

**Proof.** On an open where L has a frame e, use e⊗e to identify its
square twist with the untwisted module. Changing e to u e changes the
identification by the action of <u²>. The one-dimensional form <u²>
is isometric to <1> by multiplication of its vector coordinate by u,
and consequently acts as the identity. The local identifications agree
and glue. The same argument with D retained proves the general case. ∎

Thus a specified square-root orientation of ω_X trivializes its action
as a twist, even without a frame of the root. The statement does not
provide such a root on every X. For example ω_{P²}=O(-3) is not a square
in Pic(P²)=Z. This example only refutes universal existence of square
roots; it is not a counterexample to BLRS descent.

No extension of the published hard-moving theorem is claimed solely
from the lemma. That extension would still require checking the actual
transfer, support and residue steps. A rational trivialization instead
of a regular one changes the situation: it may have odd valuations and
therefore the nonzero residues illustrated in §3. Likewise homotopy
coherent Gysin maps on R do not by themselves make q-good support
corrections exist in B_q.

## Boundaries of the proofs

The exact controls verify the simplex-contraction signs, the linear
face-incidence calculation, and elementary square/parity identities.
They are not a decision procedure for arbitrary schemes, motivic
cohomology or the remaining Čech acyclicity. The imported foundational
results (purity, the Rost–Schmid resolution and the cited comparison
theorem) are used with their stated assumptions, not re-proved here.
