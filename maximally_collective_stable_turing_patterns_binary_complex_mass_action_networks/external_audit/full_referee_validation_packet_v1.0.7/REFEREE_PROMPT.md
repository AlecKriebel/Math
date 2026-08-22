# Independent post-submission referee audit

You are acting as an independent journal referee for the manuscript

> **Exact Diffusion Design for Maximally Collective Stable Turing Patterns in
> Binary-Complex Mass-Action Networks.**

Determine whether the stated results are valid.  Do not assume that the
authors' conclusions, proof maps, programs, stored certificates, archived
outputs, or prior `PASS` markers are correct.  A program passing is evidence
only for the assertions that its source actually checks; it is not by itself a
proof of a theorem.  Do not silently repair a gap.  If a repair is possible,
state it exactly and classify whether it changes a hypothesis, conclusion, or
headline claim.

## 1. Preserve and inventory the package

Work in a disposable copy because replay commands regenerate files.  Before
running code:

1. Record the package version, hashes, operating system, Python and dependency
   versions, and relevant external-tool versions.
2. Verify the outer and inner manifests.
3. Inventory the manuscript, supplement, source, proof aids, exact data,
   verifier source, tests, scripts, and baseline outputs.
4. Identify any private path, missing input, network dependency, undocumented
   prerequisite, or unpinned tool that could affect reproducibility.
5. Treat stored outputs as provenance only, not as an independent replay.

## 2. Read and reconstruct the mathematics

Read the main manuscript and supplement in full.  Use `review_maps/` only for
navigation and construct your own theorem-dependency map.  For every main
result record:

- exact hypotheses and quantifiers;
- parameter and dimension domains, including endpoint conventions;
- whether the conclusion is algebraic, spectral, stationary, local nonlinear,
  or global;
- every lemma, identity, certificate, or external theorem it uses;
- which steps are deductive, exact computer algebra, finite regression,
  floating-point computation, simulation, or citation-dependent.

Check, at minimum:

1. The indexed reaction topology, binary-complex mass-action realization,
   stoichiometric rank, steady-flux cone, semipositive conservation law, and
   complete positive-equilibrium Jacobian family.
2. The SCC exhaustion, including the direct (m=3) case and the (b=2a)
   edge-deletion case; Hurwitz stability of every smaller nonempty principal
   subsystem; and first instability at order (m=n-1).
3. The principal-minor diffusion-ray theorem: coefficient hypotheses,
   threshold existence and uniqueness, ordinary algebraic simplicity, and the
   exact positive-real-eigenvalue band.
4. The complete omission-minor table and the necessary-and-sufficient
   stationary diffusion law.
5. Every contrast lower bound, sharpness statement, optimum, and asymptotic
   claim.  Confirm that the scope is this topology and stationary crossings,
   not arbitrary wave instability, other networks, or a global Pareto
   frontier.
6. Homogeneous stability, critical right and left vectors, transversality,
   first-mode isolation, and exclusion of competing spatial modes.
7. The fixed-integrated-mass formulation, conservation gauge, Fredholm
   properties, reflection symmetry, center-manifold reduction, and distinction
   between the reduced flow and stationary Lyapunov-Schmidt equation.
8. The definitions and uniqueness of (w_0) and (w_2), all quadratic
   contractions, and the all-dimensional sign of the cubic coefficient.
9. The equilibrium-scaled family: admissible interval, physical rescaling,
   homogeneous and spatial certificates, transformed adjoint vector,
   transversality, gauge correction, componentwise positivity, branch
   stability, fixed contrast-product identity, and within-family minimum.
10. The robustness statement and its restriction to the
    positive-equilibrium realization manifold with one retuned scalar
    diffusion multiplier.
11. The functional-analytic justification of local exponential stability in
    the stated fixed-mass (H^1) phase space.

Explicitly inspect exceptional and boundary cases, including (m=3), (m=4),
both certified scaling endpoints, the high-dimensional regression near
(m=149), and every asserted equality case in a modulus certificate.

## 3. Audit the software semantically

Read every load-bearing generator and verifier before relying on its output.
For each entrypoint, state what it genuinely checks.  Examine whether:

- expressions are reconstructed from definitions or compared circularly with
  stored expected output;
- manuscript formulas and generated formulas share an unchecked common source;
- hard-coded coefficients or answers make a check vacuous;
- a check described as exact uses floating-point ordering, tolerances, or
  numerical eigensolvers;
- assertions are enabled and a failing child process propagates failure;
- denominators and domains are established before sign conclusions;
- clearing denominators preserves inequality direction;
- printed tables regenerate from the source polynomials named in the paper;
- equality cases are proved, rather than inferred from coefficient signs alone;
- finite tests are improperly used to support an all-dimensional claim;
- species ordering, deleted rows or columns, Fourier normalization, eigenvector
  normalization, and conservation gauges match the manuscript;
- current-profile data are separated from superseded profiles;
- simulations are used only as illustrations;
- mutation tests reject mathematically material changes;
- the replay invokes every advertised check and cannot hide a failed stage.

Trace representative central identities from the manuscript to code and
generated output.  Independently derive several without importing project
helper functions.

## 4. Execute the verification campaign

Run `bash RUN_COMPLETE_AUDIT.sh` from the packet root.  This preserving wrapper
creates clean disposable copies and orchestrates:

1. the full portable replay;
2. the minimal replay;
3. all 38 verifier entrypoints;
4. the exact and mutation tests;
5. symbolic, numerical-provenance, manuscript, stale-claim, PDF, package, and
   checksum audits;
6. representative finite-instance exporters and document/figure regeneration.

Rerun individual stages only when needed for diagnosis, mutation testing, or
an independently modified implementation.

Record every command, exit status, runtime, and relevant output.  Check that
cached files, pipelines, or stale generated artifacts cannot conceal a
failure.  Compare regenerated artifacts with supplied artifacts and explain
any byte-level or semantic difference.  A timeout, missing dependency, or
unsupported stage is **not checked**, never a pass.

## 5. Perform independent adversarial checks

Do not limit the review to author-supplied code.  At minimum:

- reconstruct small-dimensional stoichiometric and Jacobian matrices directly
  from the reaction list;
- enumerate principal blocks and omission minors independently in several
  dimensions;
- verify critical kernels, adjoint kernels, transversality, and selected cubic
  contractions independently;
- test random positive realizations and boundary cases as falsification
  attempts, while recognizing that sampling is not proof;
- mutate certificates and source coefficients to confirm rejection;
- search for denominator zeros, omitted sign assumptions, invalid endpoint
  inclusions, normalization errors, and extrapolation from finite cases;
- attempt counterexamples at and outside each claimed domain;
- check that the limitations accurately identify what is not proved.

Keep deductive proof, exact algebra, finite exhaustive computation, numerical
sampling, simulation, provenance, and consistency checks clearly separated.

## 6. Required referee report

### A. Executive verdict

Choose exactly one technical-validity category:

1. **VALID AS STATED**
2. **VALID AFTER MINOR CORRECTIONS** - only local corrections that do not alter
   a central theorem
3. **MAJOR REVISION REQUIRED** - an essential proof or reproducibility gap
4. **INVALID** - a central result is false or contradicted by a valid
   counterexample
5. **NOT FULLY VALIDATED** - evidence or execution access is insufficient

Separately recommend **accept**, **minor revision**, **major revision**,
**reject**, or **unable to recommend**.  Do not choose `VALID AS STATED` merely
because supplied programs pass.

### B. Claim-by-claim findings

For every principal theorem, classify it as independently verified, verified
conditional on a cited standard result, computationally reproduced, partially
checked, not checked, unsupported, or false.  Cite theorem/equation numbers and
file/line locations.

### C. Code and reproducibility findings

List commands and outcomes, dependency problems, independence or circularity
concerns, exact-versus-numerical distinctions, stale-data mismatches, mutation
results, and all incomplete stages.

### D. Defects

Classify each defect as fatal, major, minor mathematical, expository,
reproducibility, or cosmetic.  Support a mathematical objection with a
derivation, counterexample, failing execution, or exact unresolved step.

### E. Scope and confidence

State what was not verified and why, give calibrated confidence, and identify
the strongest remaining uncertainty.  If the entire result is valid, say so
explicitly and explain the independent evidence.  If it is not, or the audit
is incomplete, say that just as explicitly.

## Completion checklist

- [ ] Outer and inner hashes verified before execution.
- [ ] Main manuscript and supplement read completely.
- [ ] Independent theorem-dependency map constructed.
- [ ] Central claims checked against exact hypotheses and scope.
- [ ] All-dimensional proofs separated from finite evidence.
- [ ] Verifier source inspected before output was trusted.
- [ ] Circular/self-comparison checks sought explicitly.
- [ ] Exact arithmetic separated from floating-point evidence.
- [ ] Full and minimal replays completed in clean copies.
- [ ] All 38 verifier entrypoints, tests, mutations, and audits run.
- [ ] Tables and representative formulas traced to definitions.
- [ ] Small-dimensional reconstructions performed independently.
- [ ] Endpoint, exceptional-dimension, and equality cases checked.
- [ ] Counterexamples actively sought.
- [ ] Simulations treated only as numerical evidence.
- [ ] Functional-analytic stability argument assessed separately.
- [ ] Every incomplete check disclosed.
- [ ] Technical validity separated from journal recommendation.
- [ ] No conclusion inferred solely from stored logs or passing software.
