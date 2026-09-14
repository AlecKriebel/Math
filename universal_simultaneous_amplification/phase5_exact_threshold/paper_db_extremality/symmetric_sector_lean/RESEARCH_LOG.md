# Symmetric-sector formalization research log

## 2026-09-14T04:42:56.728256+00:00

Read AGENTS.md, primary manuscript sections 02–04 and Appendix A, exact symmetric verifier, and prior assessment. Work is on main; existing unrelated changes preserved. Exact goals: S_N > 0 for integer N≥3, and R_n^(2)(δ)=‖δ‖²_F S_(n−1) for symmetric loopless balanced real matrices via the actual active-chain resolvent. No full fixation theorem or biological application is claimed.

Independent reviewers started: active-model translation; finite arithmetic and analytic tail; trust and dependency audit. Initial translation issue: at k=N−1, z=−2x; the coefficient representation is not a basis. An intertwining argument and separate invertibility suffice. Initial arithmetic opportunity: a sum-of-squares identity proves A.34 positivity directly.

Completion estimate: Stage 1 3%; Stage 2 1%; Stage 3 0%; overall 1%. These estimates measure verified mathematical scope, not effort.

## 2026-09-14T04:57:42.191687+00:00 — first mathematical checkpoint

Kernel-checked: concrete coefficient matrix invertibility for every N≥3; exact S3=3/208 and S4=359/26660 (also checked through N=9 during full range build); actual analytic phase margin beta_N+epsilon_N<1 for all N≥288; exact printed N40 margin. The complete alternating-resolvent bound and Schur elimination are proved as generic finite-matrix implications. Direct coefficient witnesses for every N=3…39 have been generated, and their Lean builds are running with bounded concurrency. The 248 finite-margin checks are also running.

New proof mechanisms: both discriminant arguments have explicit sum-of-squares replacements; Q has strict row contraction; subtracting neighboring rank equations gives an M-matrix on gradients, permitting elementary upper/lower barriers in place of A.3b's binomial inequality. The binomial normalization needed for the terminal gradient equation remains a concrete proof obligation.

Independent model review found no formula mismatch. Actual active-chain definitions, kernel action, rank perturbation source, and n=3 vanishing have compiling proofs in development. Full stationarity/invertibility, orbit normalization, and the final active-to-reduced identity are not yet proved.

Completion estimate: Stage 1 35%; Stage 2 25%; Stage 3 10%; overall 23%. No claim of the full local-optimality theorem.

## 2026-09-14T04:57:40Z — finite-margin and rank-bound checkpoint

The exact printed N=40 fraction is kernel checked by `exact_margin_40`,
reducing the actual `t` recurrence and finite `beta` maximum. The generic
integer-grid witness chain to actual `t` and `beta` is compiled. The 248
finite certificates are generated and undergoing kernel verification; no
finite-table completion is claimed yet. A separate diagnostic replay of
all grid inequalities passed. Estimated completion of this finite-margin
subtask: 85%; this is not an estimate that Stage 1 as a whole is complete.

The general radial upper bound (A.21), positivity of the actual recurrence
on physical ranks, and positivity of `lowerEll` for N≥4 are compiled in
`RankBounds.lean`. The polynomial remainder connecting the induction step
to the rational bound is proved by kernel-checked field algebra. Explicit
positivity of the `c` and `1-c` denominators is proved for N≥3. These are
concrete Stage 2 components, not an all-order scalar-positivity theorem.

## 2026-09-14T14:39:58.921004+00:00 — resumed and published core checkpoint

Resumed after interrupted tool sessions; no uncompleted build is treated as successful. The committed root module cleanly builds the general coefficient invertibility proof, S3/S4 witnesses and actual analytic phase margin. Pending small-range and 248-margin builds remain explicitly pending.

New adversarial finding: the direct Y pairing gives a shifted binomial-weight sum different from the printed A.31 debt bound. This is a missing implication in that derivation; it does not yet falsify the claimed debt bound or scalar positivity. A tighter supersolution is being investigated. No mathematical gap is being replaced by a hypothesis.

Completion estimate unchanged pending validation: Stage 1 35%, Stage 2 25%, Stage 3 10%, overall 23%.

## 2026-09-14T15:06:28.754235+00:00 — all-order assembly verified

Every small-system certificate N=3…39 and every phase certificate N=40…287 compiled, including the exact unique N40 minimum. `AllOrder.reducedScalar_pos` compiled and reports only the three permitted foundational axioms. All phase hypotheses are discharged for the actual blocks, gradients, occupations, source and reward. The actual general-n physical identity compiled and passed an independent model translation audit. Final positivity assembly, clean rebuild and publication are being completed.

The A.31 shortcut has been repaired: the sharper bad-occupation supersolution Z_k=2/[3(k−1)] proves the printed bound through exact binomial reflection. The discrepancy of the original direct Y pairing is kernel certified at N=4 as 1/360. This is a gap in one printed implication, not a counterexample to the claimed bound or positivity theorem. The repair preserves every beta definition and finite certificate.

Completion estimate: Stage 1 100%, Stage 2 100%, Stage 3 98%; overall mathematical implementation 99%, pending final clean-build and trust acceptance.

## 2026-09-14T15:09:32.294699+00:00 — integrated physical positivity checkpoint

`SymmetricComponent.lean` compiled the genuine all-order physical strict positivity theorem, nonnegativity for n≥3, and exact zero characterization. The n=3 absent-sector and physical n=4/5 normalization checks also compiled. No scalar sign, feature identity, inverse, or current formula is left as a hypothesis. All queried dependencies contain only propext, Classical.choice, Quot.sound. All 321 production modules are in the aggregate import closure.

Independent model and arithmetic reviews pass. A fresh trust reviewer, who authored none of the mathematical modules, is executing a clean project build and auditing 98 principal declarations, with source hashes fixed.

Completion estimate: Stage 1 100%, Stage 2 100%, Stage 3 100% for the requested symmetric component; release validation 90%, pending the independent clean build. This does not extend the scope to the full fixation theorem.
