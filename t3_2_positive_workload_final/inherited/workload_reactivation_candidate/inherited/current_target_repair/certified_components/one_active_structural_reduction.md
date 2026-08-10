# One-active-coordinate structural reduction

Assume `A` is the only unbounded coordinate and that `B,C` remain in a fixed
finite box.  All target marks, bounded populations and lattice data are
finite phases.

## Exact polynomial rates

Every nonexit transition has the form

\[
(n,\phi)\longrightarrow(n+k,\phi'),\qquad |k|\le2,
\]

with rate

\[
c_2(\phi,e)n(n-1)+c_1(\phi,e)n+c_0(\phi,e),
\]

where the coefficients are nonnegative exact expressions in the reaction
rates and the bounded coordinates.

## Quadratic case

If `2A` is a complex, every genuine channel sourced at `2A` lowers `A` by at
least one.  All upward channels have source degree at most one.  Therefore

\[
\mathcal L A\le-c_2A(A-1)+c_1A+c_0,
\qquad c_2>0,
\]

on every phase in which no structural exit occurs.

## No-`2A` case

If `2A` is absent, every degree-one source has `A`-increment in `{0,-1}`.
The degree-one phase graph is finite.  In a recurrent class:

- a negative edge gives strictly negative stationary mean and an exact
  finite Poisson corrector;
- otherwise every recurrent degree-one edge preserves `A`.

A degree-zero birth can create only one `A`.  Its actual target contains one
`A`.  In the creator linkage, strong connectivity supplies a return path to
a zero-`A` complex.  Before the first service edge, every path source
contains one `A` and hence has linear rate.  A different linkage cannot steal
the required bounded cofactor at linear order without using the same source
complex; consuming the active `A` is already service.  Bounded-source
interruptions are retained explicitly or are structural box exits.

This proves the finite polynomial generator and the creator-service path
interfaces.  A complete universal mean-return theorem still requires the
rate-weighted current-target charging lemma stated in
`current_target_charging_remaining.md`; this file does not claim T3-2.
