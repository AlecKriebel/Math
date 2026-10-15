# Likelihood / real-PD / probability adversarial audit

**Bounded verdict: PASS.** The submitted threshold mathematics is correct under the fixed-zero-mean, nondegenerate Gaussian convention: singleton K4,4 has (WMLT,MLT)=(2,4), and the genuinely tied K11=K22 model has WMLT=2. The second source hypothesis is realized by a concrete rank-two PSD preimage of pi(I8), and every ideal polynomial vanishes there, excluding a strict nowhere-zero signed-SOS separator. No mandatory mathematical repair was found in this family.

This verdict does not certify overall source scope, historical priority, novelty, eligibility, the separate algebraic-ideal family, claimed_solved status, or publication readiness. In particular, an exact tied-model MLT is not inferred from the ordinary graph theorem. The input head was c697b4a5cc62f3b8836d8c37d82b71a1d1c53fb7, and the full frozen PROOF.md hash was 69ffeade6c2ee758e3c2869d9c5b7dd607c9a1b6782f7ecebfb81d0812fdb676.

The complete checkable derivation is [the frozen independent reconstruction](/Users/alec/Documents/Math/draft_pr_descending_audit_20261002/audits/pr212_30005310/initial_review_20261015/likelihood_threshold_adversary_01/FROZEN_RECONSTRUCTION.md). Its pre-review hash and timestamp are in [the freeze record](/Users/alec/Documents/Math/draft_pr_descending_audit_20261002/audits/pr212_30005310/initial_review_20261015/likelihood_threshold_adversary_01/RECONSTRUCTION_FREEZE.json). It was frozen at 2026-10-15T09:46:06.267029+00:00 before the inherited FINAL_REVIEW.md was opened.

## Findings and falsification attempts

| Issue tested | Independent finding | Exact evidence / limitation |
|---|---|---|
| Actual concentration model | Correct RCON spaces: diagonal blocks diagonal, cross block free; extra tie K11=K22 only in the variant | Trace-statistic pairing checked symbolically, including the factor 2 on edge terms |
| Tied statistic projection | The sufficient statistic is s11+s22; no covariance diagonal equality is imposed | Symbolic pairing and both witness statistic maps |
| PD completion iff MLE exists uniquely | Correct, with no reliance on the disputed source threshold proposition | Frozen reconstruction §2 proves score necessity, uniform spectral compactness for sufficiency, strict convexity, and the PSD separating ray for failure |
| Arbitrary completion versus estimated covariance | Correct distinction; a matching PD completion need not invert into the model | Explicit P=I8+(E12+E21)/4 has the right statistics but inverse entry (1,2)=-4/15 |
| Exceptional rank-two witness | Correct, but insufficient alone; candidate supplies the necessary open data set | diag(J4,J4) has rank two and the same statistics as I8 in both models |
| Full-dimensional positive-probability success | Correct | Open box in R16; diagonal lower bound 9801/10000, cross bound 202/10000, PD margin 8993/10000 |
| Sample rank within the box | Exactly two throughout | Left/right row determinant at least 49/50 |
| Dependence on true covariance | Event probabilities can change, but zero/positive/one classifications do not for Sigma PD | Full joint Gaussian density is positive everywhere; an explicit positive lower bound is derived in the reconstruction |
| One-sample obstruction after genuine tie | Survives all color constraints and all zero cases | Singleton endpoints and edge 3–5; nonzero sparse PSD annihilator vv^T, or e3e3^T when x3=x5=0 |
| Second source hypothesis | Holds through an actual PSD preimage | Rank-two preimage of pi(I8); an exactly rank-three preimage is also constructed |
| First source mechanism | Impossible under the primary strict nonvanishing meaning | Every pulled-back ideal polynomial vanishes at the positive-diagonal Cholesky factor I8 |
| Credited singleton MLT theorem | Correct theorem, assumptions, formula, and specialization | Blekherman–Sinn v2 Theorem 2.7 and full relevant proof read; independently re-proved the K4,4 specialization |
| Transfer to tied MLT | No transfer made | The ordinary graph theorem has no tied diagonal constraint; candidate correctly refrains from an exact claim |

The open-set argument is in the original data space, not an incorrectly chosen full statistic-space neighborhood. All two-observation data matrices in the open box admit a PD statistic completion, so this establishes positive probability even though the displayed seed Gram matrix is singular and highly special. Gaussian graphical zeros and concentration color equalities do not constrain individual realized observations to a lower-dimensional data support.

The likelihood proof treats a matching completion only as an existence certificate. For P PD with the same statistics, tr(SK)=tr(PK) on the concentration space. If alpha=lambda_min(P), the objective is bounded below by the sum of alpha lambda-log(lambda) over the eight positive eigenvalues of K. A fixed sublevel therefore has every eigenvalue bounded above and away from zero, giving compactness and attainment. The score equations identify the optimizer's inverse as a matching completion, and the strict log-determinant Hessian gives uniqueness. Conversely, a separating nonzero sparse PSD matrix A with tr(AS)=0 produces the feasible unbounded-likelihood ray I8+tA. No unproved claim that the particular displayed completion must invert into the model is needed.

The one-sample ray gives a direct check of the genuine color tie. For v=x5 e3-x3 e5, vv^T has zero entries at both diagonal positions 1 and 2, so I8+t vv^T retains K11=K22. Its only possible nonzero off-diagonal entry is the allowed edge 3–5. If both endpoint data values vanish, e3e3^T supplies a nonzero ray. The obstruction is universal, not merely almost sure.

## Independent MLT verification beyond formula substitution

The full ordinary-graph theorem applies because both parts have size four and all concentration diagonals and cross coefficients are free. Its integer M is four: 6<8<=10, and min(M,5)=4. This credited formula is consistent with the independently constructed controls, not their premise.

For four-sample data X=[U;V] with invertible square U,V, any sparse symmetric annihilator A=[D C;C^T E] would imply U^T D U=V^T E V. The ten symmetric equations in eight diagonal weights are generically independent. At U=I4 and V rows e_i+2e_(i+1), a fixed 8-by-8 coefficient minor is -16 and det(V)=-15. Thus all exceptions lie in zero sets of explicit nonzero polynomials. Almost every four-sample Gaussian datum has no nonzero PSD annihilator and therefore admits a unique MLE.

For three-sample data, take U0 to be the first three columns of I4 and V0=H U0 for the displayed rational orthogonal Hadamard matrix H in the reconstruction. The six coefficient equations have a positive all-ones solution in their eight weights, and a 6-by-6 minor is -1/16. Fixing two weights and solving continuously for the other six preserves strictly positive weights in a full-dimensional data neighborhood. Equality of the resulting weighted Gram matrices extends to an orthogonal isometry and supplies a nonzero sparse PSD annihilator throughout that neighborhood. Hence three samples fail with positive probability. Monotonicity under adding sample outer products rules out an almost-sure threshold below four. This proves the exact singleton MLT independently of generic-rank/MLT equality and without depending on the general theorem's cited extreme-ray results.

## Reproducibility, independence, and inherited-review comparison

The freshly authored [exact controls](/Users/alec/Documents/Math/draft_pr_descending_audit_20261002/audits/pr212_30005310/initial_review_20261015/likelihood_threshold_adversary_01/exact_controls.py) pass 188 assertions, with [exact results](/Users/alec/Documents/Math/draft_pr_descending_audit_20261002/audits/pr212_30005310/initial_review_20261015/likelihood_threshold_adversary_01/exact_controls_results.json). These cover the actual trace pairings, boundary-aware PSD rays, all multiaffine extrema in the box bounds, eight rational interior samples with exact Sylvester minors, two actual low-rank preimages, and the two independent singleton MLT constructions. The equality of this assertion count with the original author's count is coincidental; the programs and categories are different. No floating-point rank, optimizer, or statistical simulation is used. The universal probability and neighborhood arguments are analytic.

After inspecting the entire author verify.py, I copied it and its required PROOF.md only into this folder's private/author_replay directory and executed that isolated copy. It passed its separate 188 assertions, exit 0 with empty stderr, and recreated verification.json byte for byte: SHA-256 24491be306428410cad6fe2b58b334a351e59f3789054613d746616e31110519. The authored [replay summary](/Users/alec/Documents/Math/draft_pr_descending_audit_20261002/audits/pr212_30005310/initial_review_20261015/likelihood_threshold_adversary_01/AUTHOR_REPLAY_SUMMARY.json) records input and output hashes. All third-party replay code, copied proof text, and raw replay output remain under private/ and are excluded from the safe authored manifest.

Only after freezing the independent reconstruction did I read the full inherited FINAL_REVIEW.md, hash c7fdb11c3cb1eecd6778acffcbf5973f8e73d7a213488a5caea2e12e20e19846. Its statistical conclusions agree with this reconstruction. I challenged rather than adopted its likelihood paragraph by supplying a uniform compact-sublevel proof and an explicit completion whose inverse lies outside the model. I also checked its true-covariance, data-openness, exact-rank, zero-component, signed-SOS, and theorem-transfer assumptions directly. No statistical disagreement survived. Its 1,808-assertion independent checker was not executed in this family and is not counted as independently reproduced here. Its broader source-scope and publication disposition are not premises or conclusions of this bounded report.

The parent later reported other families' statuses and identified a new priority-related primary source. Neither was used as a proof premise. Historical priority remains a separate disposition; no research priority conclusion follows from these threshold checks.

## Conventions and exact remaining gaps

No mandatory repair is needed for this threshold family. For a standalone presentation, retain or strengthen the following precision:

- Fix S=(1/r)XX^T with a known zero mean before quoting numerical sample thresholds. Under an estimated unconstrained mean, centered Gaussian scatter has r-1 degrees of freedom: the corresponding ordinary thresholds become (3,5), and the tied weak threshold becomes 3. This is a different sample-count convention.
- Make clear that a PD statistic completion is a feasibility certificate; it need not be the inverse of a feasible concentration matrix. The optimizer supplies the special completion after solving the score equations.
- Define the separator's nonvanishing as nowhere zero on the positive-diagonal Cholesky domain. Merely being a nonzero SOS polynomial would not be excluded by a zero at I8.
- Preserve the restriction of the exact MLT=4 credit to the singleton model.

The strongest verified claim is the displayed statistical pair and tied weak threshold, together with a literal real-PD intersection realized by actual low-rank PSD matrices. Conditional on the separately checked ideal premise selecting n=3, WMLT=2 contradicts the numerical equality WMLT=n in the report's second scenario. Whether that is the historically intended question, a repaired Boolean statement, a four-cycle restriction, or a publishable novel result is not adjudicated here. The exact MLT of the tied model and any probability value between the thresholds remain uncomputed. No outside communication was initiated or drafted, and no Git, PR, queue, publication, shared tracker, database, or parent artifact was mutated.

Primary-source coverage and hashes are recorded in [SOURCE_COVERAGE.md](/Users/alec/Documents/Math/draft_pr_descending_audit_20261002/audits/pr212_30005310/initial_review_20261015/likelihood_threshold_adversary_01/SOURCE_COVERAGE.md). The audit is complete in its bounded family; completion percentages in the log refer only to this audit.
