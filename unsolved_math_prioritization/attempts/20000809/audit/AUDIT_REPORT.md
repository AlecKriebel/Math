# Independent adversarial audit: smooth Borel points and Hilbert rationality

Problem 20000809 / AIM-ARITHMETIC_GEOMETRY-0055, rank 758.
Audit date: 2026-10-05.

## Verdict: PASS, with the author's stated partial scope

**PASS_SCOPED_PARTIAL. No substantive correction to the frozen mathematical packet is required.** This verdict accepts the finite-length theorem, the counterexample to universal tangent attraction, the tangent-space correction, and the conditional BB/Gordan discussion. It does **not** certify a solution or counterexample to the general projective AIM question. The correct general disposition remains **unresolved here; five approach families examined (5/5)**.

The author freeze was preserved. Its ZIP has 25,472 bytes and SHA-256 `bc287ca76f266fbd06b5a9149c57b2da3e2ec0b822b94c554efe8b6867953a8c`. Its manifest SHA-256 is `95f814667e4dd6b68199ab9d69fc38e521b86e20ab111fa9562150fc39cb2a24`. Every ZIP member equals its corresponding authored file, every author manifest entry matches, and all 116 author assertions replay byte for byte.

The separate verifier in this audit passes **310 assertions**, uses no author implementation, and agrees with every author-reported affine and untruncated tangent character and multiplicity. It adds multiplication-commutator, Macaulay-neighbor, symbolic-flatness, characteristic-two, and interpolation controls.

This is an independent AI mathematical/code audit, not human peer review, formal proof certification, or exhaustive literature review.

## 1. Source identity and the actual question

The original [AIM workshop list](https://aimath.org/WWN/hilbertschemes/hilbertschemes.pdf), page 2, Problem 8, asks whether rationality follows from the presence of a smooth Borel-fixed Hilbert point. It gives no explicit field, characteristic, ambient dimension, or Hilbert polynomial in that item. Page 1 discusses both affine points and projective curves and defines components to be irreducible. The packet correctly treats the broader projective scope as an interpretation, not text explicitly specified by Problem 8.

The catalog title describes the supplied earlier partial tangent-weight argument. The complete earlier report was inspected; its unconditional projective homogeneous-Hom formula and proposed universal half-space implication need correction, and the frozen author packet supplies those corrections. Its retained BB implication was already present and is standard; no new-solution credit should attach to it.

All three supplied complete corpus byte counts and hashes were independently recomputed, together with the target problem and research-report canonical fingerprints. The target statement matches the catalog's stated hash and the target rank is 758. The catalog review hash was matched as metadata but not reconstructed from an unknown original serialization. `input_integrity.json` records these distinctions without including corpus text or records.

## 2. Distraction, flatness, and finite-length rationality

### 2.1 The free-family argument is valid

The leading x-monomial of each distracted generator is the original monomial, with coefficient one over k[t]. Reduction decreases x-degree and therefore terminates over that coefficient ring. The d standard monomials span the quotient. At the generic point of Spec k[t], the d displayed grid points are pairwise distinct and satisfy every generator: a forbidden exponent cannot be coordinatewise below a standard exponent. The quotient therefore has dimension at least d, and hence exactly d.

The remaining flatness step is sound, including its direction: the kernel of the spanning map k[t]^d to the quotient is a submodule of a torsion-free module. Generic vanishing of that kernel forces the kernel itself to vanish. Thus the quotient is free, not merely of constant generic rank. At each nonzero t, the same d-point argument proves that the fiber is precisely the radical ideal of those points. At zero, the specialized generators are precisely the original monomial generators.

No division by a factorial or by the characteristic occurs. The scalar sequences need to be distinct in the actual field. Algebraically closed fields of every characteristic satisfy that requirement; recycling integers modulo a small prime would not. The independent finite controls explicitly distinguish these situations.

The classical attribution is correct: [Cartwright--Erman--Velasco--Viray, *Hilbert schemes of 8 points*](https://pi.math.cornell.edu/~mike/7670-fa20/references/cartwright-et-al-hilbert-schemes-8-points-2009.pdf), published Proposition 4.15, proves monomial smoothability in arbitrary characteristic. The supplied published PDF was hashed; the proposition was independently re-extracted and its supplied rendered page inspected. The packet correctly avoids the preprint's different numbering.

### 2.2 The interpolation chart really is affine space

The locus where 1,x_1,...,x_1^(d-1) is a quotient basis is open by the determinant condition on the universal rank-d quotient. For every base algebra, the single monic relation for x_1 and the degree-<d expressions for the remaining coordinates give the entire kernel. Conversely, the displayed ideal gives that free basis. Thus the functorial equivalence is an isomorphism to affine nd-space, not just a pointwise bijection or an unspecified unirational parameterization.

The discriminant-nonzero subset is nonempty over the stated fields and dense in this affine space. Its points are reduced configurations with separate first coordinates. The full distinct-point locus is irreducible and smooth of dimension nd. Its closure is therefore an irreducible component; the chart lies in it and is dense. The symmetric-group quotient introduces no rationality assumption into this argument. The component is rational because an actual dense affine-space chart has been exhibited.

The open immersion Hilb^d(A^n) into Hilb^d(P^n), obtained by requiring support to avoid a fixed hyperplane, transfers this chart to the projective smoothable component. A finite family whose fibers lie in that chart remains a legitimate projective Hilbert family.

### 2.3 Smoothness identifies the unique component

A smooth local ring is regular and a domain, so a whole-Hilbert-scheme smooth point lies on exactly one irreducible component. Since every finite-colength monomial point lies on the smoothable component, its unique component must be that rational component. No inference from an arbitrary regular local chart to rationality is being made.

For a saturated strongly stable projective ideal with constant polynomial, a minimal generator divisible by the last variable would, by strong stability and saturation, have a proper divisor in the ideal. Thus the ideal is extended from the other variables. Its constant eventual Hilbert function forces a finite standard staircase, and its support lies in the stated affine chart. This justifies the project's characteristic-zero Borel specialization. The proof does not use a false positive-characteristic equivalence between Borel fixation and strong stability.

**Accepted scope:** every finite colength monomial ideal in every affine dimension, with whole-scheme smoothness at the Hilbert point; and the projective constant-polynomial Borel case under the stated characteristic-zero convention. Positive-dimensional projective schemes are not covered by this finite grid proof.

## 3. The odd-length example, tangent maps, and smoothness

For I_m=(x^2,xy^m,y^(m+1)), the quotient basis contains m+1 pure y-powers and m x-multiples, so its length is 2m+1. The extension to k[x,y,z] is saturated because multiplication by z is injective. Strong stability is immediate from the generator moves and extends to all ideal monomials. These verifications use the declared variable order.

The two adjacent syzygies generate the relation module; the third pair syzygy is y times the first plus x times the second. Their equations impose m+1 and then m independent coefficient conditions. Hence the affine tangent dimension is 4m+2. Smoothability supplies a component of exactly that dimension through the point, so equality between local dimension and embedding dimension proves regularity of the entire local Hilbert scheme. The argument does not assume irreducibility of the whole Hilbert scheme to establish smoothness.

The maps x^2 to xy^2 and y^(m+1) to xy^(m-1), with other generator images zero, respect both syzygies and are nonzero exactly in the stated m>=3 range. Their affine characters are (-1,2) and (1,-2). Lifting to the character lattice of the full effective diagonal projective torus gives (-1,2,-1) and (1,-2,1). Their sum is zero, so no cocharacter has strictly same-sign pairings with the entire tangent representation.

The saturation, length, smoothness, full-torus interpretation, and lack of attraction all pass. This example lies on a rational component, so it only disproves the stronger attraction proposal. It is not an irrational-component counterexample.

The attribution is accurate. [Cioffi--Lella--Marinari--Roggero](https://arxiv.org/abs/1003.2951) give the length-seven example and the odd-length family in Example 3.15(1) and Proposition 3.16. Their example cites Conca--Sidman. In [Conca--Sidman's Example 5.8](https://arxiv.org/abs/math/0402418), the relevant nonsegment ideal has the audited ideal as its saturation. The frozen packet does not falsely identify the literal unsaturated presentation there with J_3 or claim a new family.

## 4. The projective tangent correction is essential and correct

The projective tangent object is sheaf Hom. Computing untruncated degree-zero module Hom can remove deformations that change the low-degree Hilbert function while preserving the Hilbert polynomial.

At J_3, sheaf Hom agrees with the affine chart calculation and has dimension 14. Degree-zero Hom for the original homogeneous generators only permits five images of the quadratic generator, instead of seven, while the quartic generators still have seven. The same seven independent equations remain. Thus its dimension is 12. The missing characters are precisely (-1,2) and (-2,3), corresponding to x^2 mapping to xy^2 and y^3.

The character (3,2) pairs negatively with every retained weight, positively with the first missing weight, and trivially with the second. The author's claimed false-positive attraction test is therefore an actual numerical failure, not merely a dimension mismatch.

Independent commutator linearization gives:

- Full border system: 35 coefficient variables, rank 21, tangent dimension 14
- Degree-filtered border system: 33 coefficient variables, rank 21, dimension 12
- Homogeneous truncation degree 4: 56 variables, rank 42, dimension 14
- Degree 5: 98 variables, rank 84, dimension 14
- Degree 7: 203 variables, rank 189, dimension 14
- Degree 10: 413 variables, rank 399, dimension 14

All full weight multiplicities agree, not just dimensions. For the high-truncation computation, the independent implementation uses adjacent degree-(r+1) multiplication equations rather than the author's Taylor-pair code. It verifies in each relevant LCM multidegree that those neighbor relations generate all pair syzygies: dividing heads form a connected graph under degree-(r+1) edges. A path telescopes to the desired pair syzygy. This eliminates an unverified linear-presentation assumption from the finite computation.

These degree bounds are verified for this example. They should not be advertised as universal sufficient bounds for arbitrary projective ideals.

## 5. BB/Gordan and the double-generic distinction

The BB argument applies on the invariant smooth locus. A singular point cannot flow into a smooth point because the nonsmooth locus is invariant and closed. Strict tangent positivity makes the fixed point isolated for that cocharacter. The smooth attracting fiber is affine space and has the full component dimension, so its locally closed image is dense and open in the unique component. [Jelisiejew--Sienkiewicz, Theorem 1.5](https://arxiv.org/abs/1805.11558) supplies the needed smooth fiber and locally closed immersion statement. The rational separation argument for integral weights is also valid. Neither argument supplies strict positivity from smooth Borel fixation.

[Bertone--Cioffi--Roggero, Theorem 6.10](https://arxiv.org/abs/1503.03768) requires a smooth distinguished double-generic point on the isolated component. Corollary 6.11 supplies the stated ACM codimension-two case. The author has preserved these hypotheses rather than replacing the distinguished point with an arbitrary Borel point.

The quadratic Hilbert-function comparison excludes J_3 as a general saturated generic initial ideal when the initial ideal remains saturated. For the stronger high-truncation assertion, the proof has an independent route: if J_3 were the double-generic point, its associated Groebner stratum would contain a dense open neighborhood of it in the component. There are only finitely many degree-r head-tail comparisons in the Hilbert embedding; a single integral cocharacter realizes all their strict term-order inequalities. Every tangent character of that stratum then has one strict sign. Whole-scheme smoothness and openness identify this tangent with the full Hilbert tangent. The opposite characters contradict that conclusion. This reasoning justifies the compressed statement in PROOFS section 5 without assuming that saturation preserves low-degree Hilbert functions.

## 6. Independent controls and adversarial alternatives

`independent_verify.py` uses exact standard-library arithmetic and is independent of the author script. It reconstructs border multiplication operators with a fixed monomial quotient basis and linearizes their commutators. Commuting operators with the cyclic vector 1 recover the quotient algebra; the fixed monomial basis removes basis-change ambiguity. Weight-separated linear algebra then computes the full tangent representation.

Its 310 assertions include:

- Full and degree-filtered tangent characters and all multiplicities
- Four truncations, with independent syzygy-completeness graph checks
- Odd-family samples m=3,...,16, with dimension 4m+2 and the opposite pair
- All 13 strongly stable plane staircases of lengths at most six, enumerated through ordinary partitions and an independent stability filter
- Equal-product nonsegment certificates at degrees 4, 7, 11, and 30
- Symbolic Q[t] distraction S-pair reductions in ambient dimensions 1 through 4, specialization checks, and invertible evaluation matrices
- A seven-point distraction over GF(4), verifying characteristic-two vanishing and evaluation rank seven
- Exact Lagrange interpolation and monic polynomial recovery, plus an independent nonzero quadratic evaluation determinant
- Eight rejected false alternatives, including the m=2 boundary, untruncated tangent substitution, sign-flip repair, universal smooth-Borel attraction, generic quadratic Hilbert function, repeated small-field scalars, positive-characteristic strong stability, and omitted syzygies

These are supplementary finite controls. The general finite-length theorem rests on the proof, and no finite calculation settles the general projective question.

## 7. Scope of literature verification and non-blocking improvements

All 13 supplied source PDF hashes and byte counts were independently recomputed. The AIM original was re-read through the web tool. The arXiv records and relevant theorem statements were checked to the scopes recorded in `source_verification.json`. The audit did not independently redo the full irrationality proofs or run the 2025 paper's ancillary algebra code.

The current [Farkas--Pandharipande--Sammartano record](https://arxiv.org/abs/2405.11997) lists the August 2026 v3 and its forthcoming journal status. [Wu's June 2026 preprint](https://arxiv.org/abs/2606.30386) states the dimension-ten improvement. These remain distinct evidence levels. Neither supplies the required smooth monomial point: the independently accepted finite-length theorem rules that out for any genuinely irrational component. This exclusion does not rely on certifying either construction.

No mandatory mathematical revision was found. Two optional hardening improvements are worth preserving in downstream packaging:

1. The author's inventory verifier checks only top-level files. The frozen ZIP itself has been checked exhaustively and contains exactly its nine intended members, so this does not invalidate this freeze. A future packager should reject undeclared nested files as well. The audit's own packet verifier does so.
2. The high-degree double-generic exclusion can be expanded by the finite-comparison cocharacter argument above if a standalone presentation needs more exposition. Its present conclusion is justified.

The author's historical repository search observations were not independently repeated. This audit makes no current-remote-state claim, no historical-absence claim, no new priority claim, and no globally exhaustive assertion that the general question is still open. No remote writes were made.

## 8. Reproduction and safe inventory

Run `python3 -B independent_verify.py` and compare stdout with `independent_verification.json`, or run `python3 -B verify_audit.py` for the recursive audit inventory and deterministic replay. These work from arbitrary current directories and require neither author files nor external sources.

The audit directory contains only authored analysis, verifier code, deterministic results, and verification metadata. It contains no source PDF, source excerpt, rendered source image, raw dataset record, or private coordination material. The author freeze is unchanged. See `MANIFEST.json` for the exact audit inventory and hashes.
