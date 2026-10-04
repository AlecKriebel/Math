# Independent adversarial audit: Function Theory 5.60

Audit date: 2026-10-04 UTC. Target: rank 577, problem 2305060 / AMR-022-5060.

## Verdict

**PASS as an unsolved, five-turn partial-results packet.** No substantive mathematical error was found in the claimed results. The packet does not resolve the unrestricted noninteger-exponent problem and must remain classified **unsolved, 5/5**. This audit does not certify novelty or the absence of a later resolution.

The exact reviewed public manifest SHA-256 is

`3adf008f4ad92707e96290f0d6df44b61d1dbbfb3d0b050de24f53583ead13a6`.

All 11 payload files and the manifest remained unchanged. The frozen author packet was read only; audit outputs are separate. No remote writes, outside contacts, or additional proof-search attempts were made. The numerical run below is a replay of the frozen experiment, not an expanded search.

## 1. Statement and source audit

The live primary PDF at [arXiv:1809.07200](https://arxiv.org/pdf/1809.07200), printed pages 107–108, was opened and the mathematical statement checked. The privately cached images of both pages were visually inspected. The premise has numerator exponent alpha, the conclusion alpha minus one, with the denominator exponent beta unchanged. Both parameters are real and at least one; the phase has modulus one and the variable is in the open unit disc. The packet correctly preserves arbitrary analytic phi and does not introduce positivity, finite degree, or integrality into the full target.

The primary source records the natural-number-alpha case as established and lists Sheil-Small's 1980 chapter, pages 515–523, in its bibliography. The cited update reports no progress known to the source authors. That historical statement is not a current-status certificate. The catalogue URL returned an error during this audit. A bounded independent exact-title/problem-number web search found no verified later resolution; this is not a comprehensive literature theorem. The 1980 chapter itself was not independently obtained. None of the packet's proofs relies on a theorem from the related 2011, 2024, or inaccessible 1983 articles.

The private primary PDF, selected problem record, selected prior report, and both available full source corpora were rehashed and match SOURCE_MANIFEST.json. The selected prior report is only OPEN-TRIAGE and contains no proof. Repository-wide duplication and live queue state were not independently re-queried in this mathematical audit; the frozen baseline and the bounded-search qualifications are not upgraded to exhaustive claims.

## 2. Definitions, convergence, and normalization

PROOF.md lines 7–38 are correct. The analytic powers are well-defined by the logarithm branches normalized at the origin; neither 1+xz nor 1-z vanishes in the relevant open disc. Coefficientwise multiplication is the intended Hadamard convolution. At zero, the kernel has constant coefficient one, so the hypothesis forces phi(0) nonzero and scalar normalization is legitimate.

In the lift, (beta)_j is the rising factorial, with (beta)_0=1. For each compact sub-bidisc, Cauchy's estimate and the two absolutely convergent kernel series give a summable majorant. In particular, the double series is normally convergent, is jointly holomorphic, and may be rearranged and differentiated on compact subsets. Substituting (u,v)=(xz,z) gives the original convolution exactly. The same statements remain valid at the lowered exponent zero when alpha=1.

## 3. Bidisc zero-freeness: challenge and resolution

**Lemma 1 passes.** Nonvanishing on a single distinguished torus would not by itself justify interior nonvanishing. The author uses every common radius and the contraction to the origin, which supplies the missing zero-count information.

For fixed r<1 and fixed |V|=1, the family U -> F(tU,tV), 0<=t<=r, has no zeros on |U|=1. Its argument-principle integral is continuous in t and integer-valued. Analyticity holds on a common neighborhood of the integration circle, and compactness ensures the denominators in the integral do not vanish. At t=0 the function is one. Hence its zero count is zero for all t. This proves nonvanishing for |U|<=1 and |V|=1 simultaneously for every t<=r.

Only after establishing that entire side boundary does the second homotopy fix |U|<=1 and count zeros in V. Its boundary is now zero-free for all t, and its initial value is again one. Therefore F(rU,rV) is zero-free on the closed unit bidisc. Varying r proves the claim on D squared. There is no circular use of interior zero-freeness in either stage.

To recover the equal-radius condition from the original hypothesis, for v nonzero set z=v and x=u/v; then |x|=1. The radius-zero point is covered by normalization. The converse follows by restriction. Thus both the premise and conclusion are genuinely equivalent to the corresponding bidisc conditions.

## 4. Lowering, root geometry, and the affirmative range

The generalized-binomial identity is correct for every nonnegative integer coefficient index, including the vanishing coefficients when alpha is integral. Since alpha>=1, division by alpha is harmless. It yields exactly F_lower=F-u F_u/alpha.

**Lemma 2 and Theorem 3 pass.** The root identity has the correct sign. A root on the unit circle still contributes a strictly positive difference because |u|<1. Multiplicities are handled by factorization, and the constant-polynomial case is separated. The resulting strict bound Re(u p'/p)<d/2 is sufficient even at the endpoint d=2 alpha.

For each fixed v, premise zero-freeness rules out an identically zero slice. When alpha is an integer, the u-degree is at most alpha despite phi possibly having infinitely many coefficients: the finitely many u-coefficients are convergent analytic series in v. For polynomial phi, total degree and therefore u-degree are at most N. Degree drops at special v only improve the bound. Thus the stated integer-alpha result for arbitrary analytic phi and the N<=2 alpha result for arbitrary allowed real parameters follow without hidden coefficient restrictions.

The example (1+u)^N, N>2 alpha, has its lowered zero at alpha/(N-alpha), which lies strictly between zero and one. It disproves only the unrestricted slice-preserver claim. The packet correctly explains why a nonconstant lift independent of v cannot have the required coefficient structure when beta>=1. This example is not misreported as a counterexample to the target.

## 5. Other claimed identities and obstructions

The finite-measure obstruction passes. For noninteger alpha the relevant generalized binomial coefficients are nonzero for every index. Evaluating the proposed universal representation at v=0 forces moments 1-n/alpha, incompatible with the bounded total variation of a finite complex measure on the closed unit disc. The statement explicitly concerns a universal linear representation for every analytic phi, so the test phi=z^n is allowed there. If the earlier normalization convention is read as global, the same computation uses 1+epsilon z^n and subtracts the constant test; it does not invalidate the result. No preservation of zero-freeness under averaging is assumed. The separate positive-average counterexample is correct.

The coefficient calculations giving (u+v)F_uv=alpha F_v-beta F_u are correct, including the signs and the cases where generalized-binomial coefficients vanish. The diagonal restriction follows from multiplying (1-vt)^alpha and (1-vt)^(-beta). The alpha=beta diagonal is therefore identically one after normalization. The avoidance condition uF_u/F != alpha is equivalent to the desired lowered bidisc nonvanishing, and the packet correctly leaves the stronger real-part estimate unproved.

## 6. Robust polynomial and rational reduction

**Theorem 4 passes, including the closed-bidisc and parameter-boundary claims.** The following checks address the delicate steps.

1. A failed conclusion provides a phase x0 with modulus one and a zero z0 in D. Normalization excludes z0=0. Choose |z0|<s<1. The dilated premise lift F(su,sv) is analytic and zero-free throughout |u|,|v|<1/s, so it has a positive minimum on the closed unit bidisc. The failed-conclusion zero moves to z0/s, still in D.
2. Choose R with s<R<1. The dilated coefficients satisfy |a_n s^n|<=M_R(s/R)^n. The absolute double-series majorant with ratio s/R is summable on the closed unit bidisc for both alpha and alpha-1. Consequently total-degree Taylor truncations converge uniformly there. This supplies the uniform premise margin rather than merely pointwise convergence.
3. The lowered limiting one-variable function at fixed x0 is not identically zero since its constant term is one. Its zero at z0/s is isolated and has positive finite multiplicity. A sufficiently small circle contained in D has no boundary zeros. Uniform approximation and Rouche's theorem preserve a positive zero count inside, whether or not the original zero is simple.
4. Fixing a sufficiently large truncation produces both a positive premise margin on the closed bidisc and a positive lowered boundary margin on that circle. For fixed finite degree, both lifted polynomials depend continuously on the parameters and coefficients, uniformly on these compact sets. Hence sufficiently small simultaneous perturbations preserve both margins and the lowered zero count.
5. The already-proved integer case excludes every integral alpha, including alpha=1. A hypothetical counterexample thus has alpha>1 noninteger, and there is an open parameter neighborhood inside that range. Rational alpha may be selected there. Rational beta>1 may approximate beta>1; beta=1 can be kept exactly, respecting the parameter boundary. Gaussian-rational nonconstant coefficients are dense and the constant coefficient stays one.
6. No rationality is claimed or needed for x0 or the surviving zero. The theorem only rationalizes the finite input data. The final degree must exceed 2 alpha by Theorem 3. The proof supplies neither an a priori degree bound nor an example.

Thus validity for all finite-degree rational-data cases would exclude every analytic counterexample. The reduction is substantive but does not close the remaining problem.

## 7. Computational review and reproduction

The frozen manifest verifier passes with 11 payload files and no discrepancies. The frozen exact verifier passes all 208 checks. Its complete replay output is byte-for-byte identical to CHECKS.json, including the recorded Python version.

The numerical search was replayed with the unchanged program, seed, parameters, and sample schedule. SEARCH_REPLAY.json is byte-for-byte identical to SEARCH.json. It uses NumPy 2.3.5 and Python 3.12.14. There are 48 eligible parameter/degree groups, 24 samples each, hence 1,152 samples. The initial grid has 96 phases; ten selected group winners are repeated at 4,096 phases. The minima reproduced as follows:

- Coarse minimum ratio: 1.2108266594872017.
- Refined minimum ratio: 1.2108944944008464.
- No sampled ratio below one.

The construction of the convolution coefficients, reversal for numpy.roots, and common rescaling interpretation were checked. A true continuum radius gap would nominate a valid rescaling, but sampled minima are only upper bounds for their separate continuum minima; their ratio is not a certified bound in either direction. Floating-point roots supply no interval certificate. The packet prominently and correctly limits these computations to heuristic evidence and finite algebra controls.

One nonblocking naming issue is recorded in CORRECTIONS.json: search.py line 51 counts group winners below one, rather than all individual samples below one. At zero these statements are equivalent, so the recorded no-hit conclusion is unaffected. Future positive hit counts should use a clearer field name or an in-loop sample counter. No rerun or mathematical correction is required for the present packet.

## 8. Release disposition

No mandatory correction is requested. Accept the stated partial results and reduction, retain unsolved/5-of-5, and preserve all limits concerning computation, literature coverage, source access, and novelty. The unresolved noninteger-alpha, unbounded-degree case remains exactly the gap stated in PROOF.md. The separate audit records completion of review without rewriting the frozen author's pending-audit fields.

Files in this audit contain authored review, checks, and hashes only. No primary PDF, source-page image, or full source corpus is redistributed.
