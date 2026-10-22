# Independent adversarial audit: Problem 2306044 / Function Theory 6.44

Audit date: 2026-10-04 UTC. Verdict: **PASS, with stated external-theorem and historical-source limitations.** Recommend `already_solved`, negative answer, `turns_used: 1`, `turn_limit: 5`. No mathematical correction is required. This is an independent internal audit, not peer review or formal proof certification.

## Frozen inputs and isolation

The author packet was read without modification. Its exact nine-file inventory was independently checked, including all eight entries of its manifest:

- `public/SHA256SUMS.json`: `f25cf28a767af988aa7ccfbef005a6c515ddf5a1ddfd0393d25b0c8f393225b7`
- `public/proof.md`: `da2c5ebc59a77683059958c4a736499dffee6bc72c563e1f74595b09beec5f9a`

Audit outputs are separate in this directory. No remote writes, publication, external messages, helper delegation, or changes to the frozen packet were performed. Private source-reading files are not included in this audit package. The mathematical work below reviews the supplied construction; it is not another proof-search turn.

## Exact target and prior status

The normalized class is analytic and injective on the full open unit disk, with expansion starting `z`; the real subclass requires every Taylor coefficient real. Chapter 6 defines this normalization explicitly on printed p. 114. Problem 6.44, printed p. 134, uses coefficient weights `1/n`, rather than ordinary coefficientwise multiplication. Its Update 6.44 identifies a negative counterexample due to Bshouty; bibliography [122] gives the 1980 paper, pages 271–272. These statements were checked against the [Hayman–Lingham source](https://arxiv.org/pdf/1809.07200), including a visual inspection of the problem/update page. The supplied dataset record matches the mathematical target but its open-status summary conflicts with that explicit update.

The Bshouty paper's full text remains unread. The audit does not claim that the reconstructed function is Bshouty's example or that this reconstruction has novelty. The explicit exact-target attribution suffices for the historical `already_solved` classification. No conclusion is transferred to Problems 6.45 or 6.56.

## The external theorem was checked at the actual hypotheses

[Pfluger's 1985 paper](https://www.acadsci.fi/mathematica/Vol10/vol10pp447-454.pdf), p. 447, equation (1), visually states the sharp bound

\[
 |a_3-\lambda a_2^2|\leq1+2\exp\bigl(2\lambda/(\lambda-1)\bigr),\qquad 0\leq\lambda<1,
\]

for the full normalized univalent class. Its definition of that class matches the target. There is no starlikeness, convexity, boundedness, oddness, or real-coefficient assumption on this inequality. Substitution of `lambda=1/2` gives `1+2/e^2`, exactly the bound used. The realness of coefficients mentioned later on that page concerns equality cases and is not an extra hypothesis. Thus the proof has neither a parameter-range error nor an illicit subclass transfer. The theorem remains an explicitly cited mathematical dependency; this audit does not independently reprove its entire variational proof.

Source-file hashes were checked against the author's provenance:

- Hayman–Lingham PDF: `8e28fd4403a07e4e19a9816b7efaafddf9f475d59cf8c34a8255cb03833ed4f0`
- Pfluger PDF: `6da2e2921429ccd17256868cbc8c8dba2937e987af9068aaf4129bfc49c20adb`

## Analytic construction: adversarial review

### 1. No hidden pole or wrong Herglotz sign

For `0 <= t <= T`, `q=exp(t-T)` lies in `(0,1]`. Taking a unit complex number `xi` with real part `-q`, the average of `(1+xi*w)/(1-xi*w)` and its conjugate-parameter counterpart is exactly

\[
 p_t(w)=\frac{1-w^2}{1+2q w+w^2}.
\]

The sign in the denominator is correct. Both poles of the quadratic denominator are on the unit circle, never in the open disk. The case `q=1` is harmless: the expression reduces to `(1-w)/(1+w)` in the disk. Its real part, like the real part of the general average, is strictly positive.

On every closed disk `|w|<=r<1`, the representation gives uniform bounds

\[
 |p_t(w)|\leq\frac{1+r}{1-r},\qquad
 |p'_t(w)|\leq\frac{2}{(1-r)^2},\qquad
 \operatorname{Re}p_t(w)\geq\frac{1-r}{1+r}>0.
\]

These bounds hold up to the terminal time, including the repeated boundary pole in the unreduced denominator. No differentiability of the chosen angle at `t=T` is needed; the rational expression depends smoothly on `q(t)`.

### 2. Global time existence and analytic dependence are valid

For the vector field `V(t,w)=-w*p_t(w)`, differentiation of squared modulus gives

\[
 \frac{d}{dt}|w_t|^2=-2|w_t|^2\operatorname{Re}p_t(w_t)\leq0.
\]

A trajectory beginning in `|z|<=r` cannot reach the boundary of the larger disk. The displayed compact bounds give uniform local Lipschitz constants and continuation through all finite times in `[0,T]`. There is no inference from finitely sampled trajectories here. To make the usual holomorphic-dependence argument precise, choose `r<R<1`; Picard iteration is uniform for initial values on the smaller disk over short intervals, and finitely many such intervals cover `[0,T]`. Thus every flow map is holomorphic on the full disk.

### 3. Injectivity does not require a backward global self-map

Backward uniqueness is only invoked along two already existing compact trajectories. It is not necessary to solve arbitrary backward trajectories inside the disk. Equivalently, for two initial points, put `d(t)=w_t(z_1)-w_t(z_2)`. On a common compact disk,

\[
 d'(t)=a(t)d(t),\quad
 a(t)=\int_0^1 \partial_w V\bigl(t,w_t(z_2)+s(w_t(z_1)-w_t(z_2))\bigr)\,ds.
\]

The integrand is bounded and continuous. Hence `d(t)=d(0)*exp(integral a)`, so distinct initial points never meet. This closes a possible concern about the author's backward-uniqueness wording without changing its argument.

Real symmetry follows from uniqueness because the vector field has real coefficients. Zero remains fixed, and its derivative with respect to the initial value is `exp(-t)`.

### 4. Koebe composition has the correct domain and normalization

The terminal image lies in the open disk, where `k(u)=u/(1-u)^2` is analytic and injective. Cross-multiplication of `k(u)=k(v)` gives `(u-v)(1-uv)=0`; the second factor cannot vanish there. Therefore

\[
 f_T(z)=e^T k(w_T(z))
\]

is globally injective, analytic, normalized, and real-symmetric. Real symmetry of an analytic function gives real Taylor coefficients. Both factors of the proposed self-convolution are genuine members of the required class. A general converse Loewner representation theorem is not being smuggled into the argument.

## Independent coefficient derivation

The separate symbolic checker uses the raw coefficients of `w_t`, rather than copying the author's `A,B` polynomial implementation. Writing

\[
 w_t(z)=v_1(t)z+v_2(t)z^2+v_3(t)z^3+O(z^4),
\]

coefficient comparison in the rational vector field gives

\[
 v_1'=-v_1,\quad
 v_2'=-v_2+2qv_1^2,\quad
 v_3'=-v_3+4qv_1v_2-(4q^2-2)v_1^3.
\]

Direct substitution verifies the initial-value solutions

\[
 v_1=e^{-t},\quad
 v_2=2te^{-T-t},\quad
 v_3=(4t^2-4t)e^{-2T-t}+e^{-t}-e^{-3t}.
\]

Expanding the Koebe composition then gives exactly

\[
 a_2(T)=2(T+1)e^{-T},\qquad
 a_3(T)=1+(4T^2+4T+2)e^{-2T}.
\]

At `T=1/2` the pair is `(3/sqrt(e), 1+5/e)`. As an additional consistency test, this pair attains the classical bound at `lambda=1/3`: `a3-a2^2/3=1+2/e`. This observation is supplementary, not part of the proof that the input is univalent. The `T=0` boundary case correctly returns the Koebe function.

## Exact obstruction and convergence

The weights are retained in both relevant coefficients:

\[
 c_2=\frac9{2e},\qquad c_3=\frac{(1+5/e)^2}{3}.
\]

The independently factored excess is

\[
 \Delta=c_3-\tfrac12c_2^2-(1+2/e^2)
 =-\frac{2(e-7/4)(e-13/4)}{3e^2}>0.
\]

The author's elementary `2<e<3` proof already proves the sign rigorously. A separately implemented factorial-series enclosure, using truncation `N=14` rather than the author's `N=18`, proves the rational bounds

\[
 \frac{4645}{100000}<\Delta<\frac{4646}{100000}.
\]

Its finer endpoints are stored exactly as fractions in `independent_results.json`; decimal illustrations are approximately `0.04645185496594547` and `0.04645185496608374`. This is a strict contradiction, not an equality case or rounding-dependent test. Since the non-absolute expression exceeds a positive bound, passing to its absolute value is legitimate.

The convolution's analyticity is also proved rather than assumed: for every radius `r<1`, choose `sqrt(r)<R<1` and use Cauchy's coefficient estimate on the circle of radius `R`. The series of squared coefficients times `r^n/n` converges by a geometric majorant. Normalization and real coefficients are immediate. Failure of the necessary coefficient inequality therefore forces failure of injectivity. A collision witness or failure of the derivative is not required, and neither is claimed.

## Control replay, accounting, and limitations

- The author's manifest verifier passes for eight listed files.
- The author's control script passes all 114 assertions, with output byte-for-byte identical to the frozen results file in this environment.
- Those assertions are **17 nonfloating algebra/interval/baseline controls and 97 supplementary floating-point controls**, the latter comprising 48 radius checks, 48 conjugation checks, and one mesh-agreement check. They must not be described as 114 exact proofs or validated integrations.
- The independent checker passes **42 checks**, including strict frozen inventory/hashes, Herglotz algebra, the raw coefficient ODEs, composition and normalization, weight/sign mutations, a separate rational margin enclosure, and replay accounting. It requires Python and SymPy; tested with Python 3.12.14 and SymPy 1.14.0.
- The finite mutation checks check that specified wrong expressions differ from the required identities. They are not exhaustive mutation testing, nor do they prove analytic univalence.
- The analytic global argument and the sourced Fekete–Szegő theorem, rather than ODE sampling, carry the nonunivalence conclusion.

Reproduce from this audit directory:

```sh
python3 ../public/controls/verify_manifest.py
python3 ../public/controls/verify.py > author_controls_replay.json
python3 independent_verify.py
```

## Corrections and final disposition

Required mathematical corrections: **none**. Required historical correction to the recovered catalogue summary: the claim that no resolution was found in the 2018 source is contradicted by its explicit Update 6.44. The frozen author packet already makes that correction and correctly labels its result `already_solved` with no novelty claim.

The frozen `status.json` saying the independent audit is pending is an accurate pre-audit snapshot. Publication bookkeeping may record this completed audit separately; changing that frozen file would create a new author-packet version and require new hashes. Keep the unread-Bshouty qualification and computational limits when publishing. No promotion to a new mathematical discovery, no adjacent-problem closure, and no added proof-search turn is warranted.

Audit completion: 100% of the assigned verification scope. Remaining limits are the explicitly cited classical theorem, the unread original Bshouty full text, and the fact that this is an internal review rather than external peer review.
