# Cohomological corrections on the original punctured lattice

14 October 2026 UTC. Row 1775 / 30004611, shared mathematical pass 2. This bounded report preserves and proves the complementary results. It is authored mathematical work, not an independent audit, a novelty claim, or a full solution of the source's broad problem. Notation and the elementary restriction-kernel and rank-two calculations are those of the accepted pass-1 common-poset report.

## 1. Setup

Let A be central essential in V over any field, dim V = ell >= 2. Mark H = ker(alpha), set S = Sym(V*), R = S/(alpha), A' = A minus H. Let P = L(A) minus the zero flat, ordered by inclusion, and Q = {X in P : X subset H}. The top elements of P and Q are V and H. Write D_X = D(A_X), E_X = {theta in D_X : theta(alpha)=0}, and I_X = alpha S on Q and S off Q, with inclusion maps. On Q let T denote the ordinary restriction derivation sheaf and Z the Ziegler restriction derivation sheaf. All sheaves are covariant functors and all cohomology below is sheaf cohomology on the indicated finite Alexandrov space.

The normal evaluation sequence from pass 1 is exact in every rank:

0 -> E -> D --theta maps to theta(alpha)--> I -> 0.       (N)

## 2. The normal sequence splits exactly at coloops

**Proposition.** Sequence (N) splits in the category of S-module sheaves if and only if H is a coloop, equivalently the deletion center T' = intersection(A') is nonzero. This is true without a characteristic assumption and whether or not grading is required.

**Proof.** A sheaf section sigma:I -> D, evaluated at the top V, determines theta = sigma_V(1) in Der_K(S), with theta(alpha)=1. Every L in A' is a nonzero point of P outside Q; its stalk has I_L=S. Naturality of sigma on L -> V forces sigma_L(1)=theta, so theta is tangent to L. Consequently theta belongs to D(A'). Since the logarithmic divisibility conditions are homogeneous, the coefficient-degree-zero part v of theta also belongs to D(A'), and theta(alpha)=1 implies alpha(v)=1. A constant derivation tangent to every L in A' is a vector of T'. Thus T' is nonzero. Essentiality of A gives T' intersect H = 0; hence T' is one-dimensional and H is a coloop.

Conversely choose v in T' with alpha(v)=1. Define sigma_X(f)=f partial_v on I_X, with I_X regarded as its actual ideal in S. Off Q, partial_v is tangent to A_X because A_X is contained in A'. On Q, the coefficient f is divisible by alpha, so f partial_v is also tangent to H. These maps commute with all inclusion arrows and evaluate to f. They split (N). The maps preserve coefficient grading. QED.

This is genuine failure of sheaf splitting, not merely failure of a selected Euler formula: the Euler splitting available on Q cannot extend across the full original poset unless H is a coloop.

## 3. The ideal is acyclic even when the normal sequence is nonsplit

There is an exact sequence

0 -> I -> S_P -> i_* R_Q -> 0,

where S_P and R_Q are constant sheaves and i:Q -> P is the closed inclusion. For a finite poset and constant coefficients, sheaf cohomology is simplicial cohomology of its order complex. P and Q each have a maximum, so both order complexes are cones. Thus H^0(P,S_P)=S, H^0(Q,R_Q)=R, and positive cohomology of these constant sheaves vanishes. The map on global sections is the surjection S -> R. Exactness of i_* and its preservation of cohomology now give

H^0(P,I)=alpha S,       H^k(P,I)=0 for every k>0.

The global Euler derivation is a section of D, evaluating to alpha. Hence the map H^0(P,D) -> alpha S is onto and splits as S-modules. The long exact sequence of (N) therefore yields canonical isomorphisms

H^k(P,E) -> H^k(P,D)       for every k>=1,

and a split exact sequence on global sections

0 -> H^0(P,E) -> H^0(P,D) -> alpha S -> 0.

The splitting on global sections is canonical after alpha and the usual Euler derivation are fixed. It does not imply that (N) splits as a sheaf sequence.

## 4. A precise poset-support bound for both restriction defects

Let C_O and C_Z denote the cokernel sheaves on P of D -> i_*T and E -> i_*Z, respectively. Their independently identified pass-1 kernels are I tensor c^*D' and I tensor E. Pass 1 proves both restriction maps onto whenever rank(A_X)<=2. Essentiality gives rank(A_X)=codim_V X. Therefore both cokernel sheaves are supported in the closed lower ideal

W = {X in Q : 1 <= dim X <= ell-3}.

For ell<=3 this set is empty and both defects vanish. For ell>=4, every strictly increasing chain in W has at most ell-3 vertices, so its order-complex dimension is at most ell-4. A sheaf supported in a lower ideal is the exact extension by zero of its restriction to that ideal. Consequently

H^k(P,C_O)=H^k(P,C_Z)=0 for every k>ell-4.       (B)

For completeness this does not rely on a general dimension assertion: the normalized finite-poset cochain complex for a covariant sheaf F has degree n term the product of F_(x_n) over chains x_0<...<x_n. If F is supported in W, a nonzero summand has x_n in W; lower-closedness puts the whole chain in W. Thus the complex is zero in degrees n>ell-4, proving (B) directly.

This is a poset-dimension bound. It is distinct from, and is not implied merely by, the pass-1 fact that individual defect modules have support of R-codimension at least two. No sharpness claim for actual logarithmic defects is made here.

**Useful high-degree consequence.** For either restriction map write J for its image and Tbar for its named target i_*T or i_*Z. The auxiliary short exact sequence 0 -> J -> Tbar -> C -> 0 and (B) show that

H^k(P,J) -> H^k(P,Tbar)

is surjective for k=ell-3 and is an isomorphism for all k>=ell-2 (ell>=4). Thus in these latter degrees the long exact sequence of the independently identified kernel agrees with one having the named restriction target. The lower-degree correction cannot simply be discarded: the possible map H^(ell-4)(P,C) -> H^(ell-3)(P,J) prevents asserting an unqualified connecting map from H^(ell-3)(P,Tbar). At ell=4 the two defects are supported on finitely many one-dimensional flats; they have no positive cohomology, but their global sections can still produce this low-degree correction.

## 5. Actual center-punctured deletion in the coloop case

This paragraph treats the deletion convention that differs from the retained-center extension in pass 1. Suppose H is a coloop and choose v spanning T' with alpha(v)=1, giving V=H direct-sum Kv and S=R[alpha]. Put B=A^H. Every deletion hyperplane is K direct-sum Kv for its restricted hyperplane K in B. Hence

L(A') = {Y direct-sum Kv : Y in L(B)}.

The actual center-punctured deletion poset P'_cen=L(A') minus {Kv} is canonically identified with Q=L(B) minus {0} by Y -> Y direct-sum Kv. Under this identification its logarithmic derivation sheaf is

D'_cen = (S tensor_R D_B) direct-sum S_Q partial_v.       (C)

Indeed every defining equation of a deletion localization is alpha-independent, and coefficient-wise polynomial expansion in alpha gives the displayed direct sum of tangent derivations and the unconstrained normal derivation. The splitting commutes with every localization inclusion. Since S is flat over R and finite-poset cochains are finite products, cohomology commutes with this scalar extension. Since Q has a maximum, the constant summand is acyclic. Therefore

H^0(P'_cen,D'_cen) = (S tensor_R H^0(Q,D_B)) direct-sum S partial_v,

H^k(P'_cen,D'_cen) = S tensor_R H^k(Q,D_B) for k>=1.

The isomorphism of posets is intrinsic; the displayed module decomposition uses the chosen product coordinate. This gives the correct cohomology of actual center-punctured deletion. It must not be replaced by the retained-center poset, whose minimum makes positive cohomology vanish for every sheaf.

When ell=2, Q={H}. Formula (C) and the cohomology statements remain valid, with H^0(Q,D_B)=Der_K(R), not generally D(B). For an essential one-dimensional restriction B, its removed zero flat carries the logarithmic condition, so that condition is absent from the remaining single stalk. No dimension-at-least-two global-section identification is being applied at this boundary.

## Scope

The new complementary results are the exact splitting criterion, acyclicity and higher-cohomology comparison for the normal sequence, the uniform defect-support vanishing bound, and the correct product formula for center-punctured coloop deletion. These supplement the companion's all-rank complex construction; they do not assert unconditional surjectivity of the ordinary or Ziegler maps, nor a complete addition-deletion theorem, nor full resolution of Mücksch's broad Problem 6.3.
