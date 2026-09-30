# Independent review of the polynomial recurrence source correction

**Verdict: PASS_CREDITED_COMPLETE_RESOLUTION.** The exact result requested in Problem 17 is a stated corollary of the published Frantzikinakis–Kuca theorem, including the sharp exponent and bounded gaps. No mandatory correction to the frozen artifact was found. Recommend **already_solved, zero new proof attempts**. This is an independent AI source/applicability audit, not a new proof of the long published theorem or human peer review.

Reviewed artifact: `KNOWN_RESULT.md`, SHA-256
`32c2ada07cf75084e1443d3dbbe964900ef66e327873937b57f86c513c52e67e`.
The original author files were not modified. Review completed 2026-09-30 with gpt-6-astra at xhigh reasoning.

## Original and resolving primary sources

I inspected the complete relevant rendered pages and surrounding hypotheses in Frantzikinakis, *Some open problems on multiple ergodic averages*, [arXiv:1103.3808v3](https://arxiv.org/abs/1103.3808v3), Section 1.2 and Problem 17, printed p. 27. The input is a probability-preserving system with invertible commuting transformations and rationally independent integer polynomials with zero constant terms. The requested intersection lower bound has exponent ell+1; the following paragraph also predicts bounded gaps.

I separately inspected Corollary 2.11 on printed p. 10 of the full [Frantzikinakis–Kuca v2 manuscript](https://arxiv.org/abs/2207.12288v2), together with its system definition, regular-space convention, polynomial assumptions, notation for positive integers, and introduction item (iii). The corollary gives precisely that lower bound and explicitly gives bounded gaps. It imposes no ergodicity, total ergodicity, or weak-mixing condition. The total-ergodicity remark above it belongs to a different limit formula.

The [publisher's primary record](https://link.springer.com/article/10.1007/s00222-024-01313-w) independently confirms the authors, publication on 2 January 2025, and *Inventiones mathematicae* 239, 621–706. Its abstract also describes the recurrence application. The full exact statement was verified in the author manuscript, rather than inferred from the publisher abstract. The final typeset journal text was not obtained or compared line by line.

The manuscript's introduction item (iii) identifies the original Problem 17, whereas the paragraph before the corollary points to Problem 16. I verified both references. The explicit formulas and hypotheses remove the identification ambiguity; the artifact appropriately preserves the cross-reference discrepancy. No claim about the present contents of an inaccessible progress webpage is needed.

## Adversarial hypothesis checks

**Independence.** Because each constant coefficient vanishes, a rational linear combination that is constant is necessarily zero. Rational independence modulo constants is therefore the same as linear independence over Q in this problem. For integer coefficient vectors, the maximal nonzero minors determine the same rank over Q, R, and C. A pair such as n² and n²+n shows why one must not silently replace independence by distinct degrees. The artifact does not do so.

**Commutativity and ergodicity.** Inversion preserves invertibility, commutativity, and measure preservation. Neither the original nor the applicable corollary adds ergodicity. Nonergodic cases were expressly included in the independent finite diagnostics. They are not eliminated by the source's unrelated joint-ergodicity statements.

**Signs.** For S_i=T_i^{-1}, one has S_i^{-p_i(n)}A=T_i^{p_i(n)}A exactly. This matches the corollary's negative-image convention to the original positive-image convention for every n. Thus it preserves the entire set of good positive integers, not merely its nonemptiness, and also transfers bounded gaps.

**Zero constants and positive indices.** These are genuine hypotheses/conventions in the resolving statement. The manuscript defines N as positive integers. No appeal to the vacuous n=0 case is made. Sets of measure zero or one are consistent with the inequality, and no nonzero constant-shift extension is being claimed.

**Meaning of sharp.** The claimed exponent is exactly the source exponent. As a separate elementary check of its universal optimality, take a two-sided Bernoulli shift, the event that coordinate zero is 1 with probability alpha in (0,1), all transformations equal to the shift, and p_j(n)=(j+1)n^j for j=1,...,ell. These polynomials are independent, and the sites 0,p_1(n),...,p_ell(n) are pairwise distinct for every positive n. Independence of coordinates makes every intersection measure exactly alpha^(ell+1). Thus a uniformly larger lower bound cannot be substituted. This observation is not presented as a new discovery or as the proof of the recurrence theorem.

## General probability spaces and the symbolic factor

The extra factor argument in the artifact is correct. For G=Z^ell and Y={0,1}^G, the coordinate maps x↦1_A(T^g x) are measurable; because G is countable they define a measurable map Φ into the compact metrizable product Y. Its pushforward is a Borel probability measure, hence fits the regular-space hypothesis.

Define σ_i by shifting coordinates g to g+e_i. Commutativity gives Φ(T_i x)=σ_iΦ(x), and measure preservation gives σ_i-invariance of the pushforward. Let C be the zero-coordinate cylinder. For any integer k,

\[
 x\in\Phi^{-1}(\sigma_i^k C)
 \iff \Phi(x)(-ke_i)=1
 \iff T_i^{-k}x\in A
 \iff x\in T_i^kA.
\]

This verifies the sign in the artifact's displayed pullback identity. Intersections and their measures are preserved exactly, so applying the known theorem on Y transfers the conclusion to the original probability space. The factor need not be injective or surjective onto all of Y. If transformations are given modulo null sets, the countably many group relations can be enforced on a common invariant conull set, or the same construction can be performed on the generated measure algebra. No uncountable intersection of conull sets or separability assumption on the original space is required.

This settles the only potentially stronger probability-space interpretation of the original source. It does not transfer the theorem to noncommuting transformations.

## Reproducibility and evidentiary limits

The submitted verifier was replayed in an isolated copy alongside the exact frozen manuscript. It passed **142,505** assertions and produced a receipt byte-identical to the author's receipt.

The separate standard-library checker passed **22,279** assertions. It uses polynomial minors/rational elimination, independently implemented permutation actions, and explicit finite symbolic factors with pushed-forward weights. It checks 242 finite system/set cases, including 132 nonergodic cases, exact signed pullbacks and intersection measures, and distinct-site Bernoulli sharpness controls. Several examples have nonuniform invariant orbit weights. The checker does not call the author's code.

These finite controls support the convention reductions only. They do not prove the unrestricted multiple recurrence theorem, its seminorm-smoothing machinery, or infinite-system syndeticity. The reviewed conclusion rests on the exact cited published corollary. The artifact explicitly says this, preserves the final-journal-access limitation, credits the existing result, and claims no campaign novelty. The imported report's partial-progress label should therefore not override this matching theorem.

## Publication recommendation

The source correction may be published with status **already_solved 0/5**, the original proof attribution, and this independent review. Preserve the manuscript-versus-final-typeset qualification and do not turn the finite diagnostics into a claim of a new general proof or an effective gap bound. No required mathematical or source correction remains.
