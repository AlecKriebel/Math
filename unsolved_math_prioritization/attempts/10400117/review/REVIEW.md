# Independent source audit: Ohtsuki Problem 7.2

**Verdict: PASS_CREDITED_KNOWN_WITNESS.** The literal existence request is already answered by the example in its immediately following primary-source remark. Recommended status: **already_solved, 0/5 proof-search approaches**. No mandatory correction is required. This is a source and application audit, not a new quantum computation, a novelty claim, or human peer review.

The frozen `SOURCE_STATUS.md` has SHA-256 `65bbb3d8a2dadffc80524133d7d2b7ebf2580a64a48b7d5cded96bb9f573dc42`. All 112 submitted controls reproduce byte for byte; 2,331 separate exact controls pass.

## 1. The original request and the omitted answer

I inspected the rendered original printed p.472 and its preceding quantum-invariant conventions on p.471. Problem 7.2 asks for non-homeomorphic rational homology three-spheres with equal LMO invariants but different quantum G or projective-G invariants for some allowed level and some simply connected compact simple Lie group. The same proposers, Hansen and Takata, immediately name L(25,4) and L(25,9), state that their LMO invariants agree, and state that their quantum SU(2) invariants at r=5 differ. Thus this package accurately restores information omitted from the imported question. [Original primary collection, pp.471–472](https://msp.org/gtm/2002/04/gtm-2002-04-024s.pdf).

The wording can historically motivate further examples. It does not specify that a witness must be new, classify every pair, or work for every level or every group. The recommended status refers only to its literal existential request. It does not settle adjacent Problem 7.3 about separating all rational homology spheres.

## 2. Lens-space hypotheses

Both parameters are coprime to 25. The standard lens-space computation gives H1=Z/25; together with orientability and closed three-manifold duality this gives rational homology spheres. The unoriented homeomorphism orbit of 4 modulo 25 under inversion and sign is {4,6,19,21}; the corresponding orbit of 9 is {9,11,14,16}. These are disjoint. They are therefore not homeomorphic even after allowing orientation reversal. Bar-Natan–Lawrence's Corollary 5.2 independently states non-homeomorphism for precisely this pair.

## 3. Equality is for the entire LMO invariant

I checked the formula and proof of Proposition 5.1 and the rendered Corollary 5.2 in Bar-Natan–Lawrence. The convention takes L(p,q) to be p/q surgery on the unknot, and gives

\[
\widehat Z^{\rm LMO}(L(p,q))
=\langle\Omega_x,\Omega_x^{-1}\Omega_{x/p}\rangle_x
\exp\!\left(-\frac{S(q/p)}{48}\theta\right).
\]

The entire first factor depends only on p; it is not a finite-degree approximation. Definition 1.5 normalizes S(a/b)=12s(a,b) for positive b. The proposition's proof reduces the rational-surgery expression to this formula using exactly that Dedekind reciprocity identity. For the two witnesses,

\[
s(4,25)=s(9,25)=4/25,\qquad S(4/25)=S(9/25)=48/25.
\]

Hence the complete graph-valued invariants agree. Merely matching the theta coefficient would be insufficient without this formula; here the p-dependent factor also agrees. A shared normalization depending on the first-homology order preserves equality. The candidate does not claim invariance under arbitrary manifold-dependent renormalizations. [Primary rational-surgery paper, Definition 1.5, Proposition 5.1 and Corollary 5.2](https://www.math.toronto.edu/drorbn/papers/RationalSurgery/RationalSurgery.pdf).

## 4. Quantum separation and normalization limits

The exact separation at r=5 is a credited statement of Hansen–Takata in the original source, using the very invariant conventions of the question. For SU(2), h-dual=2, so r=k+2 and the allowed value r=5 corresponds to k=3. The original p.471 permits SU(2) levels r at least three. SU(2) meets the group hypotheses.

I also inspected Freed–Gompf's discussion on p.100 and rendered Table 3 on p.102. The k=3 entries for this pair are visibly different complex numbers. Their discussion observes equal magnitudes in the computed range. This is consistent with the target: Problem 7.2 asks for different complex values, and has no unequal-magnitude or nonvanishing prerequisite. Rounded table entries are corroboration only. They are neither the exact certificate nor an identification of every framing and scalar normalization with a newly evaluated tau-5 formula. The candidate correctly relies on the exact level-specific statement in the original Hansen–Takata remark, and explicitly disclaims a quantum recomputation. [Freed–Gompf primary paper, pp.100–102](https://webhomes.maths.ed.ac.uk/~v1ranick/papers/freedgompf.pdf).

This review validates that source dependence and its application. It does not independently certify a cyclotomic evaluation of either quantum invariant. That limitation is compatible with an already-known-source disposition and must remain visible in publication.

## 5. Independent checks and distinction from Problem 7.5

The submitted program's 112 exact assertions were replayed without changing the frozen receipt. The independent checker computes Dedekind symbols by Euclidean reciprocity, then compares them with an integer residue-sum formula over all 773 coprime positive pairs with denominator at most 50. It also checks orientation signs, inversion symmetry, the witness homeomorphism orbits, and the integer SL2 products for negative continued fractions [7,2,2,2] and [3,5,2]. Its 2,331 assertions are finite algebraic controls, not quantum-invariant evaluations.

Reproduction:

```
python author_replay/verify.py
python independent_checks.py
```

The earlier SU(5) campaign example concerns Conjecture 7.5, comparison of absolute values under equality of fundamental groups. It uses different lens spaces and does not establish LMO equality. Neither its computation nor its stronger magnitude inequality is needed here. The present disposition credits the original SU(2) witness and the Bar-Natan–Lawrence full-LMO formula. No new example or solution is claimed.
