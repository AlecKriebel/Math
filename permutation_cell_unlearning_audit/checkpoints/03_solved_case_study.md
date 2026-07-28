# Checkpoint 3 — Solved Application

**Date:** 2026-07-28  
**Status:** PASS after adversarial computational and narrative review

## 1. The novel applied problem

Consider a stateful approximate machine-unlearning service. It claims that,
after any permitted ordering of a fixed set of deletion requests, its terminal
model is within a declared tolerance \(\varepsilon\) of one common model that
would have been obtained by reset retraining on the retained data.

The audit problem is:

> Can an operator soundly falsify this universal all-order
> retrain-equivalence claim without computing the retrained reference model?

This is not the already-studied question of whether unlearning order can
matter. It is the narrower oracle-free decision problem of extracting a
quantitative, target-independent rejection witness from that order dependence.

## 2. NCS solution

Treat two deletion orders as the boundary paths of an NCS relation cell. If
their outputs are \(z_{ij}\) and \(z_{ji}\) in a declared metric, then every
common target \(t\) obeys

\[
  \max\{d(z_{ij},t),d(z_{ji},t)\}
  \ge \frac12 d(z_{ij},z_{ji}).
  \tag{3.1}
\]

Thus the target-free audit:

1. clones the same starting state;
2. runs the two externally equivalent orders;
3. measures their endpoint separation; and
4. rejects a universal \(\varepsilon\)-claim whenever that separation exceeds
   \(2\varepsilon\).

For more routes, the sharp output-only population bound is their Chebyshev
radius. Half the observed diameter remains a sound lower bound when computing
the exact radius is inconvenient.

The answer is one-sided. A positive bound above tolerance proves the universal
claim false. A small or zero bound is inconclusive.

## 3. Inspectable ridge witness

### 3.1 Data and protocol

The reproducible example uses the 442-by-10 diabetes design matrix bundled
with scikit-learn. Its response is population-standardized. This is a
mathematical, non-clinical example; no predictive or population-generalization
claim is made.

The fitted state is the ridge minimizer

\[
  \theta_D
  =
  \left(\lambda I+X^\top X\right)^{-1}X^\top y,
  \qquad \lambda=0.05.
\]

From that state, request \(i\) applies the fixed-preconditioner relinearized
update

\[
  U_i(\theta)
  =
  \theta+H^{-1}x_i(x_i^\top\theta-y_i),
  \qquad H=\lambda I+X^\top X.
\]

This is a transparent approximate protocol, not a claim about the internal
update rule of a deployed unlearning product.

The experiment exhaustively screened all
\(\binom{442}{2}=97{,}461\) record pairs using the closed-form relation-cell
defect. The screen is exploratory. It selected a witness before any stochastic
replicates were generated; it is not used to claim population prevalence.

### 3.2 Pair result

The strongest Euclidean cell was records 32 and 322. Direct route composition
and the analytic commutator agreed to absolute error
\(1.51\times10^{-15}\). The endpoint separation was

\[
  \|z_{32,322}-z_{322,32}\|_2
  =
  0.0272943461.
\]

In the retained-data Hessian norm, the separation was

\[
  \|z_{32,322}-z_{322,32}\|_{H_{-32,-322}}
  =
  0.0115529959.
\]

Before calculating any reset target, PC-Audit therefore certifies

\[
  \max_\pi
  \|z_\pi-\theta_{-32,-322}\|_{H_{-32,-322}}
  \ge
  0.00577649793,
  \tag{3.2}
\]

and

\[
  \max_\pi
  \left[
  F_{-32,-322}(z_\pi)
  -
  F_{-32,-322}(\theta_{-32,-322})
  \right]
  \ge
  1.66839642\times10^{-5}.
  \tag{3.3}
\]

Only after computing these target-free quantities does the script solve for the
exact retained-data ridge solution as a validation oracle. The two actual
parameter errors in the Hessian norm were 0.0102969 and 0.0107386, both
consistent with (3.2). Their objective excesses were
\(5.30130\times10^{-5}\) and \(5.76588\times10^{-5}\), also consistent with
(3.3).

The exact Pythagorean decomposition was

\[
  5.53359\times10^{-5}
  =
  3.86520\times10^{-5}
  +
  1.66840\times10^{-5},
\]

up to \(6.61\times10^{-19}\) absolute numerical error. Hence 30.15% of the
mean two-route objective excess was the exactly identifiable antisymmetric
order component; the remaining midpoint error could not be inferred without
the target.

### 3.3 Three-request result

For the selected set \(\{32,322,141\}\), all six deletion orders were executed
from the same fitted state. In the retained-Hessian metric:

- the endpoint diameter was 0.0222175847;
- the target-free half-diameter lower bound was 0.0111087924;
- the numerically computed minimum-enclosing-ball radius agreed with that
  value to less than \(10^{-15}\); and
- the actual worst exact-target error, computed only for validation, was
  0.0300663494.

Thus the target-free route geometry recovered 36.95% of the actual worst-route
error in this witness, without using the reset solution. The diameter was
supported by the orders \((322,32,141)\) and \((141,32,322)\).

All reported geometric values are ordinary double-precision calculations, not
interval-arithmetic certificates. The half-diameter inequality itself is
exact; a high-assurance deployment should propagate numerical error or use
verified arithmetic.

## 4. Response-order prediction

With update amplitude \(\tau\), the theory predicts an exact quadratic cell
defect. For the selected pair, the measured Euclidean defects at

\[
  \tau\in
  \{1,\tfrac12,\tfrac14,\tfrac18,\tfrac1{16},\tfrac1{32}\}
\]

were, respectively,

\[
  2.72943\times10^{-2},
  6.82359\times10^{-3},
  1.70590\times10^{-3},
  4.26474\times10^{-4},
  1.06619\times10^{-4},
  2.66546\times10^{-5}.
\]

The fitted log--log slope was \(1.9999999999997464\), confirming the predicted
NCS response order \(2\) to floating-point precision.

## 5. Complete affine-cell reconstruction

Because this ridge protocol is affine, the full ten-dimensional cell defect
was reconstructed from one base state and ten coordinate probes. Compared
with the analytic affine defect:

- the Frobenius error in the reconstructed linear part was
  \(4.26\times10^{-14}\);
- the constant-part error was \(1.39\times10^{-13}\); and
- 1,000 random points in the probe simplex all respected the theorem that the
  maximum defect norm occurs at a vertex.

This validates the finite affine-basis audit in a setting where the affine
promise and state-injection access are genuinely available.

## 6. Stochastic-law witness

The same pair was used to define two route laws conditional on the fixed fitted
checkpoint. Each complete route output received fresh independent isotropic
Gaussian noise in retained-Hessian coordinates. This is a deliberately powered
synthetic illustration: the noise scale and Gaussian-RBF bandwidth were
effect-calibrated from the deterministic witness, then fixed with the pair,
tolerance, sample count, and confidence level before random-number generation.

For 3,000 replicates per route, \(K=1\), and family-wise
\(\delta=0.05\):

\[
  \widehat{\operatorname{MMD}}=0.612769,
  \qquad
  e_a=0.0678483.
\]

The simultaneous pairwise lower confidence bound was

\[
  L_{12}
  =
  [0.612769-2(0.0678483)]_+
  =
  0.477073.
\]

For a declared common-target tolerance \(\varepsilon=0.10\),
\(L_{12}>2\varepsilon=0.20\). Therefore, with family-wise error at most 0.05,
the data reject the claim that both conditional route laws are within MMD
distance 0.10 of one common conditional reset law. Equivalently for this
two-route case, the radius lower bound was 0.238536 and crossed the radius
threshold 0.10.

The exact MMD under the deliberately Gaussian simulation was 0.615291, which
lies above the realized lower confidence bound. This one draw is a consistency
check, not a Monte Carlo estimate of coverage; the coverage guarantee comes
from the finite-sample theorem. The closed form was used as a validation
oracle, not as an input to the test.

## 7. What was solved

The case study supplies a complete constructive answer to the applied problem:

- an operator can turn externally equivalent deletion permutations into an NCS
  relation-cell audit;
- the observed route geometry yields a target-free quantitative lower bound on
  the worst error to every common reset target;
- for the named ridge protocol, the defect is available in closed form and has
  exactly quadratic response order;
- a six-route example demonstrates the multi-route Chebyshev geometry; and
- a bounded-kernel finite-sample rule rejects the analogous stochastic-law
  claim with controlled family-wise error.

The result proves usefulness through falsification power, not through positive
certification. It does not establish that the protocol forgot the records,
that every order-sensitive system is inaccurate, or that the selected dataset
pair is representative of deployed unlearning workloads.

## 8. Reproduction

From the project directory:

```text
./.venv/bin/python examples/run_audit_case_study.py
```

The script records package versions, SHA-256 digests of the loaded arrays,
script, and pinned requirements, fixed random seed 20260728, all numerical
outputs, and twelve scope-labeled automated consistency checks in
`examples/results/audit_case_study.json`. Its default output path is resolved
from the script location rather than the caller's working directory.
