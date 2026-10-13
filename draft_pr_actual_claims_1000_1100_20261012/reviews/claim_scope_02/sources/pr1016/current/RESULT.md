# Nonvanishing Euler classes in oriented topological bordism

Problem 30000323 / OWR-1063-006, normal queue rank 1094. Research date: 8 October 2026.

## Result and limits

The general question is **not resolved by this bounded program**. There is no claimed full proof, counterexample, or worldwide-openness certificate.

Two sufficient conditions for nonvanishing are proved below. No novelty is claimed for these elementary consequences of the standard detecting theories. They apply to the exact topological-bordism Euler class:

1. Every character summand has nonzero first Chern class modulo p.
2. There is a cyclic subgroup on which no summand becomes trivial. In particular, this holds for every representation of complex dimension at most p. A stronger sufficient numerical condition is the sum of the reciprocals of the character orders being at most 1.

A concrete (p+1)-dimensional representation of C_(p²) × C_p simultaneously defeats the ordinary-cohomology detector, the K-theory detector, and every proper-subgroup restriction. This is an obstruction to these proof strategies, **not a counterexample in topological bordism**. Its topological-bordism Euler class is not evaluated here.

Five distinct substantive approaches were used; readiness, bibliography checks, source inspection, and verification do not add turns. No inherited same-target substantive attempt was identified in the supplied gate or during this continuation.

## 1. Exact target and source interface

Let p be an odd prime, let G be a finite abelian p-group, and put

    E = MSTOP_(p).

Here MSTOP is the Thom spectrum of stable **oriented topological real bundles**. The complex orientation used throughout is induced by the natural forgetful maps

    MU → MSO → MSTOP → MSTOP_(p).

For a finite-dimensional complex G-representation V, let ξ_V = EG ×_G V → BG. If d = dim_C V, its Euler class means

    e_E(V) = s* u_E(ξ_V) ∈ E^(2d)(BG),

where s is the zero section and u_E is the Thom class induced by this orientation. The question is whether e_E(V) is nonzero whenever V^G = 0. The zero-dimensional case has Euler class 1 and is harmless.

This is Borel cohomology, not the coefficient ring of a genuine equivariant Thom spectrum. It is not unoriented MTOP, the ordinary Euler characteristic, or the unitary-bordism Euler class. Nonvanishing after this p-localization also proves nonvanishing of the corresponding integral MSTOP class. No converse comparison for an arbitrary infinite CW source is needed here.

Hanke's report [1], printed p.2423, asks the Euler-class question after distinguishing ordinary cohomology for elementary abelian groups, unitary bordism for smooth actions, and p-local K-theory for cyclic groups. Hanke–Puppe [2], §§2 and 5, supplies the exact interface: its Euler classes lie in E*(BG); its sensitivity condition is Euler localization; Lemma 5 explicitly identifies the topological-bordism spectrum and Sullivan's map MSTOP_(p) → KU_(p). The report page and the relevant preprint page were visually inspected. The available full paper is arXiv:math/0301279v1; the published metadata are Trans. AMS 358 (2006), 687–702. The publisher PDF was not retrieved (HTTP 403), and no claim of a word-for-word published/preprint comparison is made. The original OWR report is directly available.

At odd p the natural MSPL_(p) → MSTOP_(p) equivalence is available from TOP/PL being 2-primary. Section 6 explains why this does not identify the question with smooth bordism.

### Euler localization and the correct finite reduction

Write G* = Hom(G, S¹). Since G is abelian, V is a sum of characters. Let S contain the Euler classes of all sums of nontrivial characters. It is multiplicatively closed. For any unital ring R, S^(-1)R is zero exactly when 0 belongs to S: the equation 1/1 = 0 holds exactly when some s in S annihilates 1. Consequently, the universal Euler nonvanishing assertion is exactly the G-sensitivity assertion for E.

Define

    Δ_G = ∏_(χ ∈ G*, χ ≠ 1) e_E(χ).

The full assertion for a fixed G is equivalent to Δ_G being **nonnilpotent**. Indeed, if Δ_G^N = 0, the representation containing N copies of every nontrivial character is a counterexample. Conversely, any Euler monomial divides Δ_G^N for sufficiently large N; if that monomial were zero, then Δ_G^N would be zero. Merely proving Δ_G ≠ 0 would not be enough.

## 2. Approach 1: ordinary cohomology and primitive weights

Write

    G = ∏_(i=1)^r C_(p^a_i),    a_i ≥ 1,

and let χ_j have weight vector (b_ji), with b_ji read modulo p^a_i. Let u_i be the reduction modulo p of the integral first Chern class of the standard character on the i-th factor. The periodic resolution of a cyclic group, followed by the field-coefficient Künneth theorem, gives

    H*(BG; F_p) = F_p[u_1,...,u_r] ⊗ Λ(t_1,...,t_r),
    |u_i| = 2, |t_i| = 1.

In particular, the displayed polynomial ring injects. For a cyclic group of order greater than p, u_i is still the reduction of an integral first Chern class; one must not replace it by the mod-p Bockstein of t_i, which can be zero.

The ordinary orientation MSTOP_(p) → HZ_(p) → HF_p carries the canonical Euler class to the ordinary top Chern class. Since c1 is additive under tensor product,

    e_HF_p(V) = ∏_j (Σ_i (b_ji mod p) u_i).

A polynomial ring over a field is an integral domain. Thus this image is nonzero if and only if each displayed linear form is nonzero.

**Proposition 2.1.** If every character summand of V lies outside pG*, then e_E(V) ≠ 0.

Proof. Under the above decomposition, χ_j lies outside pG* exactly when at least one weight b_ji is not divisible by p. Every factor of the ordinary Euler polynomial is then nonzero, hence so is their product. A class with nonzero image under a cohomology transformation cannot be zero. ∎

This recovers every representation with no trivial summand when G is elementary abelian. It also covers many representations of mixed-exponent groups. Equivalently, each summand must remain nontrivial on G[p]. The proposition does **not** cover arbitrary nontrivial characters of order p in a factor C_(p²): such a character has weight p and has zero reduction modulo p.

**Outcome.** A proved sufficient condition. The attempt to extend it to all nontrivial weights fails at p-divisible characters; section 4 exhibits an example where even integral cohomology fails.

## 3. Approach 2: K-theory, cyclic detection, and a dimension bound

We use the cyclic p-group sensitivity established in [2], Lemma 4, and Sullivan's topological K-orientation from Lemma 5. Its multiplicativity is also explicit in [3], p.116, following Corollary 5.25. There is a minor orientation issue worth making explicit. The complex orientation on KU_(p) induced from MSTOP need not be the customary multiplicative coordinate. However, two normalized complex orientations are related on CP^∞ by

    x' = x u(x),    u(0) = 1,

with u an invertible power series. Pulling back this identity to each character line and multiplying shows that the two Euler classes differ by a unit. Their vanishing behavior is therefore identical. This argument takes place first in KU*(CP^∞), where u is genuinely invertible, so it does not assume an unproved convergence of an arbitrary geometric series on BG.

In the customary orientation, up to the invertible Bott factor, the Euler class is the image of

    λ_(-1)(V*) = ∏_j (1 − χ_j^(-1)) ∈ R(G).

The inverse-character convention has no effect on zero versus nonzero.

**Proposition 3.1.** For a finite abelian p-group, the KU_(p) Euler class of V is nonzero if and only if there exists g ∈ G such that χ_j(g) ≠ 1 for every summand χ_j.

Proof. If such g exists, restrict to the cyclic subgroup generated by g. Every restricted summand is nontrivial, and cyclic sensitivity from [2] makes the restricted Euler class nonzero; therefore the original class is nonzero.

Conversely, if no such g exists, then at each element g at least one factor in the character function

    ∏_j (1 − χ_j(g)^(-1))

is zero. The character map R(G) → complex-valued class functions is injective, so λ_(-1)(V*) is already zero in R(G), before passing to K-theory or its completion. The customary K-Euler class is zero, as is the induced-orientation Euler class by the unit argument. ∎

**Corollary 3.2.** If the kernels of the character summands do not cover G, then e_E(V) ≠ 0.

**Corollary 3.3.** If V^G = 0 and dim_C V ≤ p, then e_E(V) ≠ 0.

More generally, if the nontrivial summands have orders o_1,...,o_d and

    Σ_j 1/o_j ≤ 1,

then e_E(V) ≠ 0.

Proof. Put K_j = ker χ_j. For d ≥ 2, all K_j contain the identity, and

    |∪_j K_j| ≤ 1 + Σ_j (|K_j| − 1)
               = 1 + |G| Σ_j 1/o_j − d
               ≤ |G| − d + 1 < |G|.

For d = 1 its kernel is proper; for d = 0 the Euler class is 1. Thus some g lies outside every kernel. In particular, o_j ≥ p gives the claim when d ≤ p. ∎

**Outcome.** A proved quantitative partial result. This strategy is sharp in representation dimension: the example below has dimension p+1 and zero K-Euler class. This means the cyclic detector is sharp, not that the general topological-bordism assertion fails at dimension p+1.

## 4. Approach 3: quotient induction and an essential test representation

Take

    G = C_(p²) × C_p.

Let λ be the standard character of the first factor and β the standard character of the second. Put α = λ^p, a nontrivial character of order p. Consider

    W = α ⊕ ⨁_(a=0)^(p−1) (α^a β).

Every summand is nontrivial, dim_C W = p+1, and W^G = 0. These characters represent the p+1 one-dimensional subspaces of Hom(G, C_p). Their kernels are precisely all maximal subgroups of G.

**Proposition 4.1.** The representation W has the following properties.

(a) Its integral ordinary Euler class is zero.

(b) Its K-theory Euler class is zero already at the representation-ring level.

(c) For every proper subgroup H < G, W|_H has a trivial summand. Consequently, the Euler class of W restricts to zero on BH in every complex-oriented cohomology theory.

Proof. Let u = c1(λ), v = c1(β) in integral cohomology. We have p v = 0. W contains both α and β, so its top Chern class contains the product

    c1(α)c1(β) = p u v = u(p v) = 0.

This proves (a), and also gives vanishing after reduction modulo p.

For (b), write an element of G as (s,t) and reduce s modulo p. If s = 0 modulo p, α(s,t) = 1. Otherwise, there is exactly one a modulo p satisfying a s + t = 0 modulo p, and α^a β takes the value 1. Hence no group element avoids all the character kernels. The converse part of Proposition 3.1 proves the assertion in R(G).

For (c), every proper subgroup is contained in a maximal subgroup. All maximal subgroups have index p and are kernels of nonzero homomorphisms G → C_p, up to a nonzero scalar. The chosen characters represent all those kernels. Thus one summand is trivial on H. The Euler class of a direct sum with a trivial complex line is zero, by the zero-section definition and the Whitney product formula. ∎

This defeats an attempted induction that detects e_E(V) solely by restrictions to smaller groups: even a nonzero Euler class could be invisible to the entire proper-subgroup family. The source's unitary-bordism sensitivity theorem supplies exactly this phenomenon for W in MU, so absence of subgroup detections is not a vanishing proof.

There is also an important limitation on transfer-based repairs. In a generalized multiplicative cohomology theory the projection formula reads

    tr_H^G(res_H^G z) = z · tr_H^G(1).

It is not valid to replace tr_H^G(1) by the integer [G:H] without further proof. In K-theory, tr_H^G(1) is the induced permutation representation Ind_H^G(1). For an index-p subgroup H, its character is p on H and 0 off H, whereas the character of p copies of the trivial representation is p everywhere. Thus they differ. In particular, zero restriction of e_E(W) does not by this argument imply p e_E(W) = 0.

**Outcome.** A fully proved, dimension-sharp obstruction to the two detector methods and to naive restriction induction. The sought Euler class e_E(W) remains unevaluated. No vanishing conclusion in MSTOP follows.

## 5. Approach 4: direct formal-group elimination

Let F be the formal group law of the canonical E orientation. On the classifying space above put

    x = e_E(λ),    y = e_E(β),    z = [p]_F(x).

The tensor-product and Whitney identities give the exact formula

    e_E(W) = P_F(x,y)
           = [p]_F(x) ∏_(a=0)^(p−1) F([a]_F([p]_F(x)), y),

with exact relations

    [p²]_F(x) = 0,    [p]_F(y) = 0.

This displays the mixed-exponent obstruction concretely. W is pulled back from a representation of G/pG ≅ C_p × C_p, but the map on cohomology sends one quotient Euler coordinate to [p]_F(x). Nonvanishing in the elementary-abelian quotient does not imply nonvanishing of its inflation.

For clarity, the standard classifying map BG → (CP^∞)² gives a homomorphism

    A = E*[[X,Y]] / ([p²]_F(X), [p]_F(Y)) → E*(BG).

The formula above is the image of its indicated formal expression. **No assertion is made here that this homomorphism is injective, surjective, or a presentation of E*(BG).** Such an assertion would need an exact Gysin/Künneth argument with the actual MSTOP coefficient groups and all relevant completion and derived terms. Complex orientability by itself is not a proof of that presentation.

Under the additive ordinary orientation the expression vanishes by Proposition 4.1(a). Under the multiplicative K orientation it vanishes by Proposition 4.1(b), even before completion. Thus neither specialization can certify its nonvanishing in E, and their joint vanishing cannot certify its vanishing there. As negative controls, the corresponding projective-line representation of C_p × C_p has zero K-Euler class but nonzero ordinary Euler class, while repeated weight-p characters of C_(p²) can have zero mod-p Euler class and nonzero K-Euler class.

The direct elimination attempt does not produce either a zero relation for P_F in E*(BG) or a detecting homomorphism on which P_F is nonzero. For the universal problem, even a computation showing this one expression nonzero would need to be extended to all powers of the full Euler product Δ_G.

**Outcome.** An exact expression and an explicit, unresolved ring-theoretic interface. Treating MU coefficients as MSTOP coefficients, assuming an underived quotient formula, or inferring zero from two zero specializations would leave a gap.

## 6. Approach 5: Sullivan's splitting and smooth-bordism comparison

A potentially stronger route is to transport unitary/smooth detection across the odd-prime structure of topological bordism. This leads to a specific source that was followed rather than assumed: Madsen–Milgram [3], Chapter 5.D, Lemma 5.19 and Corollary 5.20, gives

    MSPL_(p) ≃ MSO_(p) ∧ McokJ_p.

Here the MSO factor is constructed from the map γ_p : BSO_(p) → BSPL_(p) of §5.B (5.11). Chapter 11.B explicitly calls γ_p exotic and identifies its Thom map as the map in this decomposition. Theorem 11.22 (=5.21) is an isomorphism on homotopy groups modulo torsion for that map.

The attempted proof would require a detector compatible with the **natural** complex orientation MU → MSO → MSPL → MSTOP, or an injectivity statement for its Euler monomials on BG. Neither the spectrum equivalence nor the isomorphism modulo torsion gives that statement:

- A smash-product decomposition is not automatically an orientation-preserving ring retraction to MSO or MU.
- The map governing the decomposition is γ_p, in general an exotic map, not a stipulated identification with the natural bundle-forgetting map.
- An isomorphism modulo torsion on coefficient homotopy groups does not by itself imply injectivity on the cohomology of BG or on its completed Euler classes.
- The group-dependent Euler products in question can be invisible to rational information, so a rational equivalence or torsion-free coefficient calculation is insufficient.

No compatible ring detector or required injectivity statement was constructed. In particular, the cited splitting must not be advertised as a solution to the Hanke question. This is a limitation of the attempted proof, not a claim that no such comparison could exist.

**Outcome.** The new source lead is resolved as a genuine but insufficient structural theorem. The canonical Euler-class comparison remains missing.

## 7. Verification, remaining obstruction, and stopping point

The proofs in §§2–4 are mathematical arguments. The accompanying standard-library Python checks verify only finite-group and exact-algebra ingredients:

- exact enumeration of character kernels;
- exact convolution in the integral character group ring, without numerical roots of unity;
- the projective-line obstruction for several odd primes;
- exhaustive small cases of the cyclic-avoidance dimension bound;
- negative controls obtained by removing a character, using elementary-abelian weights, inserting a trivial character, and comparing induction with scalar multiplication.

The same checks are run with normal Python, -O, and -OO. They use explicit exceptions instead of Python assert statements. They do not compute MSTOP cohomology, decide the value of e_E(W), establish convergence of a spectral sequence, or replace any topological argument.

The precise unresolved question is still whether every nontrivial-character Euler monomial survives in MSTOP_(p)*(BG), equivalently whether Δ_G is nonnilpotent for every finite abelian odd-p group. Already the explicit class P_F(x,y) for W over C_(p²) × C_p is not settled by this work. Its ordinary and K-theory images vanish, and all its proper-subgroup restrictions vanish. A successful continuation needs information about the canonical MSTOP orientation that those detectors do not retain, or a genuine topological vanishing relation. No full candidate is offered for acceptance as a solution.

Five approaches are exhausted. This packet can be independently audited for the partial lemmas and the exact source interface; it should not be marked as a solved problem.

## References

[1] B. Hanke (joint work with V. Puppe), “Equivariant Gysin maps and pulling back fixed points,” in *Cohomology of Finite Groups: Interactions and Applications*, Oberwolfach Reports 42/2005, printed pp.2423–2424. DOI: 10.4171/OWR/2005/42. https://ems.press/content/serial-article-files/46013

[2] B. Hanke and V. Puppe, *Equivariant Gysin maps and pulling back fixed points*, Transactions of the American Mathematical Society 358 (2006), 687–702. DOI: 10.1090/S0002-9947-05-03634-2. Full inspected author preprint: https://arxiv.org/abs/math/0301279 and https://arxiv.org/pdf/math/0301279. Relevant preprint locations: §§2 and 5, especially pp.3–5 and 11–12, Lemmas 3–5.

[3] I. Madsen and R. J. Milgram, *The Classifying Spaces for Surgery and Cobordism of Manifolds*, Annals of Mathematics Studies 92, Princeton University Press, 1979. Relevant printed locations: pp.99–105, 113–116, 219–220, especially (5.11), Theorem 5.12, Lemma 5.19, Corollary 5.20, and Theorem 11.22. Public scholarly copy: https://webhomes.maths.ed.ac.uk/~v1ranick/papers/madmil.pdf

[4] T. tom Dieck, *Kobordismentheorie klassifizierender Räume und Transformationsgruppen*, Mathematische Zeitschrift 126 (1972), 31–39. This is the unitary-bordism sensitivity result cited in [2]; its original proof was not re-audited in this continuation. The partial nonvanishing proofs above use the explicit cyclic argument of [2], not a new claim about genuine equivariant bordism.
