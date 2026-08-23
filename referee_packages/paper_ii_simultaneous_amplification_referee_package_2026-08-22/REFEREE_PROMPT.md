# Neutral AI-referee prompt

You are acting as an independent journal referee for a mathematical-biology
manuscript and its supplementary verifier package.  You have not been told
whether the results are correct.  Treat the manuscript, source comments,
expected terminal output, hashes, provenance notes, research logs, and any
author conclusions as claims to be checked, not evidence of correctness.
Reach your own verdict: fully validated, valid after minor corrections, major
correction required, invalid, or inconclusive / review incomplete.

Work only on a disposable copy of the delivered package, preferably in an
unprivileged sandbox or container with no personal credentials.  Do not
contact any person, upload any file, or change any external system.  The
Python dependencies are included for offline installation; no package-index
access should be needed.  If document rendering needs a missing Tectonic
resource, restrict network access to Tectonic's standard resource-bundle
endpoint.  An optional read-only Git provenance check may use the stated
remote.  Record every command, exit status, software version, and independent
calculation used in the review.

## 1. Establish identity, completeness, and scope

1. Read `README_FIRST.md`, `VERSION.md`, and `PACKAGE_MANIFEST.sha256`.
2. Independently verify the whole-package manifest, detached source-archive
   checksum, and archive's internal `MANIFEST.sha256`.  Confirm that archive
   members are safe regular files, the extracted tree is byte-identical to
   the archive payload, and the convenience PDF equals the PDF inside it.
3. The source tag is annotated and unsigned.  If an independently obtained
   repository checkout is available, inspect `verify_git_binding.py` and run
   it to compare the tag object, peeled commit, all archived repository blobs,
   and their modes.  Optionally confirm the tag and peeled commit against the
   stated remote.  Neither check authenticates the signer, hosting account, or
   authorship; record that provenance limitation.  Failure to perform this
   optional check is not a mathematical defect.
4. Read the entire PDF and LaTeX source, including declarations, limitations,
   and references.  Make a theorem ledger of every hypothesis, quantifier,
   uniformity statement, asymptotic scale, equality or strictness condition,
   and claimed computational dependency.
5. Keep the central quantifier order explicit: one graph family is chosen
   independently of fitness; for every fixed fitness in the open interval,
   amplification is asserted only for sufficiently large family index, and
   that threshold may depend on fitness.

## 2. Verify the mathematics independently

The checks below identify known load-bearing points but are not exhaustive;
actively search for omitted assumptions, missing cases, circular steps, and
counterexamples elsewhere in the manuscript.  Do not infer a proof from a
successful program run.  Re-derive every
load-bearing step, checking state spaces, orientations, dimensions,
normalizations, denominator signs, stopping boundaries, error scales,
uniformity, and limiting order.

### Model, baselines, and construction

- Derive the weighted Birth--death and death--Birth transition probabilities
  from the update rules and check the complete-graph baselines.
- Verify the definition of simultaneous amplification and `R_sim`, including
  the order of the family, fitness, and sufficiently-large-index quantifiers.
- Verify that every graph in the construction is finite, connected, loopless,
  undirected, positively weighted on its stated edges, and selected without
  using fitness.
- Check all population scales, module counts, weights, and the exact dyadic
  weak-cut choice.  Audit the nonsingular-M-matrix and exact real-algebraic
  decision argument that makes the diagonal effective.

### Lumping and weak-cut trace

- Prove strong lumpability for both update rules from the orbit action; do not
  extrapolate the finite nine-vertex audit to arbitrary sizes.
- At zero weak coupling, identify the slow module-monomorphic states and prove
  transience of all fast mixed states.
- Derive the scaled Schur complement
  `A+B(I-Q_0)^{-1}C_0`, including its orientation and interpretation as one
  weak introduction followed by exact local absorption.
- Check compact-uniform convergence on fitness intervals and the final
  diagonal choice.  Ensure that no independent-lineage approximation is
  silently substituted for local absorption.

### Center and pendant asymptotics

- Verify each conditional intensity table for both update rules.
- Re-derive early establishment from one ordinary-core mutant, including the
  stopped embedded-walk estimate and every `K/C` and `r^{-K}` error.
- Audit continuous-time core confinement and every nested strip, entrance,
  synchronization, restart, success, escape, and block-duration stopping time.
- In the Bd synchronization argument, verify that every pendant phase stops at
  the next pendant-count change or upper-strip exit, that exit is assigned the
  favorable terminal trace level, and the stopped submartingale proves
  `O(m)` expected outcomes.  Check the separate `ell=0` two-phase boundary and
  the initial resident-hub state at `ell=m`; do not accept an unstopped
  pendant-hitting expectation.
- For Bd cleanup, confirm that conditional estimates at block starts justify
  the geometric strong-Markov recursion without an independence assumption.
- For dB cleanup, check the choice
  `T=beta_0(B_0) log C`: derive
  `m exp(-T)=O(C^(1/4-beta_0))`,
  `R_0 exp(-kappa T)=O(C^(-kappa beta_0))`, and verify that the two displayed
  inequalities yield `O(C^(-B_0-2))`.  Confirm that the hub-deactivation
  integral remains `o(1)` for the enlarged coefficient.
- Check the weighted graphical construction, deletion/suppression coupling,
  pendant renewal equations, and all claimed monotonicity signs.

### Reciprocal invasion and global sweep

- Reconstruct the killed-Green estimates and hub-excursion decomposition.
- Verify the dominating immigration--death process, its exponential Lyapunov
  inequality, the finite-horizon maximum bound, and the required order of the
  horizon and truncation limits.
- Confirm that the renewal argument proves
  `u_core^Bd(1/r)=o(C^-1)` and `J_H(1/r)=o(C^-1)`, not only `O(C^-1)`.
- Derive all four module-introduction rates under Bd and dB and check their
  directions.  Recover `Z_B=sigma(r^2-1)` and
  `Z_D=2r(r-1)/sigma` independently.
- Audit the macro chain with adverse center reversals retained.  Verify that
  all accumulated errors are `o(q/C)` and that `P_U^H=1-o(q/C)` at the scale
  needed for the complete satellite sweep.

### Response functions, optimization, and conclusion

- Independently derive the normalized first-order responses
  `B(r;sigma,lambda)` and `D(r;sigma,lambda)`, including center, pair,
  pendant, and baseline terms on one common scale.
- Check denominator positivity, the feasibility gap, quadratic minimizer,
  tangency equations, sextic root isolation, interval monotonicity, and the
  strict endpoint signs.
- Verify that optimality is claimed only for fixed positive parameters in the
  displayed first-order pair--pendant response model, not for singular or
  size-dependent choices or all graph families.
- Re-derive the rational-edge specialization, both endpoint margins, and its
  algebraic threshold.
- Check the final diagonal transfer from compact-uniform response estimates to
  the theorem's pointwise-in-fitness eventual amplification statement.  Look
  specifically for an illicit exchange of limits or a fitness-dependent graph
  choice.

## 3. Audit the software before executing it

Use `CLAIM_CODE_MAP.md` only as an index.  Inspect
`run_all_referee_checks.sh`, `verify_referee_package.py`,
`verify_git_binding.py`, `bootstrap_replay.sh`, `replay.sh`, `build.sh`,
`release_bundle.sh`, `bundle_manifest.py`, `requirements.txt`,
`tests/test_verifier_fail_closed.py`, both bundled wheels, all four verifier
programs, and every import before running them.  For each condition, identify
the exact manuscript statement it is intended to check and determine whether
it checks that statement rather than a weaker surrogate.

In particular, check that:

- state enumeration is exhaustive for the stated finite instance and the Bd
  and dB orientations match the manuscript;
- exact rational or symbolic arithmetic is used wherever exactness is claimed;
- numerical approximations audit display values only and do not carry an
  infinite quantifier;
- root counts and interval endpoints are exact and leave no gap;
- hard-coded expected expressions are independently derived rather than
  accepted because the same expression occurs in both premise and check;
- all failures propagate to a nonzero exit status and no exception or failed
  condition is suppressed;
- no verifier relies on a bare Python `assert`, optimized Python is rejected,
  and the disposable early/late mutation regressions genuinely exercise
  failure propagation;
- `verify_paper_claims.py` is recognized as a marker/integration audit rather
  than a proof checker; and
- no program is credited with proving the weak-cut or stochastic asymptotics.

The finite lumping program uses one rational nine-vertex instance at fitness
`3/2`; determine exactly what this tests and what it cannot establish.  Inspect
the two included pure-Python wheels, their hashes, metadata, and licenses, and
confirm that bootstrap installation disables indexes and requires the stated
hashes.  Python itself and the document toolchain are externally provisioned.

## 4. Execute and independently cross-check

After source inspection, run `./run_all_referee_checks.sh` from the package
root with Python 3.14.6 (set `BOOTSTRAP_PYTHON` if needed).  Preserve the full
transcript and exit status.  The command verifies package identity, checks the
stated document-tool versions, creates a disposable source copy, installs the
bundled hash-pinned Python dependencies offline, runs every delivered verifier
and fail-closed regression, rebuilds the source archive and PDF through the
standalone release entry point, and compares both byte-for-byte with the
delivered artifacts.

If a required tool is unavailable or has the wrong version, record the
limitation and run the remaining checks manually; do not report complete
execution.  Perform independent cross-checks not encoded by the supplied
expected answers: recompute representative transition rates and orbit sums,
derive the response functions in an alternative calculation, check exact
sextic signs/root counts independently, and test verifier failure behavior by
changing a disposable copy of at least one expected identity.

## 5. Report

For every finding, give severity, exact theorem/page/equation or file/line,
reasoning, and a counterexample or reproduction command where applicable.
Distinguish mathematical defects, code defects, reproducibility defects,
exposition issues, and optional suggestions.

Your final report must include:

1. a theorem-by-theorem validation table;
2. a claim-to-code coverage and execution table;
3. package, environment, command, and exit-status records;
4. all unresolved assumptions or checks you could not perform;
5. an explicit assessment of whether the proof and software support the same
   stated claims without overclaiming the certificate boundary; and
6. exactly one verdict: **fully validated**, **valid after minor
   corrections**, **major correction required**, **invalid**, or
   **inconclusive / review incomplete**.

Use **fully validated** only if your independent mathematical audit, code
inspection, complete execution, and alternative cross-checks all support every
stated result.  Do not treat this prompt, prior successful output, hashes, or
the author's conclusions as evidence for that verdict.
Use **inconclusive / review incomplete** when material mathematical, code, or
execution checks could not be completed and the available evidence does not
justify one of the four substantive verdicts.
