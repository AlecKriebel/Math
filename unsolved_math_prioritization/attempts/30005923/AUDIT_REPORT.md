# Determinant moments and covariance: prior-result scope audit

Audit date: 8 October 2026. Targets: 30005923 and companion 30005922.

## Disposition

**30005923: HOLD for the constant uniform in the number of variables.** The argument in Jury–van Rensburg–Roman, arXiv:2607.25980v1, Proposition 6.1(2), supports a repaired theorem with a fixed tuple length `g`. It does not establish a constant independent of `g`. This audit neither disproves the all-`g` bound nor supplies it.

**30005922: credited prior-result coverage in the exact fixed-parameter domain, with the elementary corrections explicitly supplied below.** For each fixed finite `g`, fixed matrix sizes `k,l`, and fixed tuples `A,B` having outer spectral radii less than one, the covariance limit is the reciprocal determinant of `I-sum A_j tensor conjugate(B_j)`. The original stable-polynomial setting is covered when “determinantal representations” retains the strict row-contraction convention of OWR Lemma 9. No uniformity as `g,k,l` vary is needed for this limit. This is a verification of the authors' method and result, not a new solution claim.

Original proof-attempt turns used: **zero**. No all-`g` research was undertaken. No repository or queue changes were made. The two questions share one proof-verification dependency chain, rather than two independent research attempts.

## 1. Literal source assertions

### OWR 22/2024

The contribution *Determinants of pencils of random unitaries*, pp. 1270–1272, defines Haar measure to have total mass one and uses the abbreviation `A tensor U = sum_j A_j tensor U_j`. The norm is the square root of `||sum A_j A_j*||`.

Conjecture 12, p. 1272, writes `C(r,k)` and quantifies over all `d`-tuples satisfying the row bound. Under the literal reading that the displayed dependencies are exhaustive, the requested constant is independent of both `N` and tuple length `d`. The context does not explicitly certify a convention permitting dependence on `d`. Consequently this audit will not silently substitute `C(d,r,k)` for the target. The following suggested constant is `(1-r^2)^(-k^2)`. Monotonicity in `N` is an additional suggestion, not a hypothesis or part of the basic boundedness conclusion.

Conjecture 10 concerns fixed stable polynomials in finitely many variables with constant term one. The immediately preceding definition ties their determinantal representations to coefficient tuples of row norm strictly below one. Conjugation on the second determinant and on the second coefficient tuple is essential. Matrix sizes for the two representations need not coincide.

Primary report: <https://ems.press/content/serial-article-files/49482>.

### Jury–van Rensburg–Roman

The only listed arXiv version on the inspected abstract page is v1, submitted 28 July 2026. No journal reference or acceptance claim appears there. The HTML also displays a document date of 24 August 2026; that does not change the version identifier or certify publication.

Proposition 6.1 begins by fixing `g`. Part (2) states positive-moment bounds on the closed radius-`r` row ball with `r<1`, for every real `m>=0`, uniform over `N` and over the coefficient tuples in that fixed finite-dimensional space. Although its constant is denoted `C_2(k,m,r)`, the proof's compactness argument is in `M_k(C)^g`, and its quantitative-polynomial estimates keep the polynomial alphabet fixed. Omitting `g` from a symbol is insufficient evidence of independence from `g`.

Theorem 1.6 asserts the covariance identity under strict outer-spectral-radius assumptions. Its displayed integrand accidentally lacks a determinant on the second pencil. The scalar formula in Theorem 6.2 with zero denominator tuples fixes the intended meaning. The theorem covers a larger coefficient domain than strict row contractions, via simultaneous similarity.

Primary manuscript: <https://arxiv.org/abs/2607.25980v1> and <https://arxiv.org/pdf/2607.25980v1>.

The earlier Jury–Roman paper, arXiv:2506.04400v1, Proposition 3.5, already supplies a fixed-parameter normal-family route from a moment bound to the covariance conjecture. Its notation uses `d` for unitary matrix size and `g` for tuple length, unlike OWR. That notational change must not be mistaken for a bound uniform in variable count. Its journal version is *Journal of Functional Analysis* 291(6), article 111555, dated 15 September 2026; that is a different paper from the 2026 three-author preprint.

Sources: <https://arxiv.org/abs/2506.04400v1>, <https://doi.org/10.1016/j.jfa.2026.111555>.

## 2. Necessary authored corrections

These are corrections to literal statements or compressed steps, not hidden assumptions.

1. **The ceiling 4 in Proposition 6.1(2) is false.** With `g=4`, `k=N=1`, `X_j=3/8` and `U_j=1`, the row norm is `3/4`, whereas `|1+sum X_j U_j|^2=25/4>4`. For fixed `g` the correct universal ceiling `(1+r sqrt(g))^2` follows from the row-column factorization. Use a smooth logarithm majorant on that entire interval. The example refutes the asserted pointwise ceiling, not the averaged-moment theorem.
2. **Tail integration requires a constant term.** If `F=0`, the printed integral of the tail is zero while `E exp(mF)=1`. A valid estimate is `E exp(mF) <= 1+|m| integral_0^infinity exp(|m|t) P(|F|>t) dt`. Treat `m=0` separately. This also fixes the negative-exponent sign issue in part (1), though negative row-ball moments are not claimed here.
3. **Logarithm signs must be corrected.** The power series for `log(I+T)` has coefficient `(-1)^(n+1)/n`. Theorem 6.2 prints `(-1)^n/n` in the definition of its logarithmic random variable. Its conversion of `sum Tr(S^n)/n` to `Tr log(I-S)` also needs a minus sign. Both are repaired explicitly in the companion reconstruction.
4. **Montel provides subsequences, not automatic convergence.** In addition, fixing arbitrary `B,D` after proving the initial identity only when all four tuples are small leaves a continuation step unstated. For the companion, use joint holomorphic variables `(A,Z)` with `Z=conjugate(B)`, the product of open row balls, compact-uniform Cauchy–Schwarz bounds, uniqueness on a nonempty small open set, and the identity theorem. The proof file gives the complete subsequence argument.
5. **The second determinant must be present in Theorem 1.6.** Its omission is confirmed in both the PDF/source and HTML. We use the unambiguous scalar special case of Theorem 6.2.
6. **Trace normalization in the FK line is inessential but inaccurate.** With the normalized FK determinant, `(Tr_k tensor tau) log(LL*) = 2k log Delta_FK(L)`, not `2 log Delta_FK(L)`. Both sides still vanish. The reconstruction fixes the normalization throughout.
7. **The general exact-centering assertion in the proof of Theorem 3.3 must not be imported wholesale.** For independent Haar `U,V`, `E Tr(U V U* V*)=1/N`, although the commutator is a nonempty cyclically reduced word. The pencil application only uses positive words and their inverses; phase invariance centers each such trace exactly. The reconstruction proves precisely this sufficient restricted version and makes no acceptance claim for the general unrestricted coefficient theorem.

The tests are exact or deterministic checks of these issues and elementary interfaces. They are not Monte Carlo evidence for an infinite-dimensional uniform theorem.

## 3. Fully proved repaired statements

The accompanying `FIXED_G_PROOF.md` proves, using explicitly identified established inputs:

* For every fixed `g,k`, every `0<=r<1`, and every `m>=0`, there is a finite `C(g,k,r,m)` such that all `g`-tuples with row norm at most `r` satisfy `sup_N E |det(I+sum X_j tensor U_j)|^(2m) <= C(g,k,r,m)`.
* For every fixed `g,k,l` and fixed `A,B` satisfying `rho(sum A_j tensor conjugate(A_j))<1` and the corresponding condition for `B`, the covariance limit equals `det(I-sum A_j tensor conjugate(B_j))^(-1)`.
* For fixed `g,k,l`, convergence is locally uniform on the product of the open row balls, when expressed in the holomorphic variables `(A,conjugate(B))`. This local statement supplies no uniformity over changing parameter dimensions.

The external inputs are the operator-valued free-group norm inequality used in the manuscript, the elementary functional-calculus Hilbert–Schmidt Lipschitz inequality, Meckes–Meckes concentration, Parraud's quantitative smooth trace estimate, and the Mingo–Śniady–Speicher Gaussian fluctuation theorem. The last three precise input statements were checked in their primary PDFs. The reconstruction verifies their use and all intervening steps; it does not reprove the full historical theorems.

## 4. Exact unresolved bridge and stopping point

Nothing inspected proves `sup_g C(g,k,r,1)<infinity`. Fixed-dimensional compactness does not establish it. The coefficient-bounded-family estimates retain a fixed alphabet; the corrected pointwise ceiling and the resulting cutoff can grow with `g`. Concentration itself is dimension-free in the number of unitary factors, but that fact alone does not make its composed Lipschitz and mean bounds dimension-free.

The companion identity yields boundedness in `N` for each fixed tuple, and local uniformity for each fixed `g`. Neither conclusion controls the union over all `g`. The optional explicit constant and monotonicity are also not proved by the inspected manuscript.

Closing the all-`g` bridge requires a further theorem, a new dimension-independent proof, or authoritative clarification that the intended OWR target fixes the tuple length and allows its constant to depend on it. Such work is outside this zero-turn verification. Stop here with 30005923 held, preserving the verified fixed-`g` coverage and separately crediting the fixed-parameter companion result.

## 5. Reproducibility and source handling

`PUBLIC_SOURCE_METADATA.json` records public URLs, byte counts, hashes, versions, and inspection scope. `verify.py` produces `CHECK_RESULTS.json`. No copied third-party text, PDF, dataset content, private sources, or private coordination material is included in the authored packet. `MANIFEST.json` hashes only the authored deliverables. No raw primary source is proposed for publication.
