# Permutation-Cell Auditing for Sequential Machine Unlearning

This project applies Noncommutative Comparative Statics (NCS) to a narrowly
scoped machine-unlearning audit problem:

> How can an operator falsify a claimed all-order approximation to a common
> retraining target without first computing that target?

The proposed audit clones one trained checkpoint, applies the same deletion set
through externally equivalent request orders, and measures the resulting NCS
relation-cell defect. A sufficiently large defect is a one-sided inconsistency
witness: by the triangle inequality, no common target can be close to every
observed order. Agreement is not evidence that deletion succeeded.

## Status

Solved application and paper complete. Problem selection, formal foundations,
reproducible computation, proof compression, novelty scope, and final PDF
layout each received a clean adversarial PASS.

## Main result

For a fixed observed set of deletion-route outputs \(Y\), the Chebyshev radius
is the sharp population lower bound on worst-route error to every otherwise
unconstrained common reset target:

\[
  \max_{y\in Y} d(y,t)
  \ge r_X(Y)
  \ge \tfrac12\operatorname{diam}(Y).
\]

Thus a pair gap above \(2\varepsilon\) falsifies a universal
\(\varepsilon\)-retrain-equivalence claim without computing the retrained
model. Agreement remains inconclusive.

The final ridge witness directly checks all 97,461 deletion pairs, executes all
six orders of one three-request set, verifies exact quadratic response order,
and demonstrates a family-wise-error-controlled stochastic MMD rejection.

## Artifacts

- Paper source: `paper/paper.tex`
- Rendered paper: `output/pdf/paper.pdf`
- Formal solution: `checkpoints/02_solution_foundations.md`
- Solved case study: `checkpoints/03_solved_case_study.md`
- Executable experiment: `examples/run_audit_case_study.py`
- Machine-readable results: `examples/results/audit_case_study.json`
- Literature collision map: `literature/COLLISION_MAP.md`
- Adversarial review record: `reviews/`

Reproduce the experiment from this directory with:

```text
./.venv/bin/python examples/run_audit_case_study.py \
  --output examples/results/audit_case_study.json
```

## Planned contributions

1. A sharp, target-free Chebyshev-radius lower bound on worst-route error.
2. A finite-sample MMD rejection test for stochastic unlearning outputs.
3. A Boolean-cube NCS presentation and an affine-basis completeness result for
   testing stateless affine deletion operators.
4. A closed-form ridge-regression cell defect for fixed-preconditioner,
   relinearized deletion updates.
5. Reproducible deterministic and stochastic case studies.
6. Explicit no-go results: a zero defect does not certify unlearning, and
   adaptive request histories need not define equivalent external paths.

## Claim boundary

The project does **not** claim novelty for:

- order dependence in gradient-ascent unlearning;
- influence functions or Newton-style deletion updates;
- metamorphic testing;
- Chebyshev centers, the triangle inequality, or MMD;
- general retraining-free certification of successful unlearning.

The candidate contribution is the particular NCS reduction from deletion-order
cells to a sharp, statistically testable, gold-standard-free **rejection**
certificate.
