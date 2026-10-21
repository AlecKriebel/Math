# Publication acceptance and limitations

Research completed 20 October 2026; publication package prepared 21 October 2026 UTC.

## Disposition

**PASS for the stated partial results and exact finite computations. Overall problem status remains UNSOLVED, 5/5 avenues completed.** “Independent” describes separately derived mathematical formulations and implementations within this work, not external peer review, formal proof verification, or a priority determination.

The accepted result is the finite plane branch-integrality optimization, its smooth/SNC and dual-web subclasses, the explicitly stated pencil families, and the conditional numerical budget criterion. It is not a general solution of Garcia-Fritz's geometric hypothesis question. The source correction is necessary: the catalogue's scalar-section premise is not equivalent to the primary question. Known transfer mechanisms and published conic-tangent cyclic-cover applications remain credited.

## Computational evidence

The final main generator has SHA-256

`3bc4ef94e6b43690688b449725a3312403851ad4e0b21038a34065688056c67f`.

The final authored example results have SHA-256

`626efa2f31bee992de97964546b7fd1e31daadaa66c091875423323a8c220a2d`.

The exact results cover 12 examples, 49 searched spaces, and 12 nonzero witnesses with full lower-twist search coverage. Independent sparse-division horizontal tensors and division-free E(P)−FQ blocks reproduce all 49 dimensions. Fourteen structural/regression cases, nine main rejection controls, and six coordinate controls supplement these checks. Replays compare all five original result JSON files byte-for-byte and match the recorded main output.

Publication controls additionally reject 17 invalid-input/witness/guard mutations in each Python mode, confirm a valid line witness, preserve transformed-conic dimensions 3 and 1, test independent normal-form additivity, and check split/product equivalence. Five corruptions of saved results are rejected separately in each mode: dimension, search coverage, zero witness, incorrect bidegree, and failure of branch divisibility. Both ordinary and optimized Python run the complete suite.

## Regression disclosure

The development version incorrectly used SymPy `Poly.rem` as a coefficientwise linear multivariate normal form. The first independent formulation shared that primitive. The transformed-conic coordinate check exposed dimension 2 instead of 3, and the old implementation acceptance was superseded. The repaired main code uses Gröbner normal forms; the independent methods use an explicit sparse lexicographic division algorithm and a division-free coefficient system. The final mathematical proofs do not depend on the defective primitive. No obsolete output is offered as final evidence.

## Publication-only edits

The three proof manuscripts `RESEARCH_REPORT.md`, `HIGHER_ORDER_AUDIT.md`, and `PENCIL_COVER_AUDIT.md` are unchanged. The source-gate link in `AUDIT_LOW_TWIST.md` was made package-relative without changing mathematical content.

Nineteen `assert` statements in three independent audit scripts became explicit `if not ...: raise AssertionError(...)` checks. Every condition and explicit diagnostic is preserved. Exact AST comparison verifies that these replacements are the only semantic changes in those scripts; in normal mode their behavior is equivalent, while optimized mode intentionally retains the checks. The main generator was not edited. The complete small diff and structural review are included.

The original audit receipt is preserved verbatim. Its hashes must not be confused with the guard-hardened publication files. The annotated receipt, edit ledger, and final manifest make both versions explicit. The replay report records computations performed in isolated copies, without overwriting the packaged evidence.

## What acceptance does not establish

- No algorithm for arbitrary unspecified complex coefficients is asserted; the implementation uses QQ only.
- A plane minimum does not verify an upstairs positivity cone, resolve arbitrary cover singularities, or list all integral curves.
- Pencil base-change examples are generally not finite morphisms to the plane; exceptional corrections are essential.
- A failed specified ramification budget does not rule out all other approaches.
- The current-source search is bounded and does not prove the absence of later literature.
- Reproducible exact computations support the declared finite instances, not untested asymptotic or generic-rank claims.

This package contains authored mathematical work and public verification metadata. It does not contain raw third-party sources, datasets, or private coordination records. The package preparation itself makes no queue change and performs no GitHub publication.
