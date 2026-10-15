# Independent audit of the interval-pair lemma

Source: `sources/family370/build/sections/04-intervals.tex`, lines 69–147.

## Scope and checkpoint log

- 2026-10-07 04:29:27 UTC: **65% complete** toward checking the interval lemma.
  Direct algebra and interval geometry support the statement as written.
  Remaining work: run independent numerical diagnostics, examine unbounded
  dimension-three tails, and finish boundary-case review. No source edits,
  external communication, branch changes, commits, or pushes by this reviewer.

The hypothesis under review is precisely the weighted inequality in the source,
for nonempty open intervals, lambda positive, nonnegative coefficients, and a
bounded interval whenever its coefficient is positive. The checks concern this
lemma only; they do not establish any PDE theorem or novelty claim elsewhere.

## Exact algebra

For bounded intervals, set

\[
A=\int_{I\times J}K,\quad
E_I=\int_{I\times J}\overline K_I,\quad
E_J=\int_{I\times J}\overline K_J,\quad
D=\int_{I\times J}\frac{h^2}{\lambda^2+h^2}K,\quad
T=\int_{I\times J}\frac{h}{\lambda^2+h^2}K.
\]

The boundary term in integrating `(s-m_I) partial_s K` is
`|I| (K(s_-,s')+K(s_+,s'))/2`. Thus the sign in the source's
one-variable identity is correct. Applying both identities gives

\[
2A-E_I-E_J=(n-2)(D-d_0T).
\]

Let `c=min(c_I,c_J)`. The difference between the displayed right and left
sides of the lemma is **exactly**

\[
(n-2)c\,d_0T+(c_I-c)E_I+(c_J-c)E_J.
\]

This avoids an extra estimate in the last paragraph of the source and is an
independent check of its coefficient bookkeeping. Each endpoint integral is
strictly positive for nonempty bounded intervals because lambda is positive.

## Midpoint sign for all bounded interval pairs

Write `L=|I|`, `M=|J|`, `R=(L+M)/2`, and `q=|L-M|/2`.
The overlap density is a trapezoid: `F(r)=min(L,M)` for `0<=r<=q`,
`F(r)=R-r` for `q<=r<=R`, and zero thereafter. Therefore the formula
`max(0,min(L,M,R-r))` in the source is correct, including unequal lengths.
The actual difference distribution is `rho(h)=F(|h-d_0|)`.

For `d_0>=0` and `h>0`, `rho(h)-rho(-h)>=0`. Since
`h K(h)/(lambda^2+h^2)>0` on the positive half-line,

\[
T=\int_0^\infty\frac{hK(h)}{\lambda^2+h^2}
  [\rho(h)-\rho(-h)]\,dh\ge0.
\]

Reflection gives `T<=0` when `d_0<=0`. Consequently `d_0T>=0`.
Nothing here requires the longitudinal projections of the intervals to overlap.
For every nonzero `d_0`, the sign is strict: for positive `d_0`, take
`h=d_0+R-epsilon` with `0<epsilon<min(d_0,L,M)`; then `rho(h)>0`
and `rho(-h)=0` on a positive-measure neighborhood. The negative case
follows by reflection.

For bounded intervals, the inequality is equality when both weights are zero,
or when the positive weights are equal and the interval midpoints coincide.
Otherwise it is strict. In particular, unequal lengths alone do not force
strictness.

## Unbounded intervals and zero weights

If at most one coefficient is positive, the absolute coefficient difference
equals their sum. The kernel contribution on the right already equals the
whole integrand on the left, and any defined positive endpoint contribution
is nonnegative. This is a pointwise assertion, so Tonelli's nonnegative
extended-integral convention establishes it even when the integrals diverge.

If both weights are zero, every integrand is the zero function even if both
intervals are unbounded. The convention concerning zero-coefficient endpoint
terms is necessary and sufficient to avoid asking for nonexistent endpoints.

For `n=3`, a bounded nonempty interval with an unbounded half-line or whole-line
partner has divergent kernel integral: at infinity `K(h)` is a positive
constant times `1/|h|`. The endpoint integral with a positive bounded-interval
weight likewise diverges. The displayed nonnegative inequality is then a
legitimate extended-integral statement. Subtracting these infinite quantities
would not be legitimate, and the source does not do so. For `n>3`, those
one-unbounded-partner integrals instead converge since the tail is
`|h|^{-(n-2)}`. With both weights positive, both intervals are bounded, so
all integrations by parts involve finite integrals in every stated dimension.

The assumption `lambda>0` is substantive: the diagonal singularity at
`lambda=0` can destroy local integrability, and that boundary case is outside
the lemma. Open versus closed bounded endpoints does not affect the integrals;
the endpoint averages are well defined by the smooth kernel.

## Numerical diagnostics

`upstream_interval_checks.py` uses only the Python standard library. It compares
independent endpoint integrals against one-dimensional overlap integrals,
checks the density formula against literal geometric intersections, compares
direct and positive/negative-paired midpoint integrals, and checks the exact
weighted slack. Dimension-three closed forms furnish an additional route.
The Newton normalization is omitted because it is a common positive factor;
lambda is scaled to one. Floating-point quadrature is supporting evidence,
not a computer-assisted rigorous proof.

Command: `python3 openai_followon_lane_emden/notes/upstream_interval_checks.py`
from the repository root, using Python 3.14.6. Seed: `37020261007`.

The script passed all assertions on **614 finite cases**, including 500 seeded
random geometries, explicitly unequal/disjoint intervals, dimensions
3, 4, 5, 6, 10, and 20, equal/unequal/zero weights, and 18 fixed-geometry tests
at physical transverse separations `lambda=1e-3` and `lambda=1e-6`. It also
compared 2,456 sampled overlap lengths to literal geometric intersections.

| Check | Largest observed scaled discrepancy |
| --- | ---: |
| Midpoint integration-by-parts identity | 1.29e-13 |
| Exact weighted slack decomposition | 5.97e-14 |
| Direct versus paired midpoint integral | 3.22e-17 |
| Density total mass versus `L*M` | 1.87e-13 |
| Overlap formula versus geometric intersections | 8.12e-13 |
| Dimension-three closed forms versus quadrature | 1.10e-12 |

The smallest normalized slack was `-1.33e-15`, consistent with rounding in
the proved equality cases; no numerical counterexample was found. Every
tested normalized midpoint product was nonnegative. These figures concern
floating-point diagnostic error, not a rigorous enclosure.

For `n=3`, `lambda=1`, and the omitted common Newton normalization, use

\[
G(h)=\operatorname{arsinh}h,\qquad
H(h)=h\operatorname{arsinh}h-\sqrt{1+h^2}.
\]

`G'=K`, `H''=K`; the rectangular four-corner difference of `H` gives `A`.
The corresponding second primitives for `D` and `T` are
`h arsinh(h)-2 sqrt(1+h^2)` and `-arsinh(h)`. These yield independent
closed-form evaluations of every scalar in the exact identity. For
`I=(-1,1)` and `J=(-R,R)`, the computed kernel integrals were
11.9863, 21.1933, 30.4036, and 39.6140 at `R=10,100,1000,10000`;
successive increments approach `4 log(10)=9.21034`, as predicted by the
rigorous logarithmic-tail argument.

## Final verdict and checkpoint

**Verified claim:** the full weighted interval comparison is correct under its
stated assumptions, including arbitrary unequal or disjoint bounded intervals,
all positive transverse separations, dimensions `n>=3`, and the stated
nonnegative extended-integral treatment of unbounded zero-weight partners.
The proof does not conceal an unproved central claim. The exact nonnegative
slack formula above is a concise supplementary verification certificate.

**Substantive defects found:** none. No source repair is required for this
lemma. A possible optional exposition change is to present the exact slack
formula, but the existing defect-bound argument already proves the claim.

- 2026-10-07 04:32:13 UTC: **100% complete** toward this scoped interval-lemma
  audit. Algebra, midpoint sign, unequal/disjoint geometry, small transverse
  separations, dimension-three integrability, zero weights, equality cases,
  and reproducible numerical falsification diagnostics are complete. This
  percentage concerns the audit, not the broader discovery goal.
