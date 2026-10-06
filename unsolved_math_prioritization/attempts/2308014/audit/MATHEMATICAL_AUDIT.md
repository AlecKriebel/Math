# Independent mathematical audit: positive scalar Hankel symbols

Problem 2308014, AMR-022-8014, Function Theory Problem 8.14. Audit date: 2026-10-06 UTC.

## Decision and exact object

**ACCEPT the full characterization in the exact author freeze as a reduction to established theory. No mathematical repair is required.** This acceptance applies to bounded scalar symbols and positive semidefinite infinite Hankel operators in the explicitly stated Fourier conventions. It is not a novelty claim, a claim of historical priority, or evidence that a publication expressly announced a solution of the named Holland problem.

The accepted ZIP has SHA-256 `2c62215d1fb82098c2c3777d67f90545b9fa10cf83d4a0d5c91313f84a5a33c5`, 13,928 bytes. Its independently pinned external manifest has SHA-256 `227a90bcc9104cf0a9ce5ea45146aee4624b91a0b3e2f3198b5c43d8a5f99297`, 1,962 bytes. The accepted `author/PROOF.md` has SHA-256 `b03a79e14b89a4385f69d4fa9088ea08e011c1447dac1cf7f85ce6f6ece8da3d`, 9,591 bytes. The original nine author files are preserved byte-for-byte. Audit material does not silently replace their pending-audit historical status fields.

## 1. What is classified

With normalized circle measure, set a_n = integral f(z)z^n dm, n >= 0, and H_f = (a_{j+k}) indexed from zero. The accepted answer is

    f = g_mu + z h,   h in H-infinity,

where mu is a finite positive Borel measure on (-1,1) with

    mu({x : 1 - |x| <= t}) <= K t,  0 < t <= 1,

and, away from the two circle endpoints,

    g_mu(z) = mu((-1,1)) + integral [1/(1-x/z) - 1/(1-xz)] dmu(x).

Values at the endpoints do not matter in L-infinity. The measure is unique for each symbol/operator. The parameter h is arbitrary subject to bounded analyticity. The assertion is both necessary and sufficient, not just a sufficient family or a finite-section test.

## 2. Bounded operator and the meaning of positivity

For finitely supported c,d, the matrix pairing equals the integral of f times two analytic polynomials, one with coefficient sequence c and one with conjugated coefficient sequence d. Cauchy-Schwarz and orthogonality of circle monomials give the bound ||f||_infinity ||c||_2 ||d||_2. Thus this is a bounded sesquilinear form on a dense subspace and extends uniquely to an operator on all of ell-squared, with norm at most ||f||_infinity.

If the finite quadratic forms are nonnegative, continuity gives nonnegativity on all ell-squared. Conversely operator positivity gives every finite quadratic form. This uses every finite vector, not any fixed maximum matrix size. A bounded everywhere-defined operator is closed; there is no unresolved domain or closability issue. The positive operator cone is norm closed: if positive A_l tend to A in norm, their quadratic forms converge pointwise. Consequently the positive-symbol set is also norm closed because f maps continuously to H_f. These facts justify the positivity extensions used in the proof; no claim about entrywise or pointwise positivity is needed.

## 3. Moment existence, support, endpoints, and uniqueness

A positive operator is Hermitian. Its Hankel matrix is also symmetric, so every a_n is real. The full nonnegative Hankel quadratic form is precisely the hypothesis of the Hamburger moment theorem. The representing measure initially lies on the real line and has finite mass a_0.

For every n, 0 <= a_{2n} <= M = ||H_f||, since a_{2n} is the diagonal matrix entry at n. Positive mass on any set |x| >= 1+delta would force these even moments to grow exponentially, contradicting this bound. Taking a countable union of such sets proves support in [-1,1]; there is no unsupported passage directly from a finite test to compact support.

Since f belongs to L-infinity on a probability space, it belongs to L-one. Its Fourier coefficients tend to zero. Hence a_{2n} tends to zero, whereas dominated convergence of x^(2n) on [-1,1] gives the total mass at {-1,1}. Both endpoint atoms therefore vanish. Equality of all moments on a compact interval implies equality on polynomials, then on continuous functions by uniform polynomial approximation, and finally equality of the finite measures. The zero-operator case gives zero measure and is included.

## 4. Necessity of the endpoint tail bound

For each polynomial p, the moment identity gives

    integral |p(x)|^2 dmu <= M ||p||_(H2)^2.

For a fixed 0 < r < 1, the finite geometric sums for 1/(1-rz) converge uniformly on [-1,1]. Their squared coefficient norms tend to 1/(1-r^2), so passing to the limit is valid and gives the required reproducing-kernel estimate. For x >= r the denominator 1-rx is positive and no larger than 1-r^2. Therefore

    mu([r,1)) <= M(1-r^2) <= 2M(1-r).

Replacing r by -r in the kernel yields the corresponding negative-endpoint bound. With t=1-r the two disjoint endpoint tails have combined mass at most 4Mt for 0<t<1. At t=1 the whole mass is a_0 <= M, so K=4M also works there. This separately checks the t=1 boundary and the M=0 degeneracy.

## 5. Sufficiency of tails for a bounded symbol

For z=exp(i theta), let s=|sin theta|, q=|x|, and u=1-q. The exact difference kernel has imaginary value -2ix sin(theta)/(1-2x cos(theta)+x^2). Its absolute value is the expression used in the author proof; the minus sign is consistent with the negative-frequency moment convention.

The denominator is at least u^2 + 2q(1-|cos theta|), hence at least u^2+q s^2. If u>=1/2, then s^2<=4u^2; if u<1/2, then q>1/2. Both cases imply denominator >= (u^2+s^2)/5. Thus the absolute kernel is at most 10s/(u^2+s^2).

The pushforward measure in the u-variable obeys nu((0,t]) <= Kt. At t>1 this remains valid because its total mass is at most K. The region u<=s contributes at most 10K. On 2^j s < u <= 2^(j+1)s, the contribution is at most 20K 2^(-j). These sum to 40K, so the total is at most 50K. This establishes the claimed uniform bound and absolute integrability at every non-endpoint z, including when mu is singular or has infinitely many interior atoms accumulating at the endpoints.

No stronger integrability assumption is covertly used. For example, ordinary Lebesgue measure on (0,1) satisfies the tail bound while its integral of 1/(1-x^2) diverges. It remains included in the accepted classification, as it must.

## 6. Boundary Fourier limit

Restricting mu to [-r,r] makes both geometric series absolutely and uniformly convergent on the circle. For each fixed n this proves exactly the coefficient identity a_n(g_(mu_r)) = integral x^n dmu_r, including n=0. The nonconstant series contributes no constant term; the explicit mass term supplies a_0.

Each restricted measure obeys the same tail constant K, so all representatives have a common L-infinity bound. For fixed z other than +/-1, the difference kernel extends continuously as a function of x to [-1,1], with a finite bound depending on z. Thus the representatives converge pointwise off a null set. Dominated convergence on the circle then passes every coefficient to the limit. A separate bounded-convergence argument passes the moments to the limit. This is sound and does not interchange an uncontrolled infinite series with an endpoint-accumulating measure. No uniform convergence of the untruncated Fourier series or L-infinity norm convergence of the representatives is asserted or needed.

## 7. Exact nullspace and final sufficiency

If b=f-g_mu, all of its Fourier coefficients with indices 0,-1,-2,... vanish. The Poisson extension therefore has only strictly positive frequencies and is holomorphic, bounded by ||b||_infinity, and zero at the origin. Schwarz's lemma shows that division by z remains bounded analytic; radial boundary convergence identifies b=z h almost everywhere. This proves the precise nullspace z H-infinity, rather than incorrectly including constants.

Conversely, z h contributes no required moment. The finite quadratic form of g_mu+z h is the integral of the squared modulus of a polynomial against a positive measure. Section 2 then extends positivity to all ell-squared. All steps are available for every admissible measure, so completeness is established.

## 8. Convention controls and the half-plane bridge

For the shifted matrix f-hat(-j-k-1), multiplication of the symbol by z produces the unshifted convention. Its complete class is therefore z^(-1)g_mu + H-infinity. Reflection of the boundary argument switches positive and negative Fourier indices. These transformations are algebraic identities, not guesses from quotient notation.

Useful controls are: the constant symbol 1 gives a nonzero positive rank-one matrix in the n=0 convention and zero in the n=1 convention; any z h gives zero in n=0; an atom at -1/2 gives a positive matrix with negative odd moments; and the nonnegative pointwise symbol 1+cos(theta) has a leading two-by-two determinant -1/4 and is not a positive Hankel symbol.

For comparison to the unshifted circle operator P_+ M_k R_0 of ANS equation (14), with R_0 p(z)=p(conjugate(z)), its matrix entries are integral k(z)z^(-j-k) dm. Setting k(z)=f(conjugate(z)) gives the author convention exactly. With omega(z)=i(1+z)/(1-z), zeta=omega^(-1)(x), the Hardy-space Cayley unitary obeys

    Gamma M_k R_0 Gamma^(-1) = M_[-zeta k(zeta)] R_line.

Indeed the multiplier ratio is (i-x)/(i+x)=-zeta; any common normalization constant cancels. Thus the half-plane symbol h(x)=-zeta k(zeta), as in ANS equation (21), preserves boundedness and operator positivity by unitary conjugacy. A circle reflection containing an additional conjugate(z) factor changes this multiplier and is the shifted convention. These cannot be mixed.

The literal constant-term issue in source quotient notation is not used as a premise. The author proves its own nullspace, which fixes that issue. The direct circle formula is also independently proved rather than asserted to coincide pointwise with a Cayley-transformed source formula. These choices successfully prevent a sign, shift, or normalization gap.

## 9. Exact original-problem bridge and prior-result scope

The inspected original list asks for the bounded circle symbols generating positive Hankel operators, attributes the question to F. Holland, and supplies an editorial update saying that progress had not been reported to the editors. It does not specify a Fourier shift or impose a different scalar positivity condition. The author's two explicit conventions and boundary reflection cover the standard scalar interpretations. No extra hypothesis has been placed on the original bounded symbols. The endpoint condition restricts the parametrizing measures and is proved necessary, rather than assumed of the input symbol.

This mathematically answers that characterization under the declared conventions. The editorial update is historical evidence only. Neither it nor a failed live-site retrieval establishes present openness. No inspected source explicitly identifies itself as resolving the named Holland question, and the audit does not make that historical claim.

The following references support the prior-theory attribution. The analytic verification above is an independent check of the authored proof, not a transcription of their proofs.

- [Hayman and Lingham, Research Problems in Function Theory](https://arxiv.org/html/1809.07200v2), Problem and Update 8.14; cached PDF page 194, printed page 193.
- [Adamo, Neeb and Schober, Reflection positivity and Hankel operators—the multiplicity free case](https://arxiv.org/html/2105.08522v1), Definition 2.4, Appendix A, Theorem 4.1 and equation (21). The paper supplies the classical moment classification and a constructive bounded-symbol result.
- [FAU publication record](https://cris.fau.de/publications/273551213/), confirming Journal of Functional Analysis 283(2), 109493 (2022), [DOI](https://doi.org/10.1016/j.jfa.2022.109493).
- [Widom, Hankel matrices](https://doi.org/10.1090/S0002-9947-1966-0187099-X). Original full text was not inspected; relevant prior theorem and proof were inspected in ANS Appendix A.

## 10. Computational and acceptance limits

The 1,948 exact rational checks are finite sanity checks. They do not prove Hamburger's theorem, measure uniqueness, the endpoint estimates for all measures, boundary convergence, or the full infinite-dimensional characterization. Those are accepted on the analytic reasoning audited above.

Normal isolated and relocated replay passes. Optimized Python execution under both -O and -OO is explicitly refused, for both full and math-only modes; this is an expected guard success, never an optimized mathematical pass. Changed proof bytes, a missing member, an extra member, a corrupt internal manifest, altered stored results, and unexpected bytecode cache all fail. An independently pinned wrapper rejects a forged checker and symlink substitution before execution, and isolated replay ignores hostile current-directory/PYTHONPATH shadow modules. The trust anchor is the externally pinned archive and member inventory, not a potentially edited script certifying itself.

**Final disposition:** PRIOR_RESULT_ACCEPTED_AFTER_INDEPENDENT_MATHEMATICAL_AUDIT. Approaches remain 1/5. No mathematical patch, new approach, publication, queue edit, outreach, historical-priority certification, or formal proof-assistant verification was performed.
