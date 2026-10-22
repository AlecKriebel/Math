# Independent target and Fourier-support review of PR1141

Verdict: **PASS for the exact stated two-polynomial theorem and its stronger disjoint-support bound.** No mathematical repair is required in the reviewed `inputs/PROOF.md`, SHA256 `20bf5956520b2b53bb4b415d7d5683a6ae1cf1273bd36372accbc49fab482da1`. This is an internal adversarial review of a universal written proof, supplemented by exact finite evidence. It is not external peer review, a formal proof certificate, or a priority/openness certification.

## Scope, isolation, and sources

The review began with the proof and instructions alone. No pre-existing local audit, acceptance, summary, verification summary, or conclusion was opened. Early source searches concerned primary papers. Before the later broad query described next, the review independently reconstructed the universal deduction and derived the affine classification below, with the classification reported to the parent. That later primary-source lookup surfaced an unopened search snippet about a different AICR distribution-conjecture campaign. It was not used. This limited exposure prevents a claim of complete information isolation; it did not supply any argument or control used here. The 45% local checkpoint was persisted just after that query, although the derivation and parent update preceded it. No other reviewer was contacted; only the parent agent received progress and source requests.

All writes are confined to `reviews/target_01`. Source bodies, extracted text, renders, and temporary outputs are ignored before download. The shared index, refs, input files, and operative proof were not modified. The observed branch was `main`; no commit, push, release, tracker, paper, external communication, or additional agent was initiated.

Primary verification:

- **Exact original target:** Per Austrin's contributed section, *Zeros of Low-Degree, Low-Influence Polynomials on the Boolean Hypercube*, printed p.445 (PDF page 41) of OWR 9/2025, DOI `10.4171/owr/2025/9`. The authenticated 715061-byte PDF from `https://ems.press/content/serial-article-files/51353` has SHA256 `c70dc7acd811ff38fcfdf40f4dcc1d1ded8b185adb93ed2f9ccdeec1082b9dad`. Both extracted section and full rendered page were inspected. It asks for a common nonzero Boolean-cube point for two real multilinear polynomials with bounded relative influences, and asks for inverse-polynomial dependence on the degree. Its displayed expansion is over monomials of size at most d, and its denominator includes the empty monomial. Uniform-cube L2 agrees with that denominator by Parseval. Nonzeroness is implicit in the denominator and explicit in the reviewed theorem. The source's inverse-quadratic statement is a necessary obstruction as phrased, not a sufficient threshold; no independent verification of its cited construction is claimed here.
- **Earlier context:** the official CRYPTO 2022 chapter at `https://crypto.iacr.org/2022/papers/538804_1_En_6_Chapter_OnlinePDF.pdf`, DOI `10.1007/978-3-031-15979-4_6`, was checked through its browser-readable PDF text: printed pp.168, 190, 191-192, Conjectures 1.2/5.5 and Section 5.2. Its hypotheses average influences over distributions of unit-norm polynomials. Section 5.2 uses the strict bound delta < |Y|^(-d)/d, and specializes to delta < 2^(-d)/d on the Boolean cube. The 2025 printed non-strict endpoint fails at d=1; the reviewed proof already explicitly corrects this. Direct chapter/ePrint downloads returned HTTP 403; no downloaded byte-level pin for that PDF is claimed. The section's proof and formulas, rather than a cryptographic conclusion, were used to verify this contextual distinction.
- **Separator credit:** downloaded `https://arxiv.org/pdf/2608.03824v1`, SHA256 `bbe559c475aed158422dbf64e13526efe86ba5c2666660c016de8e9c9b8db272`. Lemma 3.5, its proof, and the relevant page-8 render were checked. The prior lemma covers arbitrary real polynomials with disjoint supports and allows the common-zero set through arbitrary leaf labels. It gives the structural O(d^4) separator reconstructed with constants in the reviewed proof. No explicit relative-influence threshold theorem was found in that lemma or its surrounding mathematical development. This observation is limited to this version and does not settle priority.
- **Markov/symmetrization credit:** downloaded `https://arxiv.org/pdf/2601.08727v3`, SHA256 `4bccb3a78c2f0658a0a2b0180726f2dbff7a9c382d3e27ebb2a0e4df801794b7`. Fact 5, Theorem 1, Corollary 1 and its page-4 render agree with the claimed Bernoulli averaging and the normalization 2m^2 on [0,1] with range [-1,1].

## Universal proof reconstruction

Fix arbitrary positive integers n,d and nonzero real multilinear f,g of degree at most d. All norms and expectations below use uniform independent signs, and all influences use the full squared norm. Assume f(x)g(x)=0 at every vertex and put delta=max_i max(RelInf_i(f),RelInf_i(g)). The success criterion is to deduce delta >= 1/(1024 d^8), without assuming support coverage, sign restrictions, or n >= d.

1. **Block bound.** For a degree-at-most-m multilinear function R on b bits, bounded by one at every vertex, with R(0)=1 and R(e_j)<=0, Bernoulli(t) averaging gives an actual univariate polynomial P of degree at most m, bounded by one throughout [0,1]. Its derivative at zero is the sum of R(e_j)-R(0), at most -b. Markov therefore gives b<=2m^2. The negative-basepoint case follows by negating R. This uses a bound throughout the interval obtained from averaging, not merely values at a finite grid.

2. **Separator with explicit depth.** Work on any restricted subcube where both polynomials remain nonzero. Neither can be a nonzero constant, since that would force the other to vanish. Let D be their maximum degree and let s be the multilinearized p^2-q^2, of degree at most 2D. The maximum absolute vertex value of s is positive. At a maximizing vertex z, precisely one of p,q is nonzero. If p(z) is nonzero, a maximal disjoint family of supports of top-degree monomials of q yields disjoint nonempty flip blocks E_j on which q becomes nonzero. The top-degree coefficient persists after fixing outside its support: any further contribution would require a strictly larger monomial, which is absent. At those single-block flips p vanishes, so s has the opposite sign. Substituting disjoint flip bits and multilinearizing cannot increase degree, and the maximizing choice bounds the substituted function by one. Step 1 gives b<=8D^2. The union of the original monomial supports has at most 8d^3 coordinates and intersects every old top-degree monomial. Querying this union decreases q's degree on every nonterminal branch. The other case decreases p's degree. Restrictions preserve disjointness and never increase degrees. At most 2d stages, each querying at most 8d^3 new coordinates, produce a total binary separator h of depth T<=16d^4. All common-zero inputs reach valid arbitrarily labeled leaves. The affine cube change preserves degree and query count.

3. **Adaptive covariance step.** For any real u, independent resampling in coordinate i defines A_i(u)=E|u(X)-u(X^(i))|. Run h's tree on X, replace its queried coordinates successively by coordinates of an independent Y, and telescope u. A complete transcript is exactly a cylinder fixing the queried X coordinates. After their replacement, the endpoint is uniform conditional on that transcript and independent of its leaf value. For each pre-query transcript, the previously replaced Y coordinates and still-unqueried X coordinates together are fresh independent signs; the new Y coordinate is independent because coordinates are never queried twice. Thus the conditional replacement pair has the unconditional resampling law for that next coordinate. Centering h at 1/2 and using |h-1/2|=1/2 gives

   |Cov(h,u)| <= (1/2) sum_i r_i A_i(u),

   where r_i is the original-input revealment probability and sum_i r_i=E[number of queries]<=T. Variable stopping times are covered by summing the finite set of pre-query transcripts. No low-degree or boundedness assumption on u enters this step.

4. **Fourier normalization.** Write a=a_0(x_without_i)+x_i a_1(x_without_i), and normalize its full squared norm to one. Orthogonality gives E a_1^2=rho and E a_0^2=1-rho, where rho is its relative influence. Independent resampling flips the sign with probability one-half. Hence the normalized squared density satisfies

   A_i(a^2)=2 E|a_0 a_1| <= 2 sqrt(rho(1-rho)) <= 2 sqrt(rho).

   This also follows from the flip difference/sum Parseval identities in the proof. Both derivations include the constant Fourier coefficient in the norm and are valid for arbitrary signed real a, rho=0, and rho=1.

5. **Target deduction, with no partition assumption.** Set u=f^2/||f||_2^2 and v=g^2/||g||_2^2. They have mean one. The separator gives hu=u and hv=0. With mu=Eh, the two covariances are 1-mu and -mu, whose absolute values sum to one even if f and g both vanish on many vertices. Steps 3-4 give

   1 <= sum_i r_i(sqrt(RelInf_i(f))+sqrt(RelInf_i(g)))
     <= 2T sqrt(delta) <= 32d^4 sqrt(delta).

   Squaring nonnegative quantities yields delta>=1/(1024d^8). Under the advertised assumption delta<=1/(4096d^8), the last upper bound is at most 1/2, a contradiction. The non-strict hypothesis in the advertised theorem is therefore safe. Equivalently, the signed density w=u-v has mean zero and E(hw)=1; applying Step 3 directly to w and using A_i(w)<=A_i(u)+A_i(v) gives the same deduction. This is an independently reconstructed formulation of the conversion, not an independent proof of the separator.

The cases n<d, negative scaling, nonzero constants, restrictions becoming identically zero, and common zeros do not create exceptions. Zero polynomials are excluded because normalization would fail. Degree zero would be a trivial separate case but is outside the positive-d theorem, where its displayed denominator d^8 is defined.

## Independent Fourier-support family: complete affine classification

This gives a universal low-degree falsification check separate from the separator/revealment mechanism. Let f=a_0+sum_i a_i x_i and g=b_0+sum_i b_i x_i be nonzero real affine polynomials. The unique multilinear Fourier expansion of fg is zero exactly when

    a_0 b_0 + sum_i a_i b_i = 0,
    a_0 b_i + b_0 a_i = 0  for every i,
    a_i b_j + a_j b_i = 0  for distinct i,j.

If a_0 and b_0 are nonzero, then b_i=-(b_0/a_0)a_i. The off-diagonal equations allow at most one nonzero a_i; the constant equation forces its square to be a_0^2. Thus the pair is scalar multiples of (1+s x_i,1-s x_i), s in {-1,1}. If exactly one constant term is nonzero, the linear equations force one entire polynomial to vanish, which is excluded.

If both constants vanish, choose a_i nonzero. Then b_i is nonzero, since otherwise all other b_j vanish by the off-diagonal equations. For j!=i, b_j=-b_i a_j/a_i. The equations between distinct j,k!=i allow at most one additional nonzero a_j. The constant equation forces one such j to exist and a_j^2=a_i^2. The pair is scalar multiples of (x_i+s x_j,x_i-s x_j). These listed pairs all are disjoint and exhaust the cases.

Every such disjoint pair has maximum relative influence **exactly 1/2**. In particular, f=1+x_1 and g=1-x_1 disprove a universal sufficient threshold with the old non-strict endpoint delta<=2^(-d)/d at d=1. They do not challenge the new inverse-polynomial theorem. The first form also checks the full-mean denominator: replacing it by the variance would incorrectly give influence one.

## New exact finite controls

`exact_target_controls.py` uses only the standard library and exact integers/Fraction. It enumerates all nonzero coefficient vectors from {-1,0,1} on all Fourier monomials up to the listed degree, modulo global sign. For each support it retains the least possible maximum relative influence, so testing disjoint pairs of supports certifies the claimed lower bound for every coefficient-box pair, not merely the chosen representatives. It independently checks exact Parseval, flip difference/sum energies, degree-weighted total influence, square-density L1 bounds, covariance multiplication identities, all common-zero support pairs, constants, zero rejection, scaling, n<declared-d threshold arithmetic, and a dimension-only full-depth bound delta>=1/(4n^2).

| n | degree bound | polynomial sign classes | distinct supports | disjoint support pairs | with common zeros | minimum pair max influence |
|---|---|---|---|---|---|---|
| 1 | 1 | 4 | 3 | 1 | 0 | 1/2 |
| 2 | 1 | 13 | 7 | 3 | 0 | 1/2 |
| 3 | 1 | 40 | 21 | 6 | 0 | 1/2 |
| 4 | 1 | 121 | 61 | 10 | 0 | 1/2 |
| 2 | 2 | 40 | 11 | 21 | 18 | 1/2 |
| 3 | 2 | 1093 | 127 | 497 | 462 | 1/2 |
| 4 | 2 | 88573 | 5519 | 26205 | 25970 | 1/3 |

The last row represents 177146 nonzero coefficient vectors and 81015 unordered disjoint polynomial sign-class pairs. Arbitrary real coefficients are covered by the written proof, not by this finite box. Normal and `python3 -O` runs passed and produced identical mathematical outputs. Six deliberate fault-injection flags (omitting the constant denominator, using full flips as resampling, accepting the old non-strict endpoint, accepting zero normalization, assuming a support partition, and changing final constant arithmetic) each failed with explicit checks in both execution modes: 12 detected wrong results. Checks do not use Python `assert`, so optimization does not disable them. These controls test specified error modes; they are not a universal implementation or formal-proof certificate.

## Findings, strongest result, and exact gap

- No blocking or nonblocking mathematical finding against the reviewed proof.
- The source's old non-strict sufficient endpoint is false at d=1; this is already accurately flagged in the proof and requires no operative repair.
- The cited 2026 separator is the decisive prior structural input and must retain its current credit. The target deduction was checked as mathematics without inferring it from a cryptographic result.
- Strongest verified stated result: every disjoint nonzero real multilinear pair of degrees at most d on the uniform Boolean cube has some coordinate with relative influence at least 1/(1024d^8). Consequently the requested common-nonzero-point guarantee holds at every delta<=1/(4096d^8).
- Exact remaining mathematical gap to this target: **none found**. The review does not establish the broader average-over-distributions conjecture, other input groups/measures, approximate-support conclusions, optimized constants, novelty, or current openness. A separate priority audit is needed for publication language about novelty.

The receipt pins reviewed input versions, primary-source availability limits, code, results, and public artifacts; its own digest must be pinned externally by the parent.
