# Turn 5: canonical Floer lifts and the missing two-surgery parity

**Final author status: original Question 10.21 unresolved after five substantive turns.** The canonical odd-Chern theorem of Turn3 is the strongest positive result. This last turn examines a genuinely presentation-independent alternative on all rational homology spheres, disproves its degree-one property, and isolates an exact remaining condition for its Euler/torsion correction. No new theorem from Floer theory is claimed: the inputs below are credited classical results.

## 1. A canonical scalar lift on all rational homology spheres

Fix the positive discriminant convention of Turn4, so the Brown invariant of a nonsingular characteristic surgery presentation is

    B(M,sigma)=signature(B)-c^T B^(-1)c modulo8.

Ozsváth–Szabó's correction term d(M,sigma) is a rational topological invariant of a rational homology Spin^c sphere. It is additive under connected sum, changes sign under orientation reversal, is invariant under conjugating sigma, and satisfies

    d(M,sigma) = (c^T B^(-1)c-signature(B))/4 modulo2.

The precise congruence is in their absolute-grading construction and Theorem1.2; it is also explicitly restated in Rustamov, Section4, printed p.6. Consequently

    F_d(M,sigma)=-4d(M,sigma) modulo16

is a canonical additive lift of B on **every rational homology sphere**, including the higher-two-primary structures not covered by Turn3. Its definition avoids a surgery representative and an arbitrary phase section. With the published negative boundary-quadratic convention, negate this whole lift instead. None of these facts alone proves its finite-type degree.

## 2. The canonical d-lift fails the degree-one requirement

**Proposition 5.1.** F_d is not a finite-type invariant of Y-degree at most one, even when restricted to integral homology spheres with their unique Spin^c structures.

**Proof.** Put P=-Sigma(2,3,5) and Q=Sigma(2,3,7), with exactly the orientations in Ozsváth–Szabó, Section8.1, printed pp.46–47 of the pinned v2 preprint. They calculate

    d(P)=-2,  HF^+_red(P)=0,
    d(Q)=0,   HF^+_red(Q)=Z supported in degree -1.

Their Theorem1.3 (proved as Theorem5.1) identifies

    chi(HF^+_red(M))-d(M)/2 = lambda(M)

on integral homology spheres, with the standard Casson normalization. Thus lambda(P)=1 and lambda(Q)=-1. Casson modulo2 is the classical Rochlin value divided by8. Both manifolds have Rochlin value8 modulo16. Independently, Ue's published paper, p.122, explicitly records d(Q)=0 and the Neumann–Siebenmann value8, whose mod16 reduction is Rochlin.

Habiro's Y2 classification of integral homology spheres therefore makes P and Q Y2-equivalent. See Massuyeau's surgery survey, Corollary3.15; the preceding original Ohtsuki source, printed p.524, states that Y2-equivalent integral homology spheres cannot be distinguished by any abelian-group-valued finite-type invariant of Y-degree less than2. Unique Spin^c structures make these statements apply without any transport choice here. A degree-at-most-one F_d would have equal values on P and Q. In fact

    F_d(P)=8,    F_d(Q)=0 modulo16.

This contradiction proves the claim. Negating the global convention leaves the inequality unchanged. ∎

This is stronger than merely observing failure to recover the spin Rochlin value on Q. It proves that the most direct canonical Floer lift violates the source's intended degree condition. It does not disprove other Spin^c lifts.

## 3. The Euler-corrected candidate and its exact unresolved condition

For any rational homology Spin^c sphere define the rational invariant

    hat_chi(M,sigma)=chi(HF^+_red(M,sigma))-d(M,sigma)/2,
    F_E(M,sigma)=8 hat_chi(M,sigma) modulo16.

The Euler characteristic is the integer-valued one from the canonical mod2 grading, as in the cited Floer literature; a rational absolute grading is not exponentiated to define it. The reduced group is finite-dimensional over Q, or equivalently one takes the alternating ranks of its free part.

F_E is a canonical topological lift of B, because it differs from F_d by8 times an integer. On integral homology spheres, the cited Casson identity gives

    F_E=8 lambda=R modulo16.

It therefore has degree at most one on that restricted class, and the Poincare/S3 calibration makes the degree exactly one there. For P and Q above, chi_red is0 and-1 respectively, and both corrected values are8. These facts do not establish degree one on all rational homology spheres, nor compatibility with every spin structure on a rational homology sphere.

Here is a precise test rather than an unsupported promotion. On a two-disjoint-Y-surgery cube, use Delta2 X=X_empty-X_1-X_2+X_12. The canonical Brown value is unchanged by each Y-surgery, hence

    -4 Delta2 d is in8Z,  so Delta2 d/2 is an integer.

It follows that Delta2 hat_chi is an integer. The candidate F_E has zero second difference on this cube **if and only if**

    Delta2 hat_chi is even.                         (1)

Thus Brown invariance already supplies integrality; the additional parity in(1) is the actual missing assertion. No implication from integrality to evenness is being used. This criterion is valid without presuming connected-sum additivity or a coherent common surgery matrix.

Rustamov's Theorem3.4 identifies, on rational homology Spin^c spheres,

    hat_chi(M,sigma)=-tau(M,sigma)+lambda(M),

where tau is the normalized scalar Turaev torsion and lambda is the normalized Casson–Walker invariant. This is a canonical topological interpretation of the corrected candidate. It does not, by itself, show that the second surgery difference is even. This work has not proved (1), nor found a counterexample to it in the remaining higher-two-primary class.

## 4. Why the known torsion finite-type theorem is insufficient here

Massuyeau's *Some finiteness properties for the Reidemeister–Turaev torsion* is a relevant primary input, but its exact hypotheses and degree must be retained. Theorem1, in the pinned v3 author version, fixes a finitely generated group G, an Euler structure, and a homological parametrization. For G of positive rank or G finite cyclic, reduction of the group-ring torsion modulo the d-th augmentation-ideal power has degree at most d+1, for d>=1. The smallest stated upper bound is2, not1.

More specifically, Theorem4.2 on finite cyclic G gives, for a family of r>=2 disjoint Torelli surgeries,

    Delta_r tau is in kappa(I^(r-2)),
    kappa(x)=x-aug(x) |G|^(-1) sum_(g in G) g.

At r=2 this is kappa(Z[G]); there is no factor of2 and no assertion of even scalar coefficients. The positive-rank Theorem4.1 similarly supplies an augmentation-ideal bound, not the required scalar parity. The general finite noncyclic case is not covered by Theorem1. Furthermore, one must identify the precise scalar coefficient and normalization used in Rustamov's formula before attempting to compare these objects; a group-ring theorem cannot simply be renamed a theorem about the scalar invariant.

Even strengthening an ideal bound need not force parity. In Z[Z/4], if g is a generator, then (g-1)^2=1-2g+g^2 lies in I^2 but not in2Z[Z/4]. This is an elementary algebraic warning, **not** a claim that this polynomial is realized by a particular surgery defect. None of the quoted torsion results supplies (1) automatically. Importing it would transfer the central difficulty to an unsupported parity claim.

## 5. Final scope and stopping point

The five author turns yield:

- A canonical, additive, genuine degree-one lift for rational homology spheres whose selected Spin^c Chern class has odd order, including all spin-induced structures and all structures when the 2-primary homology has exponent at most two
- Explicit phase-only/additivity obstructions under their stated extra hypotheses, together with a non-torsion finite-section ambiguity
- Exact characteristic-presentation cocycle and Kirby/degree-one parity laws, and a fixed higher-two-primary lens-space failure of two naive constructions
- A canonical Floer lift on all rational homology spheres which is rigorously excluded as a degree-one solution, plus a precisely formulated remaining parity problem for the Euler/torsion correction

The general natural degree-one refinement across higher-two-primary Chern data remains unconstructed. The original's abbreviated non-torsion domain is not resolved by arbitrarily choosing a finite section. The global additive obstruction does not rule out every nonadditive interpretation, and a bare phase branch is not presented as the intended geometric refinement. These are the exact remaining gaps. The original target is **unsolved after5/5**, with no historical novelty assertion. Subsequent activity is limited to independent review, correction and authorized publication of this scoped package, not a sixth proof-search turn.
