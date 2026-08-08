# Restart hostile audit: higher-rank separated-portal theorem

Date: 2026-08-07 (America/Los_Angeles)

Verdict: **PROVED, within the fixed-finite-rank separated-portal scope below.**

No literature search, network access, or external contact was used.  This
audit did not edit the candidate theorem or its verifier.

## 1. Exact audited scope

For each size parameter `s`, the graph consists of `s` disjoint unit-weight
blade edges and `Q` portal vertices.  There are fixed integers `Q,T>=1` and
type counts `s_t` satisfying

\[
 \sum_t s_t=s,\qquad s_t/s\longrightarrow\pi_t,
 \qquad \pi_t>0,\quad\sum_t\pi_t=1.
\]

Both endpoints of a type-`t` blade are joined to portal `a` with weight
`lambda_at/s`, where every `lambda_at` is fixed, finite, and strictly
positive.  There are no portal--portal edges and no edges between distinct
blades.  Thus the finite graphs are connected.  Multiplying every edge
weight by one common positive factor is immaterial, but no other scaling
variant is part of the theorem.

The conclusion is pointwise in a fixed fitness `r` and asymptotic in `s`:
for every fixed `r>=3/2`, at least one of Bd or dB is eventually strictly
suppressing relative to the corresponding complete graph.  For
`3/2<=r<=2`, the stronger limiting establishment inequality is

\[
 \alpha_B+\alpha_D<2(1-1/r).
\]

For `r>=2`, dB alone is strictly below `1/2<=1-1/r`.  The suppressing rule
may depend on `r` and on the fixed trace data.

The result does **not** cover growing `Q` or `T`, vanishing blade-type
proportions, zero incidences, `s`-dependent `lambda_at`, a portal--blade
scale other than `1/s` relative to the unit blade edge, positive-proportion
portal populations, or any direct portal network.  “Arbitrary finite
incidence rank” must therefore be read as arbitrary but fixed finite `Q,T`,
not rank growing with population size.  The portal proportion in the proved
class necessarily vanishes, while every one of the fixed blade classes
grows linearly with `s`.

## 2. Independent rate and map derivation

Put

\[
 B_a=2\sum_t\pi_t\lambda_{at},\qquad
 f_{at}=\frac{2\pi_t\lambda_{at}}{B_a},\qquad
 c_t=\sum_a f_{at},\qquad
 \ell_t=\sum_aB_af_{at}.
\]

Each row of `f` sums to one.  A clean mutant type-`t` blade seeds portal
`a`, and is successfully erased, at the following leading continuous-time
rates:

| rule | seed rate | successful parent-death rate |
|---|---:|---:|
| Bd | `2 r lambda_at/s` | `2/((r+1)s) sum_a lambda_at/B_a` |
| dB | `2 r lambda_at/(s B_a)` | `1/(r s) sum_a lambda_at` |

The factors `r/(r+1)` and `1/2` in the two death rates are the exact strong
blade resolution probabilities.  These rates follow directly from the
atomic update rules; no independent-lineage assumption is used.

With no portal edges, a portal episode never leaves its seeded singleton
portal.  For a proposed descendant-survival vector `s` and
`m_a=sum_j f_aj s_j`, direct competing-clock calculation gives

\[
 H_a^B=\frac{C m_a}{B_a+C m_a},\qquad
 H_a^D=\frac{D B_a m_a}{1+D B_a m_a},
 \qquad C=\frac{r^2}{r+1},\quad D=\frac r2.
\]

Combining a parent's death clock with its marked portal-episode clocks
independently reproduces the candidate survival maps

\[
 R_t^B=\frac{r^3}{c_t}\sum_a f_{at}
       \frac{B_am_a}{B_a+Cm_a},\qquad
 S_t^B=\frac{R_t^B}{1+R_t^B},
\]

\[
 R_t^D=\frac{r^3}{\ell_t}\sum_a f_{at}
       \frac{B_am_a}{1+DB_am_a},\qquad
 S_t^D=\frac{R_t^D}{1+R_t^D}.
\]

These are offspring-PGF survival maps, not mean-offspring approximations.
The survival vector is the largest fixed point (equivalently one minus the
minimal extinction fixed point).

## 3. Affine separation and fixed-point direction

For `3/2<=r<=2`, define

\[
 A=\frac{4(r-1)}r,\qquad k=\frac{2r}{r+1},\qquad
 J(s)_t=\min\{1,A-ks_t\}.
\]

Here `A-k=2(r^2-2)/(r(r+1))>0`.  Concavity of the clipped affine map gives

\[
 n_a:=\sum_jf_{aj}J(s_j)\leq \min\{1,A-km_a\}.
\]

Fix a parent type and write `x=S_t^B(s)`, `X=x/(1-x)`.  The Bd map implies

\[
 r^3\sum_af_{at}\frac{B_am_a}{B_a+Cm_a}=c_tX,
\]

and `x<r^3/(1+r^3)` because every portal response in the sum is strictly
below one.  If `x<=m_0=(A-1)/k`, then `J(x)=1` and `S_t^D(J(s))<1` follows
from the parent's positive death probability.  If `x>m_0`, put
`y=A-kx` and `Y=y/(1-y)`.  The certified scalar inequality is

\[
 r^3\left(\frac{Bm}{B+Cm}+\frac{Bn}{1+DBn}\right)
 < X+BY,
 \qquad n=\min\{1,A-km\},
\]

on the physical domain.  Monotonicity in the actual mark `n_a` and summing
with weights `f_at` cancel the entire Bd term, yielding

\[
 R_t^D(J(s))<Y,
 \qquad S_t^D(J(s))<J(S_t^B(s)).
\]

The direction of the final fixed-point comparison is correct.  Any
offspring survival map satisfies radial concavity
`S(theta z)>=theta S(z)` for `0<=theta<=1`: conditional on the number `M`
of potentially surviving children, the relevant function is
`1-(1-theta)^M`.  If the largest dB fixed point exceeded the positive strict
supersolution `J(x^B)`, scaling it until one coordinate first touched the
supersolution would give simultaneously equality at that coordinate and a
strict inequality there.  Hence

\[
 x_t^D<A-kx_t^B.
\]

After multiplying by `1/2`, this is exactly

\[
 \frac r{r+1}x_t^B+\frac12x_t^D<2(1-1/r).
\]

Positive `pi_t` averaging gives the claimed establishment separation.
The inherited fixed-cutoff trace argument then gives
`limsup rho_U<=alpha_U`; the strict limiting gap and convergence of both
complete-graph baselines to `1-1/r` give eventual suppression.  This last
step is an asymptotic upper bound only and makes no establishment-implies-
fixation claim.

## 4. Certificate replay and independent checks

The exact verifier was replayed once with

```text
.venv/bin/python universal_simultaneous_amplification/phase4_landmark_closure/construction/higher_threshold/asymmetric_portal_incidence/verify_higher_rank_separation.py
```

It passed all atomic normalizations, the rational `Q=3,T=2` labelled
episode and parent calculations, both compactification-denominator signs,
and the two Bernstein covers:

```text
low mark:  6 boxes, maximum depth 3, multidegree (14,2,1,3)
high mark: 11 boxes, maximum depth 6, multidegree (16,2,2,3)
ALL HIGHER-RANK SEPARATION CERTIFICATES PASS
```

The Bernstein transformation and subdivisions were then checked by a
separate exact evaluation: on every terminal box, rational local points
were mapped back to the original cube and the original power-basis
polynomial was compared exactly with its tensor Bernstein evaluation.
Every comparison agreed.  Inspection also confirmed that the listed paths
form a partition, the compactification denominator has the stated sign,
all terminal coefficients are nonnegative, and every face meeting
`0<u<1, 0<b<1` has an active positive coefficient.

Additional adversarial checks included:

- exact rational scalar-gap tests at `r=3/2` and `r=2`, with `m` at
  `0,m_0,1`, `x` close to both open endpoints, and
  `B=10^-12,1,10^12`;
- 60 high-precision multitype map and largest-fixed-point tests at
  `r=3/2`, just above `3/2`, interior fitnesses, just below `2`, and `2`,
  with portal loads spanning `10^-18` through `10^18` and highly
  concentrated incidence rows.

No sign failure or fixed-point-direction failure was found.  These tests are
audit evidence only; universality comes from the exact scalar certificate.

## 5. Degeneracies, equality, and verifier boundary

- For every admitted fixed positive data set, the inequality is strict.
  If the Bd coordinate lies below the clipping threshold, strictness comes
  from positive parent extinction; above it, strictness comes from the
  Bernstein certificate with `0<u,b<1`.
- Subcritical coordinates and a zero survival vector cause no problem.
  The comparison uses a positive supersolution because `A-k>0`.
- The endpoints `r=3/2` and `r=2`, and the mark endpoints `m=0,1`, are
  included in the certificate.  `B=0` and `B=infinity` are not physical
  data.  The gap need not be uniform as a sequence of trace parameters
  approaches an excluded boundary.
- At `r=2`, dB is strictly below its entrance factor `1/2`; for `r>2`, this
  alone supplies the class obstruction.
- The verifier's “seven-state labelled system” really does instantiate all
  nonempty portal subsets, but without portal edges only singleton subsets
  are reachable from the episode initial states and only those values are
  used.  This is sufficient for the proved theorem.  It supplies no
  verification of the still-open direct-portal resolvent.
- Zero incidences might admit extensions after deleting irrelevant types or
  by continuity, but no such extension was audited and none should be
  claimed.  Likewise, fixed-parameter strictness must not be promoted to a
  uniform gap over growing rank or singular parameter sequences.

## 6. Final classification

**PROVED:** the arbitrary-positive-incidence, fixed-`Q,T`, no-direct-portal
class obstruction at every fixed `r>=3/2`, with asymptotic eventual
suppression of at least one update rule.

**EXACTLY COMPUTED:** the scalar Bernstein certificate and the representative
rational labelled-chain identities.

**OPEN:** direct portal edges; growing portal/type rank; vanishing class
proportions or singular `s`-dependent incidence/scaling regimes; and the
universal graph problem.

No repair to the algebra or verifier is required.  When integrating the
theorem, the fixed-parameter asymptotic scope above should be stated in the
theorem itself rather than left implicit through the referenced general
model.
