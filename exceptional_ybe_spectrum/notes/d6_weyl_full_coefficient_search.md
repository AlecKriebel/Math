# Full \(19\times 19\) Weyl-coefficient search at \(d=6\)

**Date:** 2026-07-29
**Track:** independent \(d=6\) constructor/falsifier
**Status:** numerical evidence plus one exact structural branch; no exceptional
candidate found

## 1. Scope

The earlier Weyl deformation fixed all nineteen operator-Schmidt singular
values and varied only one orthogonal Schmidt frame.  The present search
removes both restrictions.

Let \(Q_1,\ldots,Q_9\) be the deterministic Hilbert--Schmidt orthonormal
Hermitian matrix-unit basis of \(M_3(\mathbb C)\), and put

\[
\begin{aligned}
A_a&=\frac{Z}{\sqrt2}\otimes Q_a,
&
A_{9+a}&=\frac{X}{\sqrt2}\otimes Q_a
\qquad(1\leq a\leq9),\\
A_{19}&=\frac{Y\otimes I_3}{\sqrt6}.
\end{aligned}
\]

The searched family is

\[
\boxed{
H(C)=\sum_{i,j=1}^{19}C_{ij}A_i\otimes A_j,
\qquad C\in M_{19}(\mathbb R).
}
\tag{1}
\]

This has \(361\) unconstrained real coefficients.  No singular values,
Schmidt frames, coefficient rank, block support, or finite symmetry are
fixed.  Since every \(A_i\) is traceless Hermitian and the frame is
orthonormal, every \(H(C)\) is automatically Hermitian and satisfies

\[
\operatorname{Tr}H(C)=0,\qquad
\operatorname{Tr}_1H(C)=\operatorname{Tr}_2H(C)=0,\qquad
\|H(C)\|_F=\|C\|_F.
\tag{2}
\]

It remains a restricted \(361\)-dimensional linear subspace of the full
real vector space of traceless Hermitian \(36\times36\) matrices.  Failure
inside (1) is not evidence of global nonexistence.

## 2. Objective and analytic gradient

For

\[
\mathcal I(H)=H^2-I_{36}
\]

and

\[
\mathcal C(H)
=H_{12}H_{23}H_{12}-H_{23}H_{12}H_{23}
-\frac13(H_{12}-H_{23}),
\]

the optimizer minimizes

\[
F_w(C)
=\frac1{36}\|\mathcal I(H(C))\|_F^2
+\frac{w}{216}\|\mathcal C(H(C))\|_F^2.
\tag{3}
\]

The code uses the exact Frobenius adjoints of both polynomial maps,
partial traces to pull the three-site gradient back to two sites, and
orthogonal projection onto the \(361\) tensor basis elements
\(A_i\otimes A_j\).  A centered finite-difference audit was performed at
a generic coefficient matrix and at the exact Weyl point, for
\(w=0,0.37,10\).  At step size \(10^{-5}\), every tested relative error
was below \(2.4\times10^{-10}\); the maximum across the complete step-size
sweep was \(1.38\times10^{-9}\).

The same calibration checks the encoded Weyl point

\[
H_0=\frac1{\sqrt3}
\left[Y\otimes Y\otimes I_9
+(X\otimes X+Z\otimes Z)\otimes F_3\right]
\]

and finds cubic residual below \(4.6\times10^{-15}\).

## 3. Predeclared production design

All seeds, weights, initialization modes, and iteration caps were written
to

```text
results/d6_weyl_full_coeff_seed_manifest.json
```

before their corresponding production calls.

The forty runs comprised:

1. six random involution-to-cubic continuation runs;
2. six perturbations of \(H_0\), continued from cubic-heavy to
   involution-heavy objectives;
3. twelve direct joint runs, two at each
   \(w\in\{0.03,0.1,0.3,1,3,10\}\);
4. four bidirectional continuation runs;
5. twelve perturbed mixtures of \(H_0\) and an exact anticommuting product
   involution, using four mixture fractions and three weights.

The direct runs allowed up to \(1200\) L-BFGS iterations.  The continuations
used up to \(300\) iterations at each of six stages, or \(250\) iterations
at each of ten or twelve bidirectional stages.  The optimizer used all
\(361\) real coefficients in every stage.

The raw JSONL records include the complete coefficient matrix, initial and
final diagnostics, every continuation stage, command line, random seed,
dependency versions, machine description, elapsed time, script hash, and
final coefficient hash.

## 4. Numerical outcome

No run approached both defining equations.  The smallest Euclidean pair
of final residual norms was

\[
\left(
\|H^2-I\|_F,\ \|\mathcal C(H)\|_F
\right)
=
(3.5886268615,\ 0.9034063467).
\tag{4}
\]

The forty endpoints did not form forty unrelated local minima.  An
independent diagnostic classified every one into one of two sharply
recognizable relation strata:

| normalized endpoint stratum | runs |
|---|---:|
| adjacent-anticommuting Hermitian involution | 29 |
| Weyl cubic with the wrong quadratic polynomial | 11 |

For the first group, after dividing by the fitted scalar, the maximum
involution residual was \(9.99\times10^{-6}\) and the maximum adjacent
anticommutator residual was \(1.58\times10^{-4}\).  For the second group,
after scalar normalization, the maximum cubic residual was
\(3.68\times10^{-6}\), and the maximum residual in

\[
3H^2+2\sqrt3H-3I=0
\tag{5}
\]

was \(3.49\times10^{-6}\).  The fitted one-variable stationarity equations
held to \(1.2\times10^{-8}\) or better.

These tolerance classifications are diagnostics, not exact
classifications of stationary points.  Their value is that the endpoints
are explained by exact algebraic mechanisms rather than being mistaken
for near-solutions.

## 5. Exact branch exposed by the random starts

The random starts consistently converged, after rescaling, to Hermitian
involutions \(K\) whose adjacent copies anticommute:

\[
K^2=I,\qquad K_{12}K_{23}+K_{23}K_{12}=0.
\tag{6}
\]

This condition has an elementary exact realization inside (1).  On one
six-dimensional site take

\[
S=Z\otimes I_3,\qquad T=X\otimes I_3,
\]

and on two sites put

\[
K=S\otimes T.
\tag{7}
\]

Then \(S^2=T^2=I\), \(ST=-TS\), and consequently

\[
K_{12}K_{23}=-K_{23}K_{12}.
\]

For any adjacent-anticommuting involution, not merely the product example,

\[
\begin{aligned}
K_{12}K_{23}K_{12}&=-K_{23},\\
K_{23}K_{12}K_{23}&=-K_{12},
\end{aligned}
\]

so

\[
\boxed{
K_{12}K_{23}K_{12}-K_{23}K_{12}K_{23}
=K_{12}-K_{23}.
}
\tag{8}
\]

Thus this exact involutive branch has cubic coefficient \(1\), not the
exceptional coefficient \(1/3\).  It cannot contain a desired solution.

For \(H=uK\), equation (3) reduces exactly to

\[
F_w(u)
=(u^2-1)^2+2wu^2\left(u^2-\frac13\right)^2.
\tag{9}
\]

Writing \(y=u^2\), a nonzero stationary point obeys

\[
y-1+w\left(y-\frac13\right)
\left(3y-\frac13\right)=0.
\tag{10}
\]

The residual pairs from all random-start weight sweeps agree with this
scalar law.  The exact verifier checks (7)--(10) using symbolic integer
matrices and symbolic polynomial arithmetic.

The numerical endpoints sometimes have Schmidt rank greater than one.
They indicate a larger adjacent-anticommuting manifold, but no exact
classification of that manifold is claimed.

## 6. Interpretation

The full coefficient freedom did not interpolate between the two exact
nearby mechanisms:

- the Weyl point satisfies the desired cubic but has eigenvalue
  multiplicities \(9+27\) and the wrong quadratic polynomial;
- the anticommuting branch supplies balanced involutions but satisfies
  the cubic with coefficient \(1\).

Direct random starts, continuation from either stratum, bidirectional
continuation, and perturbed mixtures all returned to one of these two
branches.  This is stronger falsification than the fixed-Schmidt search,
but it remains numerical and ansatz-specific.  In particular, it does
not prove that (1) contains no exceptional solution and says nothing
rigorous about an arbitrary \(36\times36\) Hermitian involution.

## 7. Reproduction

Gradient audit:

```text
/Users/alec/Documents/Math/.venv/bin/python \
  scripts/check_d6_weyl_full_coeff_gradient.py \
  --output results/d6_weyl_full_coeff_gradient_check.txt
```

One production call (all others are specified verbatim by the manifest):

```text
/Users/alec/Documents/Math/.venv/bin/python \
  scripts/d6_weyl_full_coeff_search.py \
  --seed 26073807 \
  --initialization random \
  --noise-scale 0.25 \
  --weights 1 \
  --max-iterations-per-stage 1200 \
  --output results/d6_weyl_full_coeff_runs.jsonl
```

Endpoint analysis:

```text
/Users/alec/Documents/Math/.venv/bin/python \
  scripts/analyze_d6_weyl_full_coeff_runs.py \
  --input results/d6_weyl_full_coeff_runs.jsonl \
  --output results/d6_weyl_full_coeff_analysis.json
```

Exact structural verifier:

```text
/Users/alec/Documents/Math/.venv/bin/python \
  verifiers/verify_weyl_anticommuting_branch.py \
  --output results/weyl_anticommuting_branch_exact.txt
```

The production records span
`2026-07-29T08:18:59Z`--`2026-07-29T08:27:09Z` and record Python
`3.9.6`, NumPy `2.0.2`, SciPy `1.13.1`, and
`macOS-26.5.2-arm64-arm-64bit`.

## 8. Status

- Full \(19\times19\) coefficient search: **NUMERICAL_EVIDENCE**.
- Gradient calibration: **INDEPENDENTLY_REPRODUCED numerical
  computation**.
- Anticommuting product branch and coefficient-\(1\) identity:
  **PROVED / EXACT_COMPUTATION**.
- Nonexistence of a \(d=6\) exceptional solution in (1): **not proved**.
