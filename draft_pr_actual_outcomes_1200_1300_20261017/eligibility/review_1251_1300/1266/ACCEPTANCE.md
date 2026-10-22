# Acceptance of the exact partial theorem

Problem 30000964 / OWR-1970-002. Acceptance date: 2026-10-11 UTC.

The authored proof and independent audit are AI-assisted. External human peer review and formal proof-assistant certification have not been established.

## Accepted statement

Let
\[
F(z)=\sum_{k\geq0}\zeta_k z^k/\sqrt{k!}
\]
with independent standard circular complex Gaussian coefficients. For a fixed real h in C_c^2(C), write h_r(z)=h(z/r), H=||Delta h||_2>0, and
\[
Z_0(h_r)=\sum_{F(a)=0}h(a/r)-\frac{r^2}{\pi}\int_{\mathbb C}h,
\quad \sigma=\frac14\sqrt{\frac{\zeta(3)}{\pi}},
\quad Y_r=\frac{rZ_0(h_r)}{\sigma H}.
\]
For every positive c=c(r) with c→infinity and c/r→0, and either choice s=1 or s=-1,
\[
-\frac{\zeta(3)}2\leq
\liminf_{r\to\infty}\frac{\log\mathbb P(sY_r>c)}{c^2}
\leq\limsup_{r\to\infty}\frac{\log\mathbb P(sY_r>c)}{c^2}
\leq-\frac{3\zeta(3)}{\pi^2}.
\]

The complete argument in PARTIAL_PROGRESS.md is accepted at precisely this scope, on the independent challenge documented in AUDIT.md. No mathematical correction was required. Its continuum Gaussian Hölder bound gives the upper estimate; a signed trace-class Gaussian covariance tilt with uniform variance and entropy control gives the lower estimate.

## What remains unresolved

The sharp requested rate -1/2 lies strictly between the proved constants. A rate-function limit, the exact coefficient, a counterexample, uniformity for r-dependent test functions, novelty, and a literature-wide open-status claim are not established. The official question asks about r/(log r)^2 << c << r. The cited Tsirelson results require c(log r)^2/r→0 in dimension two and do not cover that requested interval.

The missing sufficient estimate is a sharp moving-parameter logarithmic moment-generating-function asymptotic without the extra logarithmic restriction; the proof identifies its exact normalization. Fixed-order cumulants or fixed-threshold convergence do not supply it.

## Evidence and limitations

The original complete proof was independently read and reconstructed. Gaussian inequality hypotheses, coherent-frame normalization, realification factors, continuum passage, signed trace-class operators, genuine infinite-dimensional measure change, tilted concentration, entropy transfer, and all moving-parameter errors were checked. Exact source versions and inspection limits appear in SOURCE_METADATA.json and AUDIT_METADATA.json.

Finite numerical controls are supplementary. An initially overstrict finite-radius smoke-test threshold was corrected by extending the tested radius, as reported in AUDIT.md; it was not a mathematical counterexample or proof correction. Neither numerical output nor raw code is included in this publication packet.

This acceptance applies to the mathematical content preserved under the documented nonmathematical editorial redactions. No additional mathematical result is claimed by publication preparation.
