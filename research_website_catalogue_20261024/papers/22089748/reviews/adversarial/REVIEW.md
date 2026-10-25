# Adversarial review — Zenodo 22089748

**Updated disposition: a genuine defect in the published phase-proof path, with separate existing support for the main curvature result.** Supporting equation (35) has a false index-shift identity, leaving its derivation of Appendix A.31/A.36 incomplete. The same archived package contains a distinct forward-subset-chain proof that supports the symmetric-balanced curvature sign for every population size. Thus it would be too broad to say that this defect leaves the main theorem without all-order support. The false identity and the unproved debt comparison within that particular path remain recorded; no repair was attempted.

The package's existing alternative symmetric-sector proof, together with the stated sector decomposition and the separate standard/antisymmetric arguments, supports the main local-optimality conclusion. The strong-selection rigidity argument remains separately supported. This addendum narrows the scope of the previously recorded defect; it does not certify the incorrect phase identity or supply a replacement derivation of A.31.

## Publication binding and review independence

*Local Complete-Graph Optimality at Fitness Two and Strong-Selection Rigidity under Death–Birth Updating*, Alec Kriebel, August 2026, Zenodo record **22089748**, version **1.0.0**, DOI [10.5281/zenodo.22089748](https://doi.org/10.5281/zenodo.22089748).

| Published asset | SHA-256 |
|---|---|
| `complete_graph_extremality_db.pdf` — 30 pages, 235224 bytes | `ec8c09fbc4ef5f382272351f69721b6544c69f5d48bee961447e1907de2c0180` |
| `complete_graph_extremality_db_source_and_certificates.tar.gz` | `7220a09d7eb31fdd81c42b35cbeb680f8c1b257df3b3002d37146b00d81e588e` |
| `paper_i_complete_graph_extremality_referee_package_2026-08-23_r4.tar.gz` | `d8fc0193da78cd4907ca7a36950111c00c761966538d71a937320b1db23909fb` |

All five public assets, including the two detached checksum files, were checked against the fresh acquisition receipt by size, SHA-256 and Zenodo MD5. The three PDF copies within the two extracted archives are all byte-identical to the public PDF; there are no distinct extra reader PDFs to add to the 30-page reading. The full manuscript was read, including Appendices A–C and references. The debt comparison on PDF page 25 was also inspected visually against its TeX source.

The review used no sibling review or sibling control implementation, and no dedicated archived reviewer verdict. The necessary mathematical proof note opens with its historical assertion that the sector is closed; this unavoidable incidental status was read but excluded as evidence. The package README's assertions of prior independence were likewise not evidence. The initial exact controls and this index discrepancy were developed before communicating the target to the parent. After the first report was finalized, the parent supplied the path of an existing alternative mathematical proof located by another reviewer; no sibling report or code was read. The alternative note’s own opening historical “PROVED” status was necessarily encountered and was excluded as evidence. A process inventory later showed another agent's running launcher but exposed no mathematical assessment. Parent instructions then required stopping broad work and preserving the gap without attempting a repair.

This is AI-assisted mathematical review, not human peer review, formal proof-assistant verification or a novelty/priority certificate. Sources were never edited. All review files, downloaded pages, runtime and replay copies are confined to this review directory; caches are ignored. No publication, website, spreadsheet, Git or outreach action occurred.

## Exact theorem scope

The model is **directed**, not restricted to undirected or reversible graphs. A nonnegative loopless weighting has a positive incoming degree at every target. With source-to-target weight (w_{uv}), the normalized kernel has row indexed by dead target:

\[
P_{vu}=w_{uv}/\sum_{z\ne v}w_{zv},\qquad P_{vv}=0,\quad P\mathbf1=\mathbf1.
\]

A target dies uniformly. If its weighted mutant-parent fraction is (x=P_{vS}), a mutant replaces it with probability (rx/[1+(r-1)x]). Fixation is averaged over a **uniform singleton**. Independent rescaling of the incoming weights at each target changes no transition; transposing this convention or using nonuniform initialization changes the relevant problem.

Theorem 1 asserts, for each fixed (n\ge3), a positive-definite inverse-mean quadratic form on every loopless row-zero directed perturbation at (J_n), at exactly (r=2). It claims a strict local maximum, not global fitness-two maximality or a radius uniform in population size. Theorem 9 supplies the all-order positivity of its three irreducible sectors. The symmetric sector exists for (n\ge4), with (N=n-1\ge3).

Theorem 2 keeps a finite complete-support weighting fixed and expands as (r\to\infty). Its leading deficit is

\[
\rho(J_n,r)-\rho(P,r)
=\frac{1}{n^2(n-2)r}\sum_v\sum_{u<z\atop u,z\ne v}
\frac{(P_{vu}-P_{vz})^2}{P_{vu}P_{vz}}+O(r^{-2}).
\]

The equality class is (P=J_n), equivalently constant incoming weights at each target before normalization. Corollary 3 does not interchange (n\) and (r\). Theorem 5 is restricted to positive undirected triangles; Theorem 16 to the two stated symmetric weighted (K_4) families. Neither is a classification of all four-vertex weightings. The (n=2) normalized domain is a single kernel and ties the baseline.

## The precise defect

The affected source is

`r2_determinant/TRUE_INVERSE_RANK_SYMMETRIC_PHASE_CONTRACTION.md`,
SHA-256 **`0f1e270ecf696f350b8e1917c80238ca3a7f161415bebdcdf594355acaf0ce8a`**.

Its definitions (3), (4), and (31) are unambiguous:

\[
\omega_j=g_j^a=\frac{\binom{N-2}{j-1}}{2^{N-1}(N+1)},\quad
q_k=\frac{\binom{N-3}{k-2}}{2^{N-2}(N+1)},\quad
Y_k=\frac{2(k+1)}{3k(k-1)}.
\]

Here (1\le j<N), while (2\le k<N). The note says at lines 314–321, equation (35), that the bad debt is bounded “term by term” as

\[
\mathcal D=yq\le Yq
=\sum_{j=1}^{N-2}\frac{4(j+2)}{3(j+1)(N-2)}\,\omega_j.
\tag{published support 35}
\]

**The equality is false.** Substituting the definitions gives

\[
\frac{q_{j+1}}{g^a_{j+1}}=\frac{2j}{N-2},
\qquad
Yq=\sum_{j=1}^{N-2}
\frac{4(j+2)}{3(j+1)(N-2)}\,g^a_{j+1}.
\tag{direct index identity}
\]

The last factor is (g^a_{j+1}), not (g^a_j\). This is an identification of the erroneous algebra, not a proposed repaired all-order proof. The exact finite witness at **(N=40)**, within the theorem's phase-certificate range, is

\[
Yq-\sum_{j=1}^{38}\frac{4(j+2)}{3(j+1)38}\,g_j^a
=\frac{549755813107}{501063941451939840}>0.
\]

Thus one cannot replace the displayed equality by an inequality in the needed direction using the same (Yq) bound. The endpoint (N=3) happens to tie, so a smallest-order-only test would miss it. At (N=4) the discrepancy is (1/360); the (N=40) witness avoids reliance on an order below the phase argument.

The main PDF states the corresponding weaker debt inequality in **(A.31), page 25**, with the same printed (g^a_j) sum. The TeX source is `paper_db_extremality/appendices/A_sector_certificates.tex`, lines 513–528, SHA-256 **`6b5327a26c2d0f41436004942bfedc8b8ffb1f0e0d1316e234268867e7404d94`**. Its next step defines 

\[
\beta_N=\max_{1\le j\le N-2}
\frac{4(j+2)}{3(j+1)(N-2)}
\bigl[(11/25)\bar\ell_jt_j\bigr]^{-1},
\]

and ultimately concludes (\mathcal S_N\ge(1-\beta_N-\varepsilon_N)\ell f_0>0\) in (A.36), page 26. The supporting note explicitly cites (35) for the required implication (\mathcal D\le\beta_N\ell f_0\) at line 423. This is therefore part of the load-bearing all-order argument, not an unrelated exploratory calculation.

The published verifier `verify_true_inverse_rank_symmetric_phase.py`, SHA-256 **`7a1fa1f579c090cc32668392e67b9eb88e696b51ad602a90d069541e402aa512`**, constructs the printed `finite_debt_ratio` at lines 198–207 and checks its margins at lines 277–287. It independently solves the actual scalar only for (3\le N\le39). It checks several surrounding barrier formulas, but it does **not** test equation (35), compare the actual debt with the printed sum for all orders, or supply another derivation of this bridge. Successful margin checks concern the printed ratio; they do not establish that this ratio bounds the actual debt.

No alternative derivation of this specific all-order debt comparison was found in the phase proof note, manuscript appendix or its exact verifier. A later bounded inspection, requested by the parent, identified a separate existing forward-subset-chain proof of the same curvature sign. That proof does not use or establish A.31; it is described below. No new debt bound or repair was constructed.

**What is and is not established by this defect:** an intermediate equality in one supplied proof is demonstrably false, leaving that derivation of A.31/A.36 incomplete. It does **not** refute A.31 itself, Theorem 9 or Theorem 1. The package's existing regular-sector proof supplies independent all-order support for the symmetric sign, so the original broader statement that the main theorem lacked such support is superseded. Exact actual-debt probes at N=3,4,10,24,40,80,288 still satisfy the printed A.31 bound; they do not establish that bound universally.

## Independent checks before the submitted replay

`independent_controls.py` imports no submitted code and starts from the literal forward subset chain. It passed **1,685 exact assertions in 27 families**. It uses SymPy 1.14.0 for exact rational matrices and solves; no tolerance or floating-point positivity criterion is used.

For a directional kernel (P(t)=J_n+t\delta), the script expands each forward replacement probability to second order, independently solves the three triangular absorption equations, and converts the uniformly averaged fixation coefficient into the inverse-mean coefficient. This avoids the manuscript's stationary active-chain Hessian route. All first derivatives vanish and every tested second-order direction is suppressing. The resulting Frobenius-normalized sector eigenvalues are:

| n | Standard | Symmetric balanced | Antisymmetric balanced |
|---|---|---|---|
| 3 | 1/11 | absent | 1/9 |
| 4 | 87/640 | 3/208 | 57/640 |
| 5 | 8585/57314 | 359/26660 | 143/2100 |
| 6 | 453655/3078912 | 176345/14823936 | 1435/27648 |

The three published rows match exactly. The (n=6) row is additional direct-state evidence. Sums of canonical sector directions have the sum of their quadratic coefficients, testing the claimed vanishing cross terms. A separately transcribed signed standard quotient was solved through (N=15) and matches the direct-chain values where both are available.

For nonuniform directed positive kernels of orders three and four, the script independently constructs the union-dual transition law by inclusion–exclusion over the exact geometrically sampled parent set. It then computes the stationary distribution and verifies every proper-set coverage committor against the forward absorption system. A separately built one-sample active chain verifies its stationary inverse-size expectation equals (1/[n\rho(P,2)]\). The complete stationary active law also matches its printed formula. Thus the central phase/normalization identity is supported independently of the faulty later scalar estimate.

Direct expansion in (\epsilon=1/r\) on nonuniform complete directed orders three through five matches the strong-selection coefficient and the sum of squared incoming-row discrepancies. Independent incoming rescaling leaves the normalized kernel unchanged. Other negative/boundary controls cover the (n=2) degeneracy, the importance of uniform singleton averaging (individual starting-state derivatives need not vanish), and path/star/cycle strong-selection limits. Rational samples of nonuniform triangles and the (2+2\) (K_4) family have the stated signs and equality cases. These samples supplement, rather than prove, the universal low-order assertions.

`debt_index_control.py` is a second independent standard-library/Fraction implementation. It checks the false equality directly from the published binomial definitions, verifies the correctly shifted *identity* and solves the actual tridiagonal debt system at the stated probe orders. It verifies that residual of the tridiagonal solve is exactly zero. Its output clearly marks both `main_theorem_counterexample` and `A31_counterexample` as false.

## Mathematical reconstruction outside the affected bridge

The fair-geometric OR update has mutant probability (1-\mathbb E(1-x)^L=2x/(1+x)\). Its graphical union dual stays nonempty, and positivity off the diagonal gives irreducibility on proper nonempty subsets. The forward finite chain absorbs, yielding coverage by the stationary dual and the mean-set-size formula. The marked active-current calculation uses two distinct rectangular phase spaces, including the empty pre-sampling cache, and the factor of two from the stopping coin is correctly accounted for. Conflating the two phase orders would have changed the collision normalization; the direct checks distinguish them.

At the complete kernel, rank averaging commutes with the transition operator, and averaging either row-zero perturbation branch kills rank functions. This accounts for the zero first variation. The tangent embedding has the claimed column sums, and the decomposition into standard, symmetric balanced and antisymmetric balanced directions has the correct dimensions and orthogonality, including the absent symmetric sector at (n=3\). The standard proof uses its actual physical reward, not merely an auxiliary positive scalar. The antisymmetric recurrence is supported by the decreasing coupled rank-Poisson gradients. The phase-proof path for the symmetric sector has the recorded defect; the separate existing forward-chain proof has now been inspected and supports the same all-order sign.

For strong selection, the limiting complete-support chain fixes from any mutant set of size at least two; from a singleton its extinction probability is (1/n\). The transient limit is absorbing, so finite-dimensional analytic inversion justifies the expansion. A first-order loss from three or more mutants leaves at least two and contributes no first-order extinction. Pair loss contributes the two incoming competitor ratios divided by (n(n-2)\). Singleton first-step equations then give the total directed ratio sum. The elementary incoming-column reciprocal identity subtracts the complete-kernel baseline and gives exactly the displayed sum of squares. Its zero set makes every parent competition identical to (J_n\), not just asymptotically equivalent.

For noncomplete strongly connected supports, the cited primary theorem has the required directed/weighted, loopless, uniform-initialization scope. The non-strongly-connected case is separately handled by source components. A singleton cannot invade an initially resident source component; in a unique proper source component it must make a first gain before its own death. This supplies a strict upper gap to the complete limiting baseline. In undirected connected supports, once an adjacent mutant pair forms at infinite fitness, connected mutant growth is monotone and reaches fixation; the first gain/death race gives the support-degree limit. Fitness monotonicity follows from the two-variable monotone threshold coupling. These arguments preserve the fixed-graph versus growing-family quantifiers.

The triangle elimination is independent of the local theorem. Its diagonal-dominant transient equations and positive denominator support the displayed symmetric-polynomial sum of squares; the strict factor is nonzero away from equal weights. The two (K_4) orbit reductions and their printed coefficient certificates concern only the invariant families. The completed replay below reproduces their symbolic checks. No claim of a new proof for an unrestricted global fitness-two conjecture is made.

## Bounded addendum: existing alternative proof and its exact scope

After the initial verdict, the parent pointed to the already-published r2_regular_sector/LOCAL_COMPLETE_HESSIAN_THEOREM.md and its verifier verify_local_complete_hessian.py. Both were read completely. This is a different proof mechanism, based on the forward absorbing subset generator and a killed cut mode, rather than the active-chain phase/debt estimate.

Its domain is precisely the symmetric-balanced tangent sector: symmetric loopless row-zero perturbations at the complete stochastic kernel. Although the note calls this the “regular sector,” it is exactly the nonzero symmetric summand needed for Theorem 9, for every \(n\ge4\). No arbitrary directed conclusion follows from this note alone; the already stated decomposition and the separate standard/antisymmetric arguments supply those other summands.

The proof differentiates the forward committor. Its first derivative is \(-v_kq(S)\), with \(v\) solving a strictly diagonally dominant tridiagonal M-matrix system. The exact orbit moments reduce the averaged second derivative, per edge-square norm \(E=\sum_{i<j}\Delta_{ij}^2\), to \(-\mathcal D+\sum\ell_kv_k\), with every \(\ell_k>0\). The existing supersolution \(\bar v_k=(21/20)(n+k)f_k/(4n-2k)\) strictly dominates \(v\). Its cleared residual has 45 positive polynomial coefficients. The boundary coefficients multiplying the absent ranks vanish, so the same residual applies at the physical endpoints.

For \(n=6,7,8\), the existing total-response ratios are strictly less than one. For \(n\ge9\), a different polynomial \(H(q)\), with \(q=2^{k-n}\), certifies \(\ell_k\bar v_k<\mathcal D_{k-1}\). The proof splits the integer ranks into \(b=n-k-2=0,\ldots,4\) and \(b\ge5\); those cases cover every \(n\ge9\), \(2\le k\le n-2\). All small-\(b\) shifted polynomials have positive coefficients. For \(b\ge5\), positivity of \(H_0\) and \(128H_0+H_1\), together with \(0<q\le1/128\), proves the sign of \(H_0+qH_1\). Summation leaves two additional positive direct terms. Exact solves handle \(n=4,5\).

The bounded independent check alternative_scope_check.py verifies the existing bridge from the actual response/direct formulas to that polynomial. After dividing out the common positive factor \(\rho^2\), it finds

\[
\mathcal D_{k-1}-\ell_k\bar v_k
=
\frac{4(n-1)}
 {5n\,2^k(2n-k)(n-3)(n-2)(k+n-3)^2(k+n-2)^2(k+n-1)^2}\,H(q).
\]

Every displayed denominator factor is positive in the asserted range. It reconstructs the 45-term supersolution polynomial (minimum coefficient 16), the five degree-eight tail certificates (minimum coefficients 784, 696, 652, 630, 619), and both 45-term large-\(b\) certificates (minimum coefficients 19 and 2413). It also independently recovers the three finite closure ratios at \(n=6,7,8\). This checks the existing argument; it does not invent a substitute for the failed debt estimate.

The alternative result has the same normalization as the required symmetric curvature. Since \(\|\Delta\|_F^2=2E\), the inverse-mean eigenvalue \(\lambda_{\mathrm{sym}}\) converts to \(\Phi_n''/E=-4n\rho(J_n,2)^2\lambda_{\mathrm{sym}}\). This exactly gives the note's values \(-27/637\) and \(-367616/7498125\) at \(n=4,5\), agreeing with the independent forward-state checks already completed before the initial replay.

The earlier captured package run already executed this exact regular-sector verifier successfully. No new broad replay was performed for the addendum. The source hashes and bounded check are retained in alternative_source_bindings.json and alternative_scope_results.json.

**Revised scope:** the false Eq. (35) remains a real error and its particular A.31/A.36 justification remains unsupported. It does not leave the curvature sign without an existing all-order argument in the published package. The earlier report's broader inference about the main theorem is superseded, with its original files preserved under revisions/pre_alternative_scope/.

## Primary source interfaces

The original [Tkadlec et al. (2020) article](https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1007494) was checked directly. Its model specifies loopless possibly directed/weighted graphs, uniform initial mutant, target-first updating and strong connectivity. Its Theorem 1 establishes eventual strict suppression for noncomplete support and explicitly leaves weighted complete support as the residual case. Thus the import is used within its actual scope; the present manuscript supplies its own non-strong-support argument. This review does not use a generic summary of that theorem as evidence.

The original [Svoboda et al. (2024) article](https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1012008) supports the contextual existence of simultaneous-amplification families over a bounded fitness interval. It is not load-bearing for the local Hessian or strong-selection proof. The author's separate unrefereed companion/predecessor results were not accepted as proof of the current theorem. Primary page URLs, retrieval times and hashes are retained in `primary_reference_receipts.json`.

## Supplied replay and its limits

After the fresh literal-chain controls, I copied the 84-file referee package byte-for-byte into a private ignored directory and ran the exact advertised package launcher. Its pinned interpreter and dependency checks, package/source tree verification and negative controls proceeded. All mathematical verifier stages completed and emitted their success markers, including the finite symmetric solves (3\le N\le39), the printed phase-margin range (40\le N\le287), and its discriminant certificate. The internal cache remained empty as checked by the launcher. The PDF rebuild emitted the original SHA-256 and the final package-success marker.

The parent requested stopping broad replay upon confirmation of the defect. At the time the verified SIGTERM was delivered, the fast-running launcher had already finished all these checks and was in its own temporary-tree cleanup. Therefore the captured process exit is **143**, intentionally induced during cleanup, **not** an assertion failure. This is not described as a clean exit-zero replay. `replay_intentional_stop.json` records the exact process state, and the complete stdout/stderr and receipt preserve what had actually completed. No rerun was performed to manufacture a clean exit code.

A successful check transcript does not repair the gap: the verifier checks the wrongly indexed ratio's positivity margins but omits the false debt identity connecting those margins to the actual scalar. The discrepancy was obtained by independent arithmetic and persists even though the supplied tests pass.

## Exact remaining gap and disposition

The published phase/debt proof still needs a valid derivation of its A.31 bound or another explicit correction to that path. The false Eq. (35), its source lines, closed shifted identity and exact N=40 residual remain unchanged. This review does not establish A.31 or attempt its repair.

The existing separate regular-sector proof supports the same all-order symmetric curvature sign. Combined with the other reviewed sectors and the decomposition, it supplies positive support for the local-optimality conclusion; the specific phase-proof error must not be described as disproving that conclusion or leaving it wholly without an all-order proof. The global strong-selection argument also remains separately supported.

The defect remains recorded for the programme's publication decision. No human peer-review, formal proof-assistant or exhaustive novelty claim is made.
