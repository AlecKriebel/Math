# The exact Bd-catalyst ray needed for a diagonal to fitness two

Date: 2026-08-08 (America/Los_Angeles)

## Status

This is a constructive reduction, not a new excluded class.  It identifies
a strictly weaker target than an endpoint simultaneous generator.

The dB-positive pair response vanishes linearly as `r -> 2-`.  Consequently
it is enough to find growing-rank Bd catalysts whose dB cost is little-oh of
their Bd gain.  The catalyst need not itself have positive dB response, and
the combined response need not be strict at `r=2`.

## 1. Exact pair resource

For a dilute `K_2` satellite with scale `sigma`, the exact response is

\[
 B_P(r,\sigma)={2(\sigma-1)\over1+\sigma(r^2-1)},     \tag{1}
\]

\[
 D_P(r,\sigma)={2\{r(2-r)-\sigma\}
                    \over\sigma+2r(r-1)}.            \tag{2}
\]

Letting a positive rational sequence `sigma_k -> 0` gives, compact-uniformly
on every interval bounded away from one,

\[
 (B_P,D_P)\longrightarrow
 \boxed{P(r)=\left(-2,{2-r\over r-1}\right)}.        \tag{3}
\]

Thus a pair spends two units of Bd response and supplies

\[
                         \delta(r)={2-r\over r-1}>0  \tag{4}
\]

units of dB response for every fixed `r<2`.  The resource vanishes at the
endpoint, which is harmless for the definition of `R_sim`.

## 2. Catalyst-ray criterion

Let `C_k` be a fitness-independent sequence of rational growing-rank
modules, with exact full response `(B_k(r),D_k(r))`.  Every uniform-start,
entrance, reciprocal-invasion, post-establishment, and far-field term must
already be included in these coordinates.  Suppose there are positive
normalizations `c_k` and a number `r_0<2` such that, compact-uniformly for
`r in [r_0,2]`,

\[
 {B_k(r)\over c_k}\longrightarrow b(r),qquad
 \inf_{[r_0,2]}b(r)=:b_0>0,                         \tag{5}
\]

\[
                         {D_k(r)\over c_k}\longrightarrow0. \tag{6}
\]

Equivalently, after a harmless positive normalization, the response rays
converge to `(b(r),0)` with a uniformly positive Bd coordinate.  In
particular,

\[
             B_k>0,qquad {|D_k|\over B_k}\longrightarrow0. \tag{7}
\]

Choose once and for all a rational `tau>2/b_0`.  Use catalyst density
`tau/c_k` and pair density one at stage `k` (with rational rounding absorbed
by the later population scale).  Equations (3), (5), and (6) give the total
limiting response

\[
 \boxed{V(r)=\left(-2+\tau b(r),{2-r\over r-1}\right).} \tag{8}
\]

The Bd coordinate is uniformly positive on `[r_0,2]`.  For every *fixed*
`r<2`, the dB coordinate is also strictly positive.  There is no uniform
margin as `r -> 2-`, and none is required by the quantifiers.

Therefore, once the finite trace has compact-uniform error control, (5)--(6)
produce a single fitness-independent diagonal simultaneously amplifying
every fixed `r in [r_0,2)`.  Combining it with a finite-overlap response menu
covering `(1,r_0]` proves `R_sim>=2`.

This argument also shows the sharp ratio demanded at a fixed fitness.  If a
catalyst with `B>0,D<0` is mixed just strongly enough to pay the pair's Bd
cost, dB remains positive precisely when

\[
 {-D\over B}<{\delta(r)\over2}
              ={2-r\over2(r-1)}.                    \tag{9}
\]

Hence any bounded-away-from-zero cost/gain ratio fails near two.  The ratio
must actually tend to zero along the growing-rank diagonal.

## 3. Relation to the integrated endpoint score

`ENDPOINT_INTEGRATED_MODULE_TARGET.md` derives the stronger endpoint target
`mathcal D>0` and `mathcal B+mathcal D>0`.  A witness there would immediately
work, but it is more than is needed.  The catalyst criterion (5)--(7) allows
`D_k<0` at every finite rank and permits the endpoint combined response to
tie in dB.  It is therefore the primary constructive target.

For an integrated module, the exact endpoint formulas in that note can be
used directly:

\[
 B_k(2)=\mathcal B(H_k,x^{(k)}),\qquad
 D_k(2)=\mathcal D(H_k,x^{(k)}).                     \tag{10}
\]

The desired singular profile is now unambiguous:

\[
 \mathcal B(H_k,x^{(k)})>0,qquad
 {\mathcal D(H_k,x^{(k)})\over
  \mathcal B(H_k,x^{(k)})}\longrightarrow0,          \tag{11}
\]

plus compact-uniform continuation in `r` and finite-trace control.

## 4. Bounded catalyst screen

One bounded cycle tested three genuine growing-rank gateway regimes rather
than more fixed cells:

1. integrated portal-clone paths with graded edge and portal profiles;
2. integrated stars through 300 leaves, optimizing Bd gain against dB cost;
3. singular three-layer gateways of sizes `(1,k,k^2)` with edge weights on
   the `1/k` and `1/k^2` scales;
4. an `o(n)` dense twin gateway attached to a complete core, including a
   tunable internal gateway clique.

No ray with vanishing cost/gain ratio appeared.  The best star ratios moved
toward one rather than zero, and the three-layer profiles found positive Bd
only with a dB cost of the same order.  These are **NUMERICAL OBSERVATIONS**,
not obstruction theorems.  They serve only to reject those parameterizations
as immediate leads.

The next constructive search should optimize (7) directly in architectures
where an `o(n)` gateway changes a positive mass of core singleton responses;
optimizing `B+D` alone can miss the required singular ray.

## 5. Exact replay

`verify_bd_catalyst_ray_target.py` reconstructs the pair resource (3), the
mixture (8), and the exact fixed-fitness ratio condition (9) symbolically.
