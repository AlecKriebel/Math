# Independent adversarial audit: irrational local maxima

Problem 30002497 / OWR-12866-004. Audit date: 2026-10-04 UTC.

## Verdict

**The partial mathematics passes. The problem remains unsolved. One numerical
serialization correction is required before describing the saved decimal
endpoints as outward-certified intervals.**

The frozen packet correctly proves that every positive irrational local
maximum, including a non-strict one, is a stationary Wilton point. Its exclusion
of the positive roots of x²+mx=1 and their reciprocals, m≥1, also survives.
Neither conclusion answers the target existence question. No novelty claim
is established or recommended.

The original interval integration and in-memory sign assertions are sound,
conditional on the stated mpmath implementation. However, str(iv.mpf) is a
nearest-rounded display, not a directed endpoint export. The audit supplies a
corrected-export verifier and independent exact-integer interval certificates.
No change to a theorem, derivative sign, or unsolved disposition is needed.

The nine frozen author files are bound by `AUDITED_INPUTS.json`. Originals were
preserved. This audit contains no source PDFs, copied source full texts,
catalogue corpora, or private coordination inventories. No remote writes or
external communications were performed.

## 1. Exact target and source scope

The primary report asks whether the function

\[
A(x)=\int_0^\infty \{t\}\{xt\}\,dt/t^2
\]

has a strict local maximum at some positive irrational x. The quantifiers are
existential in x and in a neighborhood radius, with the strict inequality
required for every other argument in that neighborhood. It is not a question
about the normalized function A(x)/√x, about almost-everywhere behavior, or
about merely finding differentiability points.

This was checked against the complete relevant printed page 350 of OWR
06/2014, including its definition and Question 2, and against its rendered
page. [Primary report](https://doi.org/10.4171/owr/2014/06).

Balazard–Martin Theorem 1 characterizes differentiability; Proposition 30
identifies those points as positive Wilton numbers. Those statements alone
prove neither existence nor impossibility of an irrational maximum. The
author's additional extremum restriction genuinely uses the sided secants in
their Proposition 11 proof. [BM, arXiv:1305.4395v1](https://arxiv.org/abs/1305.4395v1).

The later Burrin–Lee–Marmi preprint inspected in the supplied sources studies
Brjuno/Wilton relations and regularity. Its cited results do not provide the
missing two-sided stationary increment bound. This audit is not an exhaustive
claim about all subsequent literature. [Preprint](https://arxiv.org/abs/2503.08206v1).

## 2. Parity squeeze: checked beyond the proposition's stated hypothesis

BM Proposition 11 is stated for divergent Wilton series. The audit inspected
its actual proof, equations (32)–(37), and the antecedent integral estimates
in Propositions 3 and 5. The secant construction needs only an irrational x.
For each sufficiently large odd K, a neighboring continued-fraction cell
gives h_K>0. For even K, the reversed cell orientation gives h_K<0. In both
cases h_K→0, and

\[
\frac{\Upsilon(x+h_K)-\Upsilon(x)}{h_K}
=S_K(x)+O(1/q_K).
\]

The tail estimate is an integral estimate for the positive γ-terms and is
independent of the value or convergence of their alternating series at x.
The estimates for the earlier terms depend on continued-fraction denominators
and interval length, not on divergence. Divergence enters only after (37),
when BM concludes non-differentiability. Extending availability of these
secants to every irrational, as the packet does, is therefore justified.
The parity wording was checked on the rendered source page 19.

For F=r−cΥ with c(x)>0 and r,c differentiable at x, the exact product
decomposition used in the packet is valid before passing to a limit.
Continuity of c makes c(x+h)>0 near x. Maximality yields a lower bound
on the positive-side Υ secants and an upper bound on the negative-side
secants. Consequently, for the finite real number
D=(r′(x)−c′(x)Υ(x))/c(x),

\[
\liminf S_{2k+1}\ge D,\qquad \limsup S_{2k}\le D.
\]

Since γ_j>0, S_{2k+1}≤S_{2k}. This one relation already suffices:
limsup S_{2k+1}≤D and liminf S_{2k}≥D. Both subsequences converge to D.
The author's second adjacent-sum inequality is true but unnecessary.
No boundedness of the secants or partial sums has been assumed circularly.
The argument permits equality in the local-maximum condition.

For 0<x<1, BM Proposition 1 gives A=ρ−Υ/(2x), with ρ differentiable
at irrational arguments. For x>1, the correct composition at y=1/x is

\[
A(1/t)=A(t)/t=\rho(t)/t-\Upsilon(t)/(2t^2).
\]

The reciprocal map is a local homeomorphism, so this composition has a
maximum at y. The positive coefficient 1/(2t²) permits the same lemma.
Differentiability transfers back via reciprocity; Fermat's theorem then gives
A′(x)=0. The packet does not incorrectly assert that maxima of A itself
are preserved by x↦1/x. The case x=1 is rational and outside this theorem.

## 3. Other analytic identities and boundary cases

- The tail enclosure 0≤A−A_T≤1/T follows directly from 0≤{t}{xt}≤1.
  It is uniform for every x>0 and T>0. The truncated derivative obtained by
  accounting for each moving jump is correct. Within each breakpoint cell,
  A_T″=floor(xT)/x²≥0. When floor(xT)=0, the positive linear slope rules out
  a maximum. On a fixed compact x-interval the breakpoint set is finite and
  rational. This proves the finite-cutoff claim only; uniform convergence
  does not transfer it to the infinite integral.
- The reciprocal identity A(x)=xA(1/x), its differentiated form
  xA′(x)+A′(1/x)=A(x), and the unitary dilation normalization all check.
  Equality in the Hilbert-space bound forces x=1 by examining small t.
  This is a statement about A(x)/√x. A stationary x cannot have a stationary
  reciprocal because A(x)>0.
- Differentiating BM equation (6) at a Wilton point is justified by their
  Theorem 2 and Proposition 26, not by unjustified termwise differentiation
  of the Bernoulli series. It gives the packet's equation (10).
- At a stationary Wilton point, subtracting the same integral identity and
  removing the constant φ₁(x) term gives exactly the packet's equation (11).
  For h<0 the integral must be oriented; with that convention the formula
  remains correct. Its explicit term is negative quadratic, but the known
  Lebesgue-point property controls the residual only by o(|h|). Such a
  remainder may dominate h² and have either sign.
- BDBLS Proposition 98 does prove strict rational local maxima. Its
  denominator-dependent linear term and neighborhood cannot be discarded
  when applying it along an irrational's convergents. The packet does not
  make that invalid passage. [BDBLS companion, pp. 38 and 44](https://arxiv.org/abs/math/0306251v1).

## 4. Quadratic-family exclusions

BDBLS Proposition 88 holds when φ₁(x) converges and simultaneously ensures
convergence at 1/x. At the quadratic arguments here, bounded partial
quotients ensure absolute Wilton convergence. If 1/x−x is an integer,
periodicity identifies the two φ₁ values. Algebraic substitution into
equation (10) gives

\[
A'(x)=\frac{A(x)-\log x}{1+x}.
\]

This is valid for both r_m=(√(m²+4)−m)/2 and y_m=1/r_m=m+r_m.
It is not asserted at x=1. Since A(r_m)>0 and log r_m<0, every m≥1
gives A′(r_m)>0.

For y_m, BM Proposition 28 and |B₂|≤1/6 give
A(y)≤½log y+(1+A(1))/2+ζ(2)/(6y). Its excess over log y is strictly
decreasing. The author's interval check at y=11 is sound, so m≥11 is
excluded analytically. The finite signs m=1,…,10 were independently certified
as described below. Their sign change does not establish an irrational
stationary point; the intervening rational nondifferentiability points
preclude the proposed ordinary derivative-continuity/Darboux shortcut.

## 5. Numerical rigor, defect, and independent certificates

### In-memory author integration

The event streams n and m/x enumerate all jumps of the two fractional parts.
Strict interval comparisons certify their order; ambiguous comparisons stop
the program. A simultaneous event is accepted only through equality, which
is exact for the x=1 control used here. The cutoff comparisons likewise stop
if uncertain. On each cell, the correct integrand is
x−(m+nx)/t+nm/t², whose primitive is the packet's equation (4).
The first cell uses its removable singularity correctly. Repeated occurrences
of interval x can widen bounds but do not invalidate enclosure. The [0,1/T]
tail is then added in interval arithmetic. A square-root interval contains
the exact quadratic argument; a rounded point is never substituted for it.

### Required correction: endpoint export

Inspection and exact rational testing of installed mpmath 1.3.0 show that
str(iv.mpf) formats both binary endpoints to nearest at extra display digits.
The original `bracket` comment claiming outward-safe strings is false, and
the result-building code directly uses this display conversion.

At iv.dps=40, the displayed lower endpoint of y₂=1+√2 is greater than the
stored binary lower endpoint. `verification_results.json` records the exact
positive rational difference. This disproves the export guarantee. It does
not disprove the actual mathematical enclosure of A in a particular saved
interval, nor does it invalidate any sign test performed before serialization.
The issue is tiny in size but real in a purported numerical certificate.

`verify_controls_outward.py` repairs only this boundary: it converts each
finite binary endpoint to an exact rational and rounds its decimal lower
endpoint down and upper endpoint up. Its 24 exact-rational tests include
positive, negative, zero, and mixed-sign intervals at three precisions.
Both 2048/40 and 4096/60 corrected runs pass. All eleven high-precision
derivative intervals are contained in the corresponding lower-precision
intervals, with the same signs.

The frozen original script was also rerun at both original parameter sets;
each output matched its frozen JSON file byte-for-byte. AST comparisons
confirm the corrected variant's finite_integral and A_bound functions are
unchanged. These reproducibility results are recorded in `replay_results.json`.

### Independent backend

`independent_controls.py` does not import mpmath or the original verifier.
It uses Python integers for fixed-point rational intervals with denominator
10^50. All basic operations round outward by integer floor/ceiling. Integer
square root encloses the exact quadratic root. Logarithms use range reduction
and the positive series 2Σ z^(2j+1)/(2j+1), with z∈[0,1/3] and a rigorous
geometric upper tail after 70 terms. There is no binary floating point or
platform logarithm in this certificate engine.

At cutoff 256, 579 exact corner/root tests and all eleven derivative tests
pass. The independent derivative intervals contain the corresponding
derivative intervals from both corrected author runs. In
particular, outward-rounded readable supersets are

- A′(y₉) ∈ [0.0027532, 0.0031397], strictly positive;
- A′(y₁₀) ∈ [−0.0021132, −0.0017611], strictly negative.

The other m=1,…,8 signs are positive and m=11 is negative. Reciprocity
controls at m=1,3,10 pass. A separately integrated A(1) and the elementary
bound ζ(2)/6<1/3 give a large-y excess upper bound below −0.037011 at 11.
Thus even that part of the certificate does not depend on numerical π or
Euler's constant. Repeating the independent computation reproduces its
saved result exactly. These computations verify exclusions, not extrema of
general irrational points, and are not a new research route.

## 6. Remaining gap and release disposition

The exact unresolved task is either to construct a stationary Wilton point
and prove the strict increment inequality on both sides for every sufficiently
small nonzero h, or to exclude every such point. The author supplies neither.
Finite sign checks, stationarity, the negative quadratic term alone, and
regularity almost everywhere do not supply the missing quantifiers.

The five recorded routes are substantive and their stated limitations are
accurate. The strongest verified conclusion is the stationary-Wilton necessary
condition plus the excluded quadratic/reciprocal family. The packet is suitable
as **partial, unsolved research with the serialization correction applied or
explicitly carried alongside it**. It is not suitable for a solved status or
a claim of a new solution.
