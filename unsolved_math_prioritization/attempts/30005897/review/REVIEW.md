# Independent audit: shadowing without bounded distortion

**Target:** 30005897 / OWR-14298367-003
**Reviewed:** 2026-09-30 UTC
**Reviewer:** independent gpt-6-astra execution, xhigh
**Snapshot:** `reviewed_proof.md`, SHA-256 `7aa1189fc74b7b5fcd38435db8820e551bc0671f1ee580c37d676e04ef40b53b`

## Verdict

**PASS on the mathematical argument and exact target.** The candidate proves that a bounded invertible dissipative composition operator in the source's finite-wandering-set setting has shadowing if and only if it is generalized hyperbolic, for every 1≤p<∞, over either scalar field. I found no missing hypothesis or defective step in the quantitative dual estimate, localization, measurable splitting, passage from a power to the operator, or converse. The p=1 endpoint is valid.

**Novelty is not certified.** The separable complex p=2 case is already covered by Pituk's 2026 theorem. The scalar aggregate-mass characterization is already refuted in the July 2026 Example 6.2 and must receive no new-discovery credit. The shift-coordinate realization also has explicit 2024 prior art, identified below. The full all-p band-splitting statement was not located in the checked literature. Retain qualified historical-priority language.

No mandatory mathematical repair was found. Add the 2024 shift-coordinate attribution before public presentation; the author has agreed to do so. This is an independent AI proof audit, not formal verification or journal refereeing.

## 1. Exact source scope

The requested problem page was attempted first and was inaccessible. The full pinned dataset record and original OWR source were then checked.

The 2024 report assumes a sigma-finite measure space, a bijective bimeasurable f, and measure-growth bounds for f and f^{-1}. It defines dissipativity using a wandering set W of finite positive measure whose integer translates partition X. It uses two-sided pseudotrajectories, and defines generalized hyperbolicity using closed complementary subspaces, one forward invariant and the other backward invariant, with the respective spectra inside the unit disk. These are the hypotheses and conventions in candidate (1.1)–(1.3). Allowing partition identities modulo null sets is harmless because the hypotheses preserve null sets in both directions.

The printed Open Problem (1), p. 1080, asks two distinct questions: survival of the earlier characterization, and equivalence with generalized hyperbolicity. The candidate correctly separates them. It is not proving generalized hyperbolicity versus shadowing for arbitrary Banach operators, nor addressing conservative systems or the structural-stability question numbered (2).

Primary sources: [OWR 19/2024](https://doi.org/10.4171/OWR/2024/19), pp. 1078–1081; [D'Aniello–Darji–Maiuriello](https://arxiv.org/abs/2009.11526), Definitions 2.3.2, 2.5.1, 2.6.3 and Problem 5.0.1.

## 2. Shadowing to quantitative dual expansion

### Bounded forcing

The scaling argument in Lemma 2.1 is valid because two-sided pseudotrajectories are not required to be bounded. Given bounded forcing, a bi-infinite sequence satisfying x_{j+1}=Ax_j+b_j exists by forward and backward recursion. Scaling its errors below a shadowing tolerance and subtracting the shadowing orbit yields a bounded solution with a uniform constant K. Strict versus weak tolerance conventions are handled by choosing a smaller scale. No linear selection of solutions is required.

### Dual inequality

For a finitely supported dual sequence, choose primal unit-ball vectors which approximately norm each individual functional. This is valid even if the dual norm is not attained, and works over C by controlling real parts. Applying the bounded-forcing estimate and shifting a finite sum gives

\[
 \sum_j\|u_j\|\le K\sum_j\|u_{j-1}-A^*u_j\|.
\]

I independently checked the endpoints in the candidate's special substitution. With u_j=S^{-j}u supported on -b≤j≤-a, the two nonzero residuals are -S^{b+1}u at index -b and S^a u at index -a+1. Hence

\[
 \sum_{k=a}^b\|S^ku\|\le K(\|S^au\|+\|S^{b+1}u\|)
\]

has the correct indexing. Applying it on [-j,j−1] includes the term ||u||. If both endpoint norms at ±d are at most 2||u||, summing those lower bounds for 1≤j≤d−1 contradicts the upper bound on [-d,d−1] when d>4K²+1. Thus the uniform dual expansion constant used later is proved, rather than imported from an uninspected 2026 theorem.

This part does not require reflexivity, separability, a right inverse for the forcing operator, or a complemented dual kernel. Those are common hidden pitfalls which the proof avoids.

## 3. Orbit coordinates and p=1 localization

For every integer n, the measure A↦μ(f^nA) on W is finite and mutually absolutely continuous with ν=μ|_W. This follows from (1.1), iterated in either direction. Hence rho_n is positive and finite almost everywhere. There are countably many n, so versions can be chosen simultaneously outside one ν-null set. The weights and all support-band predicates are measurable functions of these countably many densities.

The map U in (3.1) is an onto isometry: the norm identity is precisely change of variables for ν_n, summed over the disjoint orbit levels. Its inverse is obtained level by level and is measurable because f^n and f^{-n} are measurable. The countable union of images of the removed ν-null set is μ-null. If the partition was given only modulo null sets, removing its countable f-saturation first gives an invariant conull domain. No measurable choice of orbit representatives beyond the already assumed W is being made.

The conjugated shift is backward, with coefficient (rho_n/rho_{n+1})^{1/p} at output n. Its adjoint is the forward shift with the same positive weights. I checked the d-step products telescope to the factors in (3.4), including the inverse direction.

At p=1, the dual is the scalar L∞ space on the sigma-finite product measure. The indicator of any positive-measure subset of W, placed in a single coordinate, is a nonzero dual vector of norm one. For 1<p<∞ the same indicator belongs to Lq because ν(W)<∞. Thus the localization proof covers the endpoint without any L∞-dual or reflexivity assumption.

If both factors are below 2 on a positive-measure set, that set is a countable union of sets where both are at most 2−1/k; one has positive measure. Testing its indicator contradicts uniform dual expansion. Therefore at least one factor is at least 2 almost everywhere. Taking the union of exceptional null sets over all n gives a **single** conull set for the claimed pointwise density condition. The proof does not interchange an uncountable family of null sets or confuse fiberwise and operator-uniform constants.

## 4. Density condition to a d-step splitting

Let A0 contain the coordinates with a left d-step density drop. If such a coordinate were followed d steps to the left by a point without a left drop, the min-condition there would impose the opposite density inequality; multiplying gives 1≤eta², impossible. Thus A0 propagates left. Its complement C0 propagates right by the corresponding argument. Equality cases remain valid since 0<eta<1.

This yields the density ratios eta^m in the correct directions. Changing the coordinate index in the Lp norm of B^{md} gives rho_{n-md}/rho_n, not its reciprocal. The claimed restrictions are consequently contractions at rate eta^{m/p}. This rate is uniform in w, n, and m. Both subspaces are support bands and therefore closed and complementary without any abstract complementability theorem.

I tested the reverse geometry as an adversarial case: a density valley such as 2^{|n|} fails the condition at its minimum. A density peak such as 2^{-|n|} satisfies it and gives the expected generalized splitting. This confirms the directionality.

## 5. Passing from B^d to B

This is the most delicate structural step, and it is correct specifically because B is a weighted coordinate permutation.

The support of B^jM0 is the j-fold left translate of the support of M0. An invertible map takes finite intersections to the intersection of its images. Therefore B maps the intersection M into itself, using B^dM0⊂M0. Complementation commutes with this permutation of supports, so the complementary band N is the band on the finite union of the supports of B^jN0. It is invariant under B^{-1}.

On each B^jN0, commuting powers of B transfer the inverse d-step estimate with the finite condition-number factor ||B^j||||B^{-j}||. A vector in the union band can be partitioned measurably into finitely many pieces with disjoint supports, each lying in one such translated band. The images under B^{-md} remain disjoint. Adding p-th powers of norms thus preserves a single uniform factor D; the proof does not incorrectly assume projections commute with B or incur an uncontrolled factor depending on the fiber.

For p=1, the same computation is simply additivity of the L1 norm on disjoint supports. For arbitrary time k=md+r, boundedness of the finitely many remainder powers gives exponential decay. The displayed spectral-radius upper bound eta^{1/(pd)} follows by taking k-th roots. Empty bands are allowed and cause no issue.

This argument would not justify an assertion about arbitrary generalized-hyperbolic splittings of powers on arbitrary Banach spaces. The candidate explicitly supplies the additional support-band mechanism, so that possible general obstruction is avoided.

## 6. Converse

The two Green series converge absolutely and uniformly under the restriction estimates. I checked the cancellation separately in the stable and unstable sums: the stable difference gives Pb_n, and the unstable difference gives Qb_n. Commutation of P or Q with T is unnecessary. The positive powers are only applied to M and negative powers to N when estimating convergence, exactly the invariant directions available.

Subtracting this bounded correction from any pseudotrajectory leaves an exact two-sided orbit. Scaling the error tolerance gives shadowing. There is no issue at p=1 or over real scalars, and no new spectral theorem is used.

## 7. Computation and a separate non-bounded-distortion control

I read and ran the author's `verify.py`. It passed 84 band models, 55,572 exact density comparisons, 1,211 admissible local sequences, 30 dual telescoping tests, a 31-time-index Green-identity test with noncommuting projections, and 30 negative controls. These are finite sanity checks, not the reason to accept an infinite-dimensional theorem.

I also constructed an independent moving-cut model. Let W=N0 with ν{k}=2^{-k-1} and rho_n(k)=2^{k-|n-k|}. Then rho_0=1, adjacent ratios lie between 1/2 and 2, and the stable band is exactly n≤k. On that band the forward density ratio is 2^{-m}; on its complement the inverse-time ratio is 2^{-m}. This directly checks the p=1 direction with unbounded measurable cut locations. At level n, rho_n(n)/rho_n(0)=4^n, so bounded distortion fails uniformly. The candidate's mechanism therefore handles a genuinely excluded class rather than merely rephrasing a bounded-distortion special case. Exact finite formula checks are saved in `independent_checks.py` and `.json`.

## 8. Attribution and current literature

- The July 2026 [Bernardes–D'Aniello–Maiuriello paper](https://arxiv.org/abs/2607.15831), Example 6.2, was inspected directly. Its aggregate orbit-level masses are 2^n, satisfying HC, while a constant-mass positive tail prevents shadowing. This is prior work answering the other part of the OWR question negatively. In the candidate's pointwise criterion that tail has equal neighboring densities arbitrarily far out, so it fails every eta<1 test, as expected.
- [Pituk, August 2026](https://arxiv.org/abs/2608.19499), Theorem B and its stated scope were inspected. The separable complex Hilbert case, and hence separable complex p=2, is already established there. The candidate's proof is independent of this result and of the uninspected publisher proof of Dragičević–Pituk.
- [Carvalho–Darji–Varandas, 2024](https://arxiv.org/abs/2407.20890), Theorem 2.4, already gives a density-weighted sequence-space realization of arbitrary dissipative composition operators. Corollary 2.16 gives the shadowing/generalized-hyperbolicity equivalence under a finite-dimensional fiber and bounded-projection-basis restriction. The candidate's orbit-coordinate reduction must be credited to this existing framework; the reviewed corollary does not cover general measurable W. I sent this attribution correction to the author before finalizing the audit.
- [Bernardes–Bonilla–Pinto, June 2026](https://link.springer.com/article/10.1007/s00009-026-03136-w), Theorem 21, still assumes bounded distortion for its shadowing transfer. Its weighted/unweighted conjugacy is related prior context, not a located resolution of the full target.

The limited current search did not locate the candidate's full all-p support-band theorem. This negative finding is not proof of novelty. Neither the already known p=2 part, the old coordinate construction, nor the 2026 counterexample should be presented as a new discovery.

## 9. Final disposition

Mathematically the candidate is complete and passes this audit, including its equivalent pointwise density condition. The exact OWR scope is covered. No proof-search extension is needed to repair a gap. Add the explicit 2024 attribution and preserve the existing p=2 and aggregate-counterexample qualifications. A later mathematical edit should be reviewed against the immutable snapshot named above.

The remaining uncertainty is historical priority, not a gap identified in the proof. No external outreach or remote write was performed during this review.

## Citation-only update checked at 03:48 UTC

The author added the recommended CDV attribution at the start of Section 3, in the literature summary, and as reference 7. A full diff against the reviewed snapshot showed **only those citation/provenance additions**, with no mathematical statement or proof-step changes. The mathematical PASS therefore also applies to updated SHA-256 `12d02dc0bcedf8812d0e57950e5130aad8b6c308c26bc260faa4e3e3605463b3`, preserved as `reviewed_proof_citation_update.md`. The CDV-attribution recommendation is satisfied; the two optional measure-theory exposition suggestions remain optional.

### Citation-only addendum, 2026-09-30 03:51 UTC

The updated candidate with SHA-256 `46325dd61804c1d63a1283dec47341ff54efaf03fdbfa21266c0348048cc667e` was diff-checked against the reviewed snapshot. Only the requested 2024 attribution was added; mathematical content is unchanged. Duplicate attribution paragraphs, bibliography entries and bullet points were noticed and sent to the author for deduplication. The mathematical pass verdict is unaffected.

### Final-hash addendum, 2026-09-30 03:52 UTC

The deduplicated candidate SHA-256 `f38ae2dd97bb2aeb8f1e97da0f4133b84b6d43d803e2b38df2c91acc56817a8e` was diff-checked against the original mathematical snapshot. Changes consist only of the 2024 attribution, audit-status wording, and a link to this review. All three duplicate insertions have been removed. Mathematical content is unchanged, and the PASS verdict applies to this final hash.
