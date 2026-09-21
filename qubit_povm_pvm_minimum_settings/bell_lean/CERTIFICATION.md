# Lean verification certificate — version 2

**PASS: The principal results, including the stated model conventions, have complete formal proofs in Lean.**

This certificate refers to the unchanged proof/verifier snapshot checked by the complete clean-extraction run below. It does not certify every auxiliary mathematical statement or alternative proof in the manuscript. The [historical September certificate](CERTIFICATION_20260911.md) remains historical.

| Check | Fresh result |
|---|---|
| Run | `20260921T145457Z-083d0c3b` |
| Started / ended UTC | `2026-09-21T14:54:57.661032+00:00` / `2026-09-21T15:08:27.933401+00:00` |
| Production mathematical modules | 68, rebuilt from fresh project outputs, followed by `Bell` |
| Theorem/lemma declarations | 837, including private helpers |
| Public transitive axiom audits | 826 / 826 passed |
| Expanded contracts | 78 examples across all seven required files passed |
| Protected source/verifier inputs | 104, unchanged through verification |
| Compiler controls | Valid proof accepted; invalid `False` proof rejected with a type error |
| Exact artifacts and preflight | All passed; 14 compiler-free preflight stages |
| Publication and review PDFs | Both rebuilt warning-free in the same reproduction |

Authoritative records: [kernel report](reports/runs/20260921T145457Z-083d0c3b/kernel_report.json), [axiom audit](reports/runs/20260921T145457Z-083d0c3b/axiom_audit.json), [statement contracts](reports/runs/20260921T145457Z-083d0c3b/statement_audit.json), and [protected source snapshot](reports/runs/20260921T145457Z-083d0c3b/source_snapshot.json). Source-snapshot file SHA-256: `5f65a3b6d423f525b9e55e905d517d5be2011bddda19e3094dae7071098934c9`. The run preserves every executed command, exit code and log hash. Historical receipts are not substituted for changed inputs. Top-level convenience receipts identify the same fresh run.

## What is proved

- Two inputs per party with arbitrary finite input-dependent outputs: equality of ordinary finite POVM and PVM convex hulls; one shared selector chooses complete projective strategies, including their joint states.
- One-input and at-most-two-input equality; minimum-setting classification; physical 3×2 separation; the stated simple and strengthened attained values. The physical projective SOS bound is `289/10` and implies the manuscript's bound.
- Stochastic channels decompose into deterministic functions with normalized nonnegative product weights; exact whole-table processing preserves the projective convex hull.
- Independent source strategies on arbitrary finite-dimensional complex inner-product spaces of local dimension at most two correspond to fixed-qubit matrices. The source density is an actual endomorphism of the tensor product with basis-independent positivity and trace one. Genuine local isometries, tensor transport and complement allocation preserve Born probabilities, measurement normalization and projectivity.
- Arbitrary finite outcome types transport to `Fin` by equivalence, preserving complete strategies, behavior tables and ordinary convex hulls. The combined Hilbert/finite-label model has the stated equality and a finite mixture of actual Hilbert-space PVM branches.

The [claim-to-declaration map](docs/CERTIFIED_COVERAGE.md) and [model conventions](docs/MODEL_CONVENTIONS.md) give exact quantifiers and boundary conditions, including empty labels, zero-dimensional spaces, unused outcomes and zero channel probabilities. No same-state simulation, equality of raw POVM/PVM sets, closure substitution or global POVM optimum is asserted.

## Independent interpretation review and manuscript

The [independent semantic review](../version2_completion_20260921/reviews/semantic_review.md) attempted to falsify the new source models, normalization, tensor/Born transport, common-selector mixture and degenerate cases. The [verifier review](../version2_completion_20260921/reviews/verifier_review.md) separately tested missing contracts, attributed declarations, failure receipts and package integrity. These are independent AI-agent reviews, not external human peer review.

[Manuscript correspondence](reports/manuscript_correspondence_v2.json) binds the revised TeX, PDFs and review evidence to this proof snapshot. The formal proof replaces general duality/KKT with deterministic physical score gaps, the full manifold/Hessian/inertia package with feasible curves and an exact score-gap identity, and the original projective-bound derivation with an operator SOS certificate. General duality, full manifold/Hessian/inertia, broader cone/rank statements and selected auxiliary discrimination/spectral/Appendix B calculations remain manuscript-only; see the precise list in the coverage map.

## Reproduction and trust boundary

Lean is `leanprover/lean4:v4.19.0`, compiler commit `6caaee842e9495688c1567e78c0e68dbb96942aa`. Mathlib is `c44e0c8ee63ca166450922a373c7409c5d26b00b`; all nine dependency commits are fixed and checked. Public theorem dependencies use only `propext`, `Classical.choice` and `Quot.sound`. No admitted proofs, `sorryAx`, custom mathematical axioms or source-level kernel bypasses are accepted.

The compiler/runtime, machine and separately provisioned compiled dependency cache remain trust assumptions. All project proofs are rebuilt; Mathlib is not independently rebuilt. Dependency Git pins and tracked-file cleanliness are checked; they do not independently authenticate a cached compiled artifact. Ordinary Lean linter warnings occur, but proof errors, recovered panics and failed contracts are rejected.

From a clean extraction, run `python reproduce.py --bootstrap`, or use `--dependency-cache /absolute/path/to/prepared/.lake/packages`. See [complete package instructions](../VERSION_2.md) and [Lean-only instructions](OFFLINE_RUN.md). The final local ZIP is separately checked by a further clean extraction, whose outside-the-ZIP receipt and hashes avoid a self-referential archive hash. No immutable release or new DOI is created.
