# PR1156 / problem 30003650: extremum and closure adversarial audit

Audit completed: 2026-10-22 UTC. This report concerns mathematical validity within the stated definitions. It makes no priority or publication-readiness claim.

## Verdict and exact scope

**No mathematical defect found in the central theorem or its exact-ordinary-rank refinement.** Independently reconstructed arguments establish

\[
p_n^+=p_n\quad(n\ge1),\qquad P_{n,r}^+=P_{n,r}\quad(1\le r\le n).
\]

The maxima are attained, including the singular exact-rank strata. The strongest validated result is the boundary-inclusive pair of congruence identities in candidate Theorem 4, from which these extrema follow. The remaining mathematical gap is the separate general determination of the maximum finite difference `cp^+(A)-cp(A)`. Nothing here determines that function for all orders, computes every ordinary maximum `p_n`, or establishes priority.

Target identity is pinned to immutable head `57c07523247d0de1a2fbb76f3243d0369caff682`, base `293f0c3d87e07532755d3202e535490ea07e2056`, candidate path `unsolved_math_prioritization/attempts/30003650/PROOF.md`. The full candidate is 11,301 bytes with SHA-256 `a2486250c2ddd7dc0e75cbf7275c59628a7b24f1f227e6432890369de96bacdb`. The parent preproof lead check at 2026-10-22T00:14:15.439269+00:00 reported 181 ledger rows and zero identifier/CP-plus/positive-factor-rank leads. That gate is not a novelty certificate. No historical mathematical audit or acceptance was consulted.

## Independent reconstruction

Work in real symmetric `n` by `n` matrices with `A=BB^T`, with columns of `B` nonnegative for CP-rank and strictly positive for finite CP-plus-rank. Exclude `A=0` from the extrema. The integer minima exist whenever the appropriate finite factor exists, by well-ordering.

**Finite conic reduction.** Put `N=n(n+1)/2`. If more than `N` nonzero vectors `v_i` occur, the matrices `v_i v_i^T` are linearly dependent. With current positive weights `w_i`, take a nonzero dependence `c` and choose its sign to have a positive component. Then

\[
 t=\min_{c_i>0}w_i/c_i,
 \qquad w_i'=w_i-tc_i
\]

leaves the represented matrix unchanged, keeps every weight nonnegative, and annihilates a weight. Discard zero weights and repeat. If every original vector was strictly positive, every retained vector multiplied by its positive square-root weight remains strictly positive. Thus finite positive-factor ranks also admit the same dimension bound. Repeated and proportional vectors cause no exception. Consequently nonempty attainable-rank sets lie in a finite integer interval, and each has an actual largest member.

**Closed sublevels and the correct local inequality.** For fixed `k`, any sequence `A_m=D_m D_m^T` of CP-rank at most `k` may use zero padding to fix the factor shape `n` by `k`. Convergence of `A_m` bounds `trace(A_m)=||D_m||_F^2`. A factor subsequence converges in the closed nonnegative orthant, giving `A=DD^T`. Hence `F_k={A:cp(A)<=k}` is closed. If `p=cp(A)>0`, then `A` lies outside `F_(p-1)`, so every sufficiently close CP matrix has CP-rank at least `p`. This remains valid at singular points. It is lower semicontinuity; the proof never needs the opposite direction.

**Positive direction.** For `S_t=I+tJ`, `t>0`, each nonzero nonnegative vector `d` satisfies `S_t d=d+t(sum_i d_i)e>0`. A minimal factor has no zero column. Thus for `X_t=S_t A S_t^T`,

\[
 cp(X_t)\le cp^+(X_t)\le p.
\]

As `X_t` converges to `A`, closedness of `F_(p-1)` supplies `cp(X_t)>=p` throughout a sufficiently small positive interval. The two ranks equal `p` there. The eigenvalues of `S_t` are `1+nt` and `1`, so its invertibility preserves ordinary rank. No positive definiteness is assumed.

**Negative direction.** Take a minimal strictly positive factor `B` of a nonzero `A`, with `q` columns. Column sums `s_j` are positive and the finite minimum

\[
 \alpha=\min_{i,j}B_{ij}/s_j
\]

is positive, with `alpha<=1/n`. For `0<t<=alpha/2`, `T_t=I-tJ` gives `T_tB>=B/2>0`. Also

\[
 T_t^{-1}=I+\frac{t}{1-nt}J>0.
\]

Thus `C=T_t A T_t^T` has a strictly positive factor with `q` columns. A minimal nonnegative factor `D` of `C` has no zero column; hence `T_t^{-1}D` is strictly positive and factors `A`. Therefore

\[
 q=cp^+(A)\le cp(C)\le cp^+(C)\le q.
\]

Both ranks of `C` equal `q`, and invertibility preserves ordinary rank. This proof uses no semicontinuity of CP-plus-rank and no interior hypothesis. A nonminimal finite positive factor also suffices to obtain the upper bound `cp^+(A)<=p_n`.

**Actual extrema on exact rank strata.** The set `E_r={cp(A): A in CP_n, rank(A)=r}` is nonempty because it contains a diagonal rank-`r` example, and is a subset of `{1,...,N}`. Its largest member is attained by the definition of `E_r`; closedness of the stratum is irrelevant. Start with such a maximizing `A` and use the positive direction to attain that value with a finite strictly positive factor, at the same ordinary rank. Conversely, the negative direction realizes every finite positive-factor rank at ordinary rank `r` as an ordinary CP-rank at rank `r`. These two comparisons prove equality of the maxima and their attainment. Applying the same reasoning without an ordinary-rank restriction proves the unrestricted equality.

## Adversarial boundary checks

| Potential obstruction | Resolution |
|---|---|
| `n=1` | A positive scalar has both ranks one; both scalar congruences are valid. |
| Ordinary rank one | A zero coordinate can preclude a positive factor, but positive congruence removes the zero coordinates while preserving rank one. For a positive rank-one generator, both ranks are one. |
| Singular positive factors | A strictly positive `n` by `r` full-column-rank factor yields a singular matrix when `r<n`; neither congruence requires invertibility of `A`. |
| Zero columns or repeated columns | Minimal factors have no zero columns. Dependencies caused by duplicates are handled by the conic weight reduction. |
| Zero matrix | It is explicitly excluded before forming `alpha`, column sums, or positive-rank extrema. |
| Positive-factor domain is nonclosed | `(1,epsilon)(1,epsilon)^T` has CP-plus-rank one for `epsilon>0`; its limit has a zero diagonal entry and cannot have a strictly positive factor. The argument never assumes this domain is closed. |
| Exact-rank strata are nonclosed | `diag(1,epsilon)` has ordinary rank two before converging to rank one. Attainment uses finite attainable integer values, not a compact stratum. |
| Wrong semicontinuity direction | CP-rank may drop at a limit; the needed assertion is that nearby ranks cannot lie below the rank at the fixed base point. Closed sublevels give exactly this assertion. |
| A universal negative parameter independent of `B` | False: with `t=1/10` and `B=(1/100,1)^T`, the first coordinate of `T_tB` is `-91/1000`. The candidate instead uses the valid factor-dependent `alpha/2`. |
| Finite versus infinite CP-plus-rank | The negative direction starts only with a finite strictly positive factor. No bound is asserted for the infinite values. |
| Singular matrices lie on the cone boundary | Every singular positive-semidefinite matrix is on the PSD boundary; complete positivity lies inside that cone. The argument constructs boundary examples directly. |

The authored exact-rational program contains 17 finite controls for these algebraic and edge mechanisms. It was inspected before execution. Only three newly created read-only private copies were executed, in normal, `-O`, and `-OO` modes, with byte-identical successful output and zero stderr. Explicit checks raise exceptions and do not disappear under optimization. These controls do not replace the universal proofs or claim to solve general factor minimization. The public `EXACT_CONTROL_RESULTS.json` pins the source and outputs.

## Primary-source scope and credited facts

The original [Oberwolfach report](https://ems.press/content/serial-article-files/46715), printed pp. 3082-3083, presents the gap maximum and finite CP-plus maximum as separately numbered questions. The latter was bounded between `p_n` and `p_n+1`. Its displayed factor dimensions conflict with `BB^T`; the consistent vector definition in the author paper resolves this by taking `n`-vectors as factor columns. The separate full answer to Question (2) is not disqualified by leaving Question (1) unresolved.

The [complete author manuscript](https://api.newton.ac.uk/website/v0/events/preprints/NI14088) is dated November 4, 2014; [journal metadata](https://www.sciencedirect.com/science/article/pii/S0024379515003304) identifies the 2015 LAA publication, volume 482, pp. 191-206, DOI `10.1016/j.laa.2015.05.021`. Rendered manuscript pp. 4, 6, 7, and 8 were inspected. Corollary 3.4 applies to entrywise-positive CP matrices if `n<=3` or `cp<=2`. Theorem 4.9 assumes cone interior. Theorem 5.1(1)-(4) distinguishes boundary, interior, and unrestricted finite maxima; (5) gives `p_n=n` for orders 2-4, (6) gives `p_n>n` for `n>=5`, and (11) supplies interior matrices with ranks `k-1,k` for each `n+1<=k<=p_n`. Its proof states `p_5=6`. These scopes support every credited low-order and gap fact needed here. No statement from Lai-Yoshise is load-bearing in the candidate theorem or in this audit.

The remaining gap bounds follow transparently: finite positive factors make all entries positive; Corollary 3.4 gives `g_1=g_2=g_3=0` (with order one elementary) and forces any nonzero gap to start at ordinary CP-rank at least three. The maximum theorem then gives `g_4<=1` and `g_n<=p_n-3`; Theorem 5.1(11) with `k=n+1` supplies `g_n>=1` for `n>=5`. Ordinary rank bounds CP-rank from below, giving `cp^+-cp<=P_(n,r)-r`, and the positive-definite specialization gives `p_n-n`. Row duplication preserves both factor ranks: extension gives one inequality and principal restriction gives the reverse. Hence the claimed nondecreasing property of `g_n` also holds.

## Independence, artifacts, and limitations

All written artifacts and executed task code were confined to this audit folder. No candidate, service, Git index, reference, pull request, GWS, or external-communication mutation occurred. No sibling agent was contacted. Fresh third-party PDFs, extracted text, rendered pages, and raw execution output remain in `private/`; public material consists of authored reasoning, authored checkable controls, metadata, and content pins. The manifest hashes the completed artifacts and intentionally omits any self-hash.

Audit completion: 100% for the assigned closure/extremum verification. Exact remaining research gap: determine the separate maximum-gap function beyond the stated conclusions. No comprehensive current-literature review can be inferred from this focused validity audit, and no priority conclusion follows from it.
