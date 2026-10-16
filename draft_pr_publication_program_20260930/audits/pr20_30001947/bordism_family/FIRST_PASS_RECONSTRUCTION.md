# Independent bordism reconstruction

Sealed UTC: 2026-10-01T18:15:45Z. Completion estimate: 85% of this family audit. No old review or other family findings have been read. Target: original head 7914dfa8c2ddf0efb784a29accc8a05b5a24a690, problem 30001947.

## Criterion outcome

The candidate's negative answer is supported in the conventional closed, compact, integral-oriented, classical PL mod-two Witt category. The positive prior theorem is Goresky–Pardon (1989), §10.5 Theorem A, with the relevant proof in §10.7 Part A; its dimensional specialization is exactly 4j+2, not just isolated singularities. The theorem defaults to normal connected pseudomanifolds. The adapter below removes that default without extending the category to codimension-one spaces or spaces with boundary. Friedman (2015) §5.2.1 explains the historical correction and identifies the matching categories, but that footnote is corroboration, not this derivation's mathematical premise.

## Exact definitions and domain

Set F=F_2. A classical n-dimensional PL stratified pseudomanifold has no codimension-one strata. The target X is compact without boundary; its regular n-strata have integral orientations. For every singular stratum of odd codimension c=2k+1≥3 and link L of dimension 2k, require I^{m}H_k(L;F)=0, with m(c)=floor((c−2)/2). This is precisely the field-valued Witt condition. Neither an odd-dimensional-link vanishing requirement nor an IP, LSF, or s-duality hypothesis is added. The link condition supplies I^{m}H_*(X;F)≅I^{n}H_*(X;F), where n(c)=floor((c−1)/2), and therefore a nonsingular middle pairing.

Integral orientation implies orientability of every link: restrict an orientation in a chart R^s×cL to R^s×(0,1)×L_reg. Choose orientations of the Euclidean and interval factors and divide the product orientation by them. This orients every regular component of L. It is an assertion that L is orientable, not a choice of coherent orientations over the entire stratum. Thus X meets the older source's local orientability condition. Goresky–Pardon §8.3 establishes the same implication.

## Normalization adapter

Let π:X̃→X be the PL normalization. It is proper, is a homeomorphism on the regular strata, and in a chart replaces cL by the disjoint union of cK_a for the connected components K_a of the normalization L̃. Pull back regular orientations. Since lower-middle perversity obeys m(c)≤c−2, normalization induces an intersection homology isomorphism in every degree. Friedman, Singular intersection homology, Proposition 5.1.11, printed pp.192–193, proves this by induction with the cone formula and Mayer–Vietoris. The same result applies to every link. Therefore a vanishing I^{m}H_k(L;F) gives vanishing of every summand I^{m}H_k(K_a;F), so X̃ is still F-Witt.

The middle pairing is preserved, not just the vector-space dimension. Represent middle classes by PL allowable cycles in stratified general position. For two cycles of dimension n/2, their possible intersection on a codimension-c singular stratum has dimension at most −c+2m(c)≤−2. Hence all intersection points that define the pairing lie in the regular stratum. The normalization is an orientation-preserving homeomorphism there, so it gives exactly the same mod-two intersection counts. Under the normalization isomorphism, the pairings are isometric. The normalized compact space has finitely many connected components and the pairing is their orthogonal direct sum.

This avoids assuming that the mapping cylinder mentioned in the older source automatically satisfies the Witt condition; preservation of the pairing and each link's vanishing is checked directly.

## Positive theorem and boundary adapter

For each normal oriented connected component of X̃ of dimension n=4j+2>0, Goresky–Pardon §10.5 Theorem A gives zero oriented mod-two Witt bordism class. Section 10.7 Part A applies the intersection-homology odd-square relation to show its mod-two intersection Euler characteristic vanishes, and applies the cited singular-surgery boundary criterion. The present audit uses this published theorem, not skew symmetry alone: skew symmetry in characteristic two does not imply an alternating form. The theorem's printed degree-zero formula omits the usual integral-oriented Ω_0=Z exception; degree zero does not occur in this target. Friedman’s later computation explicitly includes that exception.

It remains to connect bordism to the requested bilinear Witt class. Suppose ∂W=X̃, with W a compact oriented F-Witt PL pseudomanifold with collared boundary. Write n=2m and take all groups below over F, with middle perversities identified using the Witt condition. The relative exact sequence contains

    I H_{m+1}(W,X̃) --∂--> I H_m(X̃) --i--> I H_m(W).

Put K=im ∂=ker i. Poincare–Lefschetz duality is a perfect pairing

    B_W:I H_{m+1}(W,X̃) × I H_m(W) → F.

The compatibility of the boundary map with the intersection pairing gives, for a relative class a and a boundary class x,

    b_X̃(∂a,x)=B_W(a,i x).

One can check this equality on transverse relative chains in the collar; it is also the cap-product boundary identity. All signs disappear over F_2. Thus x∈K^perp iff B_W(a,i x)=0 for every a iff i x=0, by nondegeneracy. Therefore K^perp=K. In particular dim K=(1/2)dim I H_m(X̃), and K is a Lagrangian. A nonsingular symmetric bilinear form possessing such a subspace is metabolic and represents zero in the bilinear Witt group. The isometric normalization adapter gives [b_X]=0 as well. The same boundary calculation proves bordism invariance by applying it to X_0 disjoint union −X_1.

No integral Poincare duality, integral intersection-homology universal coefficient theorem, or additional link torsion condition is used. Field-coefficient Poincare–Lefschetz duality is sufficient; Friedman’s book Theorem 8.3.9, printed p.545, supplies it, and the Witt condition identifies the complementary middle perversities. A collar is part of the cited bordism category.

## Edge cases and adversarial controls

For j=0, X has dimension two and only isolated point strata, with links disjoint unions of circles. Normalization is a disjoint union of closed integral-oriented surfaces. Their middle forms are symplectic of rank 2g and hence Witt trivial. This also independently checks the low-dimensional surgery exception explicitly discussed in the early characteristic-two paper. No target dimension is zero.

For every j≥0, RP^(4j+2) is a compact manifold and therefore automatically F-Witt. Its mod-two cohomology ring is F[a]/(a^(4j+3)), and (a^(2j+1))^2=a^(4j+2) evaluates to one. Thus its middle pairing is the one-dimensional form <1>, the nontrivial Witt class. But even-dimensional real projective space is not integral-oriented: the antipodal map on its sphere cover has degree (−1)^(4j+3)=−1. It violates the exact target hypothesis, including RP^2 at j=0.

A zero Witt class does not imply a zero vector space or an alternating bilinear form. Both the hyperbolic plane [[0,1],[1,0]] and I_2 represent zero; I_2 is not alternating and its Lagrangian is span(1,1). The candidate's stronger alternating assertion depends on the separate odd-square operation argument, not the bordism-invariance adapter alone. The present family verifies zero Witt class.

The algebra can be checked without quoting a classification theorem. The map q(v)=b(v,v) is linear over F_2. If a nonsingular form has dimension at least two, ker q contains a nonzero v. Choose w with b(v,w)=1. The plane span(v,w) is nonsingular and metabolic, and split it off orthogonally. Repeating leaves zero or one dimension. Thus the Witt class is exactly rank parity, and <1> is nonzero. The exact control program enumerates every symmetric matrix in dimensions 0–5, verifies the nonsingular count, and constructs and verifies Lagrangians for every nonsingular even-dimensional form (1,4,448 forms in dimensions 0,2,4). It is finite algebra validation, not a computational proof of the universal geometric theorem.

## Remaining gap and first-pass verdict

No gap remains for the original target under its standard closed classical PL convention. This family has not independently reproved the whole Goresky–Pardon surgery theorem or certified every historical priority claim. It has positively identified an exact published theorem and checked its adapter; therefore already_solved is justified as a literature-status correction. No global novelty or priority certificate is asserted.

There is no mathematical correction to the candidate's negative answer. For robust publication, add the normalization and boundary Lagrangian adapters and pin the source manuscript versions. The author-hosted Heidelberg report URL failed during this audit; the official MFO copy supplies the exact question at printed pp.3279–3280, especially p.3280. Replacing or supplementing the inaccessible URL is a provenance correction. The downloaded book is the July 24, 2019 manuscript, even when identified bibliographically with its 2020 published edition.
